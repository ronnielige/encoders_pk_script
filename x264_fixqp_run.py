
import os
import sys
sys.path.append("_CommonTools")
sys.path.append("_Process")
from input_yuv_config import *
from config import *
from TaskManager import *
from analyse_x264_log import *
from Tools import *
TM = TaskManager(worker_number)

x264_fullpath = bin_path + x264_exe
if not os.path.exists(x264_fullpath):
    print "Error, x264 exe not exist."
    exit(1)

final_result_file = out_path + "_x264_fixqp_" + getDateTime() + ".log"
ClearFile(final_result_file)
AppendLine(final_result_file, "       target bitrate     bitrate(kbps)   Y      U      V       enc_fps") # title

# get total task number
total_task_num = 0
cur_task_num   = 0
for p in x264_presets:
    for yuv in test_yuvs:
        for qp in fix_quant_qps:
            total_task_num = total_task_num + 1

# ******** Fix Quant *******
for p in x264_presets:
    AppendLine(final_result_file, "\nPreset " + p)
    for yuv in test_yuvs:
        AppendLine(final_result_file, "    %s"%yuv)
        for qp in fix_quant_qps:
            width  = yuv_resolution[yuv][0]
            height = yuv_resolution[yuv][1]
            fps    = yuv_fps[yuv]
            out_log = "%sx264_%s_%s_fixqp%d.log"%(out_path, yuv, p, qp)
            bitstream =  "%sx264_%s_%s_fixqp%d.bin"%(out_path, yuv, p, qp)
            cmd    = x264_fullpath + \
                     " --preset %s"%p + \
                     " --tune psnr" + \
                     " --keyint %d"%key_int + \
                     " --bframes %d"%bframes + \
                     " --b-pyramid normal" + \
                     " --ref %d"%ref + \
                     " --qp %d"%qp + \
                     " --ipratio 1.0" + \
                     " --pbratio 1.0" + \
                     " --output %s"%bitstream + \
                     " --input-fmt i420" + \
                     " --input-depth 8" + \
                     " --input-res %dx%d"%(width, height) + \
                     " --fps %d"%fps + \
                     " --frames %d"%enc_frames + \
                     " --verbose" + \
                     " --log-level info" + \
                     " --psnr" + \
                     " --threads 1" + \
                     " %s"%yuv_fullpath[yuv]
            del_bitstream_cmd = "python _CommonTools\\rm_file.py %s"%bitstream

            cur_task_num = cur_task_num + 1
            print "process %4d / %4d"%(cur_task_num, total_task_num)

            if b_del_bitstream == True:
                cmdlist = (cmd, del_bitstream_cmd, )
            else:
                cmdlist = (cmd, )
            if b_cover_result or not is_log_intact(out_log):
                TM.newTaskList(cmdlist, (out_log, ))
        TM.clearAllTaskList() # wait until all task finished

            # collect result for this yuv
        for qp in fix_quant_qps:
            out_log = "%sx264_%s_%s_fixqp%d.log"%(out_path, yuv, p, qp)
            ana_result = x264_analyse(out_log)
            AppendLine(final_result_file, "        %7s           %9.2f     %5.2f  %5.2f  %5.2f     %6.2f"%(qp, ana_result[3], ana_result[0], ana_result[1], ana_result[2], ana_result[4]))