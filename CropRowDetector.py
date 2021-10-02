import cv2
import numpy as np


# Helper Function to Draw Lines On Given Frame
def drawp(lines,frame):
	if lines is not None:
		for x1,y1,x2,y2 in lines[:,0,:]:
			# Avoids math error, and we can skip since we don't care about horizontal lines
			if x1 == x2:
				continue
			slope = (float(y2-y1))/(x2-x1)
			# Check if slope is sufficiently large, since we are interested in vertical lines
			if abs(slope)>1:
				cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),4)
	return frame

vid = cv2.VideoCapture("cropVid2.mp4")

if(vid.isOpened() == False):
	print("Error Opening Video File")

while(vid.isOpened()):
	ret, frame = vid.read()
	if ret == False:
		print("No More Frames Remaining")
		break
	# Convert to hsv format to allow for easier colour filtering
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_green = np.array([25,61,70])
	upper_green = np.array([55,190,177])
	# Filter image and allow only shades of green to pass
	mask = cv2.inRange(hsv, lower_green, upper_green)
	mask = cv2.GaussianBlur(mask,(5,5),2)

	# Perform dilation on mask
	# Dilation helps fill in gaps within a single row
	# In addition it helps blend rows that are far from the camera together
	# Hence, we get cleaner edges when we perform Canny edge detection
	kernel = np.ones((5,5),np.uint8)
	mask = cv2.dilate(mask,kernel,iterations=4)

	# Resize frame to smaller size to allow faster processing
	frame = cv2.resize(frame,(frame.shape[1]/4,frame.shape[0]/4))
	mask = cv2.resize(mask,(mask.shape[1]/4,mask.shape[0]/4))

	# Perform Canny Edge Detection
	edges = cv2.Canny(mask,100,200)

	# Perform Hough Lines Probabilistic Transform
	THRESHOLD = 30
	MIN_LINE_LENGTH = 25
	MAX_LINE_GAP = 10
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, THRESHOLD, np.array([]), MIN_LINE_LENGTH, maxLineGap=MAX_LINE_GAP)

	# Draw Detected Lines on the frame
	lineimg = drawp(lines,frame.copy())

	cv2.imshow('mask',mask)
	cv2.imshow('edges',edges)
	cv2.imshow('lineimg',lineimg)

	key = cv2.waitKey(25)
	# If Enter is pressed capture current frames
	if key == 13:
		# Save Current Frames and Exit
		cv2.imwrite('original.png',frame)
		res = cv2.bitwise_and(frame,frame, mask= mask)
		cv2.imwrite('colour_mask.png',mask)
		cv2.imwrite('colour_res.png',res)
		cv2.imwrite('edges.png',edges)
		cv2.imwrite('lineimg.png',lineimg)
	# Exit if Esc key is pressed
	if key == 27:
		break

vid.release()
cv2.destroyAllWindows()
