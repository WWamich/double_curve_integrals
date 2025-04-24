import numpy as np
import time
import matplotlib.pyplot as plt
 
def f(x, y):
    return (x + y), (2 * x * y)
 
def integrate_curve_trapezoidal(points):
    integral_sum = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        fx1, fy1 = f(x1, y1)
        fx2, fy2 = f(x2, y2)
        integral_sum += 0.5 * ((fx1 + fx2) * (x2 - x1) + (fy1 + fy2) * (y2 - y1))
    return integral_sum
 
def generate_curve_points(segment_length, radius):
    def calc_angle_step(seg_length, r):
        return 2 * np.arcsin(seg_length / (2 * r))
    start_angle = np.pi / 4
    end_angle = 5 * np.pi / 4
    angle_step = calc_angle_step(segment_length, radius)
    arc_points = []
    angle = start_angle
    while angle < end_angle:
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        arc_points.append((x, y))
        angle += angle_step
    arc_points.append((radius * np.cos(end_angle), radius * np.sin(end_angle)))
    line_points = []
    x_start, y_start = arc_points[-1]
    x_end, y_end = arc_points[0]
    steps_line = len(arc_points)
    for i in range(steps_line + 1):
        alpha = i / steps_line
        x_lin = x_start + alpha * (x_end - x_start)
        y_lin = y_start + alpha * (y_end - y_start)
        line_points.append((x_lin, y_lin))
    return np.array(arc_points + line_points)
 
deltas = [0.1, 0.01, 0.001]
radius = 2
results_curve = []
for delta in deltas:
    start_time_curve = time.time()
    points_S = generate_curve_points(delta, radius)
    integral_sum = integrate_curve_trapezoidal(points_S)
    end_time_curve = time.time()
    results_curve.append([integral_sum, end_time_curve - start_time_curve])
 
def integrate_double(delta):
    start_time = time.time()
    integral_sum = 0
    x = np.arange(-2, 2 + delta, delta)
    y = np.arange(-2, 2 + delta, delta)
    for i in range(len(x) - 1):
        for j in range(len(y) - 1):
            x_center = (x[i] + x[i + 1]) / 2
            y_center = (y[j] + y[j + 1]) / 2
            if x_center <= y_center and x_center**2 + y_center**2 <= 4:
                integral_sum += (2 * y_center - 1) * delta**2
    end_time = time.time()
    return integral_sum, end_time - start_time
 
results_double = []
for delta in deltas:
    integral_sum, time_elapsed = integrate_double(delta)
    results_double.append([integral_sum, time_elapsed])
 
truth_value = 1.25929
 
print("\nРезультаты для двойного интеграла:")
print("дельта | Интегральная сумма | Время (с) | Отклонение")
print("------ | ------------------ | --------- |-----------")
for i, delta in enumerate(deltas):
    err = truth_value - results_double[i][0]
    print(f"{delta:<5} | {results_double[i][0]:12.6f} | {results_double[i][1]:9.6f} | {err:12.6f}")
 
print("\nРезультаты для криволинейного интеграла:")
print("дельта | Интегральная сумма | Время (с) | Отклонение")
print("------ | ------------------ | --------- |-----------")
for i, delta in enumerate(deltas):
    err = truth_value - results_curve[i][0]
    print(f"{delta:<5} | {results_curve[i][0]:12.6f} | {results_curve[i][1]:9.6f} | {err:12.6f}")
 
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, delta in enumerate(deltas):
    points = generate_curve_points(delta, radius)
    x_vals, y_vals = points[:, 0], points[:, 1]
    t_full = np.linspace(np.pi / 4, 5 * np.pi / 4, 100)
    x_full = radius * np.cos(t_full)
    y_full = radius * np.sin(t_full)
    axes[i].plot(x_full, y_full, 'k--')
    axes[i].plot(x_vals, y_vals, marker='o', linestyle='-', markersize=3)
    axes[i].set_aspect('equal')
plt.tight_layout()
plt.show()
for b in deltas:
    x = np.arange(-2, 2 + b, b)
    y = np.arange(-2, 2 + b, b)
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(6, 6))
    plt.plot(X, Y, color='black', linewidth=0.5)
    plt.plot(X.T, Y.T, color='black', linewidth=0.5)
    plt.axis('equal')
    plt.show()
