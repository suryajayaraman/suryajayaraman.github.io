#!/usr/bin/env python
# coding: utf-8

##############################################
# input : root dir
# output : 1 text file with content from all files
# things to think about:
# - input for files to exclude?
# - input for folders to exclude?
# 
# Solution Description
# - get all files in root project
# - see if any of path contains hidden folder directory
# - see if any of files is in excluded list
# - Create text file with content from filtered files
##############################################

import os
from pathlib import Path
from typing import List


def getFilesInDirRecursively(rootDir : str, extension : str = '*') -> List[str]:
    if(os.path.isdir(rootDir)):
        childItems = [str(x.resolve()) for x in Path(rootDir).rglob(extension)]
        recursiveFiles = [x for x in childItems if os.path.isfile(x)]
        return recursiveFiles
    else:
        return []
    
def containsHiddenDir(directory : str) -> bool:
    return any([x.startswith('.') for x in directory.split(os.sep)])

def filterFilesFromHiddenDir(filePaths : List[str]) -> List[str]:
    return [x for x in filePaths if not containsHiddenDir(x)]

def filterExcludedFiles(filePaths : List[str], excludedFiles : List[str]) -> List[str]:
    return [x for x in filePaths if not x.split(os.sep)[-1] in excludedFiles]

def getProjectRelativePath(absolutePath : str, projectRoot : str) -> str:
    return absolutePath.replace(projectRoot, "")

def writeContentToFile(filePaths: List[str], outputFilePath : str, projectRoot : str = '') -> None:
    with open(outputFilePath, 'w') as outFile:
        for path in filePaths:
            relativePath = getProjectRelativePath(path, projectRoot)
            with open(path, 'r') as inFile:
                outFile.write(f"{relativePath}\n\n")
                
                for line in inFile:
                    outFile.write(line)
                outFile.write("\n-----------------\n")
                    
            print(f"{relativePath} written to outFile")
    return


if __name__ == "__main__":

    rootDir = '/home/surya/Downloads/detr-main/'
    FILES_TO_EXCLUDE = ['Dockerfile', 'LICENSE', 'README.md', '', 'requirements.txt', '.github']

    allFiles = getFilesInDirRecursively(rootDir)
    filteredFiles = sorted(filterExcludedFiles(filterFilesFromHiddenDir(allFiles), FILES_TO_EXCLUDE))
    writeContentToFile(filteredFiles, outputFilePath='test.txt', projectRoot=rootDir)