import unittest.mock
from abus import crypto, database, main
from abus.testbase import AbusTestBase

class BackedUpHomedirTests(AbusTestBase):
   def test_simple_end_to_end_backup(self):
      self.setup_backup_with_well_known_checksums()
      expect= {"index.sl3"}
      expect.update(s for p,s in self.expected_backups)
      result= set(direntry.name for direntry in self.find_files(self.archivedir))
      self.assertEqual(result, expect)

      # decrypting backup
      my_litte_backup= [e for e in self.find_files(self.archivedir) if e.name.startswith("40aff2e")]
      self.assertEqual(len(my_litte_backup), 1)
      self.assertEqual(my_litte_backup[0].stat().st_size, 256+80) # 80 for salt, init vector, and checksum
      with crypto.open_bin(my_litte_backup[0], "r", self.password) as f:
         blk= f.read(8192)
         self.assertEqual(len(blk), 256)
         self.assertEqual(blk, bytearray(range(256)))

   def test_error_prevents_closing_backup_run(self):
      self.setup_directories()
      self.create_homedir_file(self.homedir+"/unreadable",23)
      class mock_make_backup_copy(object):
         def __call__(self, path, expected_checksum, backup_path, open_dst_function, password):
            raise RuntimeError("file changed while reading: "+path)
      with unittest.mock.patch('abus.backup.make_backup_copy', new_callable=mock_make_backup_copy):
         main.main(["test", "-f", self.configfile, "--backup"])
      with database.open(self.databasepath) as db:
         with db._get_connection("test_error_prevents_closing_backup_run") as conn:
            rs= conn.execute("select timestamp from run").fetchall()
            self.assertEqual(rs, [(None,)])
