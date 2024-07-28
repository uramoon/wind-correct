import sys
import windcorr as wc

if len(sys.argv) < 2:
    print("Usage: python train.py [stn_no]")
    sys.exit(1)

stn_no = sys.argv[1]
wc.make_dataset(stn_no)
wc.train_model(stn_no)
