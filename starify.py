import cv2,random
import numpy as np
img = cv2.imread('Images\starbackground.png')
dimensions = img.shape
for n in range(dimensions[0]):
	for b in range(dimensions[1]):
		itemslist = [(n-1,b,0),(n-1,b,1),(n-1,b,2),(n,b-1,0),(n,b-1,1),(n,b-1,2),(n,b,0),(n,b,1),(n,b,2),(n+1,b,0),(n+1,b,1),(n+1,b,2),(n,b+1,0),(n,b+1,1),(n,b+1,2)]
		cool = True
		for q in itemslist:
			try:
				if img.item(q) != 0:
					
					cool = False
					break
			except:
				0
		if cool and random.random() > .95:
			if random.random() <.66:
				for q in itemslist[:3]:
					img.itemset(q,255)
			else:
				for q in itemslist:
					try:
						img.itemset(q,255)
					except:
						0
cv2.imwrite('Images\starbackground.png',img)