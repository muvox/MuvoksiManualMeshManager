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
    rowCounter = 0
    buttonRow = []
    buttonGrid = [[]]
    frameHeaderStore = []
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

            # Generate headers for grid frames
            frameHeaderRow.append(str(x)+str(y))
            # frameHeaderRow.append(colKey)

            # Add input fields key value into store for later iterations
            keyRow.append(colKey)

            # Add buttongroup to the row of buttons
            buttonRow.append(buttonGroup)

        # Add the row of input keys into another list for multidimensional
        # iterations
        frameHeaderStore.append(frameHeaderRow)
        keyStore.append(keyRow)
        rowCounter = rowCounter + 1
        buttonGrid.append(buttonRow)
        buttonRow = []
        keyRow = []
        colKey = []

    grid = ([sg.Frame(yy, y) for y, yy in zip(x, xx)] for x, xx in zip(buttonGrid, frameHeaderStore))
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
        [sg.Frame('', gridFrame, key='-GRID-')]
    ]
    col3 = [
        [sg.Text('Output commands', size=(60, 1))],
        [sg.Multiline('', size=(60, 40), key='-OUT-')]
    ]
    layout = [[
        sg.Col(col1),
        sg.Col(col2),
        sg.Col(col3)
    ]]

    return layout

def gridController(window, values, event):
    coordinate = event[:2]
    valueString = coordinate+"input"
    currentValue = float(values[valueString])
    print(currentValue)
    if "plusplus" in event:
        updatedValue = currentValue+0.1
    elif "plus" in event:
        updatedValue = currentValue+0.01
    elif "minusminus" in event:
        updatedValue = currentValue-0.1
    elif "minu" in event:
        updatedValue = currentValue-0.01

    fixedValue = round(updatedValue,2)
    print("{}".format(currentValue, '.5f'))

    # TODO: If value positive, add plus sign
    window[valueString].update(fixedValue)


# Create an event loop
def main():
    global keyStore
    global defaultMeshInput
    defaultGrid = mmmm.readInputToMeshGrid(defaultMeshInput)
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
            # print(keyStore)
            # for x, row in enumerate(keyStore):
            #     for y, col in enumerate(row):
            #         # print(col)
            #         window[col].update(newInput[x][y])
            # close old window
            newGrid = mmmm.readInputToMeshGrid(values['-IN-'])
            print('wokrs2')
            layout = layoutBuilder(newGrid, values['-IN-'])
            window1 = sg.Window("Demo", layout, default_element_size=(10, 10))
            window.Close()
            window = window1


        if "plus" or "minus" in event:
            gridController(window, values, event)

    window.close()


if __name__ == '__main__':
    main()
