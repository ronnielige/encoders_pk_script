# coding=gbk

import threading
import os
import codecs
import re
import subprocess
import sys
import time

from Tools import *

class ResultCollector():

  def __init__(self, source_dir, output_file):
    self.source_dir  = source_dir
    self.output_file = output_file
    # some re pattern to extract key info
    self.h265id_pattern = re.compile("[a-zA-Z]+?265")
    self.yuvfile_pattern = re.compile("[a-zA-Z0-9_]+?\d+?x\d+")
    self.qp_pattern = re.compile("RC\d+_\d+")
    self.preset_pattern = re.compile("P\d-psnr")
    self.preset_subpattern = re.compile("\d")
    self.psnr_pattern = re.compile("psnr\d+\.*\d+_\d+\.*\d+_\d+\.*\d+")
    self.psnr_y_subpatterm = re.compile("\d+\.*\d+")
    self.psnr_u_subpatterm = re.compile("_\d+\.*\d+_")
    self.psnr_v_subpatterm = re.compile("_\d+\.*\d+$")
    self.ssim_pattern = re.compile("ssim\d+\.*\d+_\d+\.*\d+_\d+\.*\d+")
    self.ssim_y_subpatterm = re.compile("\d+\.*\d+")
    self.ssim_u_subpatterm = re.compile("_\d+\.*\d+_")
    self.ssim_v_subpatterm = re.compile("_\d+\.*\d+$")
    self.bitrate_pattern = re.compile("kbps\d+\.*\d+")
    self.enctime_pattern = re.compile("-s\d+\.*\d+")
    #self.cu_ana_ratio_pattern = re.compile("cu_ana_ratio_\d+\.*\d+_\d+\.*\d+_\d+\.*\d+_\d+\.*\d+_\d+\.*\d+")
    self.cu_ana_ratio_pattern = re.compile("cu_ana_ratio((_\d+\.*\d+){1,5})")
    self.cu_ana_ratio_subpattern = re.compile("\d+\.*\d+")

  def list_pinfo_files(self):
    if sys.platform == 'linux2':
      lscmd = subprocess.Popen("ls -l *_pinfo*", shell=True, cwd=self.source_dir, stdout=subprocess.PIPE)
      time.sleep(0.1)
      result = lscmd.stdout.read().split('\n')
    elif sys.platform == 'win32':
      try:
        lscmd = subprocess.Popen("dir /B *_pinfo*", shell=True, cwd=self.source_dir, stdout=subprocess.PIPE)
        time.sleep(0.1)
        result = lscmd.stdout.read().split('\r\n')
      except Exception, e:
        return None
    else:
      return None
    result.remove('') # remove empty elements
    return result

  def analysis_pinfo(self, content):
    try:
      h265_id = self.h265id_pattern.findall(content)[0]
      yuvfile = self.yuvfile_pattern.findall(content)[0]
      qp      = int(self.qp_pattern.findall(content)[0][-2:])
      preset  = self.preset_pattern.findall(content)[0]
      preset  = int(self.preset_subpattern.findall(preset)[0])
      psnr_info  = self.psnr_pattern.findall(content)[0]
      psnr_y = float(self.psnr_y_subpatterm.findall(psnr_info)[0])
      psnr_u = float(self.psnr_u_subpatterm.findall(psnr_info)[0][1:-1])
      psnr_v = float(self.psnr_v_subpatterm.findall(psnr_info)[0][1:])
      ssim_info  = self.ssim_pattern.findall(content)[0]
      ssim_y = float(self.ssim_y_subpatterm.findall(ssim_info)[0])
      ssim_u = float(self.ssim_u_subpatterm.findall(ssim_info)[0][1:-1])
      ssim_v = float(self.ssim_v_subpatterm.findall(ssim_info)[0][1:])
      bitrate = float(self.bitrate_pattern.findall(content)[0][4:])
      enctime = float(self.enctime_pattern.findall(content)[0][2:])
      cu_ana_ratio = []
      try:
        cu_ana_ratio = self.cu_ana_ratio_pattern.findall(content)[0][0]
        cu_ana_ratio = self.cu_ana_ratio_subpattern.findall(cu_ana_ratio)
      except:
        cu_ana_ratio = []
      return [h265_id, yuvfile, bitrate, qp, preset, psnr_y, psnr_u, psnr_v, ssim_y, ssim_u, ssim_v, enctime] + cu_ana_ratio
    except Exception, e:
      return None


  def runCollect(self):
    idx_file = 1
    idx_bitrate = 2
    idx_qp = 3
    idx_preset = 4
    idx_psnr_y = 5
    idx_psnr_u = 6
    idx_psnr_v = 7
    idx_ssim_y = 8
    idx_ssim_u = 9
    idx_ssim_v = 10
    idx_enctime = 11
    idx_cu64_ana_ratio = 12
    idx_cu32_ana_ratio = 13
    idx_cu16_ana_ratio = 14
    idx_cu8_ana_ratio = 15
    idx_pu4_ana_ratio = 16

    self.pinfos = self.list_pinfo_files()
    if self.pinfos == None or len(self.pinfos) == 0:
      return

    self.num_pinfos = len(self.pinfos)
    extract_info_array = []
    for infos in self.pinfos:
      if(self.analysis_pinfo(infos) == None):
        continue
      extract_info_array.append(self.analysis_pinfo(infos))

    # list all yuvfiles
    yuvs = []
    for infos in extract_info_array:
      yuvs.append(infos[idx_file])
    self.source_files = list(set(yuvs))
    self.source_files.sort()
    # list all presets
    ps = []
    for infos in extract_info_array:
      ps.append(infos[idx_preset])
    self.presets = list(set(ps))
    self.presets.sort()

    try:
      outf = open(self.output_file, 'w')
    except Exception, e:
      return

    cnt = 0
    title = "%-34s"%("YUVFile") + \
           "  %3s"%("QP") + \
           "  %10s"%("Bitrate") + \
           "  %5s"%("PSNR_Y") + \
           "  %5s"%("PSNR_U") + \
           "  %6s"%("PSNR_V") + \
           "  %6s"%("SSIM_Y") + \
           "  %6s"%("SSIM_U") + \
           "  %6s"%("SSIM_V") + \
           "  %6s"%("EncT")

    if False: #len(extract_info_array[0]) > idx_cu8_ana_ratio:
      title = title + \
              "  %10s"%("CU64_ratio") + \
              "  %10s"%("CU32_ratio") + \
              "  %10s"%("CU16_ratio") + \
              "  %9s"%("CU8_ratio")
    if False: #len(extract_info_array[0]) > idx_pu4_ana_ratio:
      title = title + \
              "  %9s"%("PU4_ratio")
    outf.write(title + '\n')
    for preset in self.presets:
      for file in self.source_files:
        prefix = "%-34s"%(file+"_P%d"%preset)
        for infos in extract_info_array:
          if file != infos[idx_file] or preset != infos[idx_preset]:
            continue
          out_str = prefix + \
                     "  %3d"%infos[idx_qp] + \
                     "  %10.2f"%infos[idx_bitrate] + \
                     "  %5.3f"%infos[idx_psnr_y] + \
                     "  %5.3f"%infos[idx_psnr_u] + \
                     "  %6.3f"%infos[idx_psnr_v] + \
                     "  %6.3f"%infos[idx_ssim_y] + \
                     "  %6.3f"%infos[idx_ssim_u] + \
                     "  %6.3f"%infos[idx_ssim_v] + \
                     "  %6.2f"%infos[idx_enctime]
          if False: #len(extract_info_array[0]) > idx_cu8_ana_ratio:
            out_str = out_str + \
                      "  %10s"%(infos[idx_cu64_ana_ratio]) + \
                      "  %10s"%(infos[idx_cu32_ana_ratio]) + \
                      "  %10s"%(infos[idx_cu16_ana_ratio]) + \
                      "  %9s"%(infos[idx_cu8_ana_ratio])
          if False: #len(extract_info_array[0]) > idx_pu4_ana_ratio:
            out_str = out_str + \
                      "  %9s"%(infos[idx_pu4_ana_ratio])
          outf.write(out_str + '\n')
          prefix = "%-34s"%(34*" ")
          cnt = cnt + 1
    outf.close()

if __name__ == "__main__":
  #source_dir  = r"F:\lr\_HD-User_D_TEMP\_Video_data_temp\_Regression_Temp_151113_P3_635211_rev32931_org"
  #output_file = r"E:\lr\_collect_result.txt"
  if len(sys.argv) < 3:
      print "Parameter Error!"
      print "Usage:"
      print "  python  265_result_collector.py  source_dir  output_file"
      exit(0)

  source_dir  = sys.argv[1]
  output_file = sys.argv[2]
  r = ResultCollector(source_dir, output_file)
  r.runCollect()