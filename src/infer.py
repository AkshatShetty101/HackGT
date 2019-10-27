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
import json

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

state_threshold = 4
table_counter = 0
chair_counter = 'A'

frame = []

chair_coords = []
people_coords = []

tables = {}
chair_map = {}

previousStates = {}


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
            if cid in previousStates:
                print(previousStates[cid])
        print("------------------------------------")
        print("\n")


def storeState():
    for key in tables:
        table = tables[key]
        for cid in table['chairs']:
            chair = table['chairs'][cid]
            if not chair['occupied']:
                previousStates[cid] = []
                continue
            if not cid in previousStates:
                previousStates[cid] = [chair['occupied']]
            else:
                previousStates[cid].append(chair['occupied'])
                if len(previousStates[cid]) > state_threshold:
                    previousStates[cid] = previousStates[cid][1:]


def printOccupied():
    c_ch = []
    c_t = []
    for key in tables:
        table = tables[key]
        for cid in table['chairs']:
            chair = table['chairs'][cid]
            if cid in previousStates:
                # count = 0
                print(str(len(previousStates[cid]))+"-"+str(cid))
                # for val in previousStates[cid]:
                #     if val:
                #         count += 1
                if len(previousStates[cid]) >= state_threshold:
                    # print("Key %2s | Confidence %2f | Time %s | Centroid %0.2d, %0.2d" %
                    #       (key, table['confidence'], str(table['time']), *table['centroid']), end="\n")
                    # print("Key %2s | Occupied: %s | Confidence %2f | Centroid %0.2d, %0.2d" %
                    #       (cid, chair['occupied'], chair['confidence'], *chair['centroid']), end="\n")
                    c_t.append(table['centroid'])
                    c_ch.append(chair['centroid']+[cid])
                    # print("------------------------------------")
                    # print("\n")
    if len(c_ch) > 0:
        drawBox(c_ch, 1)
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
            if(dist(*chairs[i]['centroid'], *chairs[i+1]['centroid'])) > 10:
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


def clearOccupied():
    for id in tables:
        table = tables[id]
        for cid in table['chairs']:
            chair = table['chairs'][cid]
            chair['occupied'] = False


def mapPeopleToChairs():
    print("People----------------\n")
    numberOfP = 0
    clearOccupied()
    for person in people_coords:
        c = centroid(person[0], person[1], person[2], person[3])
        print(c)
        flag = False
        for id in tables:
            table = tables[id]
            for cid in table['chairs']:
                chair = table['chairs'][cid]
                # print(abs(c[0]-chair['centroid'][0]),
                #       abs(c[1]-chair['centroid'][1]))
                if dist(*c, *chair['centroid']) < 60:
                    numberOfP += 1
                    chair['occupied'] = True
                    table['time'] = time.strftime("%H")
                    table['num'] += 1
                    flag = True
                    break
            if flag:
                break
    print(numberOfP)
    print("--------------------------------")


def getTables(boxes):
    global tables
    list_t = []
    for coords in boxes[61]:
        if(coords[4] > 0.6):
            print(coords[4])
            c = centroid(*coords[0: 4])
            tid = tableID()
            tables[tid] = {'centroid': c, 'chairs': {}, 'num': 0,
                           'confidence': coords[4], 'range': dist(coords[0], coords[1], *c)}
            list_t.append(c+[tid])
    orphan_table = {'centroid': [-1, -1], 'num': -1, 'chairs': {}, 'confidence': -1,
                    'range': -1}
    tables["orphan"] = orphan_table
    drawBox(list_t, 0)
    # print(tables, end="\n\n")


def getChairs(boxes):
    list_c = []
    for chair in boxes[57]:
        if(chair[4] > .6):
            # flag = False
            c = centroid(chair[0], chair[1], chair[2], chair[3])
            list_c.append(c+["C"])
            # for key in tables:
            #     table = tables[key]
            #     for cid in table['chairs']:
            #         old_chair = table['chairs'][cid]
            #         if(dist(*old_chair['centroid'], *c)) < 10:
            #             old_chair['centroid'] = c
            #             flag = True
            #             break
            #     if flag:
            #         break
            # if flag:
            #     continue
            chair_coords.append(chair)
    # print(len(chair_coords))
    # print(chairs, end="\n\n")
    drawBox(list_c, 0)
    mapChairToTable()


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


def drawBox(list_c, flag):
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
        plt.text(c[0], c[1], c[2], bbox=dict(facecolor='red', alpha=0.5))
    if flag == 1:
        s = "./output/"+str(time.time())+".jpg"
    else:
        s = "./output/tables/"+str(time.time())+".jpg"
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
    f = open(tf, "a")
    print("Chair_map", chair_map)
    time = datetime.datetime.now()
    for idx, data in tables.items():
        for id, chair in data["chairs"].items():
            if id in chair_map and not chair["occupied"]:
                print("------------Present and someone left!----------")
                print("Chair id %s" % (str(id)))
                x = chair_map[id]
                del chair_map[id]
                daysDiff = time - x["time"]
                occupied_for = int(daysDiff.seconds//60)
                start_time = x["time"].hour*60+x["time"].minute
                y = str(occupied_for)+"," + \
                    str(x["num"])+","+str(x["table_id"])+","+str(start_time)
                print(y)
                f.write(y)
            elif (id not in chair_map) and chair["occupied"] and len(previousStates[id]) >= 4:
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
    height, width, _ = np.shape(frame)
    result = {
        'size': {
            'w': width,
            'h': height
        },
        'tables': []
    }
    for tid in tables:
        if tid == "orphan":
            continue
        table = tables[tid]
        entry = {
            'tid': tid,
            'centroid': {
                'x': int(table['centroid'][0]),
                'y': int(table['centroid'][1])
            },
            'chairs': []
        }
        for cid in table['chairs']:
            chair = table['chairs'][cid]
            c_entry = {
                'cid': cid,
                'occupied': len(previousStates[cid]) >= state_threshold,
                'centroid': {
                    'x': int(chair['centroid'][0]),
                    'y': int(chair['centroid'][1])
                }
            }
            entry['chairs'].append(c_entry)
        result['tables'].append(entry)
    print(result)
    # if use_case == "1":
    #     result['tables'] = [[], []]
    #     result['orphans'] = []
    #     sorted_tables = []
    #     for tid in tables:
    #         if(tid == 'orphan'):
    #             # print(tables[tid]['chairs'])
    #             for cid in tables[tid]['chairs']:
    #                 result['orphans'].append(
    #                     tables[tid]['chairs'][cid]['occupied'])
    #         else:
    #             sorted_tables.append(tables[tid])
    #     sorted_tables.sort(key=lambda x: -x['centroid'][1])
    #     for i, t in enumerate(sorted_tables):
    #         offset = int(t['centroid'][0]/(width/3))
    #         # print(offset, t['centroid'])
    #         sorted_chairs = []
    #         for cid in t['chairs']:
    #             sorted_chairs.append(t['chairs'][cid])
    #         sorted_chairs.sort(key=lambda x: -x['centroid'][1])
    #         back = []
    #         front = []
    #         for i, chairs in enumerate(sorted_chairs):
    #             if chairs['centroid'][1] > t['centroid'][1]:
    #                 back.append(chairs)
    #             else:
    #                 front.append(chairs)
    #         back.sort(key=lambda x: x['centroid'][0])
    #         front.sort(key=lambda x: x['centroid'][0])
    #         if i == 0:
    #             result['tables'][0].append({
    #                 'offset': offset,
    #                 'chairs': {
    #                     'back': [a['occupied'] for a in back],
    #                     'front': [a['occupied'] for a in front]
    #                 }
    #             })
    #         else:
    #             result['tables'][1].append({
    #                 'offset': offset,
    #                 'chairs': {
    #                     'back': [a['occupied'] for a in back],
    #                     'front': [a['occupied'] for a in front]
    #                 }
    #             })
    #     print(result)
    #     return result
    return result


def run(boxes):
    clearTemp()
    # getChairs(boxes)
    getPeople(boxes)
    # mapChairToTable()
    # cleanChairs()
    mapPeopleToChairs()
    storeState()
    printTables()
    # printOccupied()
    generateDataset()


def getDeets(tid):
    print(tables[int(tid)])
    return tables[int(tid)]