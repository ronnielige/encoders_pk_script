__author__ = 'lr9371'
import sys
import os
import re

if __name__ == "__main__":
  seqinfo_pattern = re.compile(".*_GOP")
  rcinfo_pattern  = re.compile("RC.*_P\d")
  qy_fps_pattern     = re.compile("FPS: \d+\.\d+")
  qy_time_pattern    = re.compile("test time: \d+")
  qy_quality_pattern = re.compile("bitrate, psnr: \d+\.\d+\s\d+\.\d+\s\d+\.\d+\s\d+\.\d+")
  idx_fps = 1
  idx_time = 2
  idx_bitrate = 2
  idx_psnr_y = 3
  idx_psnr_u = 4
  idx_psnr_v = 5

  if(len(sys.argv) == 2):
    logfile_fullname = sys.argv[1]
    logfile_path = os.path.split(logfile_fullname)[0]
    logfile_name = os.path.split(logfile_fullname)[1]
    pinfo_fullfilename = logfile_path + r"\\" + "_pinfo_qy265-3-"

    seqinfo = seqinfo_pattern.findall(logfile_name)[0][0:-4]
    rcinfo  = rcinfo_pattern.findall(logfile_name)[0]
    pinfo_fullfilename = pinfo_fullfilename + seqinfo + ".yuv" + "-" + rcinfo + "-"

    r = open(logfile_fullname, 'r')
    psnr_y = psnr_u = psnr_v = bitrate = fps = time = 0

    line = r.readline()
    while line:
      fps_info = qy_fps_pattern.findall(line)
      qua_info = qy_quality_pattern.findall(line)
      tim_info = qy_time_pattern.findall(line)
      if len(fps_info) != 0:
        fps = (float)(fps_info[0].split()[idx_fps])
      if len(qua_info) != 0:
        bitrate = (float)(qua_info[0].split()[idx_bitrate])
        psnr_y  = (float)(qua_info[0].split()[idx_psnr_y])
        psnr_u  = (float)(qua_info[0].split()[idx_psnr_u])
        psnr_v  = (float)(qua_info[0].split()[idx_psnr_v])
      if len(tim_info) != 0:
        time = (float)(tim_info[0].split()[idx_time]) / 1000
      line = r.readline()
    r.close()

    pinfo_fullfilename = pinfo_fullfilename \
                         + "psnr%.2f_%.2f_%.2f" %(psnr_y, psnr_u, psnr_v) \
                         + "-ssim0.0_0.0_0.0-kbps%.2f" %bitrate \
                         + "-s%.2f.pinfo" %time

    f = open(pinfo_fullfilename, 'w')
    f.close()

