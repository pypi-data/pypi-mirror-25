import numpy as np

def distribution(analysis):
    # 抽選数字の分布を表示する
    num_list = analysis.distribution()

    for no, i in enumerate(num_list):
        print('{round}: {num}'.format(round=no, num=i))
