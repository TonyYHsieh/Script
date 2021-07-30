import os
import sys
import shutil

def toGBName(f):
  result = os.path.splitext(f)
  return result[0] + '_GB' + result[1]


def converSB2GB(infile, outfile):
  result = []

  with open(infile, 'r') as f:
    lines = f.readlines()

  for i in range(0, len(lines)):
    line = lines[i]

    if line.find('StridedBatched') == -1:
      result.append(line)

    ret = line.find('SilentHighPrecisionAccumulate')
    if ret != -1:
      result.append(line[0:ret] + 'StridedBatched: false\n')

  with open(outfile, 'w') as f:
    for line in result:
      f.write(line)


def main():
  if len(sys.argv) != 3:
    print('python3 ConvertSBtoGB.py [input_dir] [output_dir]')
    return

  if os.path.exists(sys.argv[2]):
    shutil.rmtree(sys.argv[2])
  os.mkdir(sys.argv[2])

  for f in os.listdir(sys.argv[1]):
    infile = os.path.join(sys.argv[1], f)
    outfile = os.path.join(sys.argv[2], toGBName(f))
    converSB2GB(infile, outfile)


if __name__ == '__main__':
  main()
