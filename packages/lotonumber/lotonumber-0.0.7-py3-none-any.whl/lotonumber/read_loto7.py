import os, csv
from loto_basic import LotoBasic

def read_loto7():
    csv_file = os.path.dirname(os.path.abspath(__file__)) + '/data/loto7.csv'
    loto7_data = []
    with open(csv_file, 'rt') as fin:
        reader = csv.reader(fin)
        for num, row in enumerate(reader):
            if num == 0:
                continue
            loto7 = LotoBasic(row[0],\
                    [int(row[2]), int(row[3]), int(row[4]),\
                    int(row[5]), int(row[6]), int(row[7]), int(row[8])],\
                    [int(row[9]), int(row[10])],\
                    [int(row[11]), int(row[12]), int(row[13]), int(row[14]), int(row[15]), int(row[16])],\
                    [int(row[17]), int(row[18]), int(row[19]), int(row[20]), int(row[21]), int(row[22])], int(row[17]) )
            loto7_data.insert(0, loto7)

    return loto7_data

if __name__ == '__main__':
    data = read_loto7()
    for i in data:
        print(i)
