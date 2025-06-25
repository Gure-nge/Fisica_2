# logica_kirchhoff.py
import numpy as np

def resolver_mallas(R1, R2, R3, V1, V2):
    try:
        A = np.array([
            [R1 + R2, -R2],
            [-R2, R2 + R3]
        ])
        b = np.array([V1, V2])
        soluciones = np.linalg.solve(A, b)
        I1, I2 = soluciones
        return I1, I2
    except np.linalg.LinAlgError:
        return None, None
