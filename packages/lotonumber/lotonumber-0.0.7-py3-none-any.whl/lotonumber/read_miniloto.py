import os, csv
from loto_basic import LotoBasic

def read_miniloto():
    csv_file = os.path.dirname(os.path.abspath(__file__)) + '/data/miniloto.csv'
    miniloto_data = []
    with open(csv_file, 'rt') as fin:
        reader = csv.reader(fin)
        for num, row in enumerate(reader):
            if num == 0:
                continue
            miniloto = LotoBasic(row[0],\
                    [int(row[2]), int(row[3]), int(row[4]),\
                    int(row[5]), int(row[6])], [int(row[7])],\
                    [int(row[8]), int(row[9]), int(row[10]), int(row[11])],\
                    [int(row[12]), int(row[13]), int(row[14]), int(row[15])])
            miniloto_data.insert(0, miniloto)

    return miniloto_data

if __name__ == '__main__':
    data = read_miniloto()
    for i in data:
        print(i)
