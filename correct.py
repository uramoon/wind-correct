import sys
import windcorr as wc

if len(sys.argv) < 4:
    print("Usage: python correct.py [model] [stn_no] [yyyymmdd]")
    sys.exit(1)

file_model = sys.argv[1]
stn_no = sys.argv[2]
ymd = sys.argv[3]

wc.correct_wind(file_model, stn_no, ymd)
