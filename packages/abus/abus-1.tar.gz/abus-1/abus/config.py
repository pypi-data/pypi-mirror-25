import argparse
import logging
import os
import time

class ConfigurationError(Exception):
   pass

class Configuration(object):
   """Combined backup configuration options from command line, environment, and config file"""
   def __init__(self, argv):
      """
      Combined backup configuration options from command line, environment, and config file (determined
      by command line or environment.

      :param argv: command line arguments (`sys.argv`).
      """

      # Default values
      self.archive_root_path= None
      self.logfile_path= None
      self.include= []
      x= [
         "*#",
         "*.lck",
         "*.lock",
         "*.wav",
         "*/~*",
         "*/desktop.ini",
         "*/Ditto.db",
         "*/UsrClass.dat*",
         "*/ZbThumbnail.info",
         "*cache/*",
         "C:/cornie/.lesshst",
         "C:/cornie/.ssh",
         "C:/cornie/installers/cygwin",
         "C:/cornie/music",
         "C:/cornie/pictures",
         "C:/cornie/rawpictures",
         "C:/cornie/run/RYAplotter",
         "C:/cornie/scheduled.log",
         "C:/cornie/vimfiles",
         "C:/Users/*/Documents/My Music",
         "C:/Users/*/Documents/My Pictures",
         "C:/Users/*/Documents/My Videos",
         "C:/Users/philip/Documents/Need_For_Speed_Most_Wanted",
         "C:/Users/sonja/Documents/Trazenje posla",
         ]
      self.exclude= []
      self.password= None
      self.minimum_size_for_compression= 4096
      self.compressed_extensions= set([".jpg", ".tif", ".gz", ".tgz",])

      # Command line
      args= self._get_command_line_options(argv)
      if args.f is not None:
         config_path= args.f
      elif "ABUS_CONFIG" in os.environ:
         config_path= os.environ["ABUS_CONFIG"]
      else:
         raise ConfigurationError("Missing config file path (-f option or ABUS_CONFIG environment variable)")
      self.is_backup= args.backup
      self.is_restore= args.restore
      self.is_init= args.init
      self.list_all= args.a
      self.patterns= args.glob
      self.cutoff= args.d

      # Config file
      with open(config_path, encoding="utf-8") as f:
         try:
            self._parse_config_file(f)
         finally:
            # Initialising log file now because it might be possible despite a subsequent
            # error during parsing.
            if self.logfile_path:
               logging.basicConfig(filename=self.logfile_path,
                                   level=logging.DEBUG,
                                   format='%(asctime)s %(levelname)-7s %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S',
                                   )

      if (self.is_init or self.is_backup) and (self.is_restore or self.list_all or self.cutoff) \
              or self.is_init and self.is_backup:
         raise ConfigurationError("conflicting command line options (--backup/--init/-r/-a/-d)")
      if not self.archive_root_path:
         raise ConfigurationError("archive directory option not set")
      if not os.path.isdir(self.archive_root_path):
         raise ConfigurationError("missing archive directory ({})".format(self.archive_root_path))
      if not self.password:
         raise ConfigurationError("password directory option not set")
      if not self.include:
         raise ConfigurationError("missing or empty [include] section")
      if not self.logfile_path:
         raise ConfigurationError("logfile path option not set")

   def _parse_config_file(self, lines):
      self.include= []
      self.exclude= []
      section= None
      for line in lines:
         line= line.strip()
         if not line or line.startswith('#'):
            pass
         elif line.lower().startswith("[incl"):
            section= self.include
         elif line.lower().startswith("[excl"):
            section= self.exclude
         elif line.lower().startswith("["):
            raise ConfigurationError("unknown section name: "+line)
         elif section is not None:
            line= line.replace("\\", "/")
            if line.endswith("/"): line= line[:-1]
            section.append(line)
         else:
            splut= line.split(maxsplit=1)
            if len(splut)!=2:
               raise ConfigurationError("missing value: "+line)
            keyword, args = splut
            if keyword=="archive":
               self.archive_root_path= args
            elif keyword=="logfile":
               self.logfile_path= args
            elif keyword=="password":
               self.password= args
            else:
               raise ConfigurationError("unknown option: "+keyword)

   def _get_command_line_options(self, argv):
      parser= argparse.ArgumentParser(prog=os.path.basename(argv[0]),
         #usage='PROG [-f configfile] --backup',
         description="The Abingdon BackUp Scripts can make copies of files "
         "(defined in the abus config file) to an archive location "
         "and restore the backups to the current directories. "
         "By default files in the archive are listed.",
         )
      parser.add_argument('-f',
         action='store',
         metavar='path',
         help="path to config file required for defining backup location etc. "
         "Defaults to value of the ABUS_CONFIG environment variable")
      parser.add_argument('--init',
                          action='store_true',
                          help='creates an empty database in archive directory')
      parser.add_argument('--backup',
         action='store_true',
         help="backs up files to archive rather than listing files in archive.")
      parser.add_argument('-r', '--restore',
         action='store_true',
         help="restores files from archive to current directory rather than listing files in archive.")
      parser.add_argument('-a',
         action='store_true',
         help="includes all matching file versions in listing or restore "
         "rather than only the latest matching version of each file")
      parser.add_argument('-d',
         action='store',
         type=parse_date,
         metavar="datetime",
         help="cut-off time (format [[cc]yy]mmdd[-HHMM[SS]]) from which files are not included in "
         "listig or restore. Year defaults to current or previous if date would be in the future. "
         "Time defaults to midnight. Note that to show all files in May, the argument must be 0601")
      parser.add_argument('glob',
         nargs='*',
         help="File path pattern (* matches /) of file to be included in listing or restore")
      return parser.parse_args(argv[1:])

   @property
   def database_path(self):
      return self.archive_root_path+"/index.sl3"

   def backup_path_abs(self, archive_dir_rel, checksum):
      return self.archive_root_path +"/" +archive_dir_rel +"/" +checksum

def parse_date(string, now=None):
   today_str= time.strftime("%Y%m%d", time.localtime(now))
   d_str, minus, t_str = string.partition("-")
   if (t_str=="") == (minus==""):
      if len(d_str) in(4,6,8) and len(t_str) in(0,4,6):
         if d_str.isdigit():
            if t_str=="" or t_str.isdigit():
               full_t_str= t_str + "000000"[len(t_str):]
               full_d_str= today_str[:8-len(d_str)] + d_str
               if len(d_str)==4 and full_d_str > today_str:
                  last_year= int(today_str[:4])-1
                  full_d_str= str(last_year) + d_str
               tm= time.strptime(full_d_str + full_t_str, "%Y%m%d%H%M%S")
               return time.mktime(tm)
   raise ValueError()

