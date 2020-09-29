import io
input_mesh_array = []



def main():
    meshPositionString = ""
    counter = 1
    cacheMesh = readFile("mesh.txt")
    for array in cacheMesh:
        while(" " in array):
            array.remove(" ")

    print(input_mesh_array)
    for i in range(len(cacheMesh)):
        for j in range(len(cacheMesh[i])):
            meshPositionString = gcodeBuilder(j, i, input_mesh_array[i][j])
            print(meshPositionString)
            counter = counter+1
            # print(counter)
        counter = counter + 1

def readInputToMeshGrid(meshInput):
    formattedMesh = []
    lineSplitMesh = meshInput.splitlines()
    for line in lineSplitMesh:
        if not line:
            continue
        if (line.replace(" ", "").replace("\n", "").isnumeric()):
            continue
        if line[:1].isnumeric():
            line = line[1:]

        # remove newline characters
        formattedLine = cleanLine(line.replace("\n", ""))

        # split by whitespaces
        formattedMesh.append(formattedLine[0].split())
    # print(formattedMesh)
    return formattedMesh


def gcodeBuilder(x, y, z):
    gcode = "G29 S3 I{} J{} Z{}".format(x, y, z)
    return gcode


def readFile(filename):
    with open(filename) as my_file:
        for line in my_file:

            # Skip extra number lines from top
            if (line.replace(" ", "").replace("\n", "").isnumeric()):
                continue

            # remove extra numbers from the front of the line
            if line[:1].isnumeric():
                line = line[1:]

            # remove newline characters
            formattedLine = cleanLine(line.replace("\n", ""))

            # split by whitespaces
            input_mesh_array.append(formattedLine[0].split())

    my_file.close()
    # print(input_mesh_array)
    return input_mesh_array


# cleanns a line
def cleanLine(s):
    sep = "([+-])"
    p = chr(ord(max(s))+1)
    s = s.replace(sep, p+sep).split(p)
    return s

# if __name__ == '__main__':
    # main()
