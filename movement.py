import time
import pyautogui
import mouse
import imagehash
import cv2
from PIL import Image
import numpy as np
from math import floor
import json

kisten_grid = [
    (704, 276), (792, 276), (880, 276), (968, 276), (1056, 276), (1144, 276),
    (704, 364), (792, 364), (880, 364), (968, 364), (1056, 364), (1144, 364),
    (704, 452), (792, 452), (880, 452), (968, 452), (1056, 452), (1144, 452)
]
inventar_grid = [
    (528, 592), (616, 592), (704, 592), (792, 592), (880, 592), (968, 592),
    (1056, 592), (1144, 592), (1232, 592), (1320, 592),
    (528, 696), (616, 696), (704, 696), (792, 696), (880, 696), (968, 696),
    (1056, 696), (1144, 696), (1232, 696), (1320, 696),
    (528, 784), (616, 784), (704, 784), (792, 784), (880, 784), (968, 784),
    (1056, 784), (1144, 784), (1232, 784), (1320, 784)
]

chests = [

[],[],[
"e9929c99d2736465",
"e9929c99d2736564",
"e893948ec3d8256f",
"bbd4c80fa13a27c9",
"bbd4c90fe43231d8",
"b4cb9b4c333147c3",
"b8cba6794896c96a",
"e6ccb2c989339966",
"e9d0819fd21f994a",
"eb968dda92214c73",
],

[],[],[ # saat und garten
"e19e9c69b38a986c",
"e19e94616f8c9a33",
"e59b926c639896c9",
"e5931c69a69ad30d",
"b4c3946db2e71a91",
"eb84e41a83f89e63",
"b9c79a6c33669891",
"ea95981e66989b2d",
],

[],[],[ # essen
"fea5a086d0de89ca",
"e894c39ee33a386c",
"ee84d30b5a25b966",
"fea09597969a5960",
"e897c5d072392f4c",
"bac1e4169acbcb07",
"eac4b5d69832678c",
"eae0a59696d89b98",
],[
"bf85dac16127321e",
"f8959e8768363929",
"e897879ab2692569",
"b9c6cb998c647326",
"e8959a5ecd193ac4",
"adb0d0c99793cc99",
"ebc0951a70636ecd",
"ed9ee21c4b863863",
],

[],[ # eq
"b364cf9893966465",
"bac4cfcfa1b06330",
"e699999939cc61c6",
"b364cf9999c03867",
"bc9319cc2ec666c3",
"b1cc933266339ccd",
],[
"b3cc9b996c993246",
"e99693667961269c",
"e885979e9a4a3d49",
"b6cfcb398c244ce2",
"b364cf9893963465",
"b34ccccecd936630",
"b4d19dc607c713cc",
],

[],[ # rüstung und kleidung
"bee6d8cb39989809",
"bdd3c84e394c3463",
"ea85d38fd023a696",
"bcc2c8333c3cd4cb",
"ec8493dbcc4c711b",
"e885979ea1657a68",
],[
"bdc0969e1a33316d",
"ed91ce9cc94e344c",
"e9979e6069369748",
"eeb17bc39c0c48e1",
"eac18f9a9c4b7924",
],

[],[
"fa9591d8d36446a6",
"fb9591c4c6f00ec6",
"e493cf3924cc33c5",
"bdd0cb0f33f0283c",
"bfd0c0c3cf4c2c35",
"bcc2cb8d26f03366",
],

[ # blöcke
"bfd2b5878794c209",
"bed0948787965ae4",
"fac43b878592cc33",
"afd0b5c385568768",
"fae596879098c7c2",
"fad09587c696cc62",
"ebb4c396c6c396c0",
"ead0a583879fca70",
],

[ # boden
"fe93848cb18cc5b5",
"ff80d4a181d8b7d4",
],

[ # pet
"ec9093cfccc939b0",
"b4d3cfc64ccc3035",
"b4d39b666ccc3429",
],

[ # pinsel
"b192c92ce6196ff0",
"b992c92cc6392ff0",
"b9d0c52e66393be0",
],

[ # toolbenches
"afc5e0cfe1c390b0",
"ee83d187c4b8eca8",
"ee908d91c6586f39",
"fe85d0782f4e91c2",
"abf420f0c38dd78c",
"ffa187c0dcc202de",
"aeadd17cd480c3d2",
"ee94b185d4c5d4d1",
"eed0fdd4b0c58189",
],

[ # Grünes Hemd und Pilz Helm
"acc3d01333fc6dc4",
"e8859e98493f6437", 
]

]

known_hashes = set()
for chest in chests:
    known_hashes.update(chest)

def move_down():
    pyautogui.keyDown('s')
    time.sleep(0.2)
    pyautogui.keyUp('s')

def move_up():
    pyautogui.keyDown('w')
    time.sleep(0.2)
    pyautogui.keyUp('w')

def interact():
    pyautogui.keyDown('e')
    time.sleep(0.2)
    pyautogui.keyUp('e')
    time.sleep(0.1)

def move_down_layer():
    pyautogui.keyDown('d')
    time.sleep(0.1)
    pyautogui.keyDown('w')
    time.sleep(0.3)
    pyautogui.keyUp('w')
    pyautogui.keyUp('d')

def move_up_layer():
    pyautogui.keyDown('a')
    time.sleep(0.1)
    pyautogui.keyDown('w')
    time.sleep(0.3)
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')

def click_sort_button():
    mouse.move(1280, 400, absolute=True)
    mouse.click(button='left')
    time.sleep(0.5)

def move_from_to(a,b):
    set_mouse_position(b)
    layer_a = floor(a/3)
    layer_b = floor(b/3)
    chest_a = a%3
    chest_b = b%3

    while layer_a != layer_b:
        if layer_a != layer_b and chest_a < 2:
            chest_a = 2
            move_down()

        if layer_a > layer_b:
            move_down_layer()
            chest_a = 0
            layer_a -= 1
        else:
            move_up_layer()
            chest_a = 0
            layer_a += 1

    if chest_a == 2 and chest_b < 2:
        move_up()

    if chest_b == 2 and chest_a < 2:
        move_down()

def set_mouse_position(kiste):
    modulo = kiste%3
    if modulo == 0:
        pyautogui.moveTo(960, 100)
    elif modulo == 1:
        pyautogui.moveTo(1080, 540)
    elif modulo == 2:
        pyautogui.moveTo(960, 900)

def remove_brown_background(image):
    image_array = np.array(image)
    brown_tones = [
        [48, 33, 12],
        [49, 34, 17],
        [48, 32, 12],
        [49, 32, 12],
    ]
    tolerance = 20
    for tone in brown_tones:
        lower_bound = np.array([max(0, t - tolerance) for t in tone])
        upper_bound = np.array([min(255, t + tolerance) for t in tone])
        mask = cv2.inRange(image_array, lower_bound, upper_bound)
        image_array[mask != 0] = [255, 255, 255]  # Ersetze mit Weiß
    return Image.fromarray(image_array)

def move_item_to_slot(target):
    pyautogui.keyDown('shift')
    pyautogui.moveTo(target)
    mouse.click(button='left')
    time.sleep(0.1)
    pyautogui.keyUp('shift')


def screenshot(current_chest_index):
    screenshot = pyautogui.screenshot()

    kis_hashes, kis_empty_slots = screen_scan(screenshot, kisten_grid)
    inv_hashes, inv_empty_slots = screen_scan(screenshot, inventar_grid)

    print("Kisten-Hashes:", kis_hashes)
    print("Inventar-Hashes:", inv_hashes)

    if current_chest_index < len(chests) and chests[current_chest_index]:
        current_chest_hashes = chests[current_chest_index]
        is_alles_ablage = False
    else:
        current_chest_hashes = []
        is_alles_ablage = True

    print(is_alles_ablage)
    if is_alles_ablage:
        # Verschiebe Items aus Kiste in Inventar
        for i, kis_hash in enumerate(kis_hashes):
            if inv_empty_slots > 0 and kis_hash in known_hashes and kis_hash != "8000000000000000":
                move_item_to_slot(kisten_grid[i])
                kis_empty_slots += 1
                inv_empty_slots -= 1
                
        # Verschiebe Items aus Inventar in Kiste
        for j, inv_hash in enumerate(inv_hashes):
            if kis_empty_slots > 0 and inv_hash not in known_hashes and inv_hash != "8000000000000000":
                move_item_to_slot(inventar_grid[j])
                kis_empty_slots -= 1
                inv_empty_slots += 1
    else:
        for i, kis_hash in enumerate(kis_hashes):
            if inv_empty_slots > 0 and kis_hash not in current_chest_hashes and kis_hash != "8000000000000000":
                move_item_to_slot(kisten_grid[i])
                kis_empty_slots += 1
                inv_empty_slots -= 1
        for j, inv_hash in enumerate(inv_hashes):
            if kis_empty_slots > 0 and inv_hash in current_chest_hashes and inv_hash != "8000000000000000":
                move_item_to_slot(inventar_grid[j])
                kis_empty_slots -= 1
                inv_empty_slots += 1

    
    
def screen_scan(screenshot, grid):
    empty_slots = 0
    item_width = 72
    item_height = 48
    hashes = []
    for slot in grid:
        x = slot[0]
        y = slot[1]
        box = (x, y, x+item_width, y+item_height)
        region = screenshot.crop(box)
        processed_image = remove_brown_background(region)
        slot_hash = str(imagehash.phash(processed_image))
        hashes.append(slot_hash)
        if slot_hash == "8000000000000000":
            empty_slots += 1
        elif True or slot_hash not in known_hashes:
            unknown_image_filename = f"static/images/{slot_hash}.png"
            processed_image.save(unknown_image_filename)
    return hashes, empty_slots

def reload():
    if True:
        with open('chests.json', 'r') as f:
            chests = json.load(f)

time.sleep(1)
current = 0
layers = 10
while True:
    for i in range(0, layers*3):
        move_from_to(current, i)
        current = i
        interact()
        click_sort_button()
        reload()
        screenshot(current)
        interact()

    for i in range(layers*3 - 1, -1, -1):
        move_from_to(current, i)
        current = i
        interact()
        click_sort_button()
        reload()
        screenshot(current)
        interact()
        
    time.sleep(10)