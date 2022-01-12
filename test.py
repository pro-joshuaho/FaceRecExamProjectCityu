import csv
import names
import cv2
import os
import random

cur_path = os.path.dirname(os.path.realpath(__file__))

subjects = ['Econ', 'Phy', 'ICT', 'Psy', 'Chem', 'Bio', 'Geog', 'Chin', 'Eng', 'Maths']

with open(f'{cur_path}/info.csv', 'w', newline='') as info:
    fieldnames = ['full_name', 'first_name', 'last_name', 'seat_no', 'subject', 'paper_no'] # add student code / time remaining until exam starts

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
        line = {"full_name": full_name,"first_name": first, "last_name": last, "seat_no": f'A{i}', "subject": subjects[random.randint(0,len(subjects)-1)], "paper_no": random.randint(1,3)}
        i+=1
        print(line)
        csv_writer.writerow(line)
