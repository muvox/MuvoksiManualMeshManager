# hello_psg.py
import PySimpleGUI as sg
import meshManager as mmmm

defaultMeshInput = '''
0        1        2        3        4
0 -0.16000 +0.16000 +0.20000 -0.20000 -0.25000
1 -0.25000 -0.19000 -0.18000 -0.20000 -0.28000
2 -0.18000 -0.20000 -0.28000 -0.24000 -0.25000
3 -0.20000 +0.22000 -0.25000 -0.30000 -0.28000
4 -0.26000 -0.25000 -0.34000 -0.28000 +0.35000
'''

gridMesh = []
gridRow = []
keyRow = []
keyStore = []


def gridBuilder(mesh):
    keyRow = []
    global keyStore
    keyStore = []
    keyCounter = 0
    buttonRow = []
    buttonGrid = [[]]
    frameHeaderStore = [[]]
    frameHeaderRow = []

    for x, row in enumerate(mesh):
        for y, col in enumerate(row):
            keyString = str(x)+str(y)+str('plus')
            button1 = sg.Button('+0.01', key=keyString)
            keyCounter = keyCounter+1

            keyString = str(x)+str(y)+str('plusplus')
            button2 = sg.Button('+0.1', key=keyString)
            keyCounter = keyCounter+1

            keyString = str(x)+str(y)+str('minusminus')
            button3 = sg.Button('-0.1', key=keyString)
            keyCounter = keyCounter+1

            keyString = str(x)+str(y)+str('minus')
            button4 = sg.Button('-0,01', key=keyString)
            keyCounter = keyCounter+1

            colKey = str(x)+str(y)+'input'
            buttonGroup = [
                [button1, button2],
                [sg.In(col.format('.5f'), key=colKey)],
                [button4, button3]
                ]

            headerString = str(x)+str(y)
            # print(headerString)
            # Generate headers for grid frames
            # frameHeaderRow.append(headerString)
            frameHeaderRow.append(headerString)

            # Add input fields key value into store for later iterations
            keyRow.append(colKey)

            # Add buttongroup to the row of buttons
            buttonRow.append(buttonGroup)

        # Add the row of input keys into another list for multidimensional
        # iterations
        frameHeaderStore.append(frameHeaderRow)
        frameHeaderRow = []
        keyStore.append(keyRow)
        buttonGrid.append(buttonRow)
        buttonRow = []
        keyRow = []
        colKey = []

    # Create frame for each of the element groups
    grid = ([sg.Frame(yy, y) for y, yy in zip(x, xx)]
            for x, xx in zip(buttonGrid, frameHeaderStore))
    # grid = ([sg.Frame('', y) for y in x] for x in buttonGrid)

    return grid


def layoutBuilder(newGrid, meshInput):
    gridFrame = gridBuilder(newGrid)
    col1 = [
        [sg.Text('1. Enter mesh')],
        [sg.Multiline(meshInput, size=(60, 40), key='-IN-',
                      enter_submits=True)],
        [sg.Button('Submit')]
        ]
    col2 = [
        [sg.Text('2. Edit mesh')],
        [sg.Frame('', gridFrame, key='-GRID-')],
        [sg.Button('Export')]
    ]
    col3 = [
        [sg.Text('Output commands', size=(60, 1))],
        [sg.Multiline('', size=(60, 40), key='-OUT-', do_not_clear=True)]
    ]
    layout = [[
        sg.Col(col1),
        sg.Col(col2),
        sg.Col(col3)
    ]]

    return layout

def gridController(window, values, event):
    coordinate = event[:2]
    # print(coordinate)
    coordinateString = coordinate+"input"
    # print(coordinateString)
    currentValue = float(values[coordinateString])
    # print(currentValue)
    if "plusplus" in event:
        updatedValue = currentValue+0.1
    elif "plus" in event:
        updatedValue = currentValue+0.01
    elif "minusminus" in event:
        updatedValue = currentValue-0.1
    elif "minu" in event:
        updatedValue = currentValue-0.01

    fixedValue = round(updatedValue, 2)

    # Make sure the value has a plus sign if its greater than or equal to zero
    # Also make sure that the value has right amount of zeroe's
    if fixedValue >= 0:
        updatedString = '+'+str(fixedValue)
        while len(updatedString) < 8:
            updatedString = updatedString+'0'
        print(updatedString)
    else:
        updatedString = str(fixedValue)
        while len(updatedString) < 8:
            updatedString = updatedString+'0'

    window[coordinateString].update(updatedString)

def outputBuilder(window, values, keystore):
    for x, row in enumerate(keystore):
        for y, col in enumerate(row):
            coordinateString = str(keyStore[y][x])[0:2]
            fixedString = "G29 S3 I"+coordinateString[0:1]+" J"+coordinateString[1:2]+' Z'+values[col]
            window['-OUT-'].update(fixedString+'\n', append=True)


# Create an event loop
def main():
    global keyStore
    global defaultMeshInput
    global gridMesh
    defaultGrid = mmmm.readInputToMeshGrid(defaultMeshInput)
    print(defaultGrid)
    layout = layoutBuilder(defaultGrid, defaultMeshInput)
    window = sg.Window("Demo", layout, default_element_size=(10, 10))

    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            newInput = mmmm.readInputToMeshGrid(values['-IN-'])
            newGrid = mmmm.readInputToMeshGrid(values['-IN-'])
            layout = layoutBuilder(newGrid, values['-IN-'])
            window1 = sg.Window("Demo", layout, default_element_size=(10, 10))
            window.Close()
            window = window1
        elif "plus" in event or "minus" in event:
            # print(event)
            gridController(window, values, event)
        elif event == 'Export':
            outputBuilder(window, values, keyStore)
    window.close()


if __name__ == '__main__':
    main()
