import time
import math
import csv
def cek_error(data,y,w,len_x):
	e=0
	for i in range(0,len_x):
		if(y[i]!=data[i]):
			e+=w[i]
	return e

def cari_alfa(val):
	return 1 if val==0 else 0.5*math.log((1.0-val)/val)

def cari_c_x(val):
	return [math.exp(-val),math.exp(val)]

def update_bobot(tr,opr,cx,len_x,x,y,w):
	#error 1 or -1
	t_er=[]
	er=[]
	for i in range(0,len_x):
		if opr==1:
			if(x[i]<tr):
				t_er.append(1)
			else:
				t_er.append(-1)
		else:
			if(x[i]>=tr):
				t_er.append(1)
			else:
				t_er.append(-1)
		if(t_er[i]!=y[i]):
			er.append(1)
		else:
			er.append(0)
	#pre normalisasi
	pre_norm=[]
	_z=0
	for i in range(0,len_x):
		if(er[i]==1):
			__z=w[i]*cx[1]
			_z+=__z
			pre_norm.append(__z)
		else:
			__z=w[i]*cx[0]
			_z+=__z
			pre_norm.append(__z)
	for i in range(0,len_x):
		w[i]=pre_norm[i]/_z
	return w

def hitungClassifier(len_x,x,y,w,hipo):
	#menyimpan jumlah error,treshold, dan operator
	t_e=[]
	for i in hipo:
		h_t=[]
		for j in range(0,len_x):
			if(x[j]<i):
				h_t.append(1)
			else:
				h_t.append(-1)
		t_e.append([cek_error(h_t,y,w,len_x),i,1])
	#x lebih besar dari treshold
		h_t=[]
		for j in range(0,len_x):
			if(x[j]>=i):
				h_t.append(1)
			else:
				h_t.append(-1)
		t_e.append([cek_error(h_t,y,w,len_x),i,0])
	#cari nilai treshold terkecil
	min_t=t_e[0]
	for i in range(0,len(t_e)):
		if(min_t[0]>t_e[i][0]):
			min_t=t_e[i]
	return min_t

def pengujian(val,FinalClassifier):
	hasil=0
	for i in range(0,len(FinalClassifier)):
		bil=0
		if FinalClassifier[i][2]==1:
			if val<FinalClassifier[i][1]:
				bil=1
			else:
				bil=-1
		else:
			if val>FinalClassifier[i][1]:
				bil=1
			else:
				bil=-1
		hasil+=bil*FinalClassifier[i][0]
	return -1 if hasil<0 else 1

def training(x,y,acr_rate):
	#bobot
	w=[] 
	#hipotesis
	h=[] 
	#classifier final
	FinalClassifier=[]
	#operator
	op=[]
	#
	z=[]
	#error per clasifier
	err=[]
	#alfa_t per classifier
	alfa_t=[]
	#treshold
	t=[]
	min_x=min(x)-1
	max_x=max(x)+1
	#panjang data
	len_x=len(x)

	#c x
	c_x=[]

	# #inisialisasi bobot awal
	w=[]
	j_x=0
	j_y=0
	# for i in range(len_x):
	# 	w.append(1/len_x)
	for i in range(len_x):
		if y[i]==1:
			j_x+=1
		else:
			j_y+=1

	for i in range(len_x):
		if y[i]==1:
			w.append(1/(2*j_x))
		else:
			w.append(1/(2*j_y))
	
	hipo=[]
	#jumlah data
	ln=max_x-min_x
	#perkiraan bobot

	tmp=min_x
	for i in range(min_x,ln*2):
		if(tmp>=min_x and tmp<=max_x):
			hipo.append(tmp)
		tmp+=0.5
	akurasi=0
	loop=0
	now=time.time()
	err=[]
	alfa_t=[]
	op=[]
	c_x=[]
	t=[]
	FinalClassifier=[]
	while akurasi<acr_rate:
		tt=time.time()
		classierLemah=hitungClassifier(len_x,x,y,w,hipo)
		err.append(classierLemah[0])
		alfa_t.append(cari_alfa(classierLemah[0]))
		op.append(classierLemah[2])
		c_x.append(cari_c_x(alfa_t[loop]))
		t.append(classierLemah[1])
		FinalClassifier.append(classierLemah)
		update_bobot(t[loop],op[loop],c_x[loop],len_x,x,y,w)
		# #pengujian
		hasilUji=[]
		benar=0
		for i in range(0,len_x):
			hasilUji.append(pengujian(x[i],FinalClassifier))
			# print(f'data ke {i} x:{x[i]}, target:{y[i]}, hasil uji : {hasilUji[i]}')
			if(hasilUji[i]==y[i]):
				benar+=1
		acr=int(benar/len_x*100)
		if acr!=akurasi:
			print(f"akurasi {akurasi} %, t : {time.time()-tt} s")
		akurasi=acr
		loop+=1
	print(f'tingkat akurasi : {akurasi} %, t : {time.time()-now} s')
	return FinalClassifier

def cekHasil(cascade,luas):
	ch=[]
	for i in range(0,len(cascade)):
		ch1=[]
		for j in range(0,len(cascade[i])):
			val=0
			for k in range(0,len(cascade[i][j])):
				if cascade[i][j][k][2]==1:
					bil=1 if luas[i][j]<cascade[i][j][k][1] else -1
				else:
					bil=1 if luas[i][j]>=cascade[i][j][k][1] else -1
				val+=bil*cascade[i][j][k][0]
			val=-1 if val<0 else 1
			ch1.append(val)
		ch.append(ch1)

def main():
	#baca file csv
	dir_x='output/feature.csv'
	dir_y='output/target.csv'
	data_x =list(csv.reader(open(dir_x)))
	data_y =list(csv.reader(open(dir_y)))
	classifier=[]
	for i in range(len(data_x)):
		print(f" fitur ke {i+1} :")
		x=list(map(int,data_x[i]))
		y=list(map(int,data_y[i]))
		classifier.append(training(x,y,100))

	#save file
	with open("output/classifier.csv", 'w') as resultFile:
		wr = csv.writer(resultFile, lineterminator='\n')
		wr.writerows(classifier)

if __name__=="__main__":
	main()