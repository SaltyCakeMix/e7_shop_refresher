from pyautogui import *
import pyautogui
import time
import keyboard
import random
import os.path

# Fail-Safes
pyautogui.PAUSE = 0
# If you drag your mouse to the upper left will abort program
pyautogui.FAILSAFE = False
# Get screen res
window = pyautogui.size()
running = True

xposRandom = 50
yposRandom = 15
timeRandom = 0.1
clickDelay = 0.1

# Counter for each transaction to display at the end
covTotal = 0
mysticTotal = 0
refreshTotal = 0
printedStrings = []

def multiSearchCenter(name, conf):
    var = False
    iterator = 0
    while not var and os.path.exists(f'{name}{iterator}.PNG'):
        var = pyautogui.locateCenterOnScreen(f'{name}{iterator}.PNG', confidence=conf)
        iterator += 1
    return var

def multiSearch(name, conf):
    var = False
    iterator = 0
    while not var and os.path.exists(f'{name}{iterator}.PNG'):
        var = pyautogui.locateOnScreen(f'{name}{iterator}.PNG', confidence=conf)
        iterator += 1
    return var

def randomSleep(t):
    time.sleep(t * random.uniform(1 - timeRandom, 1 + timeRandom))
    
def loopCheck(str):
    global printedStrings

    iterator = 0
    pos = multiSearchCenter(str, 0.9)
    while pos is not None and iterator < 100:
        pyautogui.click(x=pos[0] + random.randrange(-xposRandom, xposRandom),
                        y=pos[1] + random.randrange(-yposRandom, yposRandom),
                        clicks=2, interval = clickDelay, button='left')
        pos = multiSearchCenter(str, 0.9)
        randomSleep(0.1)
        iterator += 1
    if iterator >= 100 or iterator == 0:
        printedStrings.append(f'Failed to find {str}')
        return False
    return True

def checkShop():
    global covBought
    global mysticBought
    global running
    
    # Checks for covenants
    if not covBought:
        covPos = multiSearchCenter('Covenant', 0.9)
        if covPos:
            global covTotal
            pyautogui.click(x=covPos[0] + 750 + random.randrange(-xposRandom, xposRandom),
                            y=covPos[1] + 55 + random.randrange(-yposRandom, yposRandom),
                            clicks=2, interval=clickDelay, button='left')

            if not loopCheck('CovenantConfirm'):
                running = False
                return
            covTotal += 1
            covBought = True
            randomSleep(0.1)
    
    # Checks for mystic
    if not mysticBought:
        mysticPos = multiSearchCenter('Mystic', 0.9)
        if mysticPos:
            global mysticTotal
            pyautogui.click(x=mysticPos[0] + 750 + random.randrange(-xposRandom, xposRandom),
                            y=mysticPos[1] + 55 + random.randrange(-yposRandom, yposRandom),
                            clicks=2, interval=clickDelay, button='left')
            
            if not loopCheck('MysticConfirm'):
                running = False
                return
            mysticTotal += 1
            mysticBought = True
            randomSleep(0.1)

## SETUP
# Search and go to BlueStacks
BSPos = multiSearchCenter('BlueStacks', 0.9)
if not BSPos:
    running = False
    printedStrings.append("-Cannot find BlueStacks running-")
else:
    pyautogui.click(x=BSPos[0], y=BSPos[1], button='left')
    time.sleep(0.1)

## MAIN
while running:
    covBought = False
    mysticBought = False
    
    # Check shop for things to buy
    checkShop()
    
    # Scroll downwards if anything else can be bought
    if not covBought or not mysticBought:
        pyautogui.moveTo(window[0]*0.6 + random.randrange(-xposRandom, xposRandom), window[1]/2 +
                         200 + random.randrange(-yposRandom, yposRandom), duration=0)
        # Drag upward 500 pixels in 0.2 seconds
        pyautogui.dragTo(window[0]*0.6 + random.randrange(-xposRandom, xposRandom), window[1]/2 -
                         200 + random.randrange(-yposRandom, yposRandom), duration=0.2)
        randomSleep(0.2)
        checkShop()

    # Refresh the shop
    if running:
        loopCheck('Refresh')
        loopCheck('Confirm')
        randomSleep(0.5)
        refreshTotal += 1
            
        if keyboard.is_pressed('q'):
            running = False
            printedStrings.append("-Exiting program-")

if BSPos:
    printedStrings.append(f'Covenant summons bought: {covTotal}')
    printedStrings.append(f'Mystic summons bought: {mysticTotal}')
    printedStrings.append(f'Refreshes done: {refreshTotal}')
    printedStrings.append(f'Skystones used: {refreshTotal * 3}')
    printedStrings.append(f'Gold used: {covTotal*184000 + mysticTotal*280000}')
    percent = round(100 / (refreshTotal * 3 / covTotal / 95) - 100, 2) if covTotal != 0 else 0
    printedStrings.append(f'Change in Covenant summons: {"+" if percent >= 0 else ""}{percent}%')

f = open("log.txt", "a")
for string in printedStrings:
    f.write(string + '\n')
    print(string)
f.write('\n')
f.close()