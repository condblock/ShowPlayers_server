list = [(1, '12', '231', '2025-01-01 01:30:00'), (2, '23', '5342', '2025-01-01 01:30:00')]
def formatter(list):
    text = ''
    for i in list:
        text += f'이름: {i[1]}\t학교: {i[2]}\t시작 가능 시간: {i[3]}\n'
    return text
print(formatter(list))