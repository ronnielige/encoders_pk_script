import os

abr_test_set = [
    "as265_abr_run.py",
    "qy265_abr_run.py",
    "x264_abr_run.py",
    "x265_abr_run.py",
    ]

cbr_test_set = [
    "as265_cbr_run.py",
    "qy265_cbr_run.py",
    "x264_cbr_run.py",
    "x265_cbr_run.py",
    ]

fixqp_test_set = [
    "as265_fixqp_run.py",
    "qy265_fixqp_run.py",
    "x264_fixqp_run.py",
    "x265_fixqp_run.py",
    ]

test_set = cbr_test_set + fixqp_test_set + ["hm265_abr_run.py", "hm265_fixqp_run.py",]

for script in test_set:
    os.system("python %s"%script)