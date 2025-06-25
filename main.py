# main.py
import matplotlib.pyplot as plt
from logica_kirchhoff import resolver_mallas

# Valores de prueba (puedes poner input si deseas)
R1, R2, R3 = 10, 5, 15
V1, V2 = 20, 10

I1, I2 = resolver_mallas(R1, R2, R3, V1, V2)

# Dibujo del circuito con Matplotlib
fig, ax = plt.subplots()
ax.axis("off")

# Componentes
ax.text(1, 3, f"V1 = {V1} V", fontsize=12)
ax.text(1, 2.5, f"R1 = {R1} Ω", fontsize=12)
ax.text(3.5, 2.5, f"R2 = {R2} Ω", fontsize=12)
ax.text(6, 2.5, f"R3 = {R3} Ω", fontsize=12)
ax.text(1, 1, f"V2 = {V2} V", fontsize=12)

# Corrientes
ax.text(2, 3.5, f"I1 = {I1:.2f} A", color="blue", fontsize=12)
ax.text(5, 1.5, f"I2 = {I2:.2f} A", color="red", fontsize=12)

# Líneas (simulan cables)
ax.plot([1, 3], [3, 3], color='black')  # R1
ax.plot([3, 5], [3, 3], color='black')  # R2
ax.plot([5, 7], [3, 3], color='black')  # R3
ax.plot([1, 1], [3, 1], color='black')  # V1
ax.plot([7, 7], [3, 1], color='black')  # bajada derecha
ax.plot([1, 7], [1, 1], color='black')  # base

# Flechas de corriente
ax.annotate('', xy=(2.5, 3.05), xytext=(1.5, 3.05), arrowprops=dict(facecolor='blue', arrowstyle='->'))
ax.annotate('', xy=(6.5, 3.05), xytext=(5.5, 3.05), arrowprops=dict(facecolor='red', arrowstyle='->'))

ax.set_title("Circuito visual - Leyes de Kirchhoff (2 mallas)", fontsize=14)
plt.show()
