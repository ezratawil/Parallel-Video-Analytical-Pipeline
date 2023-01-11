# Object Tracking using Lucas-Kanade Optical Flow
This project implements object tracking using the Lucas-Kanade Optical Flow algorithm in OpenCV.

# Algorithm
The Lucas-Kanade Optical Flow algorithm is a widely used method for tracking small motions in video sequences.
It uses the brightness of the pixels in an image to estimate the motion of the pixels between two consecutive frames. 
This algorithm first uses a pyramidal implementation of the Lucas-Kanade method to obtain an initial estimate of the motion at a coarse scale, 
and then refines this estimate using the iterative Lucas-Kanade method at a finer scale.
