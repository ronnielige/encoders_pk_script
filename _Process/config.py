# path settings
bin_path = "bin\\"
out_path = "output\\"

# exe names
x264_exe  = "x264.exe"
x265_exe  = "x265_v2.8.exe"
as265_exe = "cli_ashevc.exe"
qy265_exe = "AppEncoder_x64.exe"
hm265_exe = "TAppEncoder.exe"

fix_quant_qps  = [22, 27, 32, 37, 42]
#hd_bitrates    = [5000, 4000, 3000, 2000, 1000]
hd_bitrates    = [6000, 4000, 2000, 1000]
fourk_bitrates = [14000, 12000, 10000, 8000, 6000]

#x264_presets  = ["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow","placebo"]
#x265_presets  = ["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow","placebo"]
x264_presets  = ["medium", ]
x265_presets  = ["medium", ]
as265_presets = [4]
#qy265_presets = [ "ultrafast", "superfast", "veryfast", "fast", "medium", "slow", "veryslow", "placebo"]
qy265_presets = [ "fast", ]

worker_number   = 1     # set how many workers to run
b_cover_result  = True # if result of case already exists, should rerun this case
b_del_bitstream = False # whether delete bitstream

# encoder key parameters
enc_frames = 1000
bframes    = 3
ref        = 1
key_int    = 50