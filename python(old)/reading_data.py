import pandas as pd
def split_and_flatten(input_list):
    flat_list = []
    for item in input_list:
        # Check if the item contains "온라인" before splitting
        if "온라인" in item:
            flat_list.append(item)
        else:
            # Split the item and remove the closing parenthesis
            split_items = item.split('(')
            flat_list.extend([split_items[0], split_items[1].replace(')', '')])
    return flat_list

def reformat(input):
    exclude_keyword = {'온라인', 'e-러닝'}
    input_splitted = input.split(',')
    # Stripping whitespace
    input_splitted = [item.strip() for item in input_splitted]
    # Filtering out items containing any of the exclude keywords
    input_splitted = [item for item in input_splitted if not any(keyword in item for keyword in exclude_keyword)]
    result = split_and_flatten(input_splitted)
    return result


# 1:no, 2:학년, 3:학수번호, 5:교과번호, 6:이수구분, 7:교과목명, 8:영문교과목명, 11:학점, 12:시간, 15:개설학부, 16:강의요시, 17: 담당교수
# CSV 열 제목, datatype 지정 선언
titles = ['no', '학년', '학수번호', '교과번호', '이수구분', '교과목명', '영문교과목명', '학점', '시간',
          '개설학부', '강의요시', '담당교수']
types = {'no': 'int',
         '학년': 'str',
         '학수번호': 'str',
         '교과번호': 'str',
         '이수구분': 'str',
         '교과목명': 'str',
         '영문교과목명': 'str',
         '학점': 'float',
         '시간': 'float',
         '개설학부': 'str',
         '강의요시': 'str',
         '담당교수': 'str'}

if __name__ == '__main__':
    # CSV 파일 읽기
    df = pd.read_csv('source.csv',
                     usecols=[0, 1, 2, 4, 5, 7, 8, 11, 12, 15, 16, 17],
                     names=titles,
                     dtype=types,
                     index_col=None,
                     skiprows=[0])

    # 강의실 정보가 없는 rows 버림
    df = df.dropna(subset=['강의요시'])

    # 강의시간, 강의실, 강의횟수를 연산해서 저장하는 temporary dataframe 생성 -> 연산 후에 concat 으로 합침
    temp_df = pd.DataFrame(index=df.index,
                           columns=['강의시간', '강의실', '강의횟수'])
    for index, row in df.iterrows():
        temp = reformat(row['강의요시'])
        timetxt = ''
        roomtxt = ''
        count = len(temp) // 2  # Assuming each pair is a time and room
        for i in range(0, count * 2):
            if i % 2 == 0:
                timetxt += temp[i] + ','
            else:
                roomtxt += temp[i] + ','
        timetxt = timetxt.rstrip(',')
        roomtxt = roomtxt.rstrip(',')
        temp_df.loc[index] = [timetxt, roomtxt, count]
    result = pd.concat([df, temp_df], axis=1)

    print(result)