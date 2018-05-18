__author__ = 'lr9371'
import sys
import os
import re

if __name__ == "__main__":
    seqinfo_pattern = re.compile(".*_GOP")
    rcinfo_pattern  = re.compile("RC.*_MT\d")
    hm_time_pattern    = re.compile("\d+\.\d+")

    idx_total_frm = 0
    idx_bitrate = 2
    idx_psnr_y = 3
    idx_psnr_u = 4
    idx_psnr_v = 5
    hm_total_frames = 0
    hm_avg_bitrate = 0.0
    hm_total_time = 0.0
    hm_enc_fps = 0.0

    if(len(sys.argv) == 2):
        logfile_fullname = sys.argv[1]
        logfile_path = os.path.split(logfile_fullname)[0]
        logfile_name = os.path.split(logfile_fullname)[1]
        pinfo_fullfilename = logfile_path + r"\\" + "_pinfo_hm265-4-"

        seqinfo = seqinfo_pattern.findall(logfile_name)[0][0:-4]
        rcinfo  = rcinfo_pattern.findall(logfile_name)[0][0:-4]
        pinfo_fullfilename = pinfo_fullfilename + seqinfo + ".yuv" + "-" + rcinfo + "-"

        r = open(logfile_fullname, 'r')
        psnr_y = psnr_u = psnr_v = hm_total_frames = hm_avg_bitrate = hm_total_time = hm_enc_fps = 0

        line = r.readline()
        while line:
            if line.find("SUMMARY") >= 0:
                line = r.readline()
                line = r.readline()
                hm_total_frames = (int)(line.split()[idx_total_frm])
                hm_avg_bitrate = (float)(line.split()[idx_bitrate])
                psnr_y  = (float)(line.split()[idx_psnr_y])
                psnr_u  = (float)(line.split()[idx_psnr_u])
                psnr_v  = (float)(line.split()[idx_psnr_v])

            if line.find("Total Time") >= 0:
                hm_total_time = (float)(hm_time_pattern.findall(line)[0])
                hm_enc_fps = hm_total_frames / hm_total_time

            line = r.readline()
        r.close()

        pinfo_fullfilename = pinfo_fullfilename \
                             + "psnr%.2f_%.2f_%.2f" %(psnr_y, psnr_u, psnr_v) \
                             + "-ssim0.0_0.0_0.0-kbps%.2f" %hm_avg_bitrate \
                             + "-s%.2f.pinfo" %hm_total_time

        f = open(pinfo_fullfilename, 'w')
        f.close()

