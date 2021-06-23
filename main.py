
def read_data(file):
    data = list()
    with open('./input/{}.txt'.format(file), mode='rt', encoding='utf-8') as r:
        line = None
        while True:
            line = r.readline().strip('\n')
            if line == '':
                break
            tmp = list(line.split('\t'))
            tmp = tmp[:1] + list(map(int, tmp[1:]))
            data.append(tmp)
    return data


def main():
    data = read_data('data1')
    data.sort(key=lambda x: (x[2], x[1]))
    for d in data:
        print(d)

if __name__ == '__main__':
    main()