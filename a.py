import matplotlib.pyplot as plt

# Obtener las resistencias del usuario
R1 = float(input("Ingrese el valor de R1 en ohms: "))
R2 = float(input("Ingrese el valor de R2 en ohms: "))
R3 = float(input("Ingrese el valor de R3 en ohms: "))
R4 = float(input("Ingrese el valor de R4 en ohms: "))
R5 = float(input("Ingrese el valor de R5 en ohms: "))

# Obtener el voltaje del usuario
F1 = float(input("Ingrese el valor de la fuente 1 en voltios: "))
F2 = float(input("Ingrese el valor de la fuente 2 en voltios: "))

# Ley de voltajes
I2 = (-F1*R2 + F2*R1 + F2*R2 + F2*R4)/(R1*R2 + R1*R3 + R1*R5 + R2*R3 + R2*R4 + R2*R5 + R3*R4 + R4*R5)
I1 = (F1 - (I2*R2))/(R1 + R2 + R4)

# Ley de corrientes
I3 = I1 + I2

# Resultados
print("Resultados:")
print(f"Corriente I1 = {I1:.2f} A")
print(f"Corriente I2 = {I2:.2f} A")
print(f"Corriente I3 = {I3:.2f} A")

# Resolución de voltajes
V1 = I1 * R1
V2 = I3 * R2
V3 = I2 * R4
Voltaje_malla_1 = V1 + V2 + V3

V4 = I1 * R3
V5 = I3 * R2
V6 = I2 * R5
Voltaje_malla_2 = V4 + V5 + V6

print(f"Voltaje_malla_1 = {Voltaje_malla_1} V")
print(f"Voltaje_malla_2 = {Voltaje_malla_2} V")

# Dibujo del circuito
fig, ax = plt.subplots()

# Resistencias
ax.plot([0, 2], [0, 0], 'b', lw=2, label=f'R1 ({R1} ohmios)')
ax.plot([2, 4], [0, 0], 'r', lw=2, label=f'R3 ({R3} ohmios)')
ax.plot([2, 2], [0, -2], 'g', lw=2, label=f'R2 ({R2} ohmios)')
ax.plot([0, 2], [-2, -2], 'y', lw=2, label=f'R4 ({R4} ohmios)')
ax.plot([2, 4], [-2, -2], 'm', lw=2, label=f'R5 ({R5} ohmios)')

# Fuente de voltaje V1
ax.arrow(0, 0, 0.2, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
plt.text(0.1, 0.1, f'V1 = {F1}V', fontsize=12, ha='center')

# Fuente de voltaje V2
ax.arrow(4, 0, -0.2, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
plt.text(4.1, 0.1, f'V2 = {F2}V', fontsize=12, ha='center')

# Etiquetas de resistencias
plt.text(1, 0.1, 'R1', fontsize=12, ha='center', color='blue')
plt.text(3, 0.1, 'R3', fontsize=12, ha='center', color='red')
plt.text(2.2, -1, 'R2', fontsize=12, ha='center', color='green')
plt.text(1, -1.9, 'R4', fontsize=12, ha='center', color='yellow')
plt.text(3, -1.9, 'R5', fontsize=12, ha='center', color='magenta')

# Corrientes con ajuste de etiquetas
plt.arrow(0.8, 0, 0.5, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
plt.annotate(f'I1 = {I1:.2f}A', xy=(0.5, -1.0), fontsize=12, ha='center', xytext=(1.0, -1.0))
plt.arrow(3.2, 0, -0.5, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
plt.annotate(f'I2 = {I2:.2f}A', xy=(0.5, -1.0), fontsize=12, ha='center', xytext=(3.0, -1.0))
plt.arrow(2, -1.2, 0, -0.5, head_width=0.1, head_length=0.1, fc='black', ec='black')
plt.annotate(f'I3 = {I3:.2f}A', xy=(2, -1.5), fontsize=12, ha='center', xytext=(2.2, -1.5))

# Nodo A
ax.plot(2, 0, 'bo')
plt.text(2.1, 0.1, 'A', fontsize=12, ha='center')

# Malla cerrada
ax.plot([0, 4, 4, 0, 0], [0, 0, -2, -2, 0], 'k--')

# Configuraciones del grafico
plt.xlabel('x')
plt.ylabel('y')
plt.title('Leyes de Corrientes y Voltajes de Kirchhoff')
plt.grid(True)
plt.axis('equal')
plt.xlim(-1, 5)
plt.ylim(-4, 1)
plt.legend()
plt.show()