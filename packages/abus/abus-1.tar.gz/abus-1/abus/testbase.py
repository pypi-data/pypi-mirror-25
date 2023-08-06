import itertools
import os
import shutil
import unittest

from abus import database, main

class AbusTestBase(unittest.TestCase):
   @staticmethod
   def remove_dir_contents(path):
      for direntry in os.scandir(path):
         if direntry.is_dir():
            shutil.rmtree(direntry.path)
         elif direntry.is_file():
            os.unlink(direntry.path)

   @staticmethod
   def find_files(start):
      """Returns direntries for all files in `start`, recursively"""
      for direntry in os.scandir(start):
         if direntry.is_file():
            yield direntry
         elif direntry.is_dir():
            yield from AbusTestBase.find_files(direntry.path)

   @staticmethod
   def create_homedir_file(path, prime):
      os.makedirs(os.path.dirname(path), exist_ok=True)
      with open(path,"wb") as f:
         f.write(bytes(n*prime%256 for n in range(8192)))

   def setup_directories(self):
      candidates_for_tmp= ["C:/tmp", "C:/temp"]
      if "TEMP" in os.environ: candidates_for_tmp.append(os.environ["TEMP"])
      for tempdir in candidates_for_tmp:
         if os.path.isdir(tempdir):
            break
      else:
         raise Exception("Could not find a temporary directory for tests")

      self.password= "Sesam, öffne dich!"
      self.homedir= tempdir + "/abushome"
      self.archivedir= tempdir + "/abusarchive"
      self.restoredir= tempdir + "/abusrestore"
      os.makedirs(self.homedir, exist_ok=True)
      os.makedirs(self.archivedir, exist_ok=True)
      os.makedirs(self.restoredir, exist_ok=True)
      os.chdir(self.restoredir)

      # empty them
      self.remove_dir_contents(self.homedir)
      self.remove_dir_contents(self.archivedir)
      self.remove_dir_contents(self.restoredir)

      self.configfile= tempdir + "/abusconfig.cfg"
      with open(self.configfile, "w", encoding="utf-8") as f:
         print("logfile", tempdir+"/abuslog.txt", file=f)
         print("archive", self.archivedir, file=f)
         print("password", self.password, file=f)
         print("[include]", file=f)
         print(self.homedir, file=f)

      with database.open(self.databasepath, allow_create=True) as db:
         pass

   def setup_backup_with_well_known_checksums(self):
      self.setup_directories()
      self.expected_backups= set() # contains (path rel to homedir, backup filename) pairs

      path= "my_valueable_file"
      with open(self.homedir+"/"+path, "w", encoding="utf-8") as f:
         for n in range(400):
            for p in range(10):
               print(n**p, file=f, end="")
            print(file=f)
      self.expected_backups.add((path,"73672933c00ab3cd730c8715a392ee6dee9ba2c0a8e5e5d07170b6544b0113ef.z"))

      path= "my_little_file"
      with open(self.homedir+"/"+path, "wb") as f:
         f.write(bytearray(range(256)))
      self.expected_backups.add((path,"40aff2e9d2d8922e47afd4648e6967497158785fbd1da870e7110266bf944880"))

      path= "subdir_a/I_am_in_a.tif"
      self.create_homedir_file(self.homedir+"/"+path, 31)
      self.expected_backups.add((path,"498630374d56ea4c53c5baaee00b630be09ca5dbe678b11b1a81b37f1058635f"))

      path= "subdir_b/I_am_in_b.bin"
      self.create_homedir_file(self.homedir+"/"+path, 97)
      self.expected_backups.add((path,"1244d0711c6534ee79a6d3b82cea33b76e766e46cbca75791ac9fa3a30e365f3.z"))

      main.main(["test", "-f", self.configfile, "--backup"])

   def setup_multiple_backups(self):
      self.setup_directories()
      def primes():
         prev= [2]
         for c in itertools.count(3,2):
            for p in prev:
               if p*p>c:
                  yield c
                  prev.append(c)
                  break
               if c%p==0: break
      primes= primes().__iter__()

      all_paths= ["a", "b", "s/a", "s/b", "t/a", "t/b"]
      n= len(all_paths)*3//4
      for change_paths in all_paths, all_paths[:n], all_paths[-n:]:
         for path in change_paths:
            self.create_homedir_file(self.homedir+"/"+path, primes.__next__())
         main.main(["test", "-f", self.configfile, "--backup"])
         with database.open(self.databasepath) as db:
            db.testing_move_timestamps(-3000)
   @property
   def databasepath(self):
      return self.archivedir+"/index.sl3"
