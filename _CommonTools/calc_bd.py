import re
import subprocess
import sys
import time

from Tools import *
from bjm   import *

yuvfile_ends_column = 34
idx_qp     = 0
idx_rate   = 1
idx_psnr_y = 2
idx_psnr_u = 3
idx_psnr_v = 4
idx_ssim_y = 5
idx_ssim_u = 6
idx_ssim_v = 7
idx_enc_t  = 8

def calc_bd(rd_result_file_ref, rd_result_file, output_bd_file):
    '''
    Args:
        rd_result_file_ref: file containing reference rd result
        rd_result_file:     file containing new rd result
        output_bd_file:     output file containing bd-result
    Returns:
        return an array [BD-Rate-Y, BD-Rate-U, BD-Rate-V, Delta_Time]
        BD-Rate-Y: average bd-rate of Y component
        BD-Rate-U: average bd-rate of U component
        BD-Rate-V: average bd-rate of V component
        Delta_Time: average delta_time
    '''
    try:
        rd_ref_f = open(rd_result_file_ref, 'r')
        rd_f     = open(rd_result_file,     'r')
        output_bd_f = open(output_bd_file, 'w')
    except Exception, e:
        #print "Can't open rd_result file or output_bd_file!"
        print e
        return None

    r_rate_a   = []
    rate_a     = []
    r_psnr_y_a = []
    psnr_y_a   = []
    r_psnr_u_a = []
    psnr_u_a   = []
    r_psnr_v_a = []
    psnr_v_a   = []
    r_enc_t_a  = []
    enc_t_a    = []
    cnt = 0
    sum_bdr_y = sum_bdr_u = sum_bdr_v = sum_bdpsnr_y = sum_delta_t = 0.0
    sum_enc_t = sum_r_enc_t = 0.0

    ref_line = rd_ref_f.readline()
    line     = rd_f.readline()
    while ref_line and line:
        try:
            int(line.split()[0])
        except: # A new sequence starts
            sum_enc_t   = 0.0
            sum_r_enc_t = 0.0
            while len(rate_a) != 0: # empty array
                r_rate_a.pop(0)
                rate_a.pop(0)
                r_psnr_y_a.pop(0)
                psnr_y_a.pop(0)
                r_psnr_u_a.pop(0)
                psnr_u_a.pop(0)
                r_psnr_v_a.pop(0)
                psnr_v_a.pop(0)
                r_enc_t_a.pop(0)
                enc_t_a.pop(0)

        r_l_a = ref_line[yuvfile_ends_column: ].split()
        l_a   = line[yuvfile_ends_column: ].split()
        output_line = ref_line[:-1] + 2 * " " + "|" + line[yuvfile_ends_column: -1]
        try:
            r_rate_a.append(float(r_l_a[idx_rate]))
            rate_a.append(float(l_a[idx_rate]))
        except:
            ref_rd_filename = os.path.basename(rd_result_file_ref)
            rd_filename = os.path.basename(rd_result_file)
            title_line = 30 * " " +  "%-82s"%ref_rd_filename + "|" + 30 * " " +  "%-82s"%rd_filename + "\n"
            output_bd_f.write(title_line)
            output_bd_f.write(output_line + "   BDR_Y   BDR_U   BDR_V  BDPSNR_Y  delta_time" + '\n')
            ref_line = rd_ref_f.readline()
            line     = rd_f.readline()
            continue
        r_psnr_y_a.append(float(r_l_a[idx_psnr_y]))
        psnr_y_a.append(float(l_a[idx_psnr_y]))
        r_psnr_u_a.append(float(r_l_a[idx_psnr_u]))
        psnr_u_a.append(float(l_a[idx_psnr_u]))
        r_psnr_v_a.append(float(r_l_a[idx_psnr_v]))
        psnr_v_a.append(float(l_a[idx_psnr_v]))
        r_enc_t_a.append(float(r_l_a[idx_enc_t]))
        enc_t_a.append(float(l_a[idx_enc_t]))

        sum_enc_t   = sum_enc_t   + enc_t_a[-1]
        sum_r_enc_t = sum_r_enc_t + r_enc_t_a[-1]

        if len(r_psnr_y_a) == 4:
            cnt = cnt + 1
            #print  r"bdrate = %5.2f%%  %5.2f%%  %5.2f%%  %6.3fdB\n" %(100*bdrate(r_rate_a, r_psnr_y_a, rate_a, psnr_y_a), 100*bdrate(r_rate_a, r_psnr_u_a, rate_a, psnr_u_a), 100*bdrate(r_rate_a, r_psnr_v_a, rate_a, psnr_v_a), bjm(r_rate_a, r_psnr_y_a, rate_a, psnr_y_a, BD_PSNR))
            bdr_y = 100 * bdrate(r_rate_a, r_psnr_y_a, rate_a, psnr_y_a)
            bdr_u = 100 * bdrate(r_rate_a, r_psnr_u_a, rate_a, psnr_u_a)
            bdr_v = 100 * bdrate(r_rate_a, r_psnr_v_a, rate_a, psnr_v_a)
            bdpsnr_y  = bjm(r_rate_a, r_psnr_y_a, rate_a, psnr_y_a, BD_PSNR)
            sum_bdr_y    = sum_bdr_y + bdr_y
            sum_bdr_u    = sum_bdr_u + bdr_u
            sum_bdr_v    = sum_bdr_v + bdr_v
            sum_bdpsnr_y = sum_bdpsnr_y + bdpsnr_y
            delta_time   = 100.0 * (sum_r_enc_t - sum_enc_t) / sum_r_enc_t
            sum_delta_t  = sum_delta_t + delta_time
            output_line  = output_line + "  %5.2f%%  %5.2f%%  %5.2f%%  %6.3fdB  %5.2f%%"%(bdr_y, bdr_u, bdr_v, bdpsnr_y, delta_time)
            for i in range(0, 2): # remove the first two elements
                r_rate_a.pop(0)
                rate_a.pop(0)
                r_psnr_y_a.pop(0)
                psnr_y_a.pop(0)
                r_psnr_u_a.pop(0)
                psnr_u_a.pop(0)
                r_psnr_v_a.pop(0)
                psnr_v_a.pop(0)
                sum_r_enc_t = sum_r_enc_t - r_enc_t_a.pop(0)
                sum_enc_t   = sum_enc_t   - enc_t_a.pop(0)

        output_bd_f.write(output_line + '\n')
        ref_line = rd_ref_f.readline()
        line     = rd_f.readline()

    output_bd_f.write("Avg_bd_rate_y  = %5.2f%%\n"%(sum_bdr_y / cnt))
    output_bd_f.write("Avg_bd_rate_u  = %5.2f%%\n"%(sum_bdr_u / cnt))
    output_bd_f.write("Avg_bd_rate_v  = %5.2f%%\n"%(sum_bdr_v / cnt))
    output_bd_f.write("Avg_bd_psnr_y  = %5.2f%%\n"%(sum_bdpsnr_y / cnt))
    output_bd_f.write("Avg_delta_time = %5.2f%%\n"%(sum_delta_t / cnt))
    rd_ref_f.close()
    rd_f.close()
    output_bd_f.close()

if __name__ == "__main__":
    #calc_bd(r"E:\lr\151113_P3_rev32237_org.log", r"E:\lr\151113_P3_rev32237_skipInterPu_allCU_vc.log", r"E:\test.log")
    if len(sys.argv) < 4:
        print "Parameter Error!"
        print "Usage:"
        print "  python  calc_bd.py  ref_rd_file  rd_file  output_file"
        exit(0)

    ref_rd_file = sys.argv[1]
    rd_file     = sys.argv[2]
    output_file = sys.argv[3]
    calc_bd(ref_rd_file, rd_file, output_file)