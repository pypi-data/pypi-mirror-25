import sys
from all_loto import AllLoto

def main():
    if len(sys.argv) != 3:
        print("""引数の数が違います。
loto 種別(5,6,7) 抽選回(1〜)
""")
        sys.exit()

    data = AllLoto().data(int(sys.argv[1]), int(sys.argv[2]))
    print(data.nums)
