import sys
import os

def qy265_analyse(input_log):
    r = open(input_log, 'r')
    line = r.readline()
    psnr_y = psnr_u = psnr_v = 0
    bitrate = 0
    enc_fps = 0

    while line:
        if line.find("bitrate, psnr:") >= 0:
            psnr_y = float(line.split()[3])
            psnr_u = float(line.split()[4])
            psnr_v = float(line.split()[5])
            bitrate = float(line.split()[2])
        if line.find("test time") >= 0:
            enc_fps = float(line.split()[7])
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
        if line.find("bitrate, psnr:") >= 0:
            match_line = match_line + 1
        if line.find("test time") >= 0:
            match_line = match_line + 1
        line = r.readline()
    r.close()
    return match_line == 2

if __name__ == "__main__":
    if(len(sys.argv) == 4):
        prefix    = sys.argv[1]
        input_log = sys.argv[2]
        final_log = sys.argv[3]
        ana_result = qy265_analyse(input_log)
        f = open(final_log, 'a')
        f.write("%20s    %5.2f  %5.2f  %5.2f  %7.2f   %6.2f\n"%(prefix, ana_result[0], ana_result[1], ana_result[2], ana_result[3], ana_result[4]))
        f.close()
    elif(len(sys.argv) == 2):
        ana_result = qy265_analyse(sys.argv[1])
        print ana_result
