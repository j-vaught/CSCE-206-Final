from scipy.integrate import solve_ivp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class VanDerPol:
    def __init__(self):
        self.oscillators = []
        self.df = pd.DataFrame()
    def add_oscillator(self, mu, x0=1, y0=0):
        class new_oscillator:
            def __init__(self, mu, x0, y0):
                self.mu = mu
                self.x0 = x0
                self.y0 = y0
            def __str__(self):
                return f"mu={self.mu}, x0={self.x0}, y0={self.y0}"
        self.oscillators.append(new_oscillator(mu, x0, y0))
    def delete_oscillator(self, i):
        self.oscillators.pop(i)
    def get_sim_data(self, duration=30.0, dt=0.01):
        durations = np.linspace(0, duration, int(duration / dt))
        for oscillator in self.oscillators:
            def vdp(t, z):
                x, y = z
                return [y, oscillator.mu * (1 - x**2) * y - x]
            data = solve_ivp(vdp, [0, duration], [oscillator.x0, oscillator.y0], t_eval=durations)
            df = pd.DataFrame(data.y[0])
            df.index=durations
            self.df[oscillator] = df
            print(self.df)

    def plot(self, tmin=0.0, tmax=30.0):
        plt.plot(self.df.index, self.df)
        plt.xlim(tmin, tmax)
        plt.show()


vdp = VanDerPol()
vdp.add_oscillator(1.0)
vdp.add_oscillator(3.0)
vdp.add_oscillator(2.0)
vdp.delete_oscillator(1)
print(vdp.get_sim_data(dt=0.01))
vdp.plot(tmin=10)
print("hello")