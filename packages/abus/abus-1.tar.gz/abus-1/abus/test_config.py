import time
from abus import config
from abus.testbase import AbusTestBase

class ConfigTestser(AbusTestBase):
   def test_parse_date(self):
      def str2sec(s):
         return time.mktime(time.strptime(s, "%Y%m%d%H%M%S"))
      now= str2sec("20170912150000")
      for d in range(1,9):
         for t in range(8):
            for future_date in True, False:
               for future_time in True, False:
                  d_str= "20171003" if future_date else "20170912"
                  t_str= "-160723" if future_time else "-130905"
                  test_str= d_str[-d:] + t_str[:t]

                  if d in (4,6,8) and t in (0,5,7):
                     expect_str= "2016"+d_str[-4:] if future_date and d==4 else d_str
                     expect_str += (t_str[1:t]+"000000")[:6]
                     try:
                        self.assertEqual(config.parse_date(test_str, now), str2sec(expect_str))
                     except:
                        print("test string:", test_str)
                        raise
                  else:
                     with self.assertRaises(ValueError):
                        print("test string:", test_str, "result:", config.parse_date(test_str, now))

