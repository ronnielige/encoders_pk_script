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
        pinfo_fullfilename = logfile_path + r"\\" + "_pinfo_x265-3-"

        seqinfo = seqinfo_pattern.findall(logfile_name)[0][0:-4]
        rcinfo  = rcinfo_pattern.findall(logfile_name)[0][0:-4]
        pinfo_fullfilename = pinfo_fullfilename + seqinfo + ".yuv" + "-" + rcinfo + "-"

        r = open(logfile_fullname, 'r')
        i_frms = p_frms = b_frms = 0
        i_avg_psnr_y = i_avg_psnr_u = i_avg_psnr_v = 0
        p_avg_psnr_y = p_avg_psnr_u = p_avg_psnr_v = 0
        b_avg_psnr_y = b_avg_psnr_u = b_avg_psnr_v = 0
        psnr_y = psnr_u = psnr_v = total_frames = avg_bitrate = total_time = enc_fps = 0

        line = r.readline()
        while line:
            if line.find("frame I:") >= 0:
                i_frms = (int)(line.split()[4][0:-1])
                i_avg_psnr_y = (float)(line.split()[11][2:])
                i_avg_psnr_u = (float)(line.split()[12][2:])
                i_avg_psnr_v = (float)(line.split()[13][2:])
            elif line.find("frame P:") >= 0:
                p_frms = (int)(line.split()[4][0:-1])
                p_avg_psnr_y = (float)(line.split()[11][2:])
                p_avg_psnr_u = (float)(line.split()[12][2:])
                p_avg_psnr_v = (float)(line.split()[13][2:])
            elif line.find("frame B:") >= 0:
                b_frms = (int)(line.split()[4][0:-1])
                b_avg_psnr_y = (float)(line.split()[11][2:])
                b_avg_psnr_u = (float)(line.split()[12][2:])
                b_avg_psnr_v = (float)(line.split()[13][2:])
            if line.find("Global PSNR") >= 0:
                total_frames = (int)(line.split()[1])
                total_time = (float)(line.split()[4][0:-1])
                avg_bitrate = (float)(line.split()[7])
                enc_fps = total_frames / total_time
            line = r.readline()
        r.close()

        #print "frame I: %3d %5.3f %5.3f %5.3f"%(i_frms, i_avg_psnr_y, i_avg_psnr_u, i_avg_psnr_v)
        #print "frame P: %3d %5.3f %5.3f %5.3f"%(p_frms, p_avg_psnr_y, p_avg_psnr_u, p_avg_psnr_v)
        #print "frame B: %3d %5.3f %5.3f %5.3f"%(b_frms, b_avg_psnr_y, b_avg_psnr_u, b_avg_psnr_v)
        psnr_y  = (i_avg_psnr_y * i_frms + p_avg_psnr_y * p_frms + b_avg_psnr_y * b_frms) / (i_frms + p_frms + b_frms)
        psnr_u  = (i_avg_psnr_u * i_frms + p_avg_psnr_u * p_frms + b_avg_psnr_u * b_frms) / (i_frms + p_frms + b_frms)
        psnr_v  = (i_avg_psnr_v * i_frms + p_avg_psnr_v * p_frms + b_avg_psnr_v * b_frms) / (i_frms + p_frms + b_frms)

        pinfo_fullfilename = pinfo_fullfilename \
                             + "psnr%.2f_%.2f_%.2f" %(psnr_y, psnr_u, psnr_v) \
                             + "-ssim0.0_0.0_0.0-kbps%.2f" %avg_bitrate \
                             + "-s%.2f.pinfo" %total_time

        f = open(pinfo_fullfilename, 'w')
        f.close()