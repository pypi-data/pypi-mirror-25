import sys, os, csv
# import loto_basic
from read_miniloto import read_miniloto
from read_loto6 import read_loto6
from read_loto7 import read_loto7

class AllLoto:
    def __init__(self):
        self.miniloto = read_miniloto()
        self.loto6 = read_loto6()
        self.loto7 = read_loto7()

    def data(self, div, round):
        """
        ロトくじの当選データを返す。
        div:  宝くじ種別(数値 5:ミニロト, 6:ロト6, 7:ロト7)
        round: 抽選回(1〜)
        """
        if div== 5:
            return self.miniloto[round - 1]
        elif div == 6:
            return self.loto6[round - 1]
        elif div == 7:
            return self.loto7[round - 1]
        else:
            raise '宝くじ種別が不正です。div={}'.format(div)

if __name__ == '__main__':
    all_loto = AllLoto()
    loto = all_loto.data(7, 208)
    print(loto.nums)     # 当選番号のリスト
    print(loto.bonus)    # ボーナス数字のリスト
    print(loto.priznum)  # 当選者数のリスト
    print(loto.amounts)  # 当選金額のリスト
    print(loto.c_over)   # キャリーオーバー金額
