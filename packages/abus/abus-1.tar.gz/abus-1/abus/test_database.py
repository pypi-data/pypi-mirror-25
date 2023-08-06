import itertools
import sqlite3
from pprint import pprint
from abus import database
from abus.testbase import AbusTestBase

class DatabaseTests(AbusTestBase):
   def test_database_get_archive(self):
      self.setup_directories()
      checksums= ("e{:03}".format(i) for i in itertools.count()).__iter__()
      timestamps= itertools.count(1506159900, 50).__iter__()
      all_files= ["c:/home/file_{}.txt".format(c) for c in "abcdefghxy"]
      file_states= {}
      data= [] # (run_name, timestamp, path, checksum, archive_dir) list
      for run,files in [("2017-09-22 12:45","abcdefghxy"),
                        ("2017-09-23 12:45","xy"),
                        ("2017-09-24 12:45","bcdefghx"),
                        ("2017-09-25 12:45","abcfghy"),
                       ]:
         for c in files:
            file_states[c]= timestamps.__next__(), checksums.__next__()
         # this sometimes "touches" b, tests that some content is not listed twice:
         file_states["b"]= timestamps.__next__(), file_states["b"][1]
         data.extend((run,ts,"c:/home/file_{}.txt".format(c),cs,cs[:2]+"/"+cs[2:])
                     for c,(ts,cs) in file_states.items())
      with sqlite3.connect(self.databasepath) as conn:
         conn.executemany("insert into location(checksum, archive_dir) values(?,?)", set(t[3:5] for t in data))
         conn.executemany("insert into content(run_name, timestamp, path, checksum) values(?,?,?,?)", (t[0:4] for t in data))
         conn.execute("insert into run(run_name, timestamp) select run_name, max(timestamp) from content group by run_name")

      with database.open(self.databasepath) as db:
         def test_one(cutoff_date, show_all, nearly_expect):
            # nearly_expect may still contain duplicate (file,content) with different timestamps
            pacs= set((p,a,c)for p,t,a,c in nearly_expect)
            ptacs= [min(ptac for ptac in nearly_expect if ptac[0]==p and ptac[2]==a and ptac[3]==c) for p,a,c in pacs]
            expect= sorted(ptacs, key= lambda ptac: (ptac[0],-ptac[1]))
            result= list(db.get_archive_contents([], cutoff_date, show_all))
            self.assertEqual(result, expect)

            expect= [ptac for ptac in expect if ptac[0][-5] in "ab"]
            result= list(db.get_archive_contents(['*a.txt','*b.txt'], cutoff_date, show_all))
            self.assertEqual(result, expect)

            expect= [ptac for ptac in expect if ptac[0][-5]=="a"]
            result= list(db.get_archive_contents(['*a.txt'], cutoff_date, show_all))
            self.assertEqual(result, expect)

         test_one(cutoff_date=None, show_all=False,
                  nearly_expect= [(p,t,a,c) for r,t,p,c,a in data if r=="2017-09-25 12:45"],
                  )
         test_one(cutoff_date=None, show_all=True,
                  nearly_expect= [(p,t,a,c) for r,t,p,c,a in data],
                  )

         by_path= {}
         for cutoff in sorted(set(t for r,t,p,c,a in data)):
            try:
               test_one(cutoff_date=cutoff, show_all=True,
                        nearly_expect= [(p,t,a,c) for r,t,p,c,a in data if t<=cutoff],
                        )
               by_path.update({p:(p,t,a,c) for r,t,p,c,a in data if t==cutoff})
               test_one(cutoff_date=cutoff, show_all=False,
                        nearly_expect= by_path.values(),
                        )
            except:
               print("iteration data:", cutoff, by_path)
               raise
