import csv
from slp import Projection

# header_info = []
# with open('SLR_TF U.S. Sea Level Projections.csv') as file:
#     reader = csv.reader(file)

#     header_ct = 0

#     for row in reader:
#         if (header_ct < 17):
#             header_info.append(row)
#             header_ct = header_ct + 1
#         else:
#             proj = Projection(row[0], row[1])
#             print(proj)
#             print(row)

file = csv.DictReader(open('slp_data.csv'))
for row in file:
    p = Projection(
        row['PSMSL Site'],
        row['PSMSL ID'],
        row['NOAA ID'],
        row['NOAA Name'],
        row['RSL GridNum'],
        row['Lat'],
        row['Long'],

        row['RSL2005 (cm)'],
        row['RSL2020 (cm)'],
        row['RSL2030 (cm)'],
        row['RSL2040 (cm)'],
    )
    # print(row)