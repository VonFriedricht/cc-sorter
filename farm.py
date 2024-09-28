import time
import pyautogui
import mouse
import imagehash
import cv2
from PIL import Image
import numpy as np
from math import floor
import json
import pynput


def print_mouse_position():
    stop_flag = False

    def on_press(key):
        nonlocal stop_flag
        try:
            if key.char == 'p':
                stop_flag = True
                return False  # Stop listener
        except AttributeError:
            pass

    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

    while not stop_flag:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})")
        time.sleep(0.1)  # Add a small delay to avoid excessive prints

    listener.stop()  # Make sure to stop the listener when done
    print("Stopped printing mouse position.")

def move_item(target):
    pyautogui.keyDown('shift')
    pyautogui.moveTo(target)
    mouse.click(button='left')
    time.sleep(0.1)
    pyautogui.keyUp('shift')

def init_movement():
    pyautogui.keyDown('s')
    time.sleep(0.1)
    pyautogui.keyDown('d')
    time.sleep(0.3)
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')

    pyautogui.keyDown('w')
    time.sleep(2)
    pyautogui.keyUp('w')
    
def interact():
    pyautogui.keyDown('e')
    time.sleep(0.2)
    pyautogui.keyUp('e')
    time.sleep(0.1)
    
def move(button):
    pyautogui.keyDown(button)
    time.sleep(.7)
    pyautogui.keyUp(button)
    time.sleep(0.1)
    
def init_take(target, slotpos=(744,305)):
    pyautogui.moveTo(target)
    interact()
    move_item(slotpos)
    interact()

def init_equip():
    init_take((1350,500))
    init_take((960,200))
    init_take((460,500))

def end_equip():
    init_take((1350,500), (560, 640))
    init_take((960,200), (640, 640))
    init_take((460,500), (740, 640))

def changeEq(eq_slot):
    pyautogui.keyDown(eq_slot)
    time.sleep(0.2)
    pyautogui.keyUp(eq_slot)
    time.sleep(0.1)
    
def action(position):
    pyautogui.moveTo(position)
    time.sleep(0.1)
    mouse.click(button='right')
    time.sleep(0.1)
    
def act_top_right():
    changeEq("2")
    action((925, 595))
    changeEq("3")
    action((950, 550))
    action((885, 550))
    action((885, 610))
    action((955, 610))
    
def act_top_left():
    changeEq("2")
    action((1000, 595))
    changeEq("3")
    action((950, 550))
    action((1030, 550))
    action((1030, 610))
    action((955, 610))

def act_bottom_left():
    changeEq("2")
    action((1000, 480))
    changeEq("3")
    action((950, 550))
    action((1030, 550))
    action((1030, 450))
    action((955, 450))

def act_bottom_right():
    changeEq("2")
    action((920, 490))
    changeEq("3")
    action((950, 550))
    action((885, 550))
    action((885, 450))
    action((955, 450))

def act_initial_chunk():
    changeEq("1")
    action((868, 649))
    act_top_right()
    move("a")
    act_top_left()    
    move("s")
    act_bottom_left()
    move("d")
    act_bottom_right()
    move("a")
    move("a")

def act_even_chunk():
    changeEq("1")
    action((1060, 440))
    act_bottom_left()
    move("w")
    act_top_left()
    move("d")
    act_top_right()
    move("s")
    act_bottom_right()
    move("w")
    move("a")
    move("a")
    
def act_odd_chunk():
    changeEq("1")
    action((1060, 640))
    changeEq("2")
    action((964, 500))
    act_top_left()
    move("s")
    act_bottom_left()
    move("d")
    act_bottom_right()
    move("w")
    act_top_right()
    move("s")
    move("a")
    move("a")

time.sleep(1)
#init_equip()
#init_movement()
act_initial_chunk()
for i in range(1,6):
    act_even_chunk()
    act_odd_chunk()
#end_equip()

#print_mouse_position()