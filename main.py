from controlador.validations import validarLogin, menuPrincipal
from utils.encoder import Encoder

print("=== Sistema de Gestión de Arriendos ===")
#BUCLE DE INICIO DE SESION CON 3 INTENTOS 
intentos = 1
while intentos <= 3:
    try:
        empleado = validarLogin()
        if empleado is not None:
            print(f"\n Bienvenido(a) empleado #{empleado.getRun()} - Cargo: {empleado.getCargo()}\n")  
            menuPrincipal(empleado)   
            break
        else:
            print(" Usuario o contraseña incorrecta.")
            intentos += 1
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        intentos += 1

if intentos == 4:
    print(" Contraseña bloqueada. Contacte al administrador.")          