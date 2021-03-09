import sys
import subprocess

def main():

    buildCmds = []

    with open('test.log', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.find('sourceTmp') != -1:
            line = line.replace('sourceTmp', 'source')
            buildCmds.append(line)

    with open('build.sh', 'w') as file:
        for line in buildCmds:
            file.write(line)

    command = ['chmod', '755', 'build.sh']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()

if __name__ == '__main__':
    main()
