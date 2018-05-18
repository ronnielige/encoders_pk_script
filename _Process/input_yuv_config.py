hd_yuv_path    = "D://HEVC_YUV_SEQ//"
fourk_yuv_path = "D://HEVC_YUV_SEQ//4K_yuv//"

hd_test_yuvs = ["Bbasketballdrive",
                "Bbqterrace",
                "Bcactus",
                "Bkimono",
                "Bparkscene",]
fourk_test_yuvs = ["4K_football",
                   "4K_tianfu",
                   "4K_wudao",
                   ]
test_yuvs = hd_test_yuvs + fourk_test_yuvs

yuv_fullpath = {
    "Bbasketballdrive": hd_yuv_path + "Bbasketballdrive_1920x1080_8_50_500.yuv",
    "Bbqterrace":        hd_yuv_path + "Bbqterrace_1920x1080_8_60_600.yuv",
    "Bcactus":           hd_yuv_path + "Bcactus_1920x1080_8_50_500.yuv",
    "Bkimono":           hd_yuv_path + "Bkimono_1920x1080_8_24_240.yuv",
    "Bparkscene":        hd_yuv_path + "Bparkscene_1920x1080_8_24_240.yuv",
    "4K_football":       fourk_yuv_path + "4K_football_50fps_500.yuv",
    "4K_tianfu":         fourk_yuv_path + "4K_tianfu_50fps.yuv",
    "4K_wudao":          fourk_yuv_path + "4K_wudao_50fps_crop_500.yuv",
    }
yuv_resolution = {
    "Bbasketballdrive":   [1920, 1080],
    "Bbqterrace":         [1920, 1080],
    "Bcactus":            [1920, 1080],
    "Bkimono":            [1920, 1080],
    "Bparkscene":         [1920, 1080],
    "4K_football":        [3840, 2160],
    "4K_tianfu":          [3840, 2160],
    "4K_wudao":           [3840, 2160],
}
yuv_fps = {
    "Bbasketballdrive":  50,
    "Bbqterrace":         60,
    "Bcactus":            50,
    "Bkimono":            24,
    "Bparkscene":         24,
    "4K_football":        50,
    "4K_tianfu":          50,
    "4K_wudao":           50,
}