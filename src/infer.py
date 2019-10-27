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

table_counter = 0
chair_counter = 'A'

frame = []

chair_coords = []
people_coords = []

tables = {}
chair_map = {}

previousStates = []


def printDDA(dda):
    for arr in dda:
        print(arr, end="\n")


def printTables():
    for key in tables:
        table = tables[key]
        print("Table ---> Key %2s | Confidence %2f | Centroid %0.2d, %0.2d" %
              (key, table['confidence'], *table['centroid']), end="\n")
        for cid in table['chairs']:
            chair = table['chairs'][cid]
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
                # print("Key %2s | Confidence %2f | Time %s | Centroid %0.2d, %0.2d" %
                #       (key, table['confidence'], str(table['time']), *table['centroid']), end="\n")
                # print("Key %2s | Occupied: %s | Confidence %2f | Centroid %0.2d, %0.2d" %
                #       (cid, chair['occupied'], chair['confidence'], *chair['centroid']), end="\n")
                c_t.append(table['centroid'])
                c_ch.append(chair['centroid'])
                # print("------------------------------------")
                # print("\n")
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
            if(dist(*chairs[i]['centroid'], *chairs[i+1]['centroid'])) > 30:
                new_chairs[chairs[i]["key"]] = chairs[i]
        new_chairs[chairs[-1]["key"]] = chairs[-1]
        table['chairs'] = new_chairs


def mapChairToTable():
    # print("Mapping chairs started")
    # print(len(tables["orphan"]["chairs"]))
    not_orphans = set()
    for tid in tables:
        table = tables[tid]
        min = 200000
        for chair in chair_coords:
            gap = dist(*table['centroid'],
                       *centroid(chair[0], chair[1], chair[2], chair[3]))
            if(gap < min):
                min = gap
        # print(min, end="\n")
        min = max(min, table['range'])
        for chair in chair_coords:
            c = centroid(chair[0], chair[1], chair[2], chair[3])
            gap = dist(*table['centroid'], *c)
            if(gap < min):
                not_orphans.add(str(c[0])+" "+str(c[1]))
                table['chairs'][chairID()] = {'centroid': c, 'confidence': chair[4],
                                              'occupied': False}
    if len(not_orphans)-len(chair_coords) == 0:
        return
    for chair in chair_coords:
        c = centroid(chair[0], chair[1], chair[2], chair[3])
        if str(c[0])+" "+str(c[1]) not in not_orphans:
            tables["orphan"]['chairs'][chairID()] = {'centroid': c, 'confidence': chair[4],
                                                     'occupied': False}
    # print(len(tables["orphan"]["chairs"]))
    # print("Mapping chairs done")


def mapPeopleToChairs():
    # print("People----------------\n")
    for person in people_coords:
        if person[4] < 0.7:
            continue
        c = centroid(person[0], person[1], person[2], person[3])
        flag = False
        for id in tables:
            table = tables[id]
            for cid in table['chairs']:
                chair = table['chairs'][cid]
                # print(abs(c[0]-chair['centroid'][0]),
                #       abs(c[1]-chair['centroid'][1]))
                if dist(*c, *chair['centroid']) < 30:
                    chair['occupied'] = True
                    table['time'] = time.strftime("%H")
                    table['num'] += 1
                    flag = True
                    break
            if flag:
                break


def getTables(boxes):
    global tables
    for coords in boxes[61]:
        if(coords[4] > .7):
            c = centroid(*coords[0: 4])
            tables[tableID()] = {'centroid': c, 'chairs': {}, 'num': 0,
                                 'confidence': coords[4], 'range': dist(coords[0], coords[1], *c)}
    orphan_table = {'centroid': [-1, -1], 'num': -1, 'chairs': {}, 'confidence': -1,
                    'range': -1}
    tables["orphan"] = orphan_table

    # print(tables, end="\n\n")


def getChairs(boxes):
    for chair in boxes[57]:
        if(chair[4] > .7):
            flag = False
            c = centroid(chair[0], chair[1], chair[2], chair[3])
            for key in tables:
                table = tables[key]
                for cid in table['chairs']:
                    old_chair = table['chairs'][cid]
                    if(dist(*old_chair['centroid'], *c)) < 30:
                        old_chair['centroid'] = c
                        flag = True
                        break
                if flag:
                    break
            if flag:
                continue
            chair_coords.append(chair)
    # print(len(chair_coords))
    # print(chairs, end="\n\n")


def getPeople(boxes):
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
    _, ax = plt.subplots(1)
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
    plt.close()


def drawLine(list_c1, list_c2):
    # Create figure and axes
    _, ax = plt.subplots(1)
    # Display the image
    ax.imshow(frame)
    # Create a Rectangle patch
    for i in range(len(list_c1)):
        ax.plot([list_c1[i][0], list_c2[i][0]], [list_c1[i][1],
                                                 list_c2[i][1]], '--', linewidth=1, color='firebrick')
    s = "./output/"+str(time.time())+".jpg"
    plt.savefig(s)
    plt.close()


def generateDataset():
    tf = "./output/data.csv"
    with open(tf, "w+") as f:
        time = datetime.datetime.now()
        for idx, data in tables.items():
            # if data["num"] != -1:
            for id, chair in data["chairs"].items():
                if id in chair_map and not chair["occupied"]:
                    print("------------Present and someone left!----------")
                    print("Chair id %s" % (str(id)))
                    x = chair_map[id]
                    del chair_map[id]
                    daysDiff = time - x["time"]
                    occupied_for = daysDiff.seconds/60
                    print(x)
                    start_time = x["time"].hour*60+x["time"].minute
                    f.write("{},{},{},{}".format(
                        occupied_for, x["num"], x["table_id"], start_time))
                elif (id not in chair_map) and chair["occupied"]:
                    print(
                        "--------------Just occupied!------------------------------")
                    print("Chair id %s" % (str(id)))
                    chair_map[id] = {"table_id": idx,
                                     "time": time, "num": data["num"]}
        f.close()
    # printTables()
    # with open(tf) as f:
    #     f.write('{},{},{}\n'.format())


def clearAll():
    global tables, chair_coords, people_coords
    tables = {}
    chair_coords = []
    people_coords = []


def clearTemp():
    global chair_coords, people_coords
    chair_coords = []
    people_coords = []


def tableID():
    global table_counter
    table_counter += 1
    return table_counter


def chairID():
    global chair_counter
    chair_counter = chr(ord(chair_counter)+1)
    return chair_counter


def getAppData(use_case):
    global tables, frame
    result = {
        'tables': [],
        'orphans': []
    }
    width, height, _ = np.shape(frame)
    if use_case == "1":
        result['tables'] = [[], []]
        result['orphans'] = []
        sorted_tables = []
        for tid in tables:
            if(tid == 'orphan'):
                # print(tables[tid]['chairs'])
                for cid in tables[tid]['chairs']:
                    result['orphans'].append(tables[tid]['chairs'][cid]['occupied']) 
            else:
                sorted_tables.append(tables[tid])
        sorted_tables.sort(key=lambda x: -x['centroid'][1])
        for i, t in enumerate(sorted_tables):
            offset = int(t['centroid'][0]/(width/3))
            # print(offset, t['centroid'])
            sorted_chairs = []
            for cid in t['chairs']:
                sorted_chairs.append(t['chairs'][cid])
            sorted_chairs.sort(key=lambda x: -x['centroid'][1])
            back = []
            front = []
            for i, chairs in enumerate(sorted_chairs):
                if chairs['centroid'][1] > t['centroid'][1]:
                    back.append(chairs)
                else:
                    front.append(chairs)
            back.sort(key=lambda x: x['centroid'][0])
            front.sort(key=lambda x: x['centroid'][0])
            if i == 0:
                result['tables'][0].append({
                    'offset': offset,
                    'chairs': {
                        'back': [a['occupied'] for a in back],
                        'front': [a['occupied'] for a in front]
                    }
                })
            else:
                result['tables'][1].append({
                    'offset': offset,
                    'chairs': {
                        'back': [a['occupied'] for a in back],
                        'front': [a['occupied'] for a in front]
                    }
                })
        print(result)
        return result
    return ""


def run(boxes):
    clearTemp()
    getChairs(boxes)
    getPeople(boxes)
    mapChairToTable()
    cleanChairs()
    mapPeopleToChairs()
    # printTables()
    # printOccupied()
    generateDataset()
