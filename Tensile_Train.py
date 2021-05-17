import sys 
import yaml
import subprocess


def yamlname(basename, ta, tb, ca, cb, sb, alpha, beta):
  ret = basename + '_'
  ret = ret + ('t' if ta else 'n')
  ret = ret + ('t' if tb else 'n')
  ret = ret + '_'
  ret = ret + ('c' if ca else 'n')
  ret = ret + ('c' if cb else 'n')
  ret = ret + ('_sb1' if sb else '_sb0')
  ret = ret + f'_a{alpha}'
  ret = ret + f'_b{beta}'
  return ret


def check_log(basename, log):
  if log.find('clientExit=0 (PASS)') != -1:
    print(basename + ' PASS')
  else:
    print(basename + ' FAIL')


def genTmpYaml(infile, outfile, ta, tb, ca, cb, sb, alpha, beta):
    with open(infile, 'r') as f:
        lines = f.readlines()

    with open(outfile, 'w') as f:
        for line in lines:
            idx = line.find('TransposeA:')
            if idx != -1:
                line = line[:idx+11] + (' True' if ta else ' False') + '\n'

            idx = line.find('TransposeB:')
            if idx != -1:
                line = line[:idx+11] + (' True' if tb else ' False') + '\n'

            idx = line.find('ComplexConjugateA:')
            if idx != -1:
                line = line[:idx+18] + (' True' if ca else ' False') + '\n'

            idx = line.find('ComplexConjugateB:')
            if idx != -1:
                line = line[:idx+18] + (' True' if cb else ' False') + '\n'

            idx = line.find('StridedBatched:')
            if idx != -1:
                line = line[:idx+15] + (' True' if sb else ' False') + '\n'

            idx = line.find('DataInitTypeAlpha:')
            if idx != -1:
                line = line[:idx+18] + ' ' + str(alpha) + '\n'

            idx = line.find('DataInitTypeBeta:')
            if idx != -1:
                line = line[:idx+17] + ' ' + str(beta) + '\n'

            f.write(line)

def runTest(idx, ta, tb, ca, cb, sb, alpha, beta):
  basename = yamlname(sys.argv[idx].split('.')[0], ta, tb, ca, cb, sb, alpha, beta)
  
  genTmpYaml(sys.argv[idx], 'awieojf.yaml', ta, tb, ca, cb, sb, alpha, beta)

  print(basename + ' started')
  command = ["../Tensile/bin/Tensile", 'awieojf.yaml', './']
  output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
  check_log(basename, output)
  with open('test.log', 'w') as file:
      file.write(output)

  basename = 'data/' + basename

  command = ['mkdir', basename]
  subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
  command = ['mv', 'test.log', basename]
  subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
  command = ['mv', 'awieojf.yaml', basename+'/test.yaml']
  subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
  command = ['mv', '1_BenchmarkProblems', basename]
  subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()


def main():
    tA = [True, False]
    tB = [True, False]
    cA = [True, False]
    cB = [True, False]
    SB = [True, False]
    alpha = [1, 2]
    beta = [0, 2]

    command = ['mkdir', 'data']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()

    for i in range(1, len(sys.argv)):
        for ta in tA:
            for tb in tB:
                for ca in cA:
                    for cb in cB:
                        for sb in SB:
                            for al in alpha:
                                for be in beta:
                                    runTest(i, ta, tb, ca, cb, sb, al, be)

if __name__ == "__main__":
    main()
