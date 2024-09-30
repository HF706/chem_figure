import numpy as np
import matplotlib.pyplot as plt

# 定义 x 和 y 的范围
x = np.linspace(0, 60, 1000)
y = np.linspace(0, 14, 1000)
X, Y = np.meshgrid(x, y)

# H2A 分布分数，Y 为 pH，a2 为 H2A，a1 为 HA-，a0 为 A2-
a2 = 10**(-2*Y)
a1 = 10**(-Y-6.36)
a0 = 10**(-6.36-10.33)
# 分析浓度，Na2CO3 浓度为 A，盐酸浓度为 B
A = 0.1*20/(20+X)
B = 0.1*X/(20+X)
# 计算函数值
Z = 10**(-Y) - 10**(Y-14) + 2*A -B - 2*A*a0/(a2+a1+a0) - A*a1/(a2+a1+a0)

# 绘制等高线并保存数据
contours = plt.contour(X, Y, Z, levels=[0], colors='blue')

# 使用 contours.allsegs 获取等高线数据并保存到文件
with open('data.dat', 'w') as datfile:
    for seg_collection in contours.allsegs:
        for seg in seg_collection:
            for x_point, y_point in seg:
                datfile.write(f'{x_point} {y_point}\n')
            datfile.write('\n')  # 添加空行以区分不同的等高线段

# 显示绘制的图像
plt.grid(True)
plt.show()

# 读取等高线数据并计算 dY/dX
# 读取等高线数据
x_vals = []
y_vals = []
with open('data.dat', 'r') as datfile:
    for line in datfile:
        if line.strip():  # 跳过空行
            x_point, y_point = map(float, line.split())
            x_vals.append(x_point)
            y_vals.append(y_point)

x_vals = np.array(x_vals)
y_vals = np.array(y_vals)

# 对 Y 相对于 X 求导
dy_dx = np.gradient(y_vals, x_vals)

# 将导数数据保存到新的 dat 文件
with open('derivative_data.dat', 'w') as datfile:
    for x_point, dy_dx_val in zip(x_vals, dy_dx):
        datfile.write(f'{x_point} {dy_dx_val}\n')

#  绘制 dY/dX 对 X 的图像
plt.plot(x_vals, dy_dx, label='dY/dX')

# 添加标签和标题
plt.xlabel('X')
plt.ylabel('dY/dX')
plt.title('dY/dX vs X')

# 显示图像
plt.grid(True)
plt.legend()
plt.show()
