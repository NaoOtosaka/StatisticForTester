import csv

with open('../file/export.csv')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        print(row[0])

