import sys
import os


def main():

    lines = []
    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    kernels = lines[0].split(', ')[10:]
    sizes = []
    fastGflops = []
    fastKernel = []
    for line in lines[1:]:
        line = line.split(', ')
        sizes.append(line[0:9])
        gflops = [float(g) for g in line[10:]]
        fastIndex = gflops.index(max(gflops))
        fastGflops.append(gflops[fastIndex])
        fastKernel.append(kernels[fastIndex])

    for i in range(0, len(sizes)):
        sizeStr = " ".join(s for s in sizes[i])
        print('{} {} {}'.format(sizeStr, fastGflops[i], fastKernel[i]))

if __name__ == '__main__':
    main()
