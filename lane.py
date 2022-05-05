import numpy as np
import cv2

def process(image):
    
    
    image_g = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    threshold_low = 50
    threshold_high = 200
    image_canny = cv2.Canny(image_g, threshold_low, threshold_high)
    
      
    vertices = np.array([[(205,1005),(400,570), (800,570),(1016,707)]], dtype=np.int32)   
    cropped_image = region_of_interest(image_canny,np.array([vertices],np.int32),)
    
    rho = 2           
    theta = np.pi/180   
    threshold = 10   
    min_line_len = 20
    max_line_gap = 20   

    lines = cv2.HoughLinesP(cropped_image, rho, theta, threshold, np.array([]),      minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_image = draw_the_lines (image,lines)
    return line_image

def region_of_interest(img, vertices):
        
    mask = np.zeros_like(img)   
    cv2.fillPoly(mask, vertices, 255)
    
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_the_lines(img, lines):

    if lines is not None:
       
    	img = np.copy(img)

    	line_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
   
    	for line in lines:
        	for x1,y1,x2,y2 in line:      
        		cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 20)
    

    	α = 1
    	β = 1
    	γ = 0    

    	img = cv2.addWeighted(img, α, line_image, β, γ)
    return img
	


    
   
cap = cv2.VideoCapture('./video.m4v')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
  
size = (frame_width, frame_height)
result= cv2.VideoWriter('./lines.avi', 
                         cv2.VideoWriter_fourcc(*'MPEG'),
                         20, size)


while cap.isOpened():
    ret, frame = cap.read()
    if(frame is not None):
      frame = process(frame)
      result.write(frame)
    
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
    else:
      break

cap.release()
cv2.destroyAllWindows()

