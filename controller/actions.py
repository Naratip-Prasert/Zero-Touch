import pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False


def move_cursor(x, y):
    pyautogui.moveTo(x, y)


def click():
    pyautogui.click()


def double_click():
    pyautogui.doubleClick()


def swipe_action(direction):
    SCROLL_AMOUNT = 400

    if direction == "down":
        pyautogui.scroll(-SCROLL_AMOUNT)

    elif direction == "up":
        pyautogui.scroll(SCROLL_AMOUNT)