import cognitive_face as CF

KEY = 'f36fd7a2c5a84e0ea61fa81a80aed7d8'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img_url="../pic/self.jpge"
result = CF.face.detect(img_url,False,False,'age,smile,gender')
print result