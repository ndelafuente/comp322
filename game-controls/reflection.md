# Project 1 Reflection

## KEYBOARD
The keyboard controls worked very well for controlling Snake. They were fast and it was easy to remember which direction was
which. 

This control works the best with thinking through doing and performance. But because there is no visible feedback from the keys onto the screen, it may face some issues. However, the physical touch of the keys may be helpful to those who associate the controls with the directions.

## ALTERNATE KEYBOARD
Our alternate keyboard controls were very similar, as they shared the same shape as the arrow keys. So it was easy to
remember. On Nicholas' laptop, the arrow keys are half the size of the regular letter keys, so our alternate controls were much
easier to press because of that.

This works just as well as the normal WASD controls since it is the same principle but a different mapping of keys. This control does well with thinking through doing, performance (since it's fast). However, like the keyboard, there is no visible feedback on the screen (i.g. the cursor from the trackpad).

## TRACKPAD
The trackpad worked well enough. It was interesting in that you could dictate a new direction by only slightly moving the
finger in that direction. However, it also felt less precise in that if your finger moved slightly in a different direction
than what thou doth intended (perhaps you wished to move to the right, but your finger moved a bit up at the end), the input
might be interpreted in an undesirable way. In this way, it felt less reliable than the keys.

One place the track pad fell short in the five interaction rules is in performance. It fell short the bounding box of the screen prevented unlimited motion. However, it does well in Visibility and Thinking through Doing because the user can physically see on the screen where their cursor is.

## COLORED OBJECT
The colored object based movement was so cool. While we were implementing this feature, it was intersting to see the colors flipped and how the controls would react to other background noise. It was a bit difficult to get the color range that would capture the color we wanted so we had to play around to get a reasonable range. We ran into an issue because the bounds needed RGB but the directions showed HSV. Once we switched them, it worked fine. 

Because of how difficult it is for the code to pick up a color within the range, it would be difficult to use this control since there is a bit of lag. This control falls short in performance because of the lag. Furthermore, you have to move item in a linear steady motion for it to be detected accurately. 

## HAND RECOGNITION
Using the amount of fingers one was holding up as an input was just so much fun. Nicholas is one that struggles with hand
gestures however, and is very slow at forming them. This made controlling a game with them very difficult, especially with
Snake, where very fast reaction time can be necessary for controlling the snake as it nears the edge of its desmene.

We found this control to be quick and easy to control once you memorize the gestures however, if you have involuntary movements or if the program detects another finger, it might not do the direction you expected. There is no intuitive control that can be associated with the WASD keys. The hand recogniton control does well with thinking through doing and performance since our hand is attached to us but relies a lot on the user knowing the hand gestures.

## UNIQUE CONTROLS (GAMEPAD THUMBSTICK CONTROLS)
The gamepad thumbstick controls were very usable for Snake. It was intuitive and easy to remember to point the thumbstick in the
direction that I want the Snake to go. Our implementation of it meant that you have to hold down the thumbstick in that direction,
whereas pointing the thumbstick and then releasing it once the Snake was heading in your desired direction is perhaps a yet
more intuitive and convienent way to control our Snake fellow.

The thumbstick controls performance is great for snake because the controller is used as an extension of our bodies and doesn't require very complex motions of our hands. Because of this, the principle of thinking through doing works great as well.

