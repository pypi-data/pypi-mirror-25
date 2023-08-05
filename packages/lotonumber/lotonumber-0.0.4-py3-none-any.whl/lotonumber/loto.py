import sys
import numpy as np
from all_loto import AllLoto
from miniloto_analysis import MinilotoAnalysis
from loto6_analysis import Loto6Analysis
from loto7_analysis import Loto7Analysis
from algo.distribution import distribution
# from algo import distribution as dst

def main():
    if len(sys.argv) != 2:
        print("""引数の数が違います。
loto 種別(5,6,7) 抽選回(1〜)
""")
        sys.exit()

    div = int(sys.argv[1])
    if div < 5 or div > 7:
        print("宝くじ種別が違います。")
        print("""宝くじ種別:
5:ミニロト
6:ロト6
7:ロト7""")
        sys.exit()

    loto_class = [MinilotoAnalysis, Loto6Analysis, Loto7Analysis]

    all_loto = AllLoto()
    loto_data = [all_loto.miniloto, all_loto.loto6, all_loto.loto7]
        
    analysis = loto_class[div-5](loto_data[div-5])

    print(analysis.frequency())
    ratio = analysis.number_ratio()
    for no, i in enumerate(ratio):
        print("{number:2}:{val:5.3}".format(number=no+1, val=i*100))

    print(sum(ratio))

if __name__ == '__main__':
    main()
