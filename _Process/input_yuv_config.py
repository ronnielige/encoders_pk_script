hd_yuv_path    = "\\\\172.28.10.101\\ForAVT\\lr\\yuv_collect\\"
fourk_yuv_path = "F://HEVC_YUV_SEQ//4K_yuv//"
jvt_yuv_path   = "F://HEVC_YUV_SEQ//"

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
classA = ["APeopleonstreet", "Atraffic"]
classB = ["Bbasketballdrive", "Bbqterrace", "Bcactus", "Bkimono", "Bparkscene"]
classC = ["Cbasketballdrill", "Cbqmall", "Cracehorses", "Cpartyscene"]
classD = ["Dbasketballpass", "Dblowingbubbles", "Dbqsquare", "Dracehorses"]
classE = ["Efourpeople", "Ejohnny", "Ekristenandsara"]
classF = ["Fbasketballdrilltext", "Fchinaspeed", "Fslideediting", "Fslideshow"]
JVT_testsets = classA + classB + classC + classD + classE + classF

#test_yuvs = hd_test_yuvs + fourk_test_yuvs
#test_yuvs = hd_test_yuvs
test_yuvs = JVT_testsets + hd_test_yuvs

yuv_fullpath = {
    "APeopleonstreet":   jvt_yuv_path + "Apeopleonstreet_2560x1600_8_30_150.yuv",
    "Atraffic":           jvt_yuv_path + "Atraffic_2560x1600_8_30_150.yuv",
    "Bbasketballdrive":  jvt_yuv_path + "Bbasketballdrive_1920x1080_8_50_500.yuv",
    "Bbqterrace":         jvt_yuv_path + "Bbqterrace_1920x1080_8_60_600.yuv",
    "Bcactus":            jvt_yuv_path + "Bcactus_1920x1080_8_50_500.yuv",
    "Bkimono":            jvt_yuv_path + "Bkimono_1920x1080_8_24_240.yuv",
    "Bparkscene":         jvt_yuv_path + "Bparkscene_1920x1080_8_24_240.yuv",
    "Cbasketballdrill":  jvt_yuv_path + "Cbasketballdrill_832x480_8_50_500.yuv",
    "Cbqmall":            jvt_yuv_path + "Cbqmall_832x480_8_60_600.yuv",
    "Cracehorses":        jvt_yuv_path + "Cracehorses_832x480_8_30_300.yuv",
    "Cpartyscene":        jvt_yuv_path + "Cpartyscene_832x480_8_50_500.yuv",
    "Dbasketballpass":   jvt_yuv_path + "Dbasketballpass_416x240_8_50_500.yuv",
    "Dblowingbubbles":   jvt_yuv_path + "Dblowingbubbles_416x240_8_50_500.yuv",
    "Dbqsquare":          jvt_yuv_path + "Dbqsquare_416x240_8_60_600.yuv",
    "Dracehorses":        jvt_yuv_path + "Dracehorses_416x240_8_30_300.yuv",
    "Efourpeople":        jvt_yuv_path + "Efourpeople_1280x720_8_60_600.yuv",
    "Ejohnny":             jvt_yuv_path + "Ejohnny_1280x720_8_60_600.yuv",
    "Ekristenandsara":    jvt_yuv_path + "Ekristenandsara_1280x720_8_60_600.yuv",
    "Fbasketballdrilltext": jvt_yuv_path + "Fbasketballdrilltext_832x480_8_50_500.yuv",
    "Fchinaspeed":          jvt_yuv_path + "Fchinaspeed_1024x768_8_30_500.yuv",
    "Fslideediting":        jvt_yuv_path + "Fslideediting_1280x720_8_30_300.yuv",
    "Fslideshow":           jvt_yuv_path + "Fslideshow_1280x720_8_20_500.yuv",
    "4K_football":        fourk_yuv_path + "4K_football_50fps_500.yuv",
    "4K_tianfu":          fourk_yuv_path + "4K_tianfu_50fps.yuv",
    "4K_wudao":           fourk_yuv_path + "4K_wudao_50fps_crop_500.yuv",
    "G_footballdejia":   hd_yuv_path + "G_footballdejia_hd_25fps.yuv",
    "G_footballxijia":   hd_yuv_path + "G_footballxijia_hd_25fps.yuv",
    "T_jphn":             hd_yuv_path + "T_jphn_hd_25fps.yuv",
    "T_maque":            hd_yuv_path + "T_maque_hd_25fps.yuv",
    "T_misha":            hd_yuv_path + "T_misha_hd_25fps.yuv",
    "V_american":         hd_yuv_path + "V_american_hd_30fps.yuv",
    "V_hnwskn":           hd_yuv_path + "V_hnwskn_hd_25fps.yuv",
    "V_wsgs1":            hd_yuv_path + "V_wsgs1_hd_25fps.yuv",
    "V_wsgs2":            hd_yuv_path + "V_wsgs2_hd_25fps.yuv",
    "V_zghsy":            hd_yuv_path + "V_zghsy_hd_25fps.yuv",
    }
yuv_resolution = {
    "APeopleonstreet":    [2560, 1600],
    "Atraffic":            [2560, 1600],
    "Bbasketballdrive":   [1920, 1080],
    "Bbqterrace":          [1920, 1080],
    "Bcactus":             [1920, 1080],
    "Bkimono":             [1920, 1080],
    "Bparkscene":          [1920, 1080],
    "Cbasketballdrill":   [832,   480],
    "Cbqmall":             [832,   480],
    "Cracehorses":         [832,   480],
    "Cpartyscene":         [832,   480],
    "Dbasketballpass":     [416, 240],
    "Dblowingbubbles":     [416, 240],
    "Dbqsquare":           [416, 240],
    "Dracehorses":         [416, 240],
    "Efourpeople":         [1280, 720],
    "Ejohnny":              [1280, 720],
    "Ekristenandsara":     [1280, 720],
    "Fbasketballdrilltext": [832, 480],
    "Fchinaspeed":          [1024, 768],
    "Fslideediting":       [1280, 720],
    "Fslideshow":          [1280, 720],
    "4K_football":         [3840, 2160],
    "4K_tianfu":           [3840, 2160],
    "4K_wudao":            [3840, 2160],
    "G_footballdejia":    [1920, 1080],
    "G_footballxijia":    [1920, 1080],
    "T_jphn":              [1920, 1080],
    "T_maque":             [1920, 1080],
    "T_misha":             [1920, 1080],
    "V_american":          [1920, 1080],
    "V_hnwskn":            [1920, 1080],
    "V_wsgs1":             [1920, 1080],
    "V_wsgs2":             [1920, 1080],
    "V_zghsy":             [1920, 1080],
}
yuv_fps = {
    "APeopleonstreet":   30,
    "Atraffic":           30,
    "Bbasketballdrive":  50,
    "Bbqterrace":         60,
    "Bcactus":            50,
    "Bkimono":            24,
    "Bparkscene":         24,
    "Cbasketballdrill":  50,
    "Cbqmall":            60,
    "Cracehorses":        30,
    "Cpartyscene":        50,
    "Dbasketballpass":   50,
    "Dblowingbubbles":   50,
    "Dbqsquare":         60,
    "Dracehorses":       30,
    "Efourpeople":       60,
    "Ejohnny":           60,
    "Ekristenandsara":   60,
    "Fbasketballdrilltext":  50,
    "Fchinaspeed":            30,
    "Fslideediting":         30,
    "Fslideshow":           20,
    "4K_football":        50,
    "4K_tianfu":          50,
    "4K_wudao":           50,
    "G_footballdejia":   25,
    "G_footballxijia":   25,
    "T_jphn":             25,
    "T_maque":            25,
    "T_misha":            25,
    "V_american":         30,
    "V_hnwskn":           25,
    "V_wsgs1":            25,
    "V_wsgs2":            25,
    "V_zghsy":            25
}