# A simple task manager

import subprocess
import time
from Tools import *
from multiprocessing import cpu_count
from color_log import *


class TaskManager:
  m_maxTaskNumber = 1
  TaskKeeper = {}  # TaskKeeper is a dictionary
  m_cmdListsAndLogFiles = []  # A list to store all the command List
  m_LogOut = color_log()

  def __init__(self, maxTN=1):

    if maxTN > cpu_count():
      self.m_LogOut.error("  %d workers, %d cpu cores\n" % (maxTN, cpu_count()))
      # self.m_maxTaskNumber = cpu_count() - 1
    elif maxTN <= 0:
      maxTN = cpu_count() - 1
      self.m_LogOut.warn("AutoDecide workers.  %d workers, %d cpu cores\n" % (maxTN, cpu_count()))
    else:
      self.m_LogOut.warn("  %d workers, %d cpu cores\n" % (maxTN, cpu_count()))
      # self.m_maxTaskNumber = maxTN
    self.m_maxTaskNumber = maxTN
    self.TaskKeeper = {}
    self.m_cmdListsAndLogFiles = []


  def newTask(self, command, outFileName=None):
    '''
    execute command and dump the log into file
    params:
        command        : the command to execute
        outFileName    : dump the log to this file
    '''
    if len(self.TaskKeeper) < self.m_maxTaskNumber:
      if command != "":
        if outFileName != None:
          outFile = open(outFileName, 'w')
          self.m_LogOut.warn("Add new task: " + command + '\n')
          self.TaskKeeper.update({command: subprocess.Popen(command, stdout=outFile, stderr=outFile)})
        else:
          self.m_LogOut.warn("Add new task: " + command + '\n')
          self.TaskKeeper.update({command: subprocess.Popen(command, stdout=None, stderr=None)})

    else:
      # Wait until TaskKeeper has free space
      while True:
        time.sleep(0.1)
        for command, task in self.TaskKeeper.items():
          if task.poll() != None:  # Means task has terminated
            self.TaskKeeper.pop(command)

        if (len(self.TaskKeeper) < self.m_maxTaskNumber):
          break

      self.newTask(command, outFileName)


  def clearAllTask(self):
    '''
    Call after all newTask() has been called.
    '''

    while True:
      if (len(self.TaskKeeper) == 0):  # wait until all task finished
        self.m_LogOut.info("All tasks finished!")
        break
      for command, task in self.TaskKeeper.items():
        if task.poll() != None:
          self.TaskKeeper.pop(command)
      time.sleep(0.1)


  def newTaskList(self, commandList, outFileNameList, commandIdx=0):
    '''
    execute command in the commandList one by one and dump the log into file in outFileNameList
    params:
        commandList        : the command list to execute one by one
        outFileNameList    : the corresponding log file list
        commandIdx         : current command index to execute
    '''
    if len(commandList) == 0:
      return
    if commandIdx == 0:  # A new commandList arrives
      self.m_cmdListsAndLogFiles.append((commandList, outFileNameList))

    if len(self.TaskKeeper) < self.m_maxTaskNumber:
      if len(outFileNameList) > commandIdx:
        outFile = open(outFileNameList[commandIdx], 'w')
        if commandList[commandIdx] != "":  # empty command
          self.m_LogOut.warn("Add new task: " + commandList[commandIdx] + '\n')
          outFile.write(commandList[commandIdx] + "\n\n")
          self.TaskKeeper.update({commandList[commandIdx]: subprocess.Popen(commandList[commandIdx], shell=True, stdout=outFile, stderr=outFile)})
      else:
        if commandList[commandIdx] != "":  # empty command
          self.m_LogOut.warn("Add new task: " + commandList[commandIdx] + '\n')
          self.TaskKeeper.update({commandList[commandIdx]: subprocess.Popen(commandList[commandIdx], shell=True, stdout=None, stderr=None)})

    else:
      # Wait until TaskKeeper has free space
      while True:
        time.sleep(0.1)
        for command, task in self.TaskKeeper.items():
          if task.poll() != None:  # Means task has terminated
            self.TaskKeeper.pop(command)
            cmdInfo = self.getCommandInfo(command)
            cmdIndex = cmdInfo[0]
            cmdList = cmdInfo[1]
            fileList = cmdInfo[2]
            if cmdIndex < len(cmdList) - 1:  # The command list hasn't finished yet
              nextCmdIndex = cmdIndex + 1
              self.newTaskList(cmdList, fileList, nextCmdIndex)

        if (len(self.TaskKeeper) < self.m_maxTaskNumber):
          break

      self.newTaskList(commandList, outFileNameList, 0)


  def clearAllTaskList(self):
    '''
    Call after all newTaskList() has been called.
    '''

    while True:
      if (len(self.TaskKeeper) == 0):  # wait until all task finished
        self.m_LogOut.info("All tasks finished!")
        break
      for command, task in self.TaskKeeper.items():
        if task.poll() != None:
          if command != "":  # empty command
            self.TaskKeeper.pop(command)
            cmdInfo = self.getCommandInfo(command)
            cmdIndex = cmdInfo[0]
            cmdList = cmdInfo[1]
            fileList = cmdInfo[2]
            if cmdIndex < len(cmdList) - 1:  # The command list hasn't finished yet
              nextCmdIndex = cmdIndex + 1
              self.newTaskList(cmdList, fileList, nextCmdIndex)
      time.sleep(0.1)


  def getCommandInfo(self, command):
    '''
    Given a command, tell which commandList it belongs to in m_cmdListsAndLogFiles and also return the idx.
    '''
    for cmdListAndFileList in self.m_cmdListsAndLogFiles:
      cmdIndex = 0
      for cmd in cmdListAndFileList[0]:
        if cmd == command:
          return (cmdIndex, cmdListAndFileList[0], cmdListAndFileList[1])
        cmdIndex = cmdIndex + 1
    return None


  def __del__(self):

    while True:
      if (len(self.TaskKeeper) == 0):  # wait until all task finished
        break
      for command, task in self.TaskKeeper.items():
        if task.poll() != None:
          self.TaskKeeper.pop(command)
      time.sleep(0.1)
            
