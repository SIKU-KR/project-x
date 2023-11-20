import pandas as pd
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

dayDict_reverse = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Sunday'}

dayDict = {'월':0,'화':1,'수':2,'목':3,'금':4,'토':5}
template = np.zeros((6,23), int)

df = pd.read_csv('../pages/process_final.csv')
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

# ----------------- 여기서부터 기능구현 ------------------
class_count_on_time = np.zeros((6,23),int)
for room in timetable:
    room_info = timetable[room]
    for day in range(6):
        for time in range(23):
            if room_info[day][time] == 1:
                class_count_on_time[day][time] += 1

# 각 차원별로 시각화
for i in range(class_count_on_time.shape[0]):
    plt.figure(figsize=(10, 4))
    plt.bar(range(23), data[i])
    plt.title(f'Dimension {i + 1}')
    plt.xlabel('Time Slots')
    plt.ylabel('Values')
    plt.show()

# 전체 / 과 / 과&학년