import sys, os

#input 데이터 파일 입력 함수
def read_data(file):
    data = list()
    with open('./input/{}.txt'.format(file), mode='rt', encoding='utf-8') as r:
        line = None
        while True:
            line = r.readline().strip('\n')

            if line == '':
                break
            
            raw_data = list(line.split('\t'))

            tmp = list()
            for i in range(1, 9, 2):
                tmp.append(list(map(int, raw_data[i:i+2])))
            tmp = raw_data[:1] + coordinate_sort(tmp)

            data.append(tmp)
    return data

#좌표 정렬 함수
def coordinate_sort(temp):
    #1 - 좌측 상단, 2 - 우측 상단, 3 - 우측 하단, 4 - 좌측 하단
    #[x1, y1], [x2, y2], [x3, y3], [x4, y4]
    temp = list(sorted(temp, key=lambda x: x[0]))
    front = list(sorted(temp[:2], key=lambda x: x[1]))
    back = list(sorted(temp[2:], key=lambda x: x[1]))
    return front[:1] + back + front[1:]

#output 데이터 파일 출력 함수
def write_data(file, lines):
    try:
        if not os.path.exists('./output'):
            os.makedirs('./output')
    except OSError:
        print('Error: Creating Directory.')
    with open('./output/{}.txt'.format(file), mode='wt', encoding='utf-8') as w:
        i = 0
        for line in lines:
            i += 1
            string = ''
            for x in line:
                string += ' ' + x[0]
            r = "Line #{}:".format(i) + string + ", "
            r += "[[{},{}], [{},{}], [{},{}], [{},{}]]".format(line[0][1][0], line[0][1][1], line[-1][3][0], line[0][1][1], line[-1][3][0], line[-1][3][1], line[0][1][0], line[-1][3][1]) + "\n"
            w.write(r)

#(x, y) 두개의 좌표로 일차함수의 기울기와 y절편을 구하는 함수
#y = a*x + b
def linear_func(x1, y1, x2, y2):
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b

#두 일차함수의 교차점 계산하는 함수
def intersection(a, b, na, nb):
    cx = (nb - b) / (a - na)
    cy = a * cx + b
    return cx, cy

#유클리드 거리(두 점 사이의 거리) 함수
def euclidean_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

#기울기를 고려한 Line 판별 함수
def compare_box(start, next, threshold):
    #박스 상단부분 비교 부분
    sx1, sy1, sx2, sy2 = start[1][0], start[1][1], start[2][0], start[2][1]
    nx1, ny1, nx2, ny2 = next[1][0], next[1][1], next[4][0], next[4][1]
    if sx1 != sx2:
        a, b = linear_func(sx1, sy1, sx2, sy2)
        if nx1 != nx2:
            na, nb = linear_func(nx1, ny1, nx2, ny2)
            #두 일차함수의 교차점 계산
            cx, cy = intersection(a, b, na, nb)
        else:
            #nx1과 nx2의 값이 같을 경우 교차점 계산
            cx = nx1
            cy = a * cx + b
        up = euclidean_distance(nx1, ny1, cx, cy)

    #박스 하단부분 비교 부분
    sx3, sy3, sx4, sy4 = start[3][0], start[3][1], start[4][0], start[4][1]
    if sx3 != sx4:
        a, b = linear_func(sx3, sy3, sx4, sy4)
        if nx1 != nx2:
            na, nb = linear_func(nx1, ny1, nx2, ny2)
            #두 일차함수의 교차점 계산
            cx, cy = intersection(a, b, na, nb)
        else:
            #nx1과 nx2의 값이 같을 경우 교차점 계산
            cx = nx2
            cy = a * cx + b
        bottom = euclidean_distance(nx2, ny2, cx, cy)

    #박스 상하단부분 모두 일정값 이하라면 두개의 string은 같은 라인 상/하단부분 중 하나라도 일정값을 초과한다면 같은 라인이 아님.
    if up <= threshold and bottom <= threshold:
        return True
    else:
        return False

def main(input, output, threshold):
    #1 - 좌측 상단, 2 - 우측 상단, 3 - 우측 하단, 4 - 좌측 하단
    #['string', [x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    data = read_data(input)
        
    lines = []
    for d in data:
        if not lines:
            lines.append([d])
        else:
            check = False
            for i in range(len(lines)):
                if compare_box(lines[i][0], d, threshold):
                    check = True
                    break;
            if check:
                lines[i].append(d)
            else:
                lines.append([d])
    
    for i in range(len(lines)):
        lines[i].sort(key=lambda x: x[1][0])
    lines.sort(key=lambda x: x[0][1][1])

    write_data(output, lines)


if __name__ == '__main__':
    #input 데이터와 output 파일의 번호를 입력받는다.
    if len(sys.argv) != 3:
        print('usage: python main.py data_num threshold')
        sys.exit()

    main('data'+sys.argv[1], 'result'+sys.argv[1], int(sys.argv[2]))