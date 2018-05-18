import sys
import os
import re

idx_total_frm = 0
idx_bitrate = 2
idx_psnr_y = 3
idx_psnr_u = 4
idx_psnr_v = 5

def hm265_analyse(input_log):
    r = open(input_log, 'r')
    line = r.readline()
    psnr_y = psnr_u = psnr_v = 0
    bitrate = 0
    enc_fps = 0
    hm_total_frames = 0
    hm_time_pattern = re.compile("\d+\.\d+")
    while line:
        if line.find("SUMMARY") >= 0:
            line = r.readline()
            line = r.readline()
            hm_total_frames = (int)(line.split()[idx_total_frm])
            bitrate = (float)(line.split()[idx_bitrate])
            psnr_y  = (float)(line.split()[idx_psnr_y])
            psnr_u  = (float)(line.split()[idx_psnr_u])
            psnr_v  = (float)(line.split()[idx_psnr_v])
        if line.find("Total Time") >= 0:
            hm_total_time = (float)(hm_time_pattern.findall(line)[0])
            enc_fps = hm_total_frames / hm_total_time
        line = r.readline()
    r.close()

    return [psnr_y, psnr_u, psnr_v, bitrate, enc_fps]

def is_log_intact(input_log):
    if not os.path.exists(input_log):
        return False

    match_line = 0
    r = open(input_log, 'r')
    line = r.readline()
    while line:
        if line.find("SUMMARY") >= 0:
            match_line = match_line + 1
        if line.find("Total Time") >= 0:
            match_line = match_line + 1
        line = r.readline()
    r.close()
    return match_line == 2


if __name__ == "__main__":
    if(len(sys.argv) == 4):
        prefix    = sys.argv[1]
        input_log = sys.argv[2]
        final_log = sys.argv[3]
        ana_result = hm265_analyse(input_log)
        f = open(final_log, 'a')
        f.write("%20s    %5.2f  %5.2f  %5.2f  %7.2f   %6.2f\n"%(prefix, ana_result[0], ana_result[1], ana_result[2], ana_result[3], ana_result[4]))
        f.close()
    elif(len(sys.argv) == 2):
        ana_result = hm265_analyse(sys.argv[1])
        print ana_result
