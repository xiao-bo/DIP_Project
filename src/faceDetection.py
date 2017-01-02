import cv2
import sys

##demo debug for background

cascPath = "../db/haarcascade_frontalface_default.xml"        
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)#
video_capture.set(3,840)
video_capture.set(4,480)
def loop():
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        roi=[]
        # Draw a rectangle around the faces
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi=frame[x:x+w,y:y+h]
            
            
        if len(faces)>0:
            print "have person"
        else:
            print "no person"
        
        # Display the resulting frame
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def clean():
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

loop()
clean()
