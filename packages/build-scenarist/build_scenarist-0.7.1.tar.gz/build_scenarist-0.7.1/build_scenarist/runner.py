# -*- coding: UTF-8 -*-
 
import sys
import argparse
import re
import os
import platform

from subprocess import call
import subprocess
import shlex

from os.path import exists
from os import makedirs

from build_scenarist.utility import cd, run, runPythonCode
from build_scenarist.info import Info
from build_scenarist.config import bcolors

def getTargets(pathToScript):
    with open(pathToScript) as f:
        content = f.readlines()

    targetPositions = []
    for lineIndex, text in enumerate(content):
        if bool(re.match("^(\[+.*\]+)$", text)):
            targetPositions.append(lineIndex)

    targets = {}
    fro=0
    to=0
    targetName="None"
    for i, val in enumerate(targetPositions):
        fro = targetPositions[i]+1
        if i+1 < len(targetPositions):
            to = targetPositions[i+1]
        else:
            to = len(content)
        targetName = content[targetPositions[i]][1:-2]
        targetCode = '\n'.join(content[fro:to])
        targets[targetName] = targetCode
    # print targets
    return targets

def targetsNotInScript(targets, pathToScript):
    targetsCode = getTargets(pathToScript)
    result = []
    for target, params in targets:
        if not(target in targetsCode):
            result.append(target)
    return result

def executeTargets(p_targets, pathToScript):
    notFoundTargets = targetsNotInScript(p_targets, pathToScript)
    isFaill = False
    if len(notFoundTargets) != 0:
        for target in notFoundTargets:
            isFaill = True
            print bcolors.FAIL + "\nError: Target %s not found in %s" % (target, pathToScript) + bcolors.ENDC
            sys.stdout.flush()

    if isFaill == False:
        targetsCode = getTargets(pathToScript)
        for target, params in p_targets:
            print bcolors.OKGREEN + "Target " + target + "..." + bcolors.ENDC
            sys.stdout.flush()
            code = ""
            # print(params)
            for paramCode in params:
                code += "%s\n" % (paramCode) 
                # print(paramCode)
            # code += "container='sogimu/astralinux:1.11'\n"
            code += targetsCode[target]

            runPythonCode(code)
            # sys.stdout.write("\n" + bcolors.HEADER + "python >" + bcolors.ENDC + "\n")
            # sys.stdout.write(bcolors.BOLD + code + bcolors.ENDC + "\n")
            # sys.stdout.flush()
            # exec(code)
    else:
        print bcolors.FAIL + "\nError: Please, specify existed targets name!" + bcolors.ENDC
        sys.stdout.flush()

def executeTargetsInImage(targets, pathToScript, image):
    notFoundTargets = targetsNotInScript(targets, pathToScript)
    isFaill = False
    if len(notFoundTargets) != 0:
        for target in notFoundTargets:
            isFaill = True
            print bcolors.FAIL + "\nError: Target %s not found in %s" % (target, pathToScript) + bcolors.ENDC
            sys.stdout.flush()

    if isFaill == False:
        run("""
            sudo docker run -v %s:/repo %s bash -cex '
                hasPython2=$(dpkg --get-selections | grep -c -e "^python2.7\s.")
                hasPythonSetuptools=$(dpkg --get-selections | grep -c -e "^python-setuptools\s.")
                hasPipPackage=$(dpkg --get-selections | grep -c -e "^python-pip\s.")
                hasPip=$(which pip | grep -c pip)

                if [ "$hasPython2" == 0 ] || [ "$hasPythonSetuptools" == 0 ] || [ "$hasPip" == 0 ]; then
                    apt-get update
                fi

                if [ "$hasPython2" == 0 ]; then
                    echo "Package Python2 installing ..."
                    apt-get -y install python2.7
                fi

                if [ "$hasPythonSetuptools" == 0 ]; then
                    echo "Package python-setuptools installing ..."
                    apt-get -y install python-setuptools
                fi

                if [ "$hasPip" == 0 ]; then
                    if [ "$hasPipPackage" == 0 ]; then
                        echo "Package python-pip installing ..."
                        apt-get -y install python-pip
                    else
                        echo "Utility pip installing ..."
                        easy_install pip
                    fi
                fi

                hasScenarist=$(pip freeze | grep -c build-scenarist)
                if [ "$hasScenarist" == 0 ]; then
                    echo "Utilit byuild_scenarist installing ..."    
                    pip install build_scenarist
                fi

                cd /repo
                scenarist.py info
                scenarist.py run %s
            '
            """ % (os.getcwd(), image, " ".join(targets)))
    else:
        print bcolors.FAIL + "\nError: Please, specify existed targets name!" + bcolors.ENDC
        sys.stdout.flush()
