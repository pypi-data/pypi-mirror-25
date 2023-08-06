# -*- coding: UTF-8 -*-
# Copyright © 2017 Cornelius Grotjahn - This file is covered by the LICENCE file in project root directory.
import logging
import os
import sys
import traceback

from abus import config
from abus import backup, database, reconstruct
from abus import list_restore

def main(argv):
   try:
      cfg= config.Configuration(argv)
      if cfg.is_backup:
         backup.do_backup(cfg)
      elif cfg.is_restore:
         list_restore.restore(cfg)
      elif cfg.is_init:
         if os.path.exists(cfg.database_path):
            raise config.ConfigurationError(cfg.database_path+" exists already")
         with database.connect(cfg.database_path, allow_create=True):
            print("created", cfg.database_path)
      elif cfg.is_location_reconstruction:
         reconstruct.reconstruct_location(cfg)
      else:
         list_restore.list_archive(cfg)
   except config.ConfigurationError as e:
      error_message= str(e)
   except RuntimeError as e:
      error_message= str(e)
   except Exception as e:
      error_message= "".join(traceback.format_exception(type(e), e, e.__traceback__))
   else:
      logging.shutdown()
      return 0

   print("Error:", error_message, file=sys.stderr)
   if logging.root.handlers: # tests that logging could be initialised before error occurred
      logging.error(error_message)

   logging.shutdown()
   return 1

