import sys
import numpy as np
import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QApplication
from config import cfg, presets
from physics import Engine
from ui import Window

class App:
    def __init__(self):
        self.phys = Engine()
        self.ui = Window(self.update)
        self.update()
        self.ui.show()

    def update(self):
        # get ui values
        try:
            v0 = float(self.ui.v.text())
            ang = float(self.ui.a.text())
            wind = float(self.ui.w.text())
            rho = float(self.ui.d.text())
        except: return

        # 2. get preset data
        p_name = self.ui.combo.currentText()
        data = presets[p_name]
        
        # 3. run physics engine
        pts, vels, times = self.phys.calc(
            v0, ang, data['m'], rho, wind, data['cd'], data['area']
        )

        # 4. update 3d line
        if self.ui.line: self.ui.view.removeItem(self.ui.line)
        self.ui.line = gl.GLLinePlotItem(pos=pts, color=(0, 255, 127, 255), width=3)
        self.ui.view.addItem(self.ui.line)

        # 5. update stats
        dist = np.sqrt(pts[-1,0]**2 + pts[-1,1]**2)
        self.ui.res_r.setText(f"{dist:.2f} m")
        self.ui.res_h.setText(f"{np.max(pts[:,2]):.2f} m")

        # 6. update data log (1s)
        log_text = ""
        last_int_time = -1
        
        for i, t in enumerate(times):
            if int(t) > last_int_time: # only log when second changes
                last_int_time = int(t)
                speed = vels[i]
                h = pts[i, 2]
                log_text += f"T={t:.1f}s | V={speed:.2f}m/s | H={h:.1f}m\n"
        
        # add impact data
        log_text += f"T={times[-1]:.2f}s | IMPACT | Dist={dist:.2f}m"
        self.ui.log_area.setText(log_text)

        # 7. camera fix
        cdist = max(50, min(10000, dist * 1.5))
        self.ui.view.setCameraPosition(distance=cdist)

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    app = App()
    sys.exit(qapp.exec())