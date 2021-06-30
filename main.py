import sys

def read_data(file):
    data = list()
    with open('./input/{}.txt'.format(file), mode='rt', encoding='utf-8') as r:
        line = None
        while True:
            line = r.readline().strip('\n')
            if line == '':
                break
            raw = list(line.split('\t'))
            #tmp = raw[:1] + list(map(int, raw[1:]))
            tmp = list()
            for i in range(1, 9, 2):
                tmp.append(list(map(int, raw[i:i+2])))
            tmp = raw[:1] + coordinate_sort(tmp)
            data.append(tmp)
    return data

def coordinate_sort(temp):
    temp = list(sorted(temp, key=lambda x: x[1]))
    temp = list(sorted(temp[:2], key=lambda x: x[0])) + list(sorted(temp[2:], key=lambda x: -x[0]))
    return temp
    
#정렬된 bounding box 데이터를 출력 포맷에 맞춰 파일에 write한다.
def write_data(file, lines):
    with open('./output/{}.txt'.format(file), mode='wt', encoding='utf-8') as w:
        i = 0
        for line in lines:
            i += 1
            string = ''
            line.sort(key=lambda x:x[1][0])
            for x in line:
                string += ' ' + x[0]
            r = "Line #{}:".format(i) + string + ", "
            r += "[[{},{}], [{},{}], [{},{}], [{},{}]]".format(line[0][1][0], line[0][1][1], line[-1][3][0], line[0][1][1], line[-1][3][0], line[-1][3][1], line[0][1][0], line[-1][3][1]) + "\n"
            w.write(r)

#기울기 고려
def compare_box(start, next):
    variation = 30
    #윗변
    x1, y1, x2, y2 = start[1][0], start[1][1], start[2][0], start[2][1]
    nx1, ny1, nx2, ny2 = next[1][0], next[1][1], next[4][0], next[4][1]
    if x1 != x2:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        if nx1 != nx2:
            na = (ny2 - ny1) / (nx2 - nx1)
            nb = ny1 - na * nx1
            #두 일차함수의 교차점 계산
            cx = (b - nb) / (a - na)
            cy = a * cx + b
        else:
            cx = nx1
            cy = a * cx + b
        up = ((nx1 - cx) ** 2 + (ny1 - cy) ** 2)**0.5
    #아랫변
    x3, y3, x4, y4 = start[3][0], start[3][1], start[4][0], start[4][1]
    if x3 != x4:
        a = (y4 - y3) / (x4 - x3)
        b = y3 - a * x3
        if nx1 != nx2:
            na = (ny2 - ny1) / (nx2 - nx1)
            nb = ny1 - na * nx1
            #두 일차함수의 교차점 계산
            cx = (b - nb) / (a - na)
            cy = a * cx + b
        else:
            cx = nx1
            cy = a * cx + b
        bottom = ((nx2 - cx) ** 2 + (ny2 - cy) ** 2)**0.5
    
    if up < variation and bottom < variation:
        return True
    else:
        return False

#데이터의 위쪽이 항상 상단일 경우
def compare_box_1(start, next):
    variation = 15
    sx1, sy1, sx2, sy2 = start[2][0], start[2][1], start[3][0], start[3][1]
    nx1, ny1, nx2, ny2 = next[1][0], next[1][1], next[4][0], next[4][1]

    if sy1 > ny1:
        up = sy1 - ny1
    else:
        up = ny1 - sy1
    if sy2 > ny2:
        bottom = sy2 - ny2
    else:
        bottom = ny2 - sy2
    
    if up <= variation and bottom <= variation:
        return True
    else:
        return False

def main(input, output):
    #1 - 좌측 상단, 2 - 우측 상단, 3 - 우측 하단, 4 - 좌측 하단
    #['string', [x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    data = read_data(input)
    data.sort(key=lambda x: (x[1][1], x[1][0]))
    lines = list()
    line = [data[0]]
    for i in range(1, len(data)):
        if compare_box(data[i-1], data[i]):
            line.append(data[i])
        else:
            lines.append(line)
            line = [data[i]]
    lines.append(line)

    write_data(output, lines)

if __name__ == '__main__':
    #input 데이터와 output 파일의 번호를 입력받는다.
    if len(sys.argv) != 2:
        print('실행할 데이터의 번호를 입력해주세요!')
        sys.exit()

    main('data'+sys.argv[1], 'result'+sys.argv[1])