import os
import sys
sys.path.append("_CommonTools")
sys.path.append("_Process")
from input_yuv_config import *
from config import *
from TaskManager import *
from analyse_as265_log import *
from Tools import *
TM = TaskManager(worker_number)

as265_fullpath = bin_path + as265_exe
if not os.path.exists(as265_fullpath):
    print "Error, as265 exe not exist."
    exit(1)

final_result_file = out_path + "_as265_abr_result.log"
ClearFile(final_result_file)
AppendLine(final_result_file, "       target bitrate     bitrate(kbps)   Y      U      V       enc_fps") # title

# get total task number
total_task_num = 0
cur_task_num   = 0
for p in as265_presets:
    for yuv in test_yuvs:
        width  = yuv_resolution[yuv][0]
        height = yuv_resolution[yuv][1]
        bitrate_array = fourk_bitrates
        if width <= 1920 and height <= 1080:
            bitrate_array = hd_bitrates
        for bitrate in bitrate_array:
            total_task_num = total_task_num + 1

# ******** ABR *******
for p in as265_presets:
    AppendLine(final_result_file, "\nPreset %d"%p)
    for yuv in test_yuvs:
        AppendLine(final_result_file, "    %s"%yuv)
        width  = yuv_resolution[yuv][0]
        height = yuv_resolution[yuv][1]
        fps    = yuv_fps[yuv]
        bitrate_array = fourk_bitrates
        if width <= 1920 and height <= 1080:
            bitrate_array = hd_bitrates
        for bitrate in bitrate_array:
            out_log   = "%sas265_%s_%s_abr%d.log"%(out_path, yuv, p, bitrate)
            bitstream = "%sas265_%s_%s_abr%d.bin"%(out_path, yuv, p, bitrate)
            cmd    = as265_fullpath + \
                     " --preset %s"%p + \
                     " --keyint %d"%key_int + \
                     " --bframes %d"%bframes + \
                     " --bpyramid 1" + \
                     " --ref %d"%ref + \
                     " --rc 8" + \
                     " --bitrate %d"%bitrate + \
                     " --rect 0" + \
                     " --amp  0" + \
                     " --dbl  1" + \
                     " --output %s"%bitstream + \
                     " --width %d"%width + \
                     " --height %d"%height + \
                     " --fps %d"%fps + \
                     " --frames %d"%enc_frames + \
                     " --log-level 1" + \
                     " --psnr 1" + \
                     " --frame-threads 1" + \
                     " --wpp-threads 0" + \
                     " --input %s"%yuv_fullpath[yuv]
            del_bitstream_cmd = "python _CommonTools\\rm_file.py %s"%bitstream
            del_pinfo_cmd     = "python _CommonTools\\rm_file.py *info_as265*"

            cur_task_num = cur_task_num + 1
            print "process %4d / %4d"%(cur_task_num, total_task_num)
            if b_cover_result or not is_log_intact(out_log):
                TM.newTaskList((cmd, del_bitstream_cmd, del_pinfo_cmd), (out_log, ))
        TM.clearAllTaskList() # wait until all task finished

        # collect result for this yuv
        for bitrate in bitrate_array:
            out_log = "%sas265_%s_%s_abr%d.log"%(out_path, yuv, p, bitrate)
            ana_result = as265_analyse(out_log)
            AppendLine(final_result_file, "        %7s kbps      %9.2f     %5.2f  %5.2f  %5.2f     %6.2f"%(bitrate, ana_result[3], ana_result[0], ana_result[1], ana_result[2], ana_result[4]))