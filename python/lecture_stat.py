from pyscript import document
import pandas as pd
import numpy as np
from copy import deepcopy
from pyodide.http import open_url
import matplotlib.pyplot as plt

college = {
    "전체": ["전체"],
    "문과대학": [
        "국어국문학과", "영어영문학과", "중어중문학과", "철학과", "사학과", 
        "지리학과", "미디어커뮤니케이션학과", "문화콘텐츠학과"
    ],
    "이과대학": [
        "수학과", "물리학과", "화학과"
    ],
    "건축대학": [
        "건축학부"
    ],
    "공과대학": [
        "사회환경공학부", "기계항공공학부", "전기전자공학부", "화학공학부", "컴퓨터공학부",
        "산업공학부", "생물공학과", "K뷰티산업융합학과"
    ],
    "사회과학대학": [
        "정치외교학과", "경제학과", "행정학과", "국제무역학과", "응용통계학과",
        "융합인재학과", "글로벌비즈니스학과"
    ],
    "경영대학": [
        "경영학과", "기술경영학과"
    ],
    "부동산과학원": [
        "부동산학과"
    ],
    "KU융합과학기술원": [
        "미래에너지공학과", "스마트운행체공학과", "스마트ICT융합공학과", "화장품공학과", 
        "줄기세포재생공학과", "의생명공학과", "시스템생명공학과", "융합생명공학과"
    ],
    "상허생명과학대학": [
        "생명과학특성학과", "동물자원과학과", "식량자원과학과", "축산식품생명공학과", "식품유통공학과",
        "환경보건과학과", "산림조경학과"
    ],
    "수의과대학": [
        "수의예과", "수의학과"
    ],
    "예술디자인대학": [
        "커뮤니케이션디자인학과", "산업디자인학과", "의상디자인학과", "리빙디자인학과", 
        "현대미술학과", "영상영화학과"
    ],
    "사범대학": [
        "일어교육과", "수학교육과", "체육교육과", "음악교육과", "교육공학과", "교직과"
    ]
}

def get_majors(school):
    # 단과대학별 학과 리스트를 딕셔너리로 정리
    return college[school]

def makeTimeTable():
    pass

def makestats_all(timetable):
    dayDict = {'월':0,'화':1,'수':2,'목':3,'금':4,'토':5}
    template = np.zeros((6,23), int)

    try:
        df = pd.read_csv(open_url("http://127.0.0.1:5500/pages/process_final.csv"))
        df.dropna(inplace=True)
    except Exception:
        print('전처리 된 파일이 없습니다.')
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

    class_count_on_time = np.zeros((6,23),int)
    for room in timetable:
        room_info = timetable[room]
        for day in range(6):
            for time in range(23):
                if room_info[day][time] == 1:
                    class_count_on_time[day][time] += 1
    for i in range(class_count_on_time.shape[0]):
        plt.figure(figsize=(10, 4))
        plt.bar(range(23), data[i])
        plt.title(f'Dimension {i + 1}')
        plt.xlabel('Time Slots')
        plt.ylabel('Values')
        plt.show()

def makestats_major(major):
    pass