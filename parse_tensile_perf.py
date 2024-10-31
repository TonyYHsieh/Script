import os
import sys
import re

def main():
    fname = sys.argv[1]
    lints = []

    with open(fname) as f:
        lines = f.readlines()

    perf = {}
# 0,0/4,0/503,Contraction_l_Alik_Bljk_Cijk_Dijk,"(1024,1216,1,1024)",None,,None,Cijk_Alik_Bljk_F8SS_BH_AS_UserArgs_MT64x32x64_MI16x16x1_SN_GRVWA8_GRVWB8_GSU1_GSUC0_GSUWGMRR0_K1_LBSPPA128_LPA8_LPB8_MIWT2_1_SU32_SUM0_SUS256_SVW1_VWA1_WSGRA0_WSGRB0_WGM8_WGMXCC1_WGMXCCGn1,PASSED,11.4477,222764,,1,2,304,1,1,1,1,64749568,4980736,nan,395.75,85,1100,nan,1,2024-10-30 11:03:03.324149
    for line in lines:
        result = re.match(".*,.*,.*,.*,\"\(([0-9]*),([0-9]*),1,([0-9]*)\)\",None,,None,(.*),PASSED,([0-9\.]+),([0-9]+),*", line)
        if result:
            key = " ".join([result.group(1), result.group(2), result.group(3)])
            perf[key] = [result.group(5), result.group(6), result.group(4)]

    for key in perf:
        print("%s %s %s %s" %(key, perf[key][0], perf[key][1], perf[key][2]))

if __name__=="__main__":
    main()
