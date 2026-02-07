import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys


class as3:
	# Everything in SI
	k = 45
	alpha = 1.16e-5
	R1 = 0.02
	R2 = 0.05
	Ti = 200
	Tfmax = 100
	h1 = 50
	T1 = 20
	h2 = 250
	T2 = 5


	def __init__(self, Nr=5, Ntheta=4, dt=0.1):
		self.Nr = Nr
		self.Ntheta = Ntheta
		self.dt = dt

		self.dtheta = 2 * np.pi / Ntheta
		self.theta = (2 * np.arange(Ntheta + 1) + 1) * self.dtheta / 2

		self.r = np.linspace(as3.R1, as3.R2, Nr + 1)
		self.dr = self.r[1] - self.r[0]

		self.R, self.Theta = np.meshgrid(self.r, self.theta)

		self.T = np.full((Nr + 1, Ntheta + 2), as3.Ti, dtype=np.float64)

		half = Ntheta // 2
		self.h = np.zeros((Ntheta,))
		self.Tconv = np.zeros((Ntheta,))
		self.h[:half] = as3.h1
		self.h[half:] = as3.h2
		self.Tconv[:half] = as3.T1
		self.Tconv[half:] = as3.T2

		self.fig = plt.figure(figsize=(10, 10))
		self.ax = self.fig.add_subplot(111, projection='polar')
		self.ax.set_rorigin(0)
		self.mesh = self.ax.pcolormesh(
			self.Theta, self.R, self.T[:, 1:].T, 
			cmap='turbo', shading='auto', 
			vmin=as3.T2 - 1, vmax=as3.Ti + 1
		)
		plt.colorbar(self.mesh, ax=self.ax)


	def update(self, frame):
		Tnew = np.empty_like(self.T)

		Tnew[1:-1, 1:-1] = (
			  (1 - 2*as3.alpha*self.dt*(1/self.dr**2 + 1/(self.r[1:-1]*self.dtheta)**2))[:, None] * self.T[1:-1, 1:-1]
			+ (as3.alpha*self.dt/(self.r[1:-1]*self.dtheta)**2)[:, None] * (self.T[1:-1, :-2] + self.T[1:-1, 2:])
			+ (as3.alpha*self.dt/self.dr**2) * (self.T[2:, 1:-1] + self.T[:-2, 1:-1])
			+ (as3.alpha*self.dt/(2*self.r[1:-1]*self.dtheta))[:, None] * (self.T[2:, 1:-1] - self.T[:-2, 1:-1])
		)

		Tnew[0, 1:-1] = (
			  (1 - 2*as3.alpha*self.dt*(1/self.dr**2 + 1/(self.r[0]*self.dtheta)**2)) * self.T[0, 1:-1]
			+ (as3.alpha*self.dt/(self.r[0]*self.dtheta)**2) * (self.T[0, :-2] + self.T[0, 2:])
			+ (2*as3.alpha*self.dt/self.dr**2) * self.T[1, 1:-1]
		)

		Tnew[-1, 1:-1] = (
			  (as3.alpha*self.dt/(self.r[-1]*self.dtheta)**2) * (self.T[-1, 2:] + self.T[-1, :-2])
			+ (2*as3.alpha*self.dt/self.dr**2) * self.T[-2, 1:-1]
			+ (1 - 2*as3.alpha*self.dt*(1/self.dr**2 + 1/(self.r[-1]*self.dtheta)**2)) * self.T[-1, 1:-1]
			+ (as3.alpha*self.dt*self.h/as3.k*(2/self.dr + 1/self.r[-1])) * (self.Tconv - self.T[-1, 1:-1])
		)

		Tnew[:, 0] = Tnew[:, -2]
		Tnew[:, -1] = Tnew[:, 1]

		self.T = Tnew

		self.mesh.set_array(self.T[:, 1:].T.ravel())
		self.ax.set_title(f'Grid Size:(r {self.Nr}, $\\theta$ {self.Ntheta}), t = {frame * self.dt:.2f}s ({self.dt:.2f}s)\nFrame count: {frame}')


	def frame_generator(self):
		frame = 0
		while True:
			if np.max(self.T) < self.Tfmax:
				print('Time taken to drop below', self.Tfmax, '\bdegC:', frame * self.dt, '\bs')
				return
			
			yield frame
			frame += 1


	def animate(self, slowdown=1, save=True):
		ani = animation.FuncAnimation(self.fig, self.update, frames=self.frame_generator(), interval=int(self.dt*1000*slowdown), repeat=False, cache_frame_data=False)
		if save: ani.save(f'./org/r{self.Nr}th{self.Ntheta}dt{self.dt}.mp4', writer='ffmpeg', fps=120)
		else:    plt.show()


if __name__ == '__main__':
	#s = as3(30, 30, 0.005)
	#s = as3(10, 15, 0.1)
	#s = as3(100, 100, 0.01)
	s = as3(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])) # try 10 15 0.1 for testing (stable + fast)
	s.animate(save=True, slowdown=0.1) # set slowdown to 0.1 for testing to speed up generation