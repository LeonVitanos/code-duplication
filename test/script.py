import os
import itertools
import subprocess
import json
import pathlib
import plotly.express as px

if __name__ == "__main__":
    #Get the pairs of directories of the current path
    rootdir = os.path.dirname(os.path.realpath(__file__))
    paths = os.listdir(rootdir)
    paths = [x for x in paths if os.path.isdir(os.path.join(rootdir, x))]
    paths.sort(key=lambda s: list(map(int, s.split('.'))))
    pairs = list(itertools.combinations(paths, 2))
    
    n_code = []
    
    for path in paths:
        #Run cloc, with .json as output, and JavaScript as the selected language
        result = subprocess.run(['cloc', '--not-match-f=intro.js|outro.js', '-json', '-include-lang=JavaScript', os.path.join(rootdir, path, "src")], stdout=subprocess.PIPE)
        lines_of_code = json.loads(result.stdout)
        lines_of_code = lines_of_code["JavaScript"]["code"] + lines_of_code["JavaScript"]["comment"] + lines_of_code["JavaScript"]["blank"]
        n_code.append(lines_of_code)
        #print(path, "&", lines_of_code, "\\\\")
    
    
    #n_code = [1202, 1202, 1381, 1302, 2129, 2534, 2561, 2627, 2935, 2937, 3282, 1940, 1956, 2090, 2114, 2195, 2195, 2198, 2848, 2848, 2841, 2951, 3293, 3293, 3346, 3452, 3787, 3887, 4376, 4376, 4443, 4475, 4861, 4861, 4908, 4944, 5198, 5198, 5392, 5392, 5368, 5468, 5312, 5317, 5321, 5333, 5266, 5288, 5320, 5316, 5323, 15095, 15073, 15092, 15092, 6320, 6319, 6312, 6307, 6307, 4802, 4823, 4817, 4827, 14461, 14510, 14521, 14521, 14521, 5733, 5731, 5733, 5733, 5726, 6013, 6034, 6095, 6117, 6117, 6235, 6235, 6352, 6357]
    
    #Initialize matrix with 1 in diagonal
    data=[]
    i=0
    for path in paths:
        data.append([])
        data[-1]=[0]*i
        data[-1].append(1)
        zeros = [0]*(len(paths)-len(data[-1]))
        data[-1].extend(zeros)
        i+=1

    for pair in pairs:
        #Run jsinspect with specific threshold. Request output to be at json form. Ignore files which cannot be read by jsinspect
        result = subprocess.run(["jsinspect", "-reporter", "json", "-t", "30", "--ignore", 'src/intro.js|src/outro.js',
          os.path.join(pair[0], "src"), os.path.join(pair[1], "src")], stdout=subprocess.PIPE, cwd=rootdir)
        out = json.loads(result.stdout)
        sim_n_code = 0
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
                    sim_n_code+=match["instances"][i]["lines"][1]-match["instances"][i]["lines"][0] + 1

        index1 = paths.index(pair[0])
        index2 = paths.index(pair[1])
        coverage=sim_n_code/(n_code[index1]+n_code[index2])
        data[index2][index1] = coverage
        print(pair[0], "#code:", n_code[index1], pair[0], "#code:", n_code[index2], "Pair #sim:", sim_n_code, 
        "Coverage:", coverage)

    for row in data:
        print (row)
    
    fig = px.imshow(data)

    '''
    fig = px.imshow(data,
                               x = ["put all jQuery version here"],
                               y = ["put all jQuery version here"],
                               color_continuous_scale=["white", "cyan", "lightgreen", "yellow", "red"]
                              )
    '''
    fig.show()
    
    
