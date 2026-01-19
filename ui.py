# HELP
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import pyqtgraph.opengl as gl
from config import cfg, presets

class Window(QMainWindow):
    def __init__(self, run_callback):
        super().__init__()
        self.run_sim = run_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(cfg['title'])
        self.resize(1400, 900)
        self.setStyleSheet(f"background-color: {cfg['bg']}; color: {cfg['text']};")

        cw = QWidget()
        self.setCentralWidget(cw)
        lay = QHBoxLayout(cw)
        lay.setContentsMargins(0,0,0,0)

        # sidebar
        side = QFrame()
        side.setFixedWidth(320)
        side.setStyleSheet("background-color: #0a0a0a; border-right: 1px solid #222;")
        sl = QVBoxLayout(side)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #111; color: #888; padding: 10px; }
            QTabBar::tab:selected { background: #222; color: #fff; border-bottom: 2px solid #00ff7f; }
        """)
        
        # Tab 1: Controls
        t1 = QWidget()
        l1 = QVBoxLayout(t1)
        self.setup_controls(l1)
        self.tabs.addTab(t1, "Control")

        t2 = QWidget()
        l2 = QVBoxLayout(t2)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("font-family: Consolas; font-size: 12px; background: #0f0f0f;")
        l2.addWidget(QLabel("Time | Speed | Height"))
        l2.addWidget(self.log_area)
        self.tabs.addTab(t2, "Log")

        sl.addWidget(self.tabs)
        lay.addWidget(side)

        # 3d magic masala
        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor(cfg['bg'])
        lay.addWidget(self.view)
        
        # grid setup
        g = gl.GLGridItem()
        g.setSize(x=10000, y=10000)
        g.setSpacing(x=10, y=10)
        g.setColor((40, 40, 40, 100))
        self.view.addItem(g)
        self.view.setCameraPosition(distance=100, elevation=20, azimuth=45)

        # plotting
        self.line = None
        self.labels = []

    def setup_controls(self, l):
        l.setSpacing(15)
        
        # type selector
        l.addWidget(QLabel("Presets"))
        self.combo = QComboBox()
        self.combo.addItems(presets.keys())
        self.combo.currentTextChanged.connect(self.run_sim)
        self.combo.setStyleSheet("background: #111; padding: 5px;")
        l.addWidget(self.combo)

        # inputs
        self.v = self.add_inp(l, "Velocity (m/s)", "28.0")
        self.a = self.add_inp(l, "Angle (deg)", "35.0")
        self.w = self.add_inp(l, "Wind Speed (m/s)", "2.0")
        self.d = self.add_inp(l, "Air Density (kg/m^3)", "1.225")

        l.addSpacing(20)
        l.addWidget(QLabel(" ")) # code doesnt function cuz of ts idk why but keep it
        self.res_r = self.add_stat(l, "Range")
        self.res_h = self.add_stat(l, "Max Height")
        l.addStretch()

    def add_inp(self, l, txt, val):
        l.addWidget(QLabel(txt))
        b = QLineEdit(val)
        b.setStyleSheet("background: #111; border: 1px solid #333; padding: 8px;")
        b.textChanged.connect(self.run_sim)
        l.addWidget(b)
        return b

    def add_stat(self, l, txt):
        lb = QLabel("0.00")
        lb.setStyleSheet(f"color: {cfg['accent']}; font-size: 20px; font-weight: bold;")
        l.addWidget(QLabel(txt))
        l.addWidget(lb)
        return lb