from collections import defaultdict
import numpy as np # 後で必要なのでインポートしておく

class AnalysisBasic:
    def __init__(self, loto_data, loto_div):
        """
        loto_data: ロトくじデータ
        loto_div:  ロトくじ区分(5:ミニロト,6:ロト6, 7:ロト7)
        """
        self._data = loto_data # LotoBasicオブジェクトのリスト
        self.div = loto_div

    @property
    def max_no(self):
        return [31, 43, 37][self.div - 5]

    def frequency(self):
        """抽選数字の出現頻度をリストで返す
        """

        # 抽選数字データを走査し、数え上げる
        nums_dist = defaultdict(int)
        for loto_basic in self._data:
            for col in range(self.div):
                number = int(loto_basic.nums[col])
                nums_dist[number] += 1

        # 数え上げた数字(辞書)をリストに変換する
        # 数字の昇順に出現回数が並ぶ
        dist_list = list(range(self.max_no))
        for key in nums_dist.keys():
            dist_list[key-1] = nums_dist[key]

        return dist_list

    def number_ratio(self):
        """抽選数字の出現確率を返す
        """
        nums_ratio = np.array(self.frequency(), dtype=np.float64)
        return nums_ratio / sum(nums_ratio)
