import numpy as np
import cv2
img = cv2.imread('origImg.jpg')
eight = cv2.imread('eight.jpg')
height= img.shape[0]
width = img.shape[1]
ret,binaryImg = cv2.threshold(img,250,255,cv2.THRESH_BINARY)
output = np.zeros((height,width),dtype=np.uint8)
output[(img[:,:,0]>250) & (img[:,:,1]>250) & (img[:,:,2]>250)] = 255
canny = cv2.Canny(output,100,200)
#detect lines
lines = cv2.HoughLinesP(canny,1,np.pi/180,100,None,50,20)
rowPoint = np.zeros(2*lines.shape[0],dtype=np.uint16)
colPoint = np.zeros(2*lines.shape[0],dtype=np.uint16)
for i in range(lines.shape[0]):
	x1=lines[i][0][0]
	x2=lines[i][0][2]
	y1=lines[i][0][1]
	y2=lines[i][0][3]
	if((abs(y1-y2)<4 and abs(x1-x2)>width/2) or abs(x1-x2)<4):
		#cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
		rowPoint[2*i] = y1
		rowPoint[2*i+1] = y2
		colPoint[2*i] = x1
		colPoint[2*i+1] = x2
#sorting
rowPoint.sort()
colPoint.sort()
#find rectangle
rowCount = 0
colCount = 0
recRow = np.zeros(1,dtype=np.uint16)
recCol = np.zeros(1,dtype=np.uint16)
for i in range(rowPoint.shape[0]-1):
	if(abs(rowPoint[i+1]-rowPoint[i])<3 and rowPoint[i]!=0):
		rowCount += 1
	else:	
		if(rowCount==3):
			recRow = np.append(recRow,rowPoint[i])
		rowCount = 0
	if (abs(colPoint[i+1]-colPoint[i])<3):
		colCount += 1
	else:
		if(colCount==3):
			recCol = np.append(recCol,colPoint[i])
		colCount = 0
if(rowCount==3):
	recRow = np.append(recRow,rowPoint[-1])
if(colCount==3):
	recCol = np.append(recCol,colPoint[-1])
recRow=recRow[1:3]
recCol=recCol[1:3]
rectWidth = recCol[1]-recCol[0]
'''
cv2.rectangle(img,(recCol[0],recRow[0]),(recCol[1],recRow[1]),(0,255,0),3)
cv2.rectangle(img,(679,recRow[0]),(716,recRow[1]),(0,0,0),1)
'''
eight = cv2.resize(eight,(int(38*rectWidth/884),recRow[1]-recRow[0]),interpolation=cv2.INTER_CUBIC)
#679:716
img[recRow[0]:recRow[1],516*rectWidth/884+recCol[0]:554*rectWidth/884+recCol[0]]=eight
print recRow,recCol,width,eight.shape
cv2.imshow('lane',img)
if cv2.waitKey(0)>0:
	cv2.destroyAllWindows()
