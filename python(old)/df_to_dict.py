import pandas as pd
import numpy as np
from copy import deepcopy

template = {'월' : [False]*23,
            '화' : [False]*23,
            '수' : [False]*23,
            '목' : [False]*23,
            '금' : [False]*23,
            '토' : [False]*23}

df = pd.read_excel('process_final.xlsx')
df.dropna(inplace=True)
df_sliced = df.loc[:, '강의실':]
# print(df_sliced)
timetable = dict()

for index, row in df.iterrows():
    room = row['강의실']
    day = row['요일']
    times = row['강의시간'].split('-')
    start_time = int(times[0]) - 1
    end_time = int(times[1])

    # timetable에 해당 강의실이 존재하는 경우
    if room in timetable:
        for i in range(start_time, end_time):
            timetable[room][day][i] = True
    # timetable에 해당 강의실이 존재하지 않는 경우
    else:
        copied_template = deepcopy(template)
        for i in range(start_time, end_time):
            copied_template[day][i] = True
        timetable[room] = copied_template

print(timetable)

# ----------------- 여기서부터 기능구현 ------------------
class_count_on_time = np.zeros((6,23))
print(class_count_on_time)