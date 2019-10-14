hd_yuv_path    = "\\\\172.28.10.101\\ForAVT\\lr\\yuv_collect\\"
fourk_yuv_path = "F://HEVC_YUV_SEQ//4K_yuv//"

# Movie(M), TV(T), variety(V), gymnastics(G), sing(S), games(G)
hd_test_yuvs = ["G_footballdejia",
                "G_footballxijia",
                "T_jphn",
                "T_maque",
                "T_misha",
                "V_american",
                "V_hnwskn",
                "V_wsgs1",
                "V_wsgs2",
                "V_zghsy"]
fourk_test_yuvs = ["4K_football",
                   "4K_tianfu",
                   "4K_wudao",
                   ]
test_yuvs = hd_test_yuvs + fourk_test_yuvs
test_yuvs = hd_test_yuvs

yuv_fullpath = {
    "Bbasketballdrive":  hd_yuv_path + "Bbasketballdrive_1920x1080_8_50_500.yuv",
    "Bbqterrace":        hd_yuv_path + "Bbqterrace_1920x1080_8_60_600.yuv",
    "Bcactus":           hd_yuv_path + "Bcactus_1920x1080_8_50_500.yuv",
    "Bkimono":           hd_yuv_path + "Bkimono_1920x1080_8_24_240.yuv",
    "Bparkscene":        hd_yuv_path + "Bparkscene_1920x1080_8_24_240.yuv",
    "4K_football":       fourk_yuv_path + "4K_football_50fps_500.yuv",
    "4K_tianfu":         fourk_yuv_path + "4K_tianfu_50fps.yuv",
    "4K_wudao":          fourk_yuv_path + "4K_wudao_50fps_crop_500.yuv",
    "G_footballdejia":   hd_yuv_path + "G_footballdejia_hd_25fps.yuv",
    "G_footballxijia":   hd_yuv_path + "G_footballxijia_hd_25fps.yuv",
    "T_jphn":            hd_yuv_path + "T_jphn_hd_25fps.yuv",
    "T_maque":           hd_yuv_path + "T_maque_hd_25fps.yuv",
    "T_misha":           hd_yuv_path + "T_misha_hd_25fps.yuv",
    "V_american":        hd_yuv_path + "V_american_hd_30fps.yuv",
    "V_hnwskn":          hd_yuv_path + "V_hnwskn_hd_25fps.yuv",
    "V_wsgs1":           hd_yuv_path + "V_wsgs1_hd_25fps.yuv",
    "V_wsgs2":           hd_yuv_path + "V_wsgs2_hd_25fps.yuv",
    "V_zghsy":           hd_yuv_path + "V_zghsy_hd_25fps.yuv",
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
    "G_footballdejia":    [1920, 1080],
    "G_footballxijia":    [1920, 1080],
    "T_jphn":             [1920, 1080],
    "T_maque":            [1920, 1080],
    "T_misha":            [1920, 1080],
    "V_american":         [1920, 1080],
    "V_hnwskn":           [1920, 1080],
    "V_wsgs1":            [1920, 1080],
    "V_wsgs2":            [1920, 1080],
    "V_zghsy":            [1920, 1080],
}
yuv_fps = {
    "Bbasketballdrive":   50,
    "Bbqterrace":         60,
    "Bcactus":            50,
    "Bkimono":            24,
    "Bparkscene":         24,
    "4K_football":        50,
    "4K_tianfu":          50,
    "4K_wudao":           50,
    "G_footballdejia":    25,   
    "G_footballxijia":    25,
    "T_jphn":             25,
    "T_maque":            25,
    "T_misha":            25,
    "V_american":         30,
    "V_hnwskn":           25,
    "V_wsgs1":            25,
    "V_wsgs2":            25,
    "V_zghsy":            25
}