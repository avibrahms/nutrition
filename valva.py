import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Crear datos para la superficie 3D
X = np.linspace(-5, 5, 50)
Y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Crear una figura
fig = plt.figure()

# Agregar un subplot 3D
ax = fig.add_subplot(111, projection='3d')

# Dibujar la superficie
surf = ax.plot_surface(X, Y, Z, cmap='viridis')

# Agregar una barra de colores
fig.colorbar(surf)

# Mostrar la figura
plt.show()
