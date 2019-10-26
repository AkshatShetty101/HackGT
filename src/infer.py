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
import uuid
import datetime

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

tables = {}
chair_map = {}

def printDDA(dda):
    for arr in dda:
        print(arr, end="\n")


def printTables():
    for key in tables:
        table = tables[key]
        print("Key %2s | Confidence %2f | Centroid %0.2d, %0.2d" %
              (key, table['confidence'], *table['centroid']), end="\n")
        for cid in table['chairs']:
            chair = table['chairs'][cid]
            if chair['occupied']:
                print("Key %2s | Occupied: %s | Confidence %2f | Centroid %0.2d, %0.2d" %
                      (cid, chair['occupied'], chair['confidence'], *chair['centroid']), end="\n")
        print("------------------------------------")
        print("\n")


def printOccupied():
    c_ch = []
    c_t = []
    for key in tables:
        table = tables[key]
        for cid in table['chairs']:
            chair = table['chairs'][cid]
            if chair['occupied']:
                print("Key %2s | Confidence %2f | Time %s | Centroid %0.2d, %0.2d" %
                      (key, table['confidence'], str(table['time']), *table['centroid']), end="\n")
                print("Key %2s | Occupied: %s | Confidence %2f | Centroid %0.2d, %0.2d" %
                      (cid, chair['occupied'], chair['confidence'], *chair['centroid']), end="\n")
                c_t.append(table['centroid'])
                c_ch.append(chair['centroid'])
                # print("------------------------------------")
                print("\n")
    if len(c_ch) > 0:
        drawBox(c_ch)
        # drawLine(c_ch, c_t)


def cleanChairs():
    for key in tables:
        table = tables[key]
        if len(table['chairs']) < 2:
            continue
        new_chairs = {}
        chairs = []
        for cid in table['chairs']:
            temp = table['chairs'][cid]
            temp['key'] = cid
            chairs.append(temp)
        chairs.sort(key=lambda x: x['centroid'][0])
        for i in range(len(chairs)-1):
            if (abs(chairs[i]['centroid'][0]-chairs[i+1]['centroid'][0]) > 50
            or abs(chairs[i]['centroid'][1]-chairs[i+1]['centroid'][1]) > 50):
                new_chairs[chairs[i]["key"]]=chairs[i]
        table['chairs'] = new_chairs

def mapChairToTable():
    not_orphans=set()
    for coords in table_coords:
        new_entry={'centroid': centroid(
            *coords[0: 4]), 'chairs': {}, 'num': 0, 'confidence': coords[4]}
        min=200000
        for chair in chair_coords:
            gap=dist(*new_entry['centroid'],
                       *centroid(chair[0], chair[1], chair[2], chair[3]))
            if(gap < min):
                min=gap
        # print(min, end="\n")
        min=max(min, dist(coords[0], coords[1], *new_entry['centroid']))
        for chair in chair_coords:
            c=centroid(chair[0], chair[1], chair[2], chair[3])
            gap=dist(*new_entry['centroid'], *c)
            if(gap < min):
                not_orphans.add(str(c[0])+" "+str(c[1]))
                new_entry['chairs'][uuid.uuid1()]={'centroid': c, 'confidence': chair[4],
                                                     'occupied': False}
        tables[uuid.uuid1()]=new_entry
    if len(not_orphans)-len(chair_coords) == 0:
        return
    orphan_table={'centroid': [-1, -1], 'num': -1, 'chairs': {}, 'confidence': -1}
    for chair in chair_coords:
        c=centroid(chair[0], chair[1], chair[2], chair[3])
        if not str(c[0])+" "+str(c[1]) in not_orphans:
            orphan_table['chairs'][uuid.uuid1()]={'centroid': c, 'confidence': chair[4],
                                                    'occupied': False}
    tables[uuid.uuid1()]=orphan_table


def mapPeopleToChairs():
    # print("People----------------\n")
    for person in people_coords:
        if person[4] < 0.7:
            continue
        c=centroid(person[0], person[1], person[2], person[3])
        flag=False
        for id in tables:
            table=tables[id]
            for cid in table['chairs']:
                chair=table['chairs'][cid]
                # print(abs(c[0]-chair['centroid'][0]),
                #       abs(c[1]-chair['centroid'][1]))
                if abs(c[0]-chair['centroid'][0]) < 30 and \
                        abs(c[1]-chair['centroid'][1]) < 30:
                    chair['occupied']=True
                    table['time']=time.strftime("%H")
                    table['num'] += 1
                    flag=True
                    break
            if flag:
                break


def tableSizes():
    for table in table_coords:
        print(table, end = "\n")
        print(dist(table[0], table[1], table[2], table[3]), end = "\n\n")


def getTables():
    for table in boxes[61]:
        if(table[4] > .7):
            flag=False
            c=centroid(table[0], table[1], table[2], table[3])
            for key in tables:
                old=tables[key]
                if abs(old['centroid'][0]-c[0]) < 20 and abs(old['centroid'][1]-c[1]) < 20:
                    flag=True
                    break
            if flag:
                continue
            table_coords.append(table)
    # print(tables, end="\n\n")


def getChairs():
    for chair in boxes[57]:
        if(chair[4] > .7):
            flag=False
            c=centroid(chair[0], chair[1], chair[2], chair[3])
            for key in tables:
                old=tables[key]
                for cid in old['chairs']:
                    old_chair=old['chairs'][cid]
                    if abs(old_chair['centroid'][0]-c[0]) < 50 and abs(old_chair['centroid'][1]-c[1]) < 50:
                        flag=True
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
    frame=input


def drawBox(list_c):
    # Create figure and axes
    _, ax=plt.subplots(1)
    # Display the image
    ax.imshow(frame)
    # Create a Rectangle patch
    for c in list_c:
        rect=patches.Rectangle(
            (c[0]-20, c[1]-20), 40, 40, linewidth = 1, edgecolor = 'r', facecolor = 'none')
        # Add the patch to the Axes
        ax.add_patch(rect)
    s="./output/"+str(time.time())+".jpg"
    plt.savefig(s)
    plt.close()


def drawLine(list_c1, list_c2):
    # Create figure and axes
    _, ax=plt.subplots(1)
    # Display the image
    ax.imshow(frame)
    # Create a Rectangle patch
    for i in range(len(list_c1)):
        ax.plot([list_c1[i][0], list_c2[i][0]], [list_c1[i][1],
                                                 list_c2[i][1]], '--', linewidth = 1, color = 'firebrick')
    s="./output/"+str(time.time())+".jpg"
    plt.savefig(s)
    plt.close()


def setBoxes(input):
    global boxes
    boxes=input
    run()


def generateDataset():
    tf = "./output/data.csv"
    with open(tf, "w+") as f:
        time = datetime.datetime.now()
        for idx, data in tables.items():
            if data["num"] != -1:
                for id, chair in data["chairs"].items():
                    # id = "{}-{}".format(idx, chair_id)
                    if id in chair_map and not chair["occupied"]:
                        print("------------Present and someone left!----------")
                        print("Chair id %s"%(str(id)))
                        x = chair_map[id]
                        del chair_map[id]
                        daysDiff = time - x["time"]
                        occupied_for = daysDiff.seconds/60
                        print(x)
                        start_time = x["time"].hour*60+x["time"].minute
                        f.write("{},{},{},{}".format(
                            occupied_for, x["num"], x["table_id"], start_time))
                    elif (id not in chair_map) and chair["occupied"]:
                        print("--------------Just occupied!------------------------------")
                        print("Chair id %s"%(str(id)))
                        chair_map[id] = {"table_id": idx,
                                         "time": time, "num": data["num"]}
        f.close()
    # printTables()
    # with open(tf) as f:
    #     f.write('{},{},{}\n'.format())


def clearAll():
    global tables, table_coords, chair_coords, people_coords
    tables={}
    table_coords=[]
    chair_coords=[]
    people_coords=[]


def clearTemp():
    global table_coords, chair_coords, people_coords
    table_coords=[]
    chair_coords=[]
    people_coords=[]


def run():
    clearTemp()
    getTables()
    getChairs()
    getPeople()
    mapChairToTable()
    cleanChairs()
    mapPeopleToChairs()
    printTables()
    # printOccupied()
    generateDataset()
