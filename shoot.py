#usr/bin/python
#coding=utf-8
#
from numpy import *
import numpy as np
from stl import mesh
import math
import pickle

PACE = 1 #the size of dividing unit less than 1
SAVE_PATH = 'C:\\Users\\bob\\Desktop\\code\\python\\temp.pkl'
def save(f):
	f1=file(SAVE_PATH,'wb')
	pickle.dump(f,f1,True);
	f1.close()

def build_face(a,b,c):
	'''
	ma=linalg.det(mat([[b[1],b[2]],[c[1],c[2]]]))
	mb=linalg.det(mat([[b[0],b[2]],[c[0],c[2]]]))
	mc=linalg.det(mat([[b[0],b[1]],[c[0],c[1]]]))
	#ret=(x-a[0])*ma-(y-a[1])*mb+(z-a[2])*mc
	#ret=ma*x-mb*y+mc*z-ma*a[0]+mb*a[1]-mc*a[2]
	'''
	A=(b[1]-a[1])*(c[2]-a[2])-(c[1]-a[1])*(b[2]-a[2])
	B=(b[2]-a[2])*(c[0]-a[0])-(c[2]-a[2])*(b[0]-a[0])
	C=(b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1])
	D=0-A*a[0]-B*a[1]-C*a[2]
	#return [ma,-mb,mc,-ma*a[0]+mb*a[1]-mc*a[2]]
	return [A,B,C,D]

def getX(face,point):
	return (-face[1]*point[1]-face[2]*point[2]-face[3])/face[0]

def getY(face,point):
	return (-face[0]*point[0]-face[2]*point[2]-face[3])/face[1]

def getZ(face,point):
	return (-face[1]*point[1]-face[0]*point[0]-face[3])/face[2]

def X(a,b):
	return [a[1]*b[2]-b[1]*a[2],b[0]*a[2]-a[0]*b[2],a[0]*b[1]-b[0]*a[1]]

def inside_line(v0,v1,v2):
	if v0>=v1 and v0<=v2 or v0>=v2 and v0<=v1:
		return 1
	else:
		return 0
def inside_3Dline(p,a,b):
	return inside_line(p[0],a[0],b[0]) and inside_line(p[1],a[1],b[1]) and inside_line(p[2],a[2],b[2])

def same_point(p1,p2):
	if p1[0]==p2[0] and p1[1]==p2[1] and p1[2]==p2[2]:
		return True
	else:
		return False
def check_inside(p,a,b,c):#1 p on line，2 p on vector，3 p on face
	#print p
	#print a
	#print b
	#print c
	p=[round(p[0],5),round(p[1],5),round(p[2],5)]
	a=[round(a[0],5),round(a[1],5),round(a[2],5)]
	b=[round(b[0],5),round(b[1],5),round(b[2],5)]
	c=[round(c[0],5),round(c[1],5),round(c[2],5)]
	if same_point(p,a) or same_point(p,b) or same_point(p,c):
		return 1

	pa=[a[0]-p[0],a[1]-p[1],a[2]-p[2]]
	pb=[b[0]-p[0],b[1]-p[1],b[2]-p[2]]
	pc=[c[0]-p[0],c[1]-p[1],c[2]-p[2]]
	tmpa=X(pa,pb)
	tmpb=X(pb,pc)
	tmpc=X(pc,pa)

	#print tmpa,tmpb,tmpc
	if tmpa[0]==0 and tmpa[1]==0 and tmpa[2]==0:
		if inside_3Dline(p,a,b):
			return 1
	if tmpb[0]==0 and tmpb[1]==0 and tmpb[2]==0:
		#print p,b,c
		if inside_3Dline(p,b,c):
			return 1
	if tmpc[0]==0 and tmpc[1]==0 and tmpc[2]==0:
		if inside_3Dline(p,c,a):
			return 1
	#if(tmpa==0):

	if(tmpa[0]!=0):
		if(tmpa[0]>0 and tmpb[0]>0 and tmpc[0]>0 or tmpa[0]<0 and tmpb[0]<0 and tmpc[0]<0):
			return 1
		else:
			return 0
	else:#p on a-b
		pass 
	if(tmpa[1] != 0):
		if(tmpa[1]>0 and tmpb[1]>0 and tmpc[1]>0 or tmpa[1]<0 and tmpb[1]<0 and tmpc[1]<0):
			return 1
		else:
			return 0
	else:#p on b-c
		pass
	if(tmpa[2] != 0):
		if(tmpa[2]>0 and tmpb[2]>0 and tmpc[2]>0 or tmpa[2]<0 and tmpb[2]<0 and tmpc[2]<0):
			return 1
		else:
			return 0
	else:#p on c-a
		pass

	print "check_inside error"


def inside_range(pp,d1,d2,d3):
	if(pp<=max(d1,d2,d3) and pp>=min(d1,d2,d3)):
		return True
	else:
		return False

def shootX(face,point,x,a,b,c):
	if(face[0]==0):
		return 0    #no cross
	if(not (inside_range(point[1],a[1],b[1],c[1]) and inside_range(point[2],a[2],b[2],c[2]))):
		return 0 	#no cross

	x0=getX(face,point)
	if(x0>=x and x0<=point[0]):
		return check_inside([x0,point[1],point[2]],a,b,c)
	elif(x0<=x and x0>=point[0]): 
		return check_inside([x0,point[1],point[2]],a,b,c)
	else:
		return 0 #no cross


def shootY(face,point,y,a,b,c):
	if(face[1]==0):
		return 0    #no cross
	if(not (inside_range(point[0],a[0],b[0],c[0]) and inside_range(point[2],a[2],b[2],c[2]))):
		return 0 	#no cross

	y0=getY(face,point)
	if(y0>=y and y0<=point[1]):
		return check_inside([point[0],y0,point[2]],a,b,c)
	elif(y0<=y and y0>=point[1]): 
		return check_inside([point[0],y0,point[2]],a,b,c)
	else:
		return 0 #no cross

def shootZ(face,point,z,a,b,c):
	if(face[2]==0):
		return 0    #no cross
	if(not (inside_range(point[1],a[1],b[1],c[1]) and inside_range(point[0],a[0],b[0],c[0]))):
		return 0 	#no cross

	z0=getZ(face,point)
	#print z0,point[2]
	if(z0>=z and z0<=point[2]):
		#print check_inside([point[0],point[1],z0],a,b,c)
		return check_inside([point[0],point[1],z0],a,b,c)
	elif(z0<=z and z0>=point[2]): 
		return check_inside([point[0],point[1],z0],a,b,c)
	else:
		return 0 #no cross

def LUdecomp(a):
	n=len(a)
	for k in range(0,n-1):
		for i in range(k+1,n):
			if abs(a[i,k]) > 1.0e-9:
				lam=a[i,k]/a[k,k]
				a[i,k+1:n]=a[i,k+1:n]-lam*a[k,k+1:n]
				a[i,k]=lam
	return a

def LUsolve(a,b):
	n = len(a)
	for k in range(1,n):
		b[k]=b[k]-dot(a[k,0:k],b[0:k])
	b[n-1]=b[n-1]/a[n-1,n-1]
	for k in range(n-2,-1,-1):
		b[k] = (b[k] - dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
	return b

def shooter(facelist,point):
	xhitmin=0
	xhitmax=0
	yhitmin=0
	yhitmax=0
	zhitmin=0
	zhitmax=0

	xmin=-100
	xmax=100
	ymin=-100
	ymax=100
	zmin=-100
	zmax=100

	for i in facelist:#shootx
		face=build_face(i[0],i[1],i[2])
		if(xhitmin==0): 
			xhitmin=shootX(face,point,xmin,i[0],i[1],i[2])
		if(xhitmax==0):
			xhitmax=shootX(face,point,xmax,i[0],i[1],i[2])

		if(yhitmin==0):
			yhitmin=shootY(face,point,ymin,i[0],i[1],i[2])
		if(yhitmax==0):
			yhitmax=shootY(face,point,ymax,i[0],i[1],i[2])

		if(zhitmin==0):
			zhit=shootZ(face,point,zmin,i[0],i[1],i[2])
		if(zhitmax==0):
			zhit=shootZ(face,point,zmax,i[0],i[1],i[2])

	if(xhitmin==1 and xhinmax==1 and yhitmin==1 and yhitmax and zhitmax and zhitmin==1):
		return 1
	else:
		return 0  

def onface(facelist,point):
	for i in facelist:
		if check_inside(point,i[0],i[1],i[2]):
			return 1
	return 0

def connect(p1,p2):
	con_count=0
	for i in p1:
		if i in p2:
			con_count+=1
	if con_count>=2:
		return 1
	else:
		return 0

def reduce_face(facelist):
	offset=0
	for i in range(len(facelist)):
		for j in range(i+1,len(facelist)):
			if connect(facelist[i],facelist[j-offset]):
				del facelist[j-offset]
				offset+=1
	return facelist

def shootAllX(facelist,point):
	hitcounter=0
	xmin=-100
	tmplist=[]
	for i in facelist:
		face=build_face(i[0],i[1],i[2])
		if(shootX(face,point,xmin,i[0],i[1],i[2])==1):
			tmplist.append(i)
	reduce_face(tmplist)
	return len(tmplist)

def shootAllY(facelist,point):
	hitcounter=0
	ymin=-100
	tmplist=[]
	for i in facelist:
		face=build_face(i[0],i[1],i[2])
		if(shootY(face,point,ymin,i[0],i[1],i[2])==1):
			tmplist.append(i)
	reduce_face(tmplist)
	return len(tmplist)

def shootAllZ(facelist,point):
	hitcounter=0
	zmin=-100
	tmplist=[]
	for i in facelist:
		face=build_face(i[0],i[1],i[2])
		if(shootZ(face,point,zmin,i[0],i[1],i[2])==1):
			tmplist.append(i)
	reduce_face(tmplist)
	return len(tmplist)

def dice_bound(stl_mesh):
	minx=miny=minz=maxx=maxy=maxz=None
	counter=0
	listv=[(stl_mesh.vectors[0])[0],(stl_mesh.vectors[0])[1],(stl_mesh.vectors[0])[2]]
	for j in range(1,len(stl_mesh.vectors)):
		listv.append(stl_mesh.vectors[j][0])
		listv.append(stl_mesh.vectors[j][1])
		listv.append(stl_mesh.vectors[j][2])

	for i in listv:
		print i
		counter+=1
		if minx is None:
			minx=i[0]
			maxx=i[0]
			miny=i[1]
			maxy=i[1]
			minz=i[2]
			maxz=i[2]
		else:
			minx=min(minx,i[0])
			maxx=max(maxx,i[0])
			miny=min(miny,i[1])
			maxy=max(maxy,i[1])
			minz=min(minz,i[2])
			maxz=max(maxz,i[2])
	print counter
	return [minx,miny,minz,maxx,maxy,maxz]



def inside_small_dice(facelist,p):
	sx=shootAllX(facelist,p)
	sy=shootAllY(facelist,p)
	sz=shootAllZ(facelist,p)
	#print sx,sy,sz
	if sx%2==1 and sy%2==1 and sz%2==1:
		return 1
	else:
		return 0

def bulid_small_dice(x,y,z):
	global PACE
	p00=[x,y,z];
	px0=[x+PACE,y,z]
	py0=[x,y+PACE,z]
	pxy=[x+PACE,y+PACE,z]
	p11=[x,y,z+PACE]
	px1=[x+PACE,y,z+PACE]
	py1=[x,y+PACE,z+PACE]
	pzz=[x+PACE,y+PACE,z+PACE]
	listt=[[p00,px0,py0],[pxy,px0,py0],[p11,px1,py1],[pzz,px1,py1],[p00,px0,p11],[px1,px0,p11],[p00,p11,py0],[py1,p11,py0],[px1,px0,pxy],[px1,pxy,pzz],[py1,pxy,py0],[py1,pxy,pzz]]
	return listt

def build_big_dice(facelist,minx,miny,minz,maxx,maxy,maxz):
	global PACE
	if(PACE>1):
		print "pace too far!"
		return -1
	pace_times=int(1/PACE)
	#normal
	x_min=minx//1
	y_min=miny//1
	z_min=minz//1
	x_max=maxx//1+1
	y_max=maxy//1+1
	z_max=maxz//1+1
	print x_min,x_max,y_min,y_max,z_min,z_max
	print len(facelist)
	dicelist=[]
	dice_core=0
	for i in range(int(x_min*pace_times),int(x_max*pace_times)):
		for j in range(int(y_min*pace_times),int(y_max*pace_times)):
			for k in range(int(z_min*pace_times),int(z_max*pace_times)):
				#print i,j,k
				dice_core=[(i+0.5)*PACE,(j+0.5)*PACE,(k+0.5)*PACE]
				if(inside_small_dice(facelist,dice_core)==1):
					listm=bulid_small_dice(i*PACE,j*PACE,k*PACE)
					for m in listm:
						if(m in dicelist):
							print "in......"
							continue
						dicelist.append(m)
					print "add..."
	save(dicelist)
	return dicelist


def dice(stl_mesh):
	print "x:"
	#print stl_mesh.vectors
	minx,miny,minz,maxx,maxy,maxz=dice_bound(stl_mesh)
	print minx,miny,minz,maxx,maxy,maxz

	#full dice minx maxx miny maxy minz maxz
	print(len(stl_mesh.vectors))
	A=build_big_dice(stl_mesh.vectors,minx,miny,minz,maxx,maxy,maxz)
	
	#A=inside_small_dice(stl_mesh.vectors,[20,30,6])
	return len(A)
	#for i in range(minx..maxx):

if __name__ == '__main__':
	a=mat([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
	
	print a
	#LUdecomp(a);
	#print a
	eval,evec= linalg.eig(a)
	#print eval
	#print evec
	c=np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
	b=np.array([2,2,2])
	print linalg.solve(c,b)
	d=mat([[2.,3],[1,2]])
	#print linalg.det(d)
	a=[0,0,0]
	b=[0,1,0]
	c=[1,0,0]
	p=[0.25,0.25,1]
	face=build_face(a,b,c)
	print shootZ(face,p,2,a,b,c)
	facelist=[]
	facelist.append([a,b,c])
	facelist.append([a,[8,5,9],c])
	facelist.append([a,[1,300,1],[800,1,1]])
	#print reduce_face(facelist)
	face=build_face(a,[1,300,1],[800,1,1])
	print "shoot z:"
	#print shootZ(face,p,-100,a,[1,300,1],[800,1,1])

	print shootAllZ(facelist ,p)

	facelist2=[[[0,1,1.],[1,0,1.],[0,0,1.]],
 [[1,0,1.],[0,1,1.],[1,1,1.]],
 [[1,0,0.],[1,0,1.],[1,1,0.]],
 [[1,1,1.],[1,0,1.],[1,1,0.]],
 [[0,0,0.],[1,0,0.],[1,0,1.]],
 [[0,0,0.],[0,0,1.],[1,0,1.]],
 [[0,0,0.],[1,0,0.],[0,1,0.]],
 [[1,1,0.],[0,1,0.],[1,0,0.]],
 [[0,0,0.],[0,0,1.],[0,1,0.]],
 [[0,1,1.],[0,0,1.],[0,1,0.]],
 [[0,1,0.],[1,1,0.],[1,1,1.]],
 [[0,1,0.],[0,1,1.],[1,1,1.]]]
	print "sss:"
	sx=shootAllX(facelist2,[0.5,0.5,0.5])
	print sx
	'''
	print "ssssss:"
	print build_face([0,0,1],[1,0,0],[0,1,0.])
	'''
	print "ssssss:"
	#print shootZ(face,[0.5,0.5,0.5],-100,[0,0,0.],[1,0,0],[0,1,0.])
	aa=[25.74309539794922, 4.305110931396484, 8.638248443603516]
 	aaa=[24.618974685668945, 5.322914123535156, 8.638248443603516]
 	aaaa=[24.618974685668945, 5.322914123535156, 0.0]
 
 	pa=build_face(aa,aaa,aaaa)
	print shootY(pa,[30,14,7],-100,aa,aaa,aaaa)
	print pa
	#print build_face([30, 5.225504161338271, 7],aa,aaa)
	#print build_face([0,0,0.],[1,0,0.],[0,1,0.])
	#print check_inside([30, 5.225504161338271, 7],aa,aaa,aaaa)
