from numpy import sin

_options = {
  "m": 1.0,
  "b": 0.1,
  "l": 1.0,
  "g": 9.81,
}

def configure(**options):
    _options.update(options)
    globals().update(_options)
    return _options

configure()

y0 = [0.0, 0.0]

def u(t):
    return 0.0

def fun(t, y):
    theta, d_theta = y
    J = m * l * l
    d2_theta = - g / l * sin(theta) - b / J * d_theta + u(t) / J
    return [d_theta, d2_theta]
