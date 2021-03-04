import os
import re
import sys


def getHeader(filename, orientation):
    lines = []
    with open(os.path.join(filename, 'header.yaml'), 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if lines[i].find('TransposeA') != -1:
            lines[i] = '      TransposeA: ' + ('False' if (orientation[0] == 'n') else 'True') + '\n'
        if lines[i].find('TransposeB') != -1:
            lines[i] = '      TransposeB: ' + ('False' if (orientation[1] == 'n') else 'True') + '\n'

    return lines


def numToStr(sizes):
    lines = []
    for size in sizes:
        lines.append(f'          - Exact: [{size[0]}, {size[1]}, {size[2]}, {size[3]}]\n')
    return lines


def getSize(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i in range(0, len(lines)):
        key = lines.pop(0)
        if key.find('- [2, 3, 0, 1]') != -1:
            break

    lines = [lines[i*2][6:] for i in range(0, len(lines)//2)]

    allSize = []
    for line in lines:
        result = re.match(r'\[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]\n', line)
        if result:
            allSize.append([int(result.group(1)), int(result.group(2)), int(result.group(3)), int(result.group(4))])
        else:
            print("ERROR")

    bigSize = []
    bigSizeGSU = []
    midSize = []
    midSizeGSU = []
    smaSize = []
    smaSizeGSU = []
    bigM = []
    bigN = []
    bigK = []
    other = []

    CUs = 72
    for size in allSize:
        m = size[0]
        n = size[1]
        b = size[2]
        k = size[3]

        if ((m//128) * (n//128) * b) >= CUs:
            bigSize.append(size)
        elif ((m//128) * (n//128) * b * (k//4096)) >= CUs:
            bigSizeGSU.append(size)
        elif ((m//64) * (n//64) * b) >= CUs:
            midSize.append(size)
        elif ((m//64) * (n//64) * b * (k//4096)) >= CUs:
            midSizeGSU.append(size)
        elif ((m//32) * (n//32) * b) >= CUs:
            smaSize.append(size)
        elif ((m//32) * (n//32) * b * (k//4096)) >= CUs:
            smaSizeGSU.append(size)
        elif m > 1024:
            bigM.append(size)
        elif n > 1024:
            bigN.append(size)
        elif k > 4096:
            bigK.append(size)
        else:
            other.append(size)
          
    return {'bigSize' : numToStr(bigSize),
            'bigSizeGSU' : numToStr(bigSizeGSU),
            'midSize' : numToStr(midSize),
            'midSizeGSU' : numToStr(midSizeGSU),
            'smaSize' : numToStr(smaSize),
            'smaSizeGSU' : numToStr(smaSizeGSU),
            'bigM' : numToStr(bigM),
            'bigN' : numToStr(bigN),
            'bigK' : numToStr(bigK),
            'other' : numToStr(other)}

def getBody(path, filename):
    lines = []
    with open(os.path.join(sys.argv[1], filename), 'r') as f:
        lines = f.readlines()
    return lines


def main():

    lines = ['# headers\n']
    lines += getHeader(sys.argv[1], sys.argv[2])

    sizes = getSize(sys.argv[3])
    for key in sizes:
      if sizes[key]:
        lines += [f'# bodys {key}\n']
        lines += getBody(sys.argv[1], key+'.yaml')
        lines += sizes[key]
        lines += ['\n']

    lines += ['# tail\n']
    lines += getBody(sys.argv[1], 'tail.yaml')

    output = os.path.join(sys.argv[4], sys.argv[1] + '_' + sys.argv[2] + '.yaml')
    with open(output, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    main()
