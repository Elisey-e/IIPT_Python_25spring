import numpy as np
from scipy.interpolate import interp2d
from scipy.optimize import minimize

def create_constant_grid(nx, ny):
    return np.random.rand(nx, ny)

def create_linear_grid(nx, ny):
    return np.random.rand(nx, ny)

def bilinear_interpolation(x, y, grid):
    nx, ny = grid.shape
    x_idx = int(x * (nx - 1))
    y_idx = int(y * (ny - 1))
    x_frac = x * (nx - 1) - x_idx
    y_frac = y * (ny - 1) - y_idx

    interpolated_value = (grid[x_idx, y_idx] * (1 - x_frac) * (1 - y_frac) +
                          grid[x_idx + 1, y_idx] * x_frac * (1 - y_frac) +
                          grid[x_idx, y_idx + 1] * (1 - x_frac) * y_frac +
                          grid[x_idx + 1, y_idx + 1] * x_frac * y_frac)
    return interpolated_value

def l2_norm_interpolation(grid1, grid2):
    def objective(params):
        nx, ny = grid1.shape
        error = 0
        for i in range(nx):
            for j in range(ny):
                x = i / (nx - 1)
                y = j / (ny - 1)
                interpolated_value = bilinear_interpolation(x, y, grid2)
                error += (grid1[i, j] - interpolated_value) ** 2
        return error

    initial_params = np.zeros(grid2.shape)
    result = minimize(objective, initial_params, method='BFGS')
    return result.x

nx, ny = 10, 10
constant_grid1 = create_constant_grid(nx, ny)
constant_grid2 = create_constant_grid(nx, ny)
linear_grid1 = create_linear_grid(nx, ny)
linear_grid2 = create_linear_grid(nx, ny)

# Билинейная интерполяция между двумя сетками с постоянными базисными функциями
interpolated_constant = bilinear_interpolation(0.5, 0.5, constant_grid2)

# Оптимизация по L2 норме между двумя сетками с постоянными базисными функциями

#optimized_constant_grid = l2_norm_interpolation(constant_grid1, constant_grid2)

# Билинейная интерполяция между двумя сетками с кусочно-линейными аппроксимациями
interpolated_linear = bilinear_interpolation(0.5, 0.5, linear_grid2)

# Оптимизация по L2 норме между двумя сетками с кусочно-линейными аппроксимациями

#optimized_linear_grid = l2_norm_interpolation(linear_grid1, linear_grid2)

print("Interpolated value (constant grids):", interpolated_constant)
#print("Optimized grid (constant grids):", optimized_constant_grid)
print("Interpolated value (linear grids):", interpolated_linear)
#print("Optimized grid (linear grids):", optimized_linear_grid)