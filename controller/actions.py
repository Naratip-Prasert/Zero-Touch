import pyautogui

def move_cursor(x, y):
    pyautogui.moveTo(x, y)

def click():
    pyautogui.click()

def double_click():
    pyautogui.doubleClick()

def swipe_action(direction):
    if direction == "down":
        pyautogui.scroll(-500)
        # ถ้าจะใช้กับ TikTok/Shorts เปลี่ยนเป็น:
        # pyautogui.press("down")

    elif direction == "up":
        pyautogui.scroll(500)
        # ถ้าจะใช้กับ TikTok/Shorts เปลี่ยนเป็น:
        # pyautogui.press("up")