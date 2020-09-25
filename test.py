# Array for a 5 by 5 mesh
inputMesh = [["-0.16000", "-0.16000", "-0.20000", "-0.20000", "-0.25000"],
             ["-0.25000", "-0.19000", "-0.18000", "-0.20000", "-0.28000"],
             ["-0.18000", "-0.20000", "-0.28000", "-0.24000", "-0.25000"],
             ["-0.20000", "-0.22000", "-0.25000", "-0.30000", "-0.28000"],
             ["-0.26000", "-0.25000", "-0.34000", "-0.28000", "-0.35000"]]
meshPositionString = ""
convertedGcode = []
errorString = "01234"
input_mesh_array = []


def main():
    meshPositionString = ""
    counter = 1
    cacheMesh = readFile("mesh.txt")
    for array in cacheMesh:
        while(" " in array):
            array.remove(" ")

    for i in range(len(cacheMesh)):
        for j in range(len(cacheMesh[i])):
            meshPositionString = gcodeBuilder(j, i, inputMesh[i][j])
            print(meshPositionString)
            counter = counter+1
    # counter = 1
    # for i in range(len(inputMesh)):
    #     for j in range(len(inputMesh[i])):
    #         meshPositionString = gcodeBuilder(i, j, inputMesh[i][j])
    #         print(meshPositionString)
    #         print(counter)
    #         counter = counter + 1


def gcodeBuilder(x, y, z):
    gcode = "G29 S3 I{} J{} Z{}".format(x, y, z)
    return gcode


def readFile(filename):
    with open(filename) as my_file:
        for line in my_file:
            formattedLine = line.replace(" ", "")
            if(formattedLine == "01\n" or formattedLine == "012\n"
               or formattedLine == "0123\n" or formattedLine == "01234\n"):
                print("First line is bs")
                continue
            else:
                superFormatted = splitAndKeep(line[1:].replace("\n", ""))
                input_mesh_array.append(superFormatted)
            #  input_mesh_array.append(line)
            #  print(line)
    my_file.close()
    return input_mesh_array


def splitAndKeep(s):
    sep = "-"
    p = chr(ord(max(s))+1)
    return s.replace(sep, p+sep).split(p)


if __name__ == "__main__":
    main()
