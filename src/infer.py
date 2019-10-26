'''
Objectives:
Tell table to chairs mapping, if table exists
Tell chair to location mapping
Tell table to location mapping

Table - {centroid, chairs, confidence}
Chair - {centroid, confidence}
'''
from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

classes = {
    0: '__background__', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
    5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
    11: 'fire hydrant', 12: 'stop sign', 13: 'parking meter', 14: 'bench', 15: 'bird',
    16: 'cat', 17: 'dog', 18: 'horse', 19: 'sheep', 20: 'cow', 21: 'elephant', 22: 'bear',
    23: 'zebra', 24: 'giraffe', 25: 'backpack', 26: 'umbrella', 27: 'handbag', 28: 'tie',
    29: 'suitcase', 30: 'frisbee', 31: 'skis', 32: 'snowboard', 33: 'sports ball',
    34: 'kite', 35: 'baseball bat', 36: 'baseball glove', 37: 'skateboard',
    38: 'surfboard', 39: 'tennis racket', 40: 'bottle', 41: 'wine glass', 42: 'cup',
    43: 'fork', 44: 'knife', 45: 'spoon', 46: 'bowl', 47: 'banana', 48: 'apple',
    49: 'sandwich', 50: 'orange', 51: 'broccoli', 52: 'carrot', 53: 'hot dog',
    54: 'pizza', 55: 'donut', 56: 'cake', 57: 'chair', 58: 'couch', 59: 'potted plant',
    60: 'bed', 61: 'dining table', 62: 'toilet', 63: 'tv', 64: 'laptop', 65: 'mouse',
    66: 'remote', 67: 'keyboard', 68: 'cell phone', 69: 'microwave', 70: 'oven',
    71: 'toaster', 72: 'sink', 73: 'refrigerator', 74: 'book', 75: 'clock', 76: 'vase',
    77: 'scissors', 78: 'teddy bear', 79: 'hair drier', 80: 'toothbrush'}

frame = []

table_coords = []
chair_coords = []
people_coords = []

tables = []


def printDDA(dda):
    for arr in dda:
        print(arr, end="\n")


def printTables():
    temp = []
    for table in tables:
        for chair in table['chairs']:
            if chair['occupied']:
                print("Confidence %2f | Centroid %0.2d, %0.2d" %
                      (table['confidence'], *table['centroid']), end="\n")
                print("Occupied: %s | Confidence %2f | Centroid %0.2d, %0.2d" %
                      (chair['occupied'], chair['confidence'], *chair['centroid']), end="\n")
                temp.append(chair['centroid'])
                print("------------------------------------")
                print("\n")
    if len(temp) > 0:
        drawBox(temp)


def cleanChairs():
    for table in tables:
        if len(table['chairs']) < 2:
            continue
        table['chairs'].sort(key=lambda x: x['centroid'][0])
        temp = []
        for i in range(len(table['chairs'])-1):
            if (abs(table['chairs'][i]['centroid'][0]-table['chairs'][i+1]['centroid'][0]) > 50) or (abs(table['chairs'][i]['centroid'][1]-table['chairs'][i+1]['centroid'][1]) > 50):
                temp.append(table['chairs'][i])
        temp.append(table['chairs'][len(table['chairs'])-1])
        table['chairs'] = temp
        # print(table['chairs'])


def mapChairToTable():
    not_orphans = set()
    for table in table_coords:
        temp = {'centroid': centroid(
            *table[0: 4]), 'chairs': [], 'confidence': table[4]}
        min = 20000000000
        for chair in chair_coords:
            gap = dist(*temp['centroid'],
                       *centroid(chair[0], chair[1], chair[2], chair[3]))
            if(gap < min):
                min = gap
        # print(min, end="\n")
        min = max(min, dist(table[0], table[1], *temp['centroid']))
        for chair in chair_coords:
            c = centroid(chair[0], chair[1], chair[2], chair[3])
            gap = dist(*temp['centroid'], *c)
            if(gap < min):
                not_orphans.add(str(c[0])+" "+str(c[1]))
                temp['chairs'].append(
                    {'centroid': c, 'confidence': chair[4], 'occupied': False})
        tables.append(temp)
    if len(not_orphans)-len(chair_coords) == 0:
        return
    orphan_table = {'centroid': [-1, -1], 'chairs': [], 'confidence': -1}
    for chair in chair_coords:
        c = centroid(chair[0], chair[1], chair[2], chair[3])
        if not str(c[0])+" "+str(c[1]) in not_orphans:
            orphan_table['chairs'].append(
                {'centroid': c, 'confidence': chair[4], 'occupied': False})
    tables.append(orphan_table)


def mapPeopleToChairs():
    # print("People----------------\n")
    for person in people_coords:
        if person[4] < 0.7:
            continue
        c = centroid(person[0], person[1], person[2], person[3])
        flag = False
        for table in tables:
            for chair in table['chairs']:
                # print(abs(c[0]-chair['centroid'][0]),
                #       abs(c[1]-chair['centroid'][1]))
                if abs(c[0]-chair['centroid'][0]) < 50 and \
                        abs(c[1]-chair['centroid'][1]) < 50:
                    chair['occupied'] = True
                    flag = True
                    break
            if flag:
                break


def tableSizes():
    for table in table_coords:
        print(table, end="\n")
        print(dist(table[0], table[1], table[2], table[3]), end="\n\n")


def getTables():
    for table in boxes[61]:
        if(table[4] > .7):
            flag = False
            c = centroid(table[0], table[1], table[2], table[3])
            for old in tables:
                if abs(old['centroid'][0]-c[0]) < 20 and abs(old['centroid'][1]-c[1]) < 20:
                    flag = True
                    break
            if flag:
                continue
            table_coords.append(table)
    # print(tables, end="\n\n")


def getChairs():
    for chair in boxes[57]:
        if(chair[4] > .7):
            flag = False
            c = centroid(chair[0], chair[1], chair[2], chair[3])
            for old in tables:
                for old_chair in old['chairs']:
                    if abs(old_chair['centroid'][0]-c[0]) < 20 and abs(old_chair['centroid'][1]-c[1]) < 20:
                        flag = True
                        break
                if flag:
                    break
            if flag:
                continue
            chair_coords.append(chair)
    # print(len(chair_coords))
    # print(chairs, end="\n\n")


def getPeople():
    # print("People-------------------------\n")
    for person in boxes[1]:
        # print(person)
        if(person[4] > .7):
            people_coords.append(person)
    # print(len(people_coords))


def dist(x1, y1, x2, y2):
    return pow(pow(x1-x2, 2)+pow(y1-y2, 2), 0.5)


def centroid(x1, y1, x2, y2):
    return [0.5*(x1+x2), 0.5*(y1+y2)]


def setFrame(input):
    global frame
    frame = input


def drawBox(list_c):
    # Create figure and axes
    fig, ax = plt.subplots(1)
    # Display the image
    ax.imshow(frame)
    # Create a Rectangle patch
    for c in list_c:
        rect = patches.Rectangle(
        (c[0]-20, c[1]-20), 40, 40, linewidth=1, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
    s = "./output/"+str(time.time())+".jpg"
    plt.savefig(s)


def setBoxes(input):
    global boxes
    boxes = input
    run()


def clearAll():
    tables = []
    table_coords = []
    chair_coords = []
    people_coords = []


def clearTemp():
    table_coords = []
    chair_coords = []
    people_coords = []


def run():
    clearTemp()
    getTables()
    getChairs()
    getPeople()
    mapChairToTable()
    cleanChairs()
    mapPeopleToChairs()
    printTables()
