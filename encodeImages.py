import os
import cv2
import face_recognition
import numpy as np
import sys
# from main import findEncodings    cannot use cuz "circular import"??

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    path = 'imagesAttendance'
    classNames = []
    images = []
    cur_path = os.path.dirname(os.path.realpath(__file__))
    myList = os.listdir(f'{cur_path}/{path}')
    # print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{cur_path}/{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    # print(classNames)

    encodeListKnown = findEncodings(images)
    # print('encoding Complete', len(encodeListKnown))
    encodeListKnown = np.array(encodeListKnown)
    print(encodeListKnown.shape)
    dimensions = encodeListKnown.shape

    print('Array:\n', encodeListKnown)
    file = open(f"{cur_path}/encodingDoc.txt", "w+")

    content = str(encodeListKnown)

    # print(type(encodeListKnown[[0,0]]))

    file.write(content)
    file.close()

# file = open("file1.txt", "r")
# content = file.read()
#
# print("\nContent in file1.txt:\n", content)
# file.close()