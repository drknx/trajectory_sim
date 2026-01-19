cfg = {
    'title': "trajectory sim",
    'bg': '#050505',
    'accent': '#00ff7f', # spring green
    'text': '#cccccc',
    
    # physics defaults
    'dt': 0.01, # time step
    'g': 9.81,
}

# presets
presets = {
    'Javelin': {'cd': 0.28, 'area': 0.005, 'm': 0.8},
    'Sphere':  {'cd': 0.47, 'area': 0.05,  'm': 10.0},
    'Brick':   {'cd': 1.05, 'area': 0.1,   'm': 2.0},
}