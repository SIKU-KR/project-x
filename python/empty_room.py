import pandas as pd
import numpy as np
from copy import deepcopy
import re
from pyodide.http import open_url

def get_emptylist(building, time, day):
    dayDict = {'월':0,'화':1,'수':2,'목':3,'금':4,'토':5}
    template = np.zeros((6,23), int)
    df = pd.read_csv(open_url("http://127.0.0.1:5500/pages/process_final.csv"), dtype='str')
    df.dropna(inplace=True)
    # print(df_sliced)
    timetable = dict()
    for index, row in df.iterrows():
        room = row['강의실']
        day = row['요일']
        times = row['강의시간'].split('-')
        start_time = int(times[0]) - 1
        end_time = int(times[1])
        # 해당 요일, 시간의 index : timetable[room][dayDict[day]][i]
        # timetable에 해당 강의실이 존재하는 경우
        if room in timetable:
            for i in range(start_time, end_time):
                timetable[room][dayDict[day]][i] = 1
        # timetable에 해당 강의실이 존재하지 않는 경우
        else:
            copied_template = deepcopy(template)
            for i in range(start_time, end_time):
                copied_template[dayDict[day]][i] = 1
            timetable[room] = copied_template
    # print(timetable)
    classroom = list()
    data = timetable.keys()
    result = process_data(data, classroom)
    classroom_data = {key: value for key, value in result.items() if "온라인" not in key and "미배정" not in key}
    # classroom_data
    # 4개씩 잘라서 문자열로 출력
    result = []
    for room in classroom_data[building]:
        if room in timetable:
            schedule = timetable[room]
            if schedule[dayDict[day]][time-1] == 0:
                result.append(room)
            else:
                continue
    return result

def split_string_by_number(s):
    return re.split(r'(\d+)', s)

def process_data(data, classroom):
    result = {}
    for item in data:
        classroom = split_string_by_number(item)[0]
        if classroom in result.keys():
            result[classroom].append(item)
        else :
            result[classroom] = []
            result[classroom].append(item)
    return result