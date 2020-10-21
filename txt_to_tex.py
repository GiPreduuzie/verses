#!/usr/bin/env python3

import os
import shutil
from glob import glob

def remove_trailing_empty_lines(directory = "."):
    files = glob("%s/*.txt" % (directory))
    for filepath in files:
        content = []
        with open(filepath, "r") as f:
            content = f.readlines()
            content.reverse()
            startIndex = 0
            while startIndex < len(content):
                if content[startIndex].strip() != "":
                    break
                else:
                    startIndex += 1
            if startIndex == 0:
                continue
            print(filepath)
            content = [content[index] for index in range(startIndex, len(content))]
            content[0] = content[0].replace("\n", "")
            content.reverse()
        with open(filepath, "w") as f:
            f.writelines(content)


def transpile(inputDirectory, outputDirectory):
    files = glob("%s/*.txt" % (inputDirectory))
    for inputFilepath in files:
        outputFilepath = inputFilepath.replace(inputDirectory, outputDirectory, 1)
        outputFilepath = outputFilepath.split(".")[0] + ".tex"
        output = []
        lines = []
        with open(inputFilepath, "r") as f:
            lines = f.readlines()
        output.append("\section{%s}" % (lines[0].replace("\n", "")))
        output.append("\\begin{verse}")
        for line in [lines[index] for index in range(2, len(lines))]:
            if line.strip() == "":
                output[len(output) - 1] = output[len(output) - 1].replace("\\\\", "")
                output.append("")
            else:
                output.append("%s\\\\" % (line.replace("\n", "")))
        output[len(output) - 1] = output[len(output) - 1].replace("\\", "")
        output.append("\end{verse}")
        with open(outputFilepath, "w+") as f:
            f.write("\n".join(output))


def update_index_file(directory = ".", index = "index"):
    files = glob("%s/*.tex" % (directory))
    output = []
    for filepath in files:
        if index in filepath:
            continue
        output.append("\include{./%s}" % (filepath.replace(".tex", "")))
    output.sort()
    indexpath = "%s/%s.tex" % (directory, index)
    with open(indexpath, "w+") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    inputDirectory = "txt"
    outputDirectory = "tex"

    shutil.rmtree(outputDirectory, ignore_errors=True, onerror=None)

    remove_trailing_empty_lines(inputDirectory)
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    transpile(inputDirectory, outputDirectory)
    update_index_file(outputDirectory)
 