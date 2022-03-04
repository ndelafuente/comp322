'''
Authors: Nico de la Fuente, Sabrina Galban, Nicholas Wilder
Date: 3/3/2022

game_controls.py: Implementing different forms of game controls, including forms prescribed by the assignment, which
were alternate keyboard controls, trackpad controls, color-based motion tracking, finger-counting based controls.

Finally, we implemented a unique control method of our own choosing. We decided to go thumbstick control on 
a gamepad, implemented with the module pygame.
'''

from asyncio import sleep
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
    colorLower = (29, 86,  6)
    colorUpper = (64, 255, 255)

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    threshold = 40

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()


    while True:
        direction = last_dir

        frame = vs.read()
        
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width = 600)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Creating mask.
        frame = cv2.inRange(frame, colorLower, colorUpper)
        mask = cv2.erode(frame, None, iterations = 2)
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
                        direction = 'left'                      
                    else:
                        direction = 'right'                       
                else:
                    # Prioritize y movement
                    if dY < 0:
                        direction = 'up'
                    else:
                        direction = 'down'

                if direction != last_dir:
                    pyautogui.press(direction)
                    last_dir = direction
                    print(direction)

        # Show direction on screen.
        frame = cv2.putText(frame, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)

        # Update the frame and update the frames we have seen.
        cv2.imshow('Game Control Window', frame)
        cv2.waitKey(1)
        num_frames += 1


def finger_tracking():
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp
    global last_dir

    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    # getting hand detection from mediapipes and saving it to a variable
    # r_hand for right hand since we're only using the right hand.
    r_hand = mp.solutions.hands

    # providing information on accuracy to track hand
    hand = r_hand.Hands(static_image_mode = False,
        max_num_hands = 1,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5)

    # starting ability to draw and save to a variable.
    draw_hand = mp.solutions.drawing_utils 

    # copied over code from color tracking to frame, flip, resize, and convert to RGB    
    
    direction = ''
    while True:
        frame = vs.read()
            
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width = 600)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # using converted frame, get results from processed image and save these results
        framed_hand = hand.process(frame)

        # for loop to go through all multi_hand_landmarks
        frame_width = frame.shape[0]
        frame_height = frame.shape[1]

        major_hand_features = []
        num_fingers = 0

        if framed_hand.multi_hand_landmarks is not None:
            for right_hand in framed_hand.multi_hand_landmarks:
                for id, lm in enumerate(right_hand.landmark):
                    new_x = round(frame_width * lm.x)
                    new_y = round(frame_height * lm.y)
                    frame = cv2.circle(frame, (new_x, new_y), 6, (255,0,255), cv2.FILLED)

                    major_hand_features.append((id, new_x, new_y))


        if len(major_hand_features) > 0:
            if major_hand_features[4][1] < major_hand_features[3][1]:
                num_fingers += 1

            if major_hand_features[8][2] < major_hand_features[6][2]:
                num_fingers += 1
            
            if major_hand_features[12][2] < major_hand_features[10][2]:
                num_fingers += 1
            
            if major_hand_features[16][2] < major_hand_features[14][2]:
                num_fingers += 1
            
            if major_hand_features[20][2] < major_hand_features[18][2]:
                num_fingers += 1
        
        if num_fingers == 1:
            direction = "up"
        elif num_fingers == 2:
            direction = "left"
        elif num_fingers == 3:
            direction = "right"
        elif num_fingers == 5:
            direction = "down"

        if direction != last_dir:
            pyautogui.press(direction)
            last_dir = direction
            print(direction)
        
        frame = cv2.putText(frame,str(int(num_fingers)),(10,70),cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.imshow("Image", frame)
        cv2.waitKey(1)


def unique_control():
    # Our unique control will be using a gamepad to control a game, implemented with pygame.
    import pygame

    pygame.init()
    # Using the joystick.
    pygame.joystick.init()

    horizontal_axis_position = 0
    vertical_axis_position = 0

    controller_id = 0
    left_thumbstick_horizontal_axis_id = 0
    left_thumbstick_vertical_axis_id   = 1

    controller = pygame.joystick.Joystick(controller_id)
    controller.init()

    print(controller.get_name())

    axes = controller.get_numaxes()

    # Input loop.
    while True:

        # Handling events but not currently doing anything with them.
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                pass
                #print("Joystick moved.")
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Button released.")

        horizontal_axis_position = controller.get_axis(left_thumbstick_horizontal_axis_id)
        vertical_axis_position   = controller.get_axis(left_thumbstick_vertical_axis_id)

        # Axis output.
        if horizontal_axis_position != 0 or vertical_axis_position != 0:
            print(f"Horizontal axis position: {horizontal_axis_position}")
            print(f"Vertical axis position:   {vertical_axis_position}")

        global last_position
        global last_dir
        direction = ''

        thumbstick_rest_tolerance = .05
        jitter_threshold = .10

        # Go in the direction that is most being pointed towards with the thumbstick.
        if abs(horizontal_axis_position) > abs(vertical_axis_position):
            if horizontal_axis_position > 0 + thumbstick_rest_tolerance:
                direction = 'right'
            elif horizontal_axis_position < 0 - thumbstick_rest_tolerance:
                direction = 'left'
            else:
                
                direction = last_dir
        else:
            if vertical_axis_position > 0 + thumbstick_rest_tolerance:
                direction = 'down'
            elif vertical_axis_position < 0 - thumbstick_rest_tolerance:
                direction = 'up'
            else:
                
                direction = last_dir

        if direction != '':
            pyautogui.press(direction)
            print(direction)

        last_dir = direction

        # Pause for a bit.    
        pygame.time.delay(10)
            
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
