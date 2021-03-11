import os
import itertools
import subprocess
import json

if __name__ == "__main__":
    #Get the pairs of directories of the current path
    rootdir = os.path.dirname(os.path.realpath(__file__))
    paths = os.listdir(rootdir)
    paths = [x for x in paths if os.path.isdir(os.path.join(rootdir, x))]
    pairs = list(itertools.combinations(paths, 2))
    
    for path in paths:
        result = subprocess.run(['cloc', '-json', '-include-lang=JavaScript', os.path.join(rootdir, path)], stdout=subprocess.PIPE)
        lines_of_code = json.loads(result.stdout)["JavaScript"]["code"]
        #print(lines_of_code)

    for pair in pairs:
        result = subprocess.run(["jsinspect", "-reporter", "json", "-t", "30",  pair[0], pair[1]], stdout=subprocess.PIPE, cwd=rootdir)
        out = json.loads(result.stdout)
        for match in out:
            print(match["instances"])
            print(len(match["instances"]))
            #print(match["instances"])
            #print(i)
            #break
        #out = json.loads(result.stdout)
        #print(out)
        break
    
