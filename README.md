# DIP_Project

opencv2+ pygame

#Reference web
Pygame  
[Offical site](http://www.pygame.org/hifi.html)  

Pygame Tutorial  
- (https://www.kancloud.cn/digest/python-notes/163851)  
- (http://www.bkjia.com/Pythonjc/1067115.html)  

FaceAPI  
[Offical site](https://www.microsoft.com/cognitive-services/en-us/face-api/documentation/get-started-with-face-api/GettingStartedwithFaceAPIinPython)  

Project Flow-Chart   
[Flow](https://drive.google.com/open?id=0BwT2ANLIx93qVzJUUHNzLV8yUzA)

##usgae 
These files can be executed individiual in src  
src/ageDetection.py - return age of humans at image.  
src/faceDetection.py - detect humans face in camera. 

These class file can be call by main.py.(npc.py and dialog.py) 
I hope build good model for main.py.  
src/npc.py - simple npc class  
src/dialog.py - simple dialog class  
src/main.py - main of game. now can run npc class and dialog class


## git note
Before you start coding , please type follow command:
```
git pull origin master
```
Maybe git ask you commit your code.
So you have to commit your code , 
```
git add yourfile
git commit -m 'your commit'
```
and pull again. 

Then you may encounter merge conflict, you have to edit error file 
and find conflict part.  

Merge it and commit again.
```
git commit -m 'merge'
```
Now you can push it to remote master.

```
git push origin master
```



