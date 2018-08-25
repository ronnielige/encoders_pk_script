import os
import re
import glob
import datetime

def AppendLine(input_f, line, b_cover_result=True):
    b_line_exists = False
    if b_cover_result == False: # should not over write
        f = open(input_f, 'r')
        rline = f.readline()
        while rline:
            if rline.find(line) >= 0:
                b_line_exists = True
                break
            line = f.readline()
        f.close()

    if b_cover_result or b_line_exists == False:
        f = open(input_f, 'a')
        f.write(line + "\n")
        f.close()

def ReplaceLine(input_f, output_f, key_word, new_line):
    inf = open(input_f, 'r')
    outf = open(output_f)

def ClearFile(input_f):
    f = open(input_f, 'w')
    f.close()

def CheckPath(pathName, createIfNotExist=0):
  if not os.path.exists(pathName):
    if createIfNotExist:
      os.mkdir(pathName)
      print pathName + "created!!!"
    return 0
  return 1


def CheckFile(FileName):
  if not os.path.exists(FileName):
    return 0
  return 1


def DelFiles(FileName):
  for fl in glob.glob(FileName):
    # Do what you want with the file
    os.remove(fl)
    # os.system("del %s" % FileName)


def FindFileNameStartWith(path, name_start):
  candidate_files = []
  for i in os.listdir(path):
    if os.path.isfile(os.path.join(path, i)) and name_start in i:
      candidate_files.append(i)
  return candidate_files

def getDateTime():
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return nowTime

if __name__ == '__main__':
    print getDateTime()
