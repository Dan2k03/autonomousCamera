
import cv2 

#THIS CODE IS BEING IMPLEMENTED FOR STOP SIGNS CURRENTLY IF THERE ARE ANY OTHERS THAT NEED TO BE IMPLEMENTED CONTACT DANIEL

# distance from camera to object(sign) measured 
# centimeter 
Known_distance = 25.5
#sign = 76.2

# width of sign in the real world or Object Plane 
# centimeter 
Known_width = 6.3
#sign = 14.3

# Colors 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
  
# defining the fonts 
fonts = cv2.FONT_HERSHEY_COMPLEX 
  
# sign detector object 
stop_detector = cv2.CascadeClassifier("cascade_stop_sign.xml")
lTurn_detector = cv2.CascadeClassifier("cascade_turn_left8.xml")  
rTurn_detector = cv2.CascadeClassifier("cascade_turn_right6.xml") 
  
# focal length finder function 
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image): 
  
    # finding the focal length 
    focal_length = (width_in_rf_image * measured_distance) / real_width 
    return focal_length 
  
# distance estimation function 
def Distance_finder(Focal_Length, real_sign_width, sign_width_in_frame): 
  
    distance = (real_sign_width * Focal_Length)/sign_width_in_frame 
  
    # return the distance 
    return distance 

  
def sign_data(image, type): 
  
    sign_width = 0  # making sign width to zero 
  
    # converting color image to gray scale image 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
    # detecting sign in the image 
    if (type == 'stop'):
        signs = stop_detector.detectMultiScale(gray_image, 1.3, 5) 
    elif (type == 'left'):
        signs = lTurn_detector.detectMultiScale(gray_image, 1.3, 5) 
    elif (type == 'right'):
        signs = rTurn_detector.detectMultiScale(gray_image, 1.3, 5) 
  
    # looping through the signs detect in the image 
    # getting coordinates x, y , width and height 
    for (x, y, h, w) in signs: 
  
        # draw the rectangle on the sign 
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2) 
  
        # getting sign width in the pixels 
        sign_width = w 
  
    # return the sign width in pixel 
    return sign_width 


# What the code does when it sees a specific time

def Decision(sign_read):
    if (sign_read == 'STOP'):
        print('STOPPED')
        #ADD STUFF
    elif (sign_read == 'TURN LEFT'):
        print('LEFT')
        #ADD STUFF
    elif (sign_read == 'TURN RIGHT'):
        print('RIGHT')
        #ADD STUFF
  
  
  
# reading reference_image from directory 
ref_image = cv2.imread("Ref_image3.png") 
  
# find the sign width(pixels) in the reference_image 
ref_image_sign_width = sign_data(ref_image, 'stop') 
  
# get the focal by calling "Focal_Length_Finder" 
# sign width in reference(pixels), 
# Known_distance(centimeters), 
# known_width(centimeters) 
Focal_length_found = Focal_Length_Finder( 
    Known_distance, Known_width, ref_image_sign_width) 
  
print(Focal_length_found) 
  
# show the reference image 
cv2.imshow("ref_image", ref_image) 
  
# initialize the camera object so that we 
# can get frame from it 
cap = cv2.VideoCapture(0) 
  
# looping through frame, incoming from  
# camera/video 
while True: 
  
    # reading the frame from camera 
    _, frame = cap.read() 
  
    # calling sign_data function to find 
    # the width of signs(pixels) in the frame 
    stop_sign_width_in_frame = sign_data(frame, 'stop')
    
    left_sign_width_in_frame = sign_data(frame, 'left')  

    right_sign_width_in_frame = sign_data(frame, 'right') 
  
    # check if the stop sign is zero then not  
    # find the distance 
    if stop_sign_width_in_frame != 0: 
        
        # finding the distance by calling function  
        # Distance finder function
        Distance = Distance_finder( 
            Focal_length_found, Known_width, stop_sign_width_in_frame) 
        
        # main decision
        Decision('STOP')


    #UNCOMMENT THESE BLOCKS TO SEE TEXT APPEAR ON CAMERA
        '''
        # draw line as background of text 
        cv2.line(frame, (30, 30), (230, 30), RED, 32) 
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28) 
  
        # Drawing Text on the screen 
        cv2.putText( 
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),  
          fonts, 0.6, GREEN, 2) 
        '''
    
    # check if there is a left turn sign on screen
    if left_sign_width_in_frame != 0:
        # finding the distance by calling function  
        # Distance finder function
        Distance = Distance_finder( 
            Focal_length_found, Known_width, left_sign_width_in_frame) 
        
        # main decision
        Decision('TURN LEFT')
  
        '''
        # draw line as background of text 
        cv2.line(frame, (30, 30), (230, 30), RED, 32) 
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28) 
  
        # Drawing Text on the screen 
        cv2.putText( 
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),  
          fonts, 0.6, GREEN, 2) 
        '''
          
    #check if there is a right turn sign on screen
    if right_sign_width_in_frame != 0:
        # finding the distance by calling function  
        # Distance finder function
        Distance = Distance_finder( 
            Focal_length_found, Known_width, right_sign_width_in_frame) 
        
        # main decision
        Decision('TURN RIGHT')
  
        '''
        # draw line as background of text 
        cv2.line(frame, (30, 30), (230, 30), RED, 32) 
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28) 
  
        # Drawing Text on the screen 
        cv2.putText( 
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),  
          fonts, 0.6, GREEN, 2) 
        '''
  
    # show the frame on the screen 
    cv2.imshow("frame", frame) 
  
    # quit the program if you press 'q' on keyboard 
    if cv2.waitKey(1) == ord("q"): 
        break
  
# closing the camera 
cap.release() 
  
# closing the windows that are opened 
cv2.destroyAllWindows() 
