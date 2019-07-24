
# import numpy
def integral(fileImage):
	tmp=[]
	try:
		for i in range(0,len(fileImage)):
			tmp1=[]
			for j in range(len(fileImage[0])):
				tmp1.append(hitungIntegral(fileImage,i,j))
			tmp.append(tmp1)
	except IndexError:
		print('error')
	return tmp
#tmp
def hitungIntegral(fileImage,x,y):
	tmp=0
	for k in range(0, x+1):
		for l in range(0, y+1):
			tmp+=fileImage[k][l]
		pass
	return tmp
