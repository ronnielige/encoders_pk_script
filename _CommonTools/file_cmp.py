import os
import filecmp
import sys
from Tools import *
from color_log import *


def fileCompareAndDel(file_a, file_b, file_log_cmptrue, file_log_cmpfalse, del_file_flag_cmptrue, del_file_flag_cmpfalse, misc_info):
  dc = filecmp.cmp(file_a, file_b)
  logout = color_log()
  if dc:
    logout.warn("\"%s\" and \"%s\" are identical, Congratulation!\n" % (file_a, file_b))
    # if file_log_cmptrue != None:
    # f = open(file_log_cmptrue, 'w')
    # f.write("\"%s\" and \"%s\" are identical\n"%(file_a, file_b));
    # f.close()
    if del_file_flag_cmptrue == "1":
      # logout.warn("aaaa\n")
      os.remove(file_a)
      # os.system("del %s" % file_a)
    if del_file_flag_cmptrue == "2":
      # logout.warn("bbbb\n")
      os.remove(file_b)
      # os.system("del %s" % file_b)
    if del_file_flag_cmptrue == "3":
      # logout.warn("cccc\n")
      os.remove(file_a)
      os.remove(file_b)
      # os.system("del %s %s" % (file_a, file_b))
  else:
    logout.error("\"%s\" and \"%s\" are not identical!!!\n" % (file_a, file_b))
    if file_log_cmpfalse != None:
      f = open(file_log_cmpfalse, 'w')
      f.write("\"%s\"\nand\n\"%s\"\nare not identical!!!\n\n" % (file_a, file_b))
      if misc_info != None:
        misc_infos = misc_info.split('\t')
        for info in misc_infos:
          f.write(info)
          f.write("\n\n")
      f.close()
    if del_file_flag_cmpfalse == "1":
      # logout.warn("aaaa\n")
      os.remove(file_a)
      # os.system("del %s" % file_a)
    if del_file_flag_cmpfalse == "2":
      # logout.warn("bbbb\n")
      os.remove(file_b)
      # os.system("del %s" % file_b)
    if del_file_flag_cmpfalse == "3":
      # logout.warn("cccc\n")
      os.remove(file_a)
      os.remove(file_b)
      # os.system("del %s %s" % (file_a, file_b))


if __name__ == "__main__":
  logout = color_log()
  # logout.warn("hiiiiiiii\n")
  if (len(sys.argv) >= 3):
    file_a = sys.argv[1]
    file_b = sys.argv[2]

    if (len(sys.argv) >= 4):
      file_log_cmptrue = sys.argv[3]
    else:
      file_log_cmptrue = None

    if (len(sys.argv) >= 5):
      file_log_cmpfalse = sys.argv[4]
    else:
      file_log_cmpfalse = None

    if (len(sys.argv) >= 6):
      del_file_flag_cmptrue = sys.argv[5]
    else:
      del_file_flag_cmptrue = None

    if (len(sys.argv) >= 7):
      del_file_flag_cmpfalse = sys.argv[6]
    else:
      del_file_flag_cmpfalse = None

    if (len(sys.argv) >= 8):
      misc_info = sys.argv[7]
    else:
      misc_info = None

    if CheckFile(file_a) and CheckFile(file_b):
      fileCompareAndDel(file_a, file_b, file_log_cmptrue, file_log_cmpfalse, del_file_flag_cmptrue, del_file_flag_cmpfalse, misc_info)
    else:
      logout.error("%s or %s doesn't exist!" % (file_a, file_b))
      if file_log_cmpfalse != None:
        f = open(file_log_cmpfalse, 'w')
        f.write("\"%s\"\nor\n\"%s\"\ndoesn't exist!!!!\n\n" % (file_a, file_b))
        if misc_info != None:
          misc_infos = misc_info.split('\t')
          for info in misc_infos:
            f.write(info)
            f.write("\n\n")
        f.close()
  else:
    logout.error("Must given 2 file name to compare!")