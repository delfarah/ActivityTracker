import pyautogui
try:
    c = 1
    while True:
        x, y = pyautogui.position()
        print(c)
        c = c+1;
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr)
        print('\b' * len(positionStr))
except KeyboardInterrupt:
    print('\n')
