import os.path
import queue
import sqlite3
import time
from contextlib import contextmanager

@contextmanager
def open(database_path, allow_create=False):
   db= _Database(database_path, allow_create)
   yield db
   db.close()

class _Database(object):
   def __init__(self, database_path, allow_create):
      self.path= database_path
      self.connection_pool_size= 1
      self.connection_pool= queue.Queue()
      existed= os.path.exists(database_path)
      if not existed and not allow_create:
         raise RuntimeError("could not find database "+database_path)
      for _ in range(self.connection_pool_size):
         conn= sqlite3.connect(database_path, timeout=60, check_same_thread=False)
         conn.isolation_level= None # autocommit
         self.connection_pool.put(conn)
      if not existed:
         self._create_tables()
   def close(self):
      for _ in range(self.connection_pool_size):
         self.connection_pool.get().close()

   @contextmanager
   def _get_connection(self, caller):
      conn= self.connection_pool.get()
      try:
         yield conn
      finally:
         self.connection_pool.put(conn)

   def _make_runname(self, timestamp):
      tm= time.localtime(timestamp)
      # format chosen to make the run name a "word" in most editors:
      return time.strftime("%Y_%m_%d_%H%M", tm)

   def _create_tables(self):
      with self._get_connection("_create_tables") as conn:
         conn.execute("""create table content(
            run_name text not null,
            path text not null,
            timestamp float not null,
            checksum text not null)""")
         conn.execute("create unique index content_pk on content(run_name, path)")
         conn.execute("""create table checksum_cache(
            dev int not null,
            ino int not null,
            timestamp float not null,
            checksum text not null)""")
         conn.execute("create table run(run_name text not null, timestamp float)")
         conn.execute("create unique index run_pk on run(run_name)")
         conn.execute("create unique index checksum_cache_pk on checksum_cache(dev, ino)")
         conn.execute("""create table location(
            checksum text not null,
            archive_dir text not null)""")
         conn.execute("create unique index location_pk on location(checksum)")
         conn.execute("create index location_archivedir on location(archive_dir)")

   def open_backup_run(self):
      run_name= self._make_runname(time.time())
      with self._get_connection("open_backup_run") as conn:
         conn.execute("insert into run(run_name) values(?)", [run_name])
      return run_name

   def complete_backup_run(self, run_name):
      with self._get_connection("close_backup_run") as conn:
         cur= conn.execute("update run set timestamp=? where run_name = ?", [time.time(), run_name])
         if cur.rowcount!=1:
            raise RuntimeError("could not complete run "+run_name)
         conn.execute("delete from run where timestamp is null")

   def get_purgeable_backups(self):
      """Returns iterable of (age_factor, checksum) for all backups that are no longer current.
      File with largest age_factor is most preferred for purging.
      """
      with self._get_connection("get_purgeable_backups") as conn:
         cur= conn.execute("""select CHECKSUM.checksum
                  ,CHECKSUM.birthtime
                  ,min(run.timestamp) as deathtime
               from (select checksum, min(timestamp) as birthtime, max(run_name) as last_alive
                     from content
                     group by checksum
                     ) as CHECKSUM
                  join run on run.run_name > CHECKSUM.last_alive and run.timestamp is not null
                  left join content on content.run_name = run.run_name and content.checksum = CHECKSUM.checksum
               where content.checksum is null
               group by CHECKSUM.checksum, CHECKSUM.birthtime
            """)
         now= time.time()
         return (((now - deathtime) / (deathtime - birthtime), checksum) for checksum,birthtime,deathtime in cur)

   def lookup_checksum(self, st_dev, st_ino, timestamp):
      with self._get_connection("lookup_checksum") as conn:
         for (checksum,) in conn.execute("""
               select checksum
                  from checksum_cache
                  where dev=? and ino=? and timestamp=?""", (st_dev, st_ino, timestamp)):
            return checksum
         return None

   def remember_checksum(self, st_dev, st_ino, timestamp, checksum):
      with self._get_connection("remember_checksum") as conn:
         cur= conn.execute("""
            update checksum_cache
            set timestamp= ?, checksum= ?
            where dev=? and ino=?""", (timestamp, checksum, st_dev, st_ino))
         if cur.rowcount==0:
            conn.execute("insert into checksum_cache(timestamp, checksum, dev, ino) values(?,?,?,?)",
               (timestamp, checksum, st_dev, st_ino))

   def lookup_archivedir(self, checksum):
      with self._get_connection("lookup_archivedir") as conn:
         for (archive_dir,) in conn.execute("select archive_dir from location where checksum=?", [checksum]):
            return archive_dir
         return None

   def remember_archivedir(self, checksum, archive_dir_rel):
      with self._get_connection("remember_archivedir") as conn:
         conn.execute("insert into location(checksum, archive_dir) values(?,?)", (checksum, archive_dir_rel))

   def add_backup_entry(self, run_name, path, timestamp, checksum):
      with self._get_connection("add_backup_entry") as conn:
         conn.execute("""insert into content(run_name, path, timestamp, checksum)
            values(?,?,?,?)""", (run_name, path, timestamp, checksum))

   def getarchivedir_usage(self):
      with self._get_connection("getarchivedir_usage") as conn:
         rows= conn.execute("select archive_dir, count(*) as n from location group by archive_dir")
         return {archive_dir:n for archive_dir,n in rows}

   def get_archive_contents(self, patterns, cutoff_date, show_all):
      """

      :param pattern: like-operator patterns for path to match any of
      :type pattern: string list
      :param cutoff_date: time after which files are ignored or None
      :type cutoff_date: time.time() format
      :param show_all: whether all files should be returned rather than just those from the latest run
      :type show_all: bool
      :return: iterable of (path, timestamp, archive_dir, checksum)
      :rtype:
      """
      with self._get_connection("get_archive_contents") as conn:
         sql= "select distinct path, min(timestamp), archive_dir, content.checksum from content"
         sql_args= []
         where_clauses= [] # to be built now but added later
         where_args= []

         if cutoff_date is None:
            if show_all:
               # show all without cutoff date is just everything
               pass
            else:
               # show one without cutoff means latest run
               where_clauses.append("run_name = (select max(run_name) from content)")
         else:
            if show_all:
               # show all with cutoff date
               where_clauses.append("timestamp <= ?")
               where_args.append(cutoff_date)
            else:
               # show one with cutoff date requires subquery for the latest
               sql += " join (select path as p, max(timestamp) as t from content "
               sql +=       " where timestamp <= ?"
               sql_args.append(cutoff_date)
               sql +=       " group by path) as latest"
               sql +=  " on path = latest.p and timestamp = latest.t"

         sql += " join location on location.checksum = content.checksum"

         if patterns:
            where_clauses.append("("
               +" or ".join("path glob ?" for x in patterns)
               +")")
            where_args.extend(patterns)

         if where_clauses:
            sql += " where " + " and ".join(where_clauses)
            sql_args.extend(where_args)

         sql += " group by path, archive_dir, content.checksum"
         sql += " order by path, min(timestamp) desc"
         yield from conn.execute(sql, sql_args)

   def testing_move_timestamps(self, offset):
      """Adds `offset` to all timestamps in the database, including run names,
      in order to allow backups made at the same time for testing
      to have different names"""
      with self._get_connection("testing_move_timestamps") as conn:
         conn.execute("update run set timestamp= timestamp+?", [offset])
         conn.execute("update content set timestamp= timestamp+?", [offset])

         runs= conn.execute("select run_name, timestamp from run").fetchall()
         params= []
         for old_names, timestamp in runs:
            params.extend((old_names, self._make_runname(timestamp)))
         case_clause= "when ? then ? "*len(runs) +"end"
         conn.execute("update content set run_name= case run_name "+case_clause, params)
         conn.execute("update run set run_name= case run_name "+case_clause, params)
