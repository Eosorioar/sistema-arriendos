from controlador.validations import inicial, validarLogin
from controlador.dto_empleado import EmpleadoDTO
from utils.encoder import Encoder

def menuAccesoUsuarios():
    print("""
||------------------------||
||   SISTEMA DE ARRIENDOS ||
||------------------------||
||1. Login de acceso      ||
||2. Crear cuenta empleado||
||------------------------||
""")

def crearCuentaEmpleado():
    print("\n=== CREAR CUENTA DE EMPLEADO ===")
    run = input("Ingrese RUN: ")
    nombre = input("Ingrese nombre: ")
    apellido = input("Ingrese apellido: ")
    codigo = int(input("Ingrese código de empleado: "))
    cargo = input("Ingrese cargo: ")
    password = input("Ingrese contraseña: ")
    
    # Verificar si el empleado ya existe
    empleado_existente = EmpleadoDTO().buscarEmpleado(run)
    if empleado_existente is not None:
        print("❌ El empleado ya existe en el sistema")
        return False
    
    # Crear nuevo empleado
    resultado = EmpleadoDTO().agregarEmpleado(run, nombre, apellido, codigo, cargo, password)
    print(f"✅ {resultado}")
    return True

def main():
    print("\n" + "="*50)
    print("       SISTEMA DE GESTIÓN DE ARRIENDOS")
    print("="*50)
    
    menuAccesoUsuarios()
    opc = input("Ingrese opción: ")
    
    if opc == '1':
        ##### LOGIN CON EMPLEADO #####
        intentos = 1
        while intentos <= 3:
            try:
                resu = validarLogin()  # Este pide RUN y password
                if resu is not None:
                    print(f"\n✅ Bienvenido(a) Sr(a). {resu.getNombre()} {resu.getApellido()}")
                    print(f"📋 Cargo: {resu.getCargo()}")
                    print("="*50)
                    inicial()
                    break
                else:
                    print("❌ RUN o contraseña incorrecta")
                    intentos += 1
                    if intentos <= 3:
                        print(f"📝 Intentos restantes: {4 - intentos}")
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Intente nuevamente")
                
        if intentos == 4:
            print("🚫 Contraseña bloqueada - Demasiados intentos fallidos")
            
    elif opc == '2':
        ##### CREAR CUENTA EMPLEADO #####
        try:
            crearCuentaEmpleado()
        except Exception as e:
            print(f"❌ Error al crear cuenta: {e}")
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()