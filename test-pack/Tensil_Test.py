import sys 
import yaml
import subprocess


def yamlname(basename, ta, tb, alpha, beta):
  ret = basename + '_'
  ret = ret + ('t' if ta else 'n')
  ret = ret + ('t' if tb else 'n')
  ret = ret + '_'
  ret = ret + 'a%d' % alpha
  ret = ret + '_'
  ret = ret + 'b%d' % beta
  return ret


def check_log(basename, log):
  if log.find('clientExit=0 (PASS)') != -1:
    print(basename + ' PASS')
  else:
    print(basename + ' FAIL')


def runTest(idx, ta, tb, alpha, beta):
  basename = yamlname(sys.argv[idx].split('.')[0], ta, tb, alpha, beta)
  
  with open(sys.argv[idx]) as file:
      test_yaml = yaml.load(file, Loader=yaml.FullLoader)

  test_yaml['BenchmarkProblems'][0][0]['TransposeA'] = ta
  test_yaml['BenchmarkProblems'][0][0]['TransposeB'] = tb
  test_yaml['GlobalParameters']['DataInitTypeAlpha'] = alpha
  test_yaml['GlobalParameters']['DataInitTypeBeta'] = beta

  with open('awieojf.yaml', 'w') as file:
      documents = yaml.dump(test_yaml, file)

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
    alpha = [1, 2]
    beta = [0, 2]

    command = ['mkdir', 'data']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()

    for i in range(1, len(sys.argv)):
        for ta in tA:
            for tb in tB:
                for al in alpha:
                    for be in beta:
                        runTest(i, ta, tb, al, be)

if __name__ == "__main__":
    main()
