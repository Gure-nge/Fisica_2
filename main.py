# main.py
from logica_kirchhoff import resolver_2_mallas

def mostrar_menu():
    while True:
        print("\n=== Simulador de Leyes de Kirchhoff ===")
        print("1. Resolver circuito de 2 mallas")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            resolver_2_mallas()
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    mostrar_menu()
