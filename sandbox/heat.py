
from numpy import *
from scipy import *
from scipy.integrate import *
from matplotlib.pyplot import *
from matplotlib.animation import *

def make_config(free, sources, initial_temp):
    free = array(free, dtype=bool)
    sources = array(sources, dtype=bool)
    initial_temp = array(initial_temp, dtype=float)

    n_rows, n_cols = grid_size = shape(free)

    locations = nonzero(free)
    locations = [ij for ij in zip(*locations)]
    n = len(locations)

    M = zeros(grid_size)
    for k, ij in enumerate(locations):
        M[ij] = k+1

    def find(ij):
        return locations.index(ij)
  
    A = zeros((n, n))
    for k, ij in enumerate(locations): # row
        i, j = ij
        if i > 0 and free[i-1, j]:
            l = find((i-1, j))
            A[k, l] += 1.0
        if i < n_rows-1 and free[i+1, j]:
            l = find((i+1, j))
            A[k, l] += 1.0
        if j > 0 and free[i, j-1]:
            l = find((i, j-1))
            A[k, l] += 1.0
        if j < n_cols-1 and free[i, j+1]:
            l = find((i, j+1))
            A[k, l] += 1.0
        if free[ij]:
            A[k, k] -= sum(A[k,:])
    B = []
    for i in range(n_rows):
        for j in range(n_cols):
            if sources[i, j] != 0:
                k = find((i,j))
                column = zeros(n, dtype=float)
                column[k] = 1
                B.append(column)
    B = array(B).T          


    x0 = zeros(n)
    for k, ij in enumerate(locations):
        #print(k, ij, initial_temp[ij])
        x0[k] = initial_temp[ij]

    return A, B, x0, locations


free = [
    [1, 1, 1, 0, 1], 
    [1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1]
]


sources = [
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0]
]

initial_temp = [
    [   0.0,   0.0, 0, 0,  0.0], 
    [   0.0,   0.0, 0, 0,  0.0],
    [     0,     0, 0, 0,  0.0]
]


A, B, x0, locations = make_config(free, sources, initial_temp)



print(locations)
print(A)
print(B)

#print("x0", x0)

def to_image(x):
    M = ones_like(free) * nan
    for k, v in enumerate(x):
        #print(locations[k], v)
        M[locations[k]] = v
    masked_array = np.ma.array(M, mask=np.isnan(M))
    return masked_array

y0 = x0
t0, tf = 0.0, 60.0

def fun(t, y):
    return A @ y + B @ u(t)

def u(t):
    return [20.0]
#    if t <= 10.0:
#        return [10.0]
#    else:
#        return [0.0]

xt = solve_ivp(fun, y0=y0, t_span=(t0, tf), dense_output=True).sol

fps = 1.0
N = int(fps * (tf - t0)) + 1 # 60 fps
t = linspace(t0, tf, N)
x = xt(t)


def movie(t, x):
    fig = figure()
    #ion()
    set_cmap("viridis")
    cmap = matplotlib.cm.get_cmap()
    cmap.set_bad("grey",1.0)

    image = imshow(to_image(x[0]), interpolation="nearest", animated=True)
    gca().set_xticks([])
    gca().set_yticks([])
    clim(0, 100)
    colorbar()

    def update(t_x):
        t_, x_ = t_x
        image.set_array(to_image(x_))
        title_ = title(f"time: {t_:.2f}")
        clim(0, 100.0)
        #return image, title_

    anim = FuncAnimation(fig, update, frames=zip(t, x), interval=int(1000 / fps), 
                         repeat=False, blit=False)
    show()

C_K = [array(B, dtype=int64)]
Ai = array(A, dtype=int8)
for i in range(1, len(y0)):
    C_K += [Ai @ C_K[-1]]
C_K = concatenate(C_K, axis=1)
 

plot(t, x.T)
movie(t, x.T) 



