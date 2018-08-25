
import os
import sys
sys.path.append("_CommonTools")
sys.path.append("_Process")
from input_yuv_config import *
from config import *
from TaskManager import *
from analyse_hm265_log import *
from Tools import *
TM = TaskManager(worker_number)

hm265_fullpath = bin_path + hm265_exe
if not os.path.exists(hm265_fullpath):
    print "Error, hm265 exe not exist."
    exit(1)
hm_cfg_file = bin_path + "hm16_15cfg\\encoder_randomaccess_main_GOP48_FixQ_IBBBP_ref2.cfg"

final_result_file = out_path + "_hm265_fixqp_" + getDateTime() + ".log"
ClearFile(final_result_file)
AppendLine(final_result_file, "       target bitrate     bitrate(kbps)   Y      U      V       enc_fps") # title

# get total task number
total_task_num = 0
cur_task_num   = 0
for yuv in test_yuvs:
    for qp in fix_quant_qps:
        total_task_num = total_task_num + 1

# ******** Fix Quant *******
for yuv in test_yuvs:
    AppendLine(final_result_file, "    %s"%yuv)
    for qp in fix_quant_qps:
        width  = yuv_resolution[yuv][0]
        height = yuv_resolution[yuv][1]
        fps    = yuv_fps[yuv]
        out_log = "%shm265_%s_qp%d.log"%(out_path, yuv, qp)
        bitstream =  "%shm265_%s_qp%d.bin"%(out_path, yuv, qp)
        rec_yuv = "%shm265_%s_qp%d_rec.yuv"%(out_path, yuv, qp)
        cmd    = hm265_fullpath + \
                 " -c %s"%hm_cfg_file + \
                 " -q %d"%qp + \
                 " -b %s"%bitstream + \
                 " -o %s"%rec_yuv + \
                 " -wdt %d"%width + \
                 " -hgt %d"%height + \
                 " -fr %d"%fps + \
                 " -f %d"%enc_frames + \
                 " -i %s"%yuv_fullpath[yuv]
        del_bitstream_cmd = "python _CommonTools\\rm_file.py %s"%bitstream
        del_recyuv_cmd    = "python _CommonTools\\rm_file.py %s"%rec_yuv
        cur_task_num = cur_task_num + 1
        print "process %4d / %4d"%(cur_task_num, total_task_num)

        if b_del_bitstream == True:
            cmdlist = (cmd, del_bitstream_cmd, del_recyuv_cmd)
        else:
            cmdlist = (cmd, del_recyuv_cmd)

        if b_cover_result or not is_log_intact(out_log):
            TM.newTaskList(cmdlist, (out_log, ))
    TM.clearAllTaskList() # wait until all task finished

    # collect result for this yuv
    for qp in fix_quant_qps:
        out_log = "%shm265_%s_qp%d.log"%(out_path, yuv, qp)
        ana_result = hm265_analyse(out_log)
        AppendLine(final_result_file, "        %7s           %9.2f     %5.2f  %5.2f  %5.2f     %6.2f"%(qp, ana_result[3], ana_result[0], ana_result[1], ana_result[2], ana_result[4]))