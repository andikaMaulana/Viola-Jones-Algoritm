import IntegralImage as II
from HaarLikeFeatureV2 import HaarLikeFeature
import Utils as Utils
import numpy as np
import cv2
import time
import csv

def main():
	pos_faces_path = 'training/positive'
	pos_nonface_path = 'training/negative'
	# pos_faces_path='file/p'
	# pos_nonface_path='file/n'
	faces_training=Utils.load_images(pos_faces_path)
	nonfaces_training=Utils.load_images(pos_nonface_path)

	print ("faces :"+str(len(faces_training)))
	print ("nonfaces :"+str(len(nonfaces_training)))

	#integral images
	print("\nload integral faces ...")
	faces_integral=[cv2.integral(faces_training[i]) for i in range(0,round(len(faces_training)))]
	print("load integral nonfaces ...")
	nonfaces_integral=[cv2.integral(nonfaces_training[i]) for i in range(0,round(len(nonfaces_training)))]

	#HaarLikeFeature
	numCascade=[2,5,9]
	# numCascade=[2,0,0]

	print("load HaarLikeFeature faces ...")
	hlf=HaarLikeFeature()
	hlf.set_numCascade(numCascade)
	hlf.set_nilaiIntegral(faces_integral)
	print("load HaarLikeFeature nonfaces ...")
	facesCascade=hlf.HLF()
	hlf.set_nilaiIntegral(nonfaces_integral)
	nonfacesCascade=hlf.HLF()
	#AdaBoost
	img=facesCascade+nonfacesCascade
	#labeling
	print("creating feature ...")
	target=[1 if i<len(facesCascade) else -1 for i in range(len(img))]

	#pengelompokan fitur
	feature=[]
	_a_=[]
	_b_=[]
	for i in range(0,len(numCascade)):
		for j in range(0,numCascade[i]):
			feature__=[]
			for k in range(0,len(img)):
				feature__.append(img[k][i][j])
			a=np.array(feature__)
			b=np.array(target)
			a_,idx=np.unique(a,return_index=True)
			b_=b[idx]
			_a_.append(np.ndarray.tolist(a_))
			_b_.append(np.ndarray.tolist(b_))
	
	with open("output/feature.csv", 'w') as resultFile:
	    wr = csv.writer(resultFile, lineterminator='\n')
	    wr.writerows(_a_)
	with open("output/target.csv", 'w') as resultFile:
	    wr = csv.writer(resultFile, lineterminator='\n')
	    wr.writerows(_b_)

if __name__=="__main__":
	main()