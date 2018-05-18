import sys
import os

def x264_analyse(input_log):
    r = open(input_log, 'r')
    line = r.readline()
    psnr_y = psnr_u = psnr_v = 0
    bitrate = 0
    enc_fps = 0

    while line:
        # x264 [info]: PSNR Mean Y:23.755 U:33.865 V:33.164 Avg:25.290 Global:25.218 kb/s:1022.15
        if line.find("x264 [info]: PSNR Mean Y") >= 0:
            sp = line.split(":")
            #print sp
            psnr_y = float(sp[2][0:-2])
            psnr_u = float(sp[3][0:-2])
            psnr_v = float(sp[4][0:-4])
            bitrate = float(sp[7][0:-1])
            #print psnr_y, psnr_u, psnr_v, bitrate
        # encoded 500 frames, 66.42 fps, 1022.15 kb/s
        if line.find("encoded") >= 0:
            enc_fps = float(line.split(',')[1][0:-4])
            #print enc_fps
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
        if line.find("x264 [info]: PSNR Mean Y") >= 0:
            match_line = match_line + 1
        if line.find("encoded") >= 0 >= 0:
            match_line = match_line + 1
        line = r.readline()
    r.close()
    return match_line == 2

if __name__ == "__main__":
    if(len(sys.argv) == 4):
        prefix    = sys.argv[1]
        input_log = sys.argv[2]
        final_log = sys.argv[3]
        ana_result = x264_analyse(input_log)
        f = open(final_log, 'a')
        f.write("%20s    %5.2f  %5.2f  %5.2f  %7.2f   %6.2f\n"%(prefix, ana_result[0], ana_result[1], ana_result[2], ana_result[3], ana_result[4]))
        f.close()
