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
        "산업공학과", "신산업융합학과", "생물공학과", "K뷰티산업융합학과"
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
        "줄기세포재생공학과", "의생명공학", "시스템생명공학과", "융합생명공학과"
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
        "일어교육과", "수학교육과", "체육교육과", "음악교육과", "교육공학과"
    ]
}

majorvalue = {
    "국어국문학과": "국어국문학과",
    "영어영문학과": "영어영문학과",
    "중어중문학과": "중어중문학과",
    "철학과": "철학과",
    "사학과": "사학과, 유럽문화학",
    "지리학과": "지리, 지리학과",
    "미디어커뮤니케이션학과": "미디어커뮤니케이션학과, 커뮤니케이션",
    "문화콘텐츠학과": "문화콘텐츠학과",
    "수학과": "수학과",
    "물리학과": "물리",
    "화학과": "화학과",
    "건축학부": "건축, 건축공학, 건축학부, 건축설계, 주거환경",
    "사회환경공학부": "환경공학과, 인프라시스템, 사회환경플랜트, 사회환경공학부, 기술융합공학과",
    "기계항공공학부": "항공우주정보시스템공학과, 기계공학부, 기계항공공학부",
    "전기전자공학부": "전기공학과, 전자공, 전기전자공학부",
    "화학공학부": "융합신소재공, 화학공, 유기나노시스템공, 화학공학부",
    "컴퓨터공학부": "소프트웨어학과, 컴퓨터공학과, 컴퓨터공학부",
    "산업공학과": "산업공학과",
    "신산업융합학과": "신산업융합학과",
    "생물공학과": "생물공",
    "K뷰티산업융합학과": "K뷰티산업융합학과",
    "정치외교학과": "정치외교학과",
    "경제학과": "경제학과",
    "행정학과": "행정학과",
    "국제무역학과": "국제무역학과",
    "응용통계학과": "응용통계학과",
    "융합인재학과": "융합인재학부,융합인재학과",
    "글로벌비즈니스학과": "글로벌비즈니스학과",
    "경영학과": "경영",
    "기술경영학과": "기술경영학과",
    "부동산학과": "부동산학과",
    "미래에너지공학과": "미래에너지공학",
    "스마트운행체공학과": "스마트운행체공학",
    "스마트ICT융합공학과": "스마트ICT융합공학",
    "화장품공학과": "화장품공학",
    "줄기세포재생공학과": "줄기세포재생공학, 분자생명공학",
    "의생명공학과": "의생명공학",
    "시스템생명공학과": "시스템생명공학",
    "융합생명공학과": "융합생명공학",
    "생명과학특성학과": "생명과학특성",
    "동물자원과학과": "동물자원과학",
    "식량자원과학과": "식량자원과학, 응용생물과",
    "축산식품생명공학과": "축산식품공,축산식품생명공학",
    "식품유통공학과": "식품유통공학",
    "환경보건과학과": "환경과학, 환경보건과학",
    "산림조경학과": "산림조경",
    "수의예과": "수의예과",
    "수의학과": "수의학과, 반려동물융합",
    "커뮤니케이션디자인학과": "커뮤니케이션디자인",
    "산업디자인학과": "산업디자인",
    "의상디자인학과": "의상디자인",
    "리빙디자인학과": "리빙디자인",
    "현대미술학과현대미술": "현대미술",
    "영상영화학과": "영상영화학과",
    "일어교육과": "일어교육과, 교직과",
    "수학교육과": "수학교육과, 교직과",
    "체육교육과": "체육교육과, 교직과",
    "음악교육과": "음악교육과, 교직과",
    "교육공학과": "교육공학과, 교직과",
    "영어교육과": "영어교육과, 교직과"
}


def get_majors(school):
    # 단과대학별 학과 리스트를 딕셔너리로 정리
    return college[school]

def makeTimeTable():
    pass

def makestats_all(school=None ,major=None, grade=None):
    dayDict = {'월':0,'화':1,'수':2,'목':3,'금':4,'토':5}
    template = np.zeros((6,23), int)
    try:
        df = pd.read_csv(open_url("http://127.0.0.1:5500/pages/process_final.csv"), dtype='str')
        df.dropna(inplace=True)
    except Exception:
        print('전처리 된 파일이 없습니다.')
    
    if school is None:
        pass
    elif grade is None:
        # Filter based on major using majorvalue dictionary
        major_filter = df['전공'].apply(lambda x: any(maj in x for maj in majorvalue[major].split(', ')))
        df = df[major_filter]
    else:
        # Filter based on both school and major using majorvalue dictionary
        school_major_filter = df['전공'].apply(lambda x: any(maj in x for maj in majorvalue[major].split(', ')))
        df = df[(df['전공'].str.contains(school) | school_major_filter) & df['학년'].str.contains(grade)]

        
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
    return class_count_on_time
