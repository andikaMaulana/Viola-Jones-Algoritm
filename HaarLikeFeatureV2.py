import os
class HaarLikeFeature(object):
	"""docstring for HaarLikeFeature"""
	def __init__(self):
		# super(HaarLikeFeature, self).__init__()
		self.nilaiIntegral=[]
		self.numCascade=[]
		self.idx=0
		self.num_zoom=0
		self.feature=[
		[[1,2,22,5,"tw_v"],[1,2,7,5,"th_h"]],
			[[2,6,8,5,"tw_h"],[1,1,10,10,"tw_v"],[4,4,6,3,"th_v"],[1,1,4,6,"th_h"],[10,1,5,5,"tw_h"]],
			[[2,2,10,5,"tw_h"],[8,1,5,5,"th_v"],[5,10,5,5,"tw_h"],[5,5,10,6,"tw_v"],[2,2,10,5,"th_h"],
			[6,6,15,5,"tw_v"],[2,4,6,5,"th_h"],[3,3,10,4,"tw_v"],[1,10,20,6,"tw_v"]]]

	def set_nilaiIntegral(self,val):
		self.nilaiIntegral=val

	def set_numCascade(self,val):
		self.numCascade=val

	def get_nilaiIntegral(self):
		return self.nilaiIntegral

	def get_feature(self):
		return self.feature

	def set_feature(self,val):
		self.feature=val

	def zoom(self):
		self.num_zoom+=1
		for i in range(0,len(self.feature)):
			for  j in range(len(self.feature[i])):
				for k in range(0,4):
					self.feature[i][j][k]=round(self.feature[i][j][k]*1.5)

	def hitung_luas(self,posX,posY,width,height):
		D=self.nilaiIntegral[self.idx][posY+height][posX+width]
		C=self.nilaiIntegral[self.idx][posY+height][posX]
		A=self.nilaiIntegral[self.idx][posY][posX]
		B=self.nilaiIntegral[self.idx][posY][posX+width]
		hasil=(A+D-(B+C))
		if(self.num_zoom>0):
			for i in range(self.num_zoom):
				hasil/=2.25
		return int(hasil)

	def two_horizontal(self,posX,posY,width,height):
		posX1 = posX + width
		posY1 = posY + height
		luas1=self.hitung_luas(posX-1,posY-1,width-1,height)
		luas2=self.hitung_luas(posX1-1,posY-1,width-1,height)
		return luas2-luas1

	def two_vertical(self,posX,posY,width,height):	#use
		posX1 = posX + width
		posY1 = posY + height
		luas1=self.hitung_luas(posX-1,posY-1,width-1,height)#white
		luas2=self.hitung_luas(posX-1,posY1-1,width-1,height)#black
		return luas2-luas1

	def three_horizontal(self,posX,posY,width,height): #use
		posX1 = posX + width
		posY1 = posY + height
		luas1=self.hitung_luas(posX,posY,width,height)#black
		luas2=self.hitung_luas(posX,posY1,width,height)#white
		luas3=self.hitung_luas(posX,posY1+height,width,height)#black
		return (luas3+luas1)-luas2

	def three_vertical(self,posX,posY,width,height):
		posX1 = posX + width
		posY1 = posY + height
		luas1=self.hitung_luas(posX,posY,width,height)
		luas2=self.hitung_luas(posX1,posY,width,height)
		luas3=self.hitung_luas(posX1+width,posY,width,height)
		return luas3+luas1-luas2

	def HLF(self):
		data=[]
		for i in range(0,len(self.nilaiIntegral)):
			self.idx=i
			dataCascade=[]
			for j in range(0,len(self.numCascade)):
				cascade=[]
				for k in range(0,self.numCascade[j]):					
					if(self.feature[j][k][4]=="tw_h"):
						cascade.append(self.two_horizontal(
							self.feature[j][k][0],
							self.feature[j][k][1],
							self.feature[j][k][2],
							self.feature[j][k][3]))
					elif(self.feature[j][k][4]=="tw_v"):
						cascade.append(self.two_vertical(
							self.feature[j][k][0],
							self.feature[j][k][1],
							self.feature[j][k][2],
							self.feature[j][k][3]))
					elif(self.feature[j][k][4]=="th_h"):
						cascade.append(self.three_horizontal(
							self.feature[j][k][0],
							self.feature[j][k][1],
							self.feature[j][k][2],
							self.feature[j][k][3]))
					else:
						cascade.append(self.three_vertical(
							self.feature[j][k][0],
							self.feature[j][k][1],
							self.feature[j][k][2],
							self.feature[j][k][3]))
				dataCascade.append(cascade)
			data.append(dataCascade)
		return data
