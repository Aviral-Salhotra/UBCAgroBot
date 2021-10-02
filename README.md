# Crop Row Detection
For AgroBot one of the main concern is the robot's navigation. The robot must autonomously navigate the crop rows and for this task we are taking a computer vision approach. The goal of this script is to efficiently detect crop rows on a video.

### Colour Filtering 
To accomplish this task, we need to first denoise the image. In particular, since we know we are looking for crops which are green in colour, we can filter based on colour. We convert our image to HSV format and define upper and lower bound for shades of green we capture. For example, here is an original frame from the video:  
![original](https://user-images.githubusercontent.com/24803574/76119649-c9720b80-5fe7-11ea-8bcd-c252435a0ed9.png)

Now, we use the upper and lower bounds on our green colour to generate a mask. This is the resulting mask:  
![colour_mask_orig](https://user-images.githubusercontent.com/24803574/76119665-cf67ec80-5fe7-11ea-8c1f-2648eafdb0ac.png)

By using bitwise _and_ operator we see that this mask does correspond to the green regions of our image:  
![colour_res](https://user-images.githubusercontent.com/24803574/76119675-d42ca080-5fe7-11ea-8fdf-d7717e21d24b.png)

### Denoising and Smoothing
Next, we need to denoise the resulting mask (which is a binary image contains the crop rows). To do this, we perform gaussian blurring following by multiple iterations of dilation. Here is the resulting mask after dilation:  
![colour_mask](https://user-images.githubusercontent.com/24803574/76120133-c1669b80-5fe8-11ea-817d-6deae99e3d27.png)

The reason we use dilation is because we want to fill the gaps in the mask to get a cleaner representation of our rows and also we want rows that are far from the camera to be merged into one. This is because these rows are not relevant to our navigation system and by merging them, we can avoid detecting them in our edge and line detection in subsequent steps.

### Line Detection
Although, the mask image is a binary image and it can be used directly with Hough transform, the large number of points in the image lead to noisy and slow computation. Hence, Canny edge detection was used to first decrease the number of points in image. The following image shows the results of the edge detection:  
![edges](https://user-images.githubusercontent.com/24803574/76120380-45208800-5fe9-11ea-9148-a26522ea4417.png)

Following this, we used Hough lines transform. We used the probabilistic version implemented in openCV due to faster compute time and also the ability to specify parameters such as _minimum line length_ and _maximum line gap_. The following image shows the resulting lines we detected.  
![lineimg](https://user-images.githubusercontent.com/24803574/76120640-d132af80-5fe9-11ea-9db2-9124b5167203.png)

### How does this fit in with the rest of the system?
We are currently using these lines and calculating their intersection which occurs at **vanishing point**. Then we are using a PID controller to minimimize the distance of this vanishing point from the center of our frame. Using this method, we are able to centre our chassis over the crop rows we are traversing.

  
