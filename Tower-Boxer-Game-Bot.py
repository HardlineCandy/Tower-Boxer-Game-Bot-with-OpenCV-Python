import cv2
import numpy as np
import keyboard
import time
from PIL import Image
from mss import mss

# https://pythonmana.com/2021/04/20210413180602497y.html
# https://gist.github.com/chriskiehl/2906125
import win32api
import win32con

left_arrow_button = 0x25
right_arrow_button = 0x27

#############################
screen_resolution_x = 1920
screen_resolution_y = 1080

game_screen_left_border = 770  
game_screen_right_border = 1160
game_screen_top_border = 100 
game_screen_bottom_border = 840 

top = game_screen_top_border
left = game_screen_left_border
width = game_screen_right_border - game_screen_left_border
height = game_screen_bottom_border - game_screen_top_border
game_region = {'top': top, 'left': left, 'width': width, 'height': height}

# istenen bölgenin ekran görüntüsünü al ve o ekran görüntüsünü
# içeren numpy dizisini döndür.
def take_ss(region):
    sct = mss()
    im = sct.grab(region)
    img = Image.frombytes('RGB', im.size, im.rgb)
    img_array = np.array(img)

    return img_array

def find_object(big_img, small_img):
    result = cv2.matchTemplate(big_img, small_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.93

    y, x = np.where( result >= threshold)
    
    return y, x

def press_button(button):
    win32api.keybd_event(button, 0,0,0)
    time.sleep(0.01)
    win32api.keybd_event(button, 0 ,win32con.KEYEVENTF_KEYUP ,0)


# esc tuşuna basıldığında programın kapatılması için
# bir fonksiyon tanımlanıp esc tuşuna kısayol atanması.
run = 1


def exit():
    global run
    run = 0


keyboard.add_hotkey("esc", exit)

#yazılım çalıştıktan sonra oyunu açmak için süre
time.sleep(3)

boksor_loc = 1 # 0: sol , 1: sag

#oyundan alınan ekran görüntüsü içerisinde
#boksorün konumu. tüm ekrandaki değil.
boksor_y_loc = 560

left_obstacle_img = cv2.imread('obstacle_left.png')
left_obstacle_img = cv2.cvtColor(left_obstacle_img, cv2.COLOR_BGR2RGB)

right_obstacle_img = cv2.imread('obstacle_right.png')
right_obstacle_img = cv2.cvtColor(right_obstacle_img, cv2.COLOR_BGR2RGB)

i = 0
a = 0
distance_tresh = 200
while run:
    button_pressed = 0
    
    game_img = take_ss(game_region)

    if boksor_loc == 1:
        right_obs_y, right_obs_x = find_object(game_img,right_obstacle_img)
        
        i = 0
        while i < len(right_obs_y):
            if boksor_y_loc - right_obs_y[i] < distance_tresh:
                press_button(left_arrow_button)
                boksor_loc = 0
                button_pressed = 1
                i = len(right_obs_y) #break
            i += 1
            
        if button_pressed == 0:
            press_button(right_arrow_button)

    else:
        left_obs_y, left_obs_x = find_object(game_img,left_obstacle_img)
        
        i = 0
        while i < len(left_obs_y):
            if boksor_y_loc - left_obs_y[i] < distance_tresh:
                press_button(right_arrow_button)
                boksor_loc = 1
                button_pressed = 1
                i = len(left_obs_y) #break
            i += 1
            
        if button_pressed == 0:
            press_button(left_arrow_button)

