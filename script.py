import os
import sys
import itertools
import subprocess
import json
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def merge_ranges(ranges):
    ranges = iter(sorted(ranges))
    current_start, current_stop = next(ranges)
    for start, stop in ranges:
        if start > current_stop:
            # Gap between segments: output current segment and start a new one.
            yield current_start, current_stop
            current_start, current_stop = start, stop
        else:
            # Segments adjacent or overlapping: merge.
            current_stop = max(current_stop, stop)
    yield current_start, current_stop

if __name__ == "__main__":
    #Get the pairs of directories of the current path
    rootdir = os.path.dirname(os.path.realpath(__file__))
    paths = os.listdir(rootdir)
    paths = [x for x in paths if os.path.isdir(os.path.join(rootdir, x))]
    paths.sort(key=lambda s: list(map(int, s.split('.'))))
    #paths = paths[0:4]
    pairs = list(itertools.combinations(paths, 2))
    
    n_code = []    
    for path in paths:
        #Run cloc, with .json as output, and JavaScript as the selected language
        result = subprocess.run(['cloc', '--fullpath', 
        '--not-match-f=\"src/intro.js|src/outro.js\"',
        '-json', '-include-lang=JavaScript', os.path.join(rootdir, path, "src")], stdout=subprocess.PIPE)
        lines_of_code = json.loads(result.stdout)["JavaScript"]["code"]
        n_code.append(lines_of_code)
        print(path, "&", lines_of_code, "\\\\")
    
    #Initialize matrix with 1 in diagonal and all other to 0
    data=[]
    i=0
    for path in paths:
        data.append([])
        data[-1]=[0]*i
        data[-1].append(1)
        zeros = [0]*(len(paths)-len(data[-1]))
        data[-1].extend(zeros)
        i+=1

    if os.path.exists("temp.js"):
        os.remove("temp.js")
    for pair in pairs:
        try:
            #Run jsinspect with specific threshold. Request output to be at json form. Ignore files which cannot be read by jsinspect
            result = subprocess.run(["jsinspect", "-reporter", "json", "-t", "10", "--ignore", 
            'src/intro.js|src/outro.js',
            os.path.join(pair[0], "src"), os.path.join(pair[1], "src")], stdout=subprocess.PIPE, cwd=rootdir)
            out = json.loads(result.stdout.decode('utf-8'))
        except:
            sim_n_code=0
            print("An exception occurred with jsinspect", result.stdout.decode('utf-8')[0:200])
        
        sim_n_code = 0
        
        files =[]
        files_code_lines=[]
        
        #For every match, add the files and lines of these files to two lists
        for match in out: 
            flag=False
            for i, instance in enumerate(match["instances"]):
                if i+1==len(match["instances"]):
                    break
                if not pathlib.Path(match["instances"][i]["path"]).parts[0] == pathlib.Path(match["instances"][i+1]["path"]).parts[0]:
                    #Versions are different
                    flag=True
                    break
            if flag:
                for i, instance in enumerate(match["instances"]):
                    p = match["instances"][i]
                    if p["path"] not in files:
                        files.append(p["path"])
                        files_code_lines.append([])
                    files_code_lines[files.index(p["path"])].append(p["lines"])

        #From these two lists, take then number of lines while removing overlapping ranges
        sim_n_code = 0
        n_splits = 0
        for matches in files_code_lines:
            n_splits+=len(matches)

        for i, lines in enumerate(files_code_lines):
            #Find the merged ranges
            merged_ranges = merge_ranges(lines)
            m = []
            for r in merged_ranges:
                m.append(r)

            #Open file, and save to a temporary file the lines that are in the match range
            f = open(os.path.join(rootdir,files[i][2:]), "r")
            lines = f.readlines()
            temp = open("temp.js", "a")
            for j, line in enumerate(lines):
                for r in m:
                    if r[0]-1 <= j <= r[1]-1:
                        temp.write("%s" % line)
                        break
            temp.close()
        
        if files:
            #Now we run cloc on this file to count only the code lines
            try:
                result = subprocess.run(['cloc', '-json', '-include-lang=JavaScript', "temp.js"], stdout=subprocess.PIPE)
                lines_of_code = json.loads(result.stdout)
                sim_n_code = lines_of_code["JavaScript"]["code"]-len(files)
            except:
                sim_n_code = 0
                print("An exception occurred with cloc", result.stdout.decode('utf-8')[0:200])
            open('temp.js', 'w').close() #clean file

        #Having the #lines_of_code for both versions, as well as the #similar_lines_of_code we can calculate the coverage
        index1 = paths.index(pair[0])
        index2 = paths.index(pair[1])
        coverage=sim_n_code/(n_code[index1]+n_code[index2])
        data[index2][index1] = coverage
        print(pair[0], "#code:", n_code[index1], pair[1], "#code:", n_code[index2], "Pair #sim:", sim_n_code, 
        "Coverage:", coverage)

    #Dont calculate upper half and diagonal
    mask = np.zeros_like(data)
    mask[np.triu_indices_from(mask)] = True

    #Color pallete similar to paper
    cmap = LinearSegmentedColormap.from_list(
        name='test', 
        colors=["white", "cyan", "lightgreen", "yellow", "red"]
    )

    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(data, cmap=cmap, square=True, vmin=0, vmax=1,
    linewidths=0.01, linecolor='grey', xticklabels=paths, yticklabels=paths, mask=mask, cbar_kws={"orientation": "horizontal"})
    fig.savefig(os.path.join(rootdir, "out", "heatmap.png"), dpi=400)