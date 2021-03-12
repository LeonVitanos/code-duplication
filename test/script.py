import os
import itertools
import subprocess
import json
import pathlib

if __name__ == "__main__":
    #Get the pairs of directories of the current path
    rootdir = os.path.dirname(os.path.realpath(__file__))
    paths = os.listdir(rootdir)
    paths = [x for x in paths if os.path.isdir(os.path.join(rootdir, x))]
    paths.sort()
    pairs = list(itertools.combinations(paths, 2))
    
    n_code = []

    for path in paths:
        print(path, end=",")

    print("\n")

    '''
    for path in paths:
        #Run cloc, with .json as output, and JavaScript as the selected language
        result = subprocess.run(['cloc', '-json', '-include-lang=JavaScript', os.path.join(rootdir, path)], stdout=subprocess.PIPE)
        lines_of_code = json.loads(result.stdout)["JavaScript"]["code"]
        n_code.append(lines_of_code)
        print(path, "&", lines_of_code, "\\\\")
        #print(lines_of_code)
    '''


    for pair in pairs:
        #Run jsinspect with specific threshold. Request output to be at json form. Ignore files which cannot be read by jsinspect
        result = subprocess.run(["jsinspect", "-reporter", "json", "-t", "30", "--ignore", 'src/intro.js|src/outro.js',
          pair[0], pair[1]], stdout=subprocess.PIPE, cwd=rootdir)
        out = json.loads(result.stdout)
        sim_n_code = 0
        for match in out:
            if len(match["instances"])==2: # for now only dealing with the simple case where there is a match with 2 instances
                #Check if the version of the paths is the same or not
                if pathlib.Path(match["instances"][0]["path"]).parts[0] == pathlib.Path(match["instances"][1]["path"]).parts[0]:
                    print('same')
                else:
                    # i think n_of lines will not be always the same
                    # i think we need the diff of both instances
                    sim_n_code=(match["instances"][0]["lines"][1]-match["instances"][0]["lines"][0] +
                    match["instances"][1]["lines"][1]-match["instances"][1]["lines"][0] + 2)
        
        index1 = paths.index(pair[0])
        index2 = paths.index(pair[1])
        print("Path 1 #code:", n_code[index1], "Path 2 #code:", n_code[index2], "Pair #sim:", sim_n_code, 
        "Coverage:", sim_n_code/(n_code[index1]+n_code[index2]))
