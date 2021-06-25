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
    

def write_data(file, lines):
    with open('./output/{}.txt'.format(file), mode='wt', encoding='utf-8') as w:
        i = 0
        for line in lines:
            i += 1
            string = ''
            line.sort(key=lambda x:x[1][0])
            for x in line:
                string += x[0]
            r = "Line #{}: ".format(i) + string + ", "
            r += "[[{},{}], [{},{}], [{},{}], [{},{}]]".format(line[0][1][0], line[0][1][1], line[-1][3][0], line[0][1][1], line[-1][3][0], line[-1][3][1], line[0][1][0], line[-1][3][1]) + "\n"
            w.write(r)

def compare_box(start, next):
    return False


def main(input, output):
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
    if len(sys.argv) != 2:
        print('실행할 데이터의 번호를 입력해주세요!')
        sys.exit()

    main('data'+sys.argv[1], 'result'+sys.argv[1])