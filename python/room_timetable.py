from pyscript import document
import pandas as pd
import numpy as np
from copy import deepcopy
from pyodide.http import open_url

def getRoomlist():
    try:
        df = pd.read_csv(open_url("http://127.0.0.1:5500/pages/process_final.csv"))
        df.dropna(inplace=True)
        room_set = set(df['강의실'])
        room_list = list(room_set)
        return room_list
    except FileNotFoundError:
        print('전처리 된 파일이 없습니다.')

def make_timetable(room):
    timeTableObject = document.querySelector("#timetable tbody")
    timeTableObject.innerHTML = ''
    
    time_col = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
                        '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30']

    try:
        df = pd.read_csv(open_url("http://127.0.0.1:5500/pages/process_final.csv"))
        df.dropna(inplace=True)
    except Exception:
        print('전처리 된 파일이 없습니다.')
          
    # 해당 강의실의 시간표 처리를 위한 변수들
    dayDict = {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4, '토': 5}
    template = np.zeros((6, 23), int)
    stemplate = np.zeros((6,23), dtype='<U20')
    timetable = dict()
    classtable = dict()


    # timetable과 classtable 형성 (시간표 내용들)
    for index, row in df[df['강의실'] == room].iterrows():
        day = row['요일']
        times = row['강의시간'].split('-')
        start_time = int(times[0]) - 1
        end_time = int(times[1])

        # 해당 요일, 시간의 index : timetable[room][dayDict[day]][i]
        # timetable에 해당 강의실이 존재하는 경우
        if room in timetable:
            for i in range(start_time, end_time):
                timetable[room][dayDict[day]][i] = 1
                classtable[room][dayDict[day]][i] = row['과목명']
        # timetable에 해당 강의실이 존재하지 않는 경우
        else:
            copied_template = deepcopy(template)
            copied_classes = deepcopy(stemplate)
            for i in range(start_time, end_time):
                copied_template[dayDict[day]][i] = 1
                copied_classes[dayDict[day]][i] = row['과목명']
            timetable[room] = copied_template
            classtable[room] = copied_classes
    try:
        # 시간표 내용 형식으로 만들기
        valueList = []
        for i in range(22):
            val_row = []
            for j in range(7):
                if j == 0:
                    val_row.append(time_col[i])
                else:
                    if timetable[room][j-1][i] == 1:
                        val_row.append(classtable[room][j-1][i])
                    else:
                        val_row.append('')
            valueList.append(tuple(val_row))
        print(valueList)

    except KeyError:
        print(f"{room} not in dataset")
        return

    for line in valueList:
        tr = document.createElement('tr')
        for cell_data in line:
            td = document.createElement('td')
            td.textContent = cell_data
            tr.appendChild(td)
        timeTableObject.appendChild(tr)