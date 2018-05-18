import os
import re

# Base class FileParser
class BaseFileParser:
  m_fileName = ""
  m_matchPattern = ""

  def __init__(self, fileName):
    self.m_fileName = fileName

  def compile(self, pattern, flag=re.M):
    self.m_matchPattern = re.compile(pattern, flag)

  def findPatternInFile(self):
    if not os.path.exists(self.m_fileName):
      return []

    file = open(self.m_fileName, 'r')
    content = file.read()
    file.close()
    match = self.m_matchPattern.findall(content)

    return match