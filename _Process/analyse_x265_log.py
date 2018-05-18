import sys
import os

def x265_analyse(input_log):
    r = open(input_log, 'r')
    line = r.readline()
    psnr_y = psnr_u = psnr_v = 0
    bitrate = 0
    enc_fps = 0

    i_frms = p_frms = b_frms = 0
    i_avg_psnr_y = i_avg_psnr_u = i_avg_psnr_v = 0
    p_avg_psnr_y = p_avg_psnr_u = p_avg_psnr_v = 0
    b_avg_psnr_y = b_avg_psnr_u = b_avg_psnr_v = 0

    while line:
        if line.find("frame I:") >= 0:
            start = line.find("x265 [info]: frame I:")
            i_frms = (int)(line[start:].split()[4][0:-1])
            i_avg_psnr_y = (float)(line[start:].split()[11][2:])
            i_avg_psnr_u = (float)(line[start:].split()[12][2:])
            i_avg_psnr_v = (float)(line[start:].split()[13][2:])
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
            bitrate = (float)(line.split()[7])
            enc_fps = total_frames / total_time
        line = r.readline()
    r.close()
    psnr_y  = (i_avg_psnr_y * i_frms + p_avg_psnr_y * p_frms + b_avg_psnr_y * b_frms) / (i_frms + p_frms + b_frms)
    psnr_u  = (i_avg_psnr_u * i_frms + p_avg_psnr_u * p_frms + b_avg_psnr_u * b_frms) / (i_frms + p_frms + b_frms)
    psnr_v  = (i_avg_psnr_v * i_frms + p_avg_psnr_v * p_frms + b_avg_psnr_v * b_frms) / (i_frms + p_frms + b_frms)
    return [psnr_y, psnr_u, psnr_v, bitrate, enc_fps]

def is_log_intact(input_log):
    if not os.path.exists(input_log):
        return False

    match_line = 0
    r = open(input_log, 'r')
    line = r.readline()
    while line:
        if line.find("frame I:") >= 0:
            match_line = match_line + 1
        elif line.find("frame P:") >= 0:
            match_line = match_line + 1
        elif line.find("frame B:") >= 0:
            match_line = match_line + 1
        if line.find("Global PSNR") >= 0:
            match_line = match_line + 1
        line = r.readline()
    r.close()
    return match_line == 4

if __name__ == "__main__":
    if(len(sys.argv) == 4):
        prefix    = sys.argv[1]
        input_log = sys.argv[2]
        final_log = sys.argv[3]
        ana_result = x265_analyse(input_log)
        f = open(final_log, 'a')
        f.write("%20s    %5.2f  %5.2f  %5.2f  %7.2f   %6.2f\n"%(prefix, ana_result[0], ana_result[1], ana_result[2], ana_result[3], ana_result[4]))
        f.close()
