# physics.py
import numpy as np
from config import cfg

class Engine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pts = []
        self.vels = [] # storage of speeds
        self.times = []

    def calc(self, v0, angle, mass, rho, wind, cd, area):
        self.reset()
        
        dt = cfg['dt']
        g = cfg['g']
        
        # initilize vectors
        rad = np.radians(angle)
        v = np.array([v0 * np.cos(rad), 0.0, v0 * np.sin(rad)])
        p = np.array([0.0, 0.0, 0.0])
        w = np.array([0.0, wind, 0.0]) # wind vector
        
        t = 0.0
        
        # run loop
        for _ in range(20000): # max steps
            # relative vel for drag
            v_rel = v - w
            sp = np.linalg.norm(v_rel)
            
            if sp > 0: # calc drag only if moving
                drag = -0.5 * rho * (sp**2) * cd * area * (v_rel / sp)
            else:
                drag = np.array([0.,0.,0.])

            acc = (drag / mass) + np.array([0, 0, -g])
            v += acc * dt
            p += v * dt
            t += dt

            # save
            self.pts.append(p.copy())
            self.vels.append(np.linalg.norm(v))
            self.times.append(t)
            
            if p[2] < 0: break # exit

        return np.array(self.pts), self.vels, self.times