import cognitive_face as CF
import cv2
KEY = 'f36fd7a2c5a84e0ea61fa81a80aed7d8'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

def getAge(frame):
	
	cv2.imwrite("b.jpg",frame)
	tmp="b.jpg"
	result = CF.face.detect(tmp,False,False,'age,smile,gender')
	print result
