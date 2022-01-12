import csv

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'imagesAttendance'
images = []
classNames = []
cur_path = os.path.dirname(os.path.realpath(__file__))
myList = os.listdir(f'{cur_path}/{path}')
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{cur_path}/{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open(f'{cur_path}/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')
    #can link it to the database if have time

encodeListKnown = findEncodings(images)
print('encoding Complete', len(encodeListKnown))

cap = cv2.VideoCapture(0) # 0 is the id

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurface = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurface, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and min(faceDis) < 0.4:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            print(faceDis)
            seat_number = ''
            subject = ''
            paper_no = ''
            with open(f'{cur_path}/info.csv', 'r', newline='') as profiles:
                csv_reader = csv.DictReader(profiles, delimiter=',')
                for line in csv_reader:
                    if line['full_name'] == classNames[matchIndex]:
                        seat_number = line['seat_no']
                        subject = line['subject']
                        paper_no = line['paper_no']
            y1, x2, y2, x1 = y1-20, x2+20, y2+20, x1-20

            # exam_details = f'{name} {chr(10)}{subject} paper{paper_no}'
            # exam_details = chr(10).join([name, f'{subject} paper {paper_no}'])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.rectangle(img, (x1-150, y1), (x1, y2+20), (99,248,171), cv2.FILLED) # left box
            cv2.rectangle(img, (x1, y2-20), (x2, y2+20), (121,240,108), cv2.FILLED) # bottom box
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) # bottom text (name)
            cv2.putText(img, f'{subject} paper {paper_no}', (x1+6, y2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
            cv2.putText(img, "seat no:", (x1-135, y1+40), cv2.FONT_HERSHEY_SIMPLEX , 1, (0,0,0), 2)
            cv2.putText(img, seat_number, (x1-135, y1+95), cv2.FONT_HERSHEY_SIMPLEX , 2, (0,0,0), 2) ##
            markAttendance(name)
        elif min(faceDis) > 0.4:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 - 20, x2 + 20, y2 + 20, x1 - 20
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 20), (x2, y2 + 20), (121, 240, 108), cv2.FILLED)  # bottom box
            cv2.putText(img, "Not Recognized", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)




# imgElon = face_recognition.load_image_file('stills/Elon Musk.jpg')
# imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
# imgTest = face_recognition.load_image_file('stills/Elon test.jpg')
# imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)
#
# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255,0,255), 2)
#
# results = face_recognition.compare_faces([encodeElon],encodeTest)
# faceDis = face_recognition.face_distance([encodeElon],encodeTest)
# cv2.putText(imgTest,f'{results} {round(faceDis[0],2)}',(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
#
# print(results, faceDis)
#
# cv2.imshow('Elon Musk', imgElon)
# cv2.imshow('Elon Test', imgTest)
# cv2.waitKey(0)