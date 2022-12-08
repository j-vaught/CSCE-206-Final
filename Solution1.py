import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp

class VanDerPol:
    oscillators = []
    df=pd.DataFrame()
    def _init_(self):
        self.oscillators = []
    def add_oscillator(self, mu, x0=1, y0=0):
        temp = [mu, x0, y0]
        self.oscillators.append(temp)
    def delete_oscillator(self, index):
        del self.oscillators[index]
    def get_individual_sim_data(self, duration, dt,index):#gets individual sim data, since I did not want to implement this inside a for loop.
        def dv_dt_new( t, U, mu=self.oscillators[index][0]):
            return [U[1], mu*U[1]*(1-U[0]*U[0])-U[0]]
        t_pts = np.linspace(0, duration, int(duration/dt))
        solution = solve_ivp(dv_dt_new, (0, duration), np.array([self.oscillators[index][1],self.oscillators[index][2]]), t_eval=t_pts, rtol=1.e-8, atol=1.e-8)  
        v_pts = solution.y[0,:]
        v_pts.shape
        list=[]
        for v_solve_ivp in zip(v_pts.flatten()):
            list.append(v_solve_ivp[0])
        return list
    def get_sim_data(self, duration=30, dt=0.01):
        list=[]
        nameList=[]
        for index in range(len(self.oscillators)):
            list.append(self.get_individual_sim_data(duration, dt, index))
            nameList.append(index)
        self.df = pd.DataFrame(data={nameList[i]:list[i] for i in range(len(nameList))}, index=np.linspace(0, duration, int(duration/dt)))
        return self.df
    def plot(self, tmin=0, tmax=30.0):
        plt.plot(self.df.index, self.df)
        plt.xlim(tmin, tmax)
        plt.show()

#main function
vdp = VanDerPol()
vdp.add_oscillator(1.0) # oscillator 0
vdp.add_oscillator(3.0) # oscillator 1
vdp.add_oscillator(2.0) # oscillator 2
vdp.delete_oscillator(1)
print(vdp.get_sim_data(dt=0.01))
vdp.plot(tmin=10)