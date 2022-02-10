from cv2 import threshold
import pyautogui



last_position = (None,None)
last_dir = ''

def keypress():
    ''' 
    Choose any four keys that a user can press to control the game.
    Update this doc string with your choices. 
    '''

    import keyboard
    while True:
        if keyboard.is_pressed('j'):
            pyautogui.press('left')
            print('left')
        if keyboard.is_pressed('l'):
            pyautogui.press('right')
            print('right')
        if keyboard.is_pressed('i'):
            pyautogui.press('up')
            print('up')
        if keyboard.is_pressed('k'):
            pyautogui.press('down')
            print('down')


def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        global last_position
        global last_dir

        threshold = 20

        (old_x, old_y) = last_position
        if old_x is None or old_y is None:
            last_position = (x, y)
        else:
            # Find difference between previous and current position
            x_diff = x - old_x
            y_diff = y - old_y

            if abs(x_diff) > threshold or abs(y_diff) > threshold:
                # Try to use the values as directional input
                if abs(x_diff) > abs(y_diff):
                    # Prioritize x movement
                    if x_diff < 0:
                        pyautogui.press('left')
                        print(f'{last_position} x_diff {x_diff}, left')
                    else:
                        pyautogui.press('right')
                        print(f'{last_position} x_diff {x_diff}, right')
                else:
                    # Prioritize y movement
                    if y_diff < 0:
                        pyautogui.press('up')
                        print(f'{last_position} y_diff {x_diff}, up')
                    else:
                        pyautogui.press('right')
                        print(f'{last_position} y_diff {x_diff}, down')
            
                last_position = (x, y)


    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = None
    colorUpper = None

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()


    while True:
        # your code here
        continue
        



def finger_tracking():
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    # put your code here


def unique_control():
    # put your code here
    pass

def main():
    control_mode = input("How would you like to control the game? ")
    if control_mode == '1':
        keypress()
    elif control_mode == '2':
        trackpad_mouse()
    elif control_mode == '3':
        color_tracker()
    elif control_mode == '4':
        finger_tracking()
    elif control_mode == '5':
        unique_control()

if __name__ == '__main__':
	main()
