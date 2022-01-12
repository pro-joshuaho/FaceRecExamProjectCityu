import csv
import names
import cv2
import os

cur_path = os.path.dirname(os.path.realpath(__file__))


with open(f'{cur_path}/info.csv', 'w', newline='') as info:
    fieldnames = ['first_name', 'last_name', 'seat_no'] # add student code

    csv_writer = csv.DictWriter(info, fieldnames=fieldnames, delimiter=',')

    csv_writer.writeheader()

    # for i in range(0,40):
    #     first_name = names.get_first_name()
    #     last_name = names.get_last_name()
    #     seat_no = f'A{i+1}'
    #     line = {'first_name':first_name, 'last_name':last_name, 'seat_no': seat_no}
    #     print(line)
    #     csv_writer.writerow(line)

    myList = os.listdir(f'{cur_path}/imagesAttendance')
    print(myList)
    split_Names = []
    i=1
    for cl in myList:
        curImg = cv2.imread(f'{cur_path}/imagesAttendance/{cl}')
        full_name = os.path.splitext(cl)[0]
        first, last = full_name.split(' ')
        line = {"first_name": first, "last_name": last, "seat_no": f'A{i}'}
        i+=1
        print(line)
        csv_writer.writerow(line)
