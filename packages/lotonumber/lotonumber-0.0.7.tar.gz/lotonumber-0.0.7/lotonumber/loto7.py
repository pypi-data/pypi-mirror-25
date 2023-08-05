import sys
from all_loto import AllLoto

def main():
    all_loto = AllLoto()

    if len(sys.argv) != 2:
        print("""引数の数が違います。
loto7 抽選回(1〜)
""")
        sys.exit()

    round = int(sys.argv[1])
    if round <= 0 or round > len(all_loto.loto7):
        print("抽選回が最大値を超えています。")
        print("抽選回≦{}".format(len(all_loto.loto7)))
        sys.exit()

    data = all_loto.data(7, int(sys.argv[1]))
    print(data.nums, data.bonus)

if __name__ == '__main__':
    main()
