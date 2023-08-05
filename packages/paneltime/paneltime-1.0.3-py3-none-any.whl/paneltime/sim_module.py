#!/usr/bin/env python
# -*- coding: utf-8 -*-

#simulalte a panel data GARCH model

import numpy as np
import regprocs as rp
import regobj
import functions as fu


class simulation:
	"""Creates an object that can simulate ARIMA-GARCH-timeseries data"""
	def __init__(self,N,T,beta,rho=[0.0001],lmbda=[-0.0001],psi=[0.0001],gamma=[00.0001],omega=0.1,mu=1,z=1,residual_sd=0.001,group_sd=0,names=['x','const','Y','ID']):

		self.args,self.p,self.q,self.m,self.k,self.beta_len=self.new_args(beta,rho,lmbda,psi,gamma,omega,mu,z)
		self.T=T
		self.names=['x','const','Y','ID']
		self.N=N
		self.residual_sd=residual_sd
		self.group_sd=group_sd
		self.max_lags=np.max((self.p,self.q,self.m,self.k))
		self.L=rp.make_lag_matrices(T,self.max_lags)
		self.I=np.diag(np.ones(T))
		self.zero=self.I*0		
		self.AAR_1MA, self.GAR_1MA=matrices=self.set_garch_arch()
		
	def sim_many(self,n):
		for i in range(n):
			d=dict()
			X,Y,groups=self.sim()
			save_dataset(X,Y,groups,self.names,i)
		
	def sim(self):
		args=self.args
		if self.residual_sd==0:
			raise RuntimeError("Zero residual error not allowed.")
		e=np.random.normal(0,self.residual_sd,(self.N,self.T,1))
		if self.group_sd>0:
			eRE=e+np.random.normal(0,self.group_sd,(self.N,1,1))
		else:
			eRE=e
		
		u=fu.dot(self.AAR_1MA,eRE)
		
	
		if self.m>0:
			h=np.log(eRE**2+args['z'])
			group_eff=np.random.normal(0,1,(self.N,1,1))*args['mu']
			lnv=fu.dot(self.GAR_1MA,h)+group_eff+args['omega']
		else:
			lnv=0	
			
		v=np.exp(lnv)
		v_inv=np.exp(-lnv)
		
		eRE_GARCH=eRE*v
		
		X=np.random.normal(0,1,(self.N,self.T,self.beta_len-1))
		X=np.concatenate((np.ones((self.N,self.T,1)),X),2)
		Y_pred=fu.dot(X,args['beta'])
		Y=Y_pred+eRE_GARCH
		
		X=reshape(X,self.max_lags+1)
		Y=reshape(Y,self.max_lags+1)
		groups=np.ones((self.N,self.T,1))*np.arange(self.N).reshape((self.N,1,1))
		groups=reshape(groups,self.max_lags+1)
		return X,Y,groups

	def new_args(self,beta,rho,lmbda,psi,gamma,omega,mu,z):
		p=len(rho)
		q=len(lmbda)
		m=len(psi)
		k=len(gamma)
		beta_len=len(beta)		
		args=dict()
		args['beta']=np.array(beta).reshape((beta_len,1))
		args['omega']=omega
		args['rho']=np.array(rho)
		args['lambda']=np.array(lmbda)
		args['psi']=np.array(psi)
		args['gamma']=np.array(gamma)
		if m>0:
			args['mu']=mu
			args['z']=z
		else:
			args['mu']=0
			args['z']=0

		return args,p,q,m,k,beta_len

	
		
		
	def set_garch_arch(self):
		args,p,q,m,k=self.args,self.p,self.q,self.m,self.k
		AMA=self.I+rp.lag_matr(self.L,self.zero,q,args['lambda'])
		X=self.I-rp.lag_matr(self.L,self.zero,p,args['rho'])
		AAR_1=np.linalg.inv(X)
		AAR_1MA=fu.dot(AAR_1,AMA)
		X=self.I-rp.lag_matr(self.L,self.zero,k,args['gamma'])
		GAR_1=np.linalg.inv(X)
		GMA=rp.lag_matr(self.L,self.zero,m,args['psi'])	
		GAR_1MA=fu.dot(GAR_1,GMA)
		return AAR_1MA, GAR_1MA
	


def reshape(X,n):
	X=X[:,n:,:]
	return np.concatenate(X,0)
	



def save_dataset(X,Y,groups,names,i):
	k=len(X[0])
	h=[]
	for j in range(len(X[0])):
		h.append(names[0]+str(j))
	h[0]=names[1]
	h=np.array([h])
	X=np.concatenate((h,X),0)
	Y=np.concatenate(([[names[2]]],Y),0)
	groups=np.concatenate(([[names[3]]],groups),0)
	data=np.concatenate((X,Y,groups),1)
	fu.savevar(data,'/simulations/data'+str(i),'csv')	