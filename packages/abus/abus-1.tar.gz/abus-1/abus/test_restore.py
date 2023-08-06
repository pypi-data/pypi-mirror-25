import os
from abus import main, backup, crypto, database
from abus.testbase import AbusTestBase

class RestoreTests(AbusTestBase):
   def test_simple_restore(self):
      self.setup_backup_with_well_known_checksums()
      self.remove_dir_contents(self.restoredir)
      main.main(["test", "-f", self.configfile, "-r"])
      self.assertEqual(sum(1 for _ in self.find_files(self.restoredir)), len(self.expected_backups))
      for relpath, archive_name in self.expected_backups:
         actual= backup.calculate_checksum(self.restoredir+"/"+relpath)
         expected= archive_name[:64]
         self.assertEqual(actual, expected)

   def test_restore_does_not_overwrite(self):
      self.setup_backup_with_well_known_checksums()
      self.remove_dir_contents(self.restoredir)
      filenames= [path.partition("/")[0] for path,_ in self.expected_backups]
      for filename in filenames:
         with open(filename,"w",newline='\n') as f: f.write("Hello World\n")
      main.main(["test", "-f", self.configfile, "-r"])
      for filename in filenames:
         actual= backup.calculate_checksum(filename)
         self.assertEqual(actual, "d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26")

   def test_no_partial_backupfile_is_left(self):
      self.setup_backup_with_well_known_checksums()
      relpath, archivename= max(self.expected_backups)
      path= self.homedir+"/"+relpath
      expected_checksum= "42" # causes Exception which is expected not to leave file behind
      password= "Would you like to buy some air?"
      open_dst_function= crypto.open_lzma
      backup_path= self.archivedir+"/42"
      with self.assertRaisesRegex(Exception, "file changed while reading"):
         backup.make_backup_copy(path, expected_checksum, backup_path, open_dst_function, password)
      self.assertFalse(os.path.exists(backup_path))
      self.assertFalse(os.path.exists(backup_path+".part"))
      # making doubly sure the file would normally have been created (the source path might just be wrong, for example):
      backup.make_backup_copy(path, archivename[:64], backup_path, open_dst_function, password)
      self.assertTrue(os.path.exists(backup_path))
      self.assertFalse(os.path.exists(backup_path+".part"))

   def test_allversions_restore(self):
      self.setup_multiple_backups()
      n_versions= sum(1 for direntry in self.find_files(self.archivedir)
                        if len(direntry.name) in(64,66))
      main.main(["test", "-f", self.configfile, "-r", "-a"])
      self.find_files(self.restoredir)
      n_restored= sum(1 for _ in self.find_files(self.restoredir))
      self.assertEqual(n_restored, n_versions)
