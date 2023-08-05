import os, csv
from loto_basic import LotoBasic

def read_loto6():
    csv_file = os.path.dirname(os.path.abspath(__file__)) + '/data/loto6.csv'
    loto6_data = []
    with open(csv_file, 'rt') as fin:
        reader = csv.reader(fin)
        for num, row in enumerate(reader):
            if num == 0:
                continue
            loto6 = LotoBasic(row[0],\
                    [int(row[2]), int(row[3]), int(row[4]),\
                    int(row[5]), int(row[6]), int(row[7])],\
                    [int(row[8])],\
                    [int(row[9]), int(row[10]), int(row[11]), int(row[12]), int(row[13])],\
                    [int(row[14]), int(row[15]), int(row[16]), int(row[17]), int(row[18])], int(row[19]) )
            loto6_data.insert(0, loto6)

    return loto6_data

if __name__ == '__main__':
    data = read_loto6()
    for i in data:
        print(i)
