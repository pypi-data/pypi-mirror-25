import logging
import os
import sys
import traceback

from abus import config
from abus import backup, database
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
         with database.open(cfg.database_path,allow_create=True):
            print("created", cfg.database_path)
      else:
         list_restore.list_archive(cfg)
   except config.ConfigurationError as e:
      error_message= str(e)
   except RuntimeError as e:
      error_message= str(e)
   except Exception as e:
      error_message= "\n".join(traceback.format_exception(type(e), e, e.__traceback__))
   else:
      return 0

   print("Error:", error_message, file=sys.stderr)
   if logging.root.handlers: # tests that logging could be initialised before error occurred
      logging.error(error_message)

   return 1


#
# TODO test that errors are issued if directory cannot be read
#
