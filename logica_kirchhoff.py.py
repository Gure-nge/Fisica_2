# logica_kirchhoff.py
import numpy as np

def resolver_2_mallas():
    print("=== Resolución de circuito con 2 mallas (Leyes de Kirchhoff) ===")

    # Solicitar valores al usuario
    try:
        R1 = float(input("R1 (resistencia en malla 1): "))
        R2 = float(input("R2 (resistencia compartida entre mallas): "))
        R3 = float(input("R3 (resistencia en malla 2): "))
        V1 = float(input("V1 (fuente en malla 1): "))
        V2 = float(input("V2 (fuente en malla 2): "))
    except ValueError:
        print("⚠️ Entrada inválida. Usa solo números.")
        return

    # Matriz de coeficientes (A) y vector de términos independientes (b)
    A = np.array([
        [R1 + R2, -R2],
        [-R2, R2 + R3]
    ])
    b = np.array([V1, V2])

    # Resolver el sistema
    try:
        soluciones = np.linalg.solve(A, b)
        I1, I2 = soluciones
        print(f"\nResultado:")
        print(f"I1 (corriente en malla 1) = {I1:.4f} A")
        print(f"I2 (corriente en malla 2) = {I2:.4f} A")
    except np.linalg.LinAlgError:
        print("⚠️ El sistema no tiene solución única (matriz singular). Revisa los datos.")
