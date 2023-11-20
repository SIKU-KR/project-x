import pandas as pd
import re

file_name = "data_basic.xlsx"

df = pd.read_excel(file_name)

print(df)

# 두개의 칼럼만 필요할듯?
selected_columns = ['교과목명', '강의요시/강의실', '담당교수','수강학부(과)/전공', '학년', '학수번호']

df_selected = df[selected_columns]

# df_selected

df= df_selected.dropna() #강의실이 배정되지 않은 결측값만 제거
# df

# 강의요시를 분할하여 새로운 DataFrame 생성
new_rows = []
for index, row in df.iterrows():
    name = row["교과목명"]
    times = row["강의요시/강의실"].split(", ")
    prof = row["담당교수"].strip()
    major = row["수강학부(과)/전공"]
    grade = row["학년"]
    sbjno = row["학수번호"]
    for time in times:
        new_rows.append([name, time, prof, major, grade, sbjno])

# 새로운 DataFrame 생성
new_df = pd.DataFrame(new_rows, columns=["과목명", "시간", "교수", "전공", "학년", "학수번호"])

# 결과 출력
# new_df

# 강의실, 요일, 시간 정보를 추출하여 새로운 열 추가
new_df['강의실'] = new_df['시간'].apply(lambda x: re.search(r'\((.*?)\)', x).group(1) if re.search(r'\((.*?)\)', x) else '')
new_df['요일'] = new_df['시간'].apply(lambda x: re.search(r'([월화수목금토일]+)', x).group(1) if re.search(r'([월화수목금토일]+)', x) else '')
new_df['강의시간'] = new_df['시간'].apply(lambda x: re.search(r'(\d{1,2}-\d{1,2})', x).group(1) if re.search(r'(\d{1,2}-\d{1,2})', x) else '')

# 결과 출력
print("전처리된 데이터프레임:")
# new_df

new_df.drop(['시간'], axis=1, inplace=True)

new_df.to_csv('process_final.csv', index=False)

