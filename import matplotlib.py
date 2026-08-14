import matplotlib.pyplot as plt
import numpy as np

# Generate x values
x = np.linspace(0, np.pi, num=50)

# Compute sin(x) and cos(x)
y = np.sin(x)
z = np.cos(x)   # FIXED

# Plot graphs
plt.plot(x, y, color="red", marker="x", markersize=6, label="sin(x)")
plt.plot(x, z, color="pink", marker="o", markersize=3, label="cos(x)")

# Labels and title
plt.xlabel("value of x")
plt.ylabel("sin(x) / cos(x)")
plt.title("GRAPH OF SINX AND COSX")

# Legend
plt.legend()

# Show graph
plt.show()
OUTPUT:

