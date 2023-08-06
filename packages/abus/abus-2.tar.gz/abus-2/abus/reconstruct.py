import logging
import os
import re

from abus import config, database

def reconstruct_location(cfg):
   """
   Reconstructs the location table from scanning the archive dir

   :type cfg: Configuration
   """
   logging.info("starting location index reconstruction")
   re_archive_filename= re.compile(r"[0-9a-f]{64}")
   result= {}
   dirqueue= [cfg.archive_root_path]
   while dirqueue:
      dirpath= dirqueue.pop()
      archive_dir= os.path.relpath(dirpath, start=cfg.archive_root_path).replace("\\","/")
      for direntry in os.scandir(dirpath):
         if direntry.is_dir():
            dirqueue.append(direntry.path)
         elif direntry.is_file():
            m= re_archive_filename.match(direntry.name)
            if m:
               checksum= m.group(0)
               result[checksum]= archive_dir
   with database.connect(cfg.database_path) as db:
      inserts, deltes, updates = db.reconstruct_location(result)

   logging.info("location index reconstruction added %d, removed %d, changed %d entries", inserts, deltes, updates)
