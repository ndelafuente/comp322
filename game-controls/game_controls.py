from cv2 import threshold
import pyautogui



last_position = (None,None)
last_dir = ''

def keypress():
    ''' 
    The new keys a user can press to play the game:

    j = left
    l = right
    i = up
    k = down
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



        threshold = 50

        (old_x, old_y) = last_position
        if old_x is None or old_y is None:
            last_position = (x, y)
        else:
            # Find difference between previous and current position
            x_diff = x - old_x
            y_diff = y - old_y

            if abs(x_diff) > threshold or abs(y_diff) > threshold:

                dir = last_dir
                # Try to use the values as directional input
                if abs(x_diff) > abs(y_diff):
                    # Prioritize x movement
                    if x_diff < 0:
                        dir = 'left'
                        
                    else:
                        dir = 'right'
                else:
                    # Prioritize y movement
                    if y_diff < 0:
                        dir = 'up'

                    else:
                        dir = 'down'
                
                if dir != last_dir:
                    pyautogui.press(dir)
                    print(dir)
                last_position = (x, y)
                last_dir = dir 


    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range.
    # Using red-colored notebook as object.
    colorLower = (0, 44,  100)
    colorUpper = (0, 100, 100)

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    threshold = 20

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()


    while True:
        # Team code here.
        frame = vs.read()
        cv2.flip(frame, 1)
        imutils.resize(frame, width = 600)
        cv2.GaussianBlur(frame, (5, 5), 0)
        cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Creating mask.
        mask = cv2.inRange(frame, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)

        # Find contours. Only need the first item in the returned findContours() tuple.
        contoursTuple = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        list = contoursTuple[0]
        
        # Find the center of the object.
        # Do only if we've found any contours.
        if len(list) > 0:
            center = None
            maxContour = max(list, key = cv2.contourArea)

            # Check if the largest contour is large enough to be our object.
            minEnclosingCircleTuple = cv2.minEnclosingCircle(maxContour)
            largestContourRadius = minEnclosingCircleTuple[1]

            if(largestContourRadius > 10):
                M = cv2.moments(maxContour)
                center = (int (M['m10'] / M['m00']), int (M['m01'] / M['m00']))

                pts.appendleft(center)

        # Now find the direction.
        if num_frames >= 10 and len(pts) >= 10:
            (dX, dY) = (pts[0][0] - pts[9][0], pts[0][1] - pts[9][1])
            

            # Use threshold to decide if difference is large enough.
            if abs(dX) > threshold or abs(dY) > threshold:
                # Try to use the values as directional input
                if abs(dX) > abs(dY):
                    # Prioritize x movement
                    if dX < 0:
                        pyautogui.press('left')
                        print(f'dX {dX}, left')
                    else:
                        pyautogui.press('right')
                        print(f'dX {dX}, right')
                else:
                    # Prioritize y movement
                    if dY < 0:
                        pyautogui.press('up')
                        print(f'dY {dY}, up')
                    else:
                        pyautogui.press('down')
                        print(f'dY {dY}, down')
        # Show direction on screen.
        cv2.putText(frame, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)



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
