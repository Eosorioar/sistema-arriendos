from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_cliente import ClienteDTO
from controlador.dto_vehiculo import VehiculoDTO
from controlador.dto_arriendo import ArriendoDTO
from modelo.empleado import Empleado
from modelo.cliente import Cliente
from modelo.vehiculo import Vehiculo
from modelo.arriendo import Arriendo
import msvcrt
import sys 
import re 
# ========== VALIDACIONES ENTRADA ==========
def validar_run(run):
    """
    Valida formato de RUN chileno (12345678-9 o 12345678-K)
    """
    if not run.strip():
        return False, "❌ El RUN no puede estar vacío"
    
    # Convertir 'k' a 'K' para consistencia
    run = run.upper()
    
    # Validar formato con soporte para K
    if not re.match(r'^[0-9]{7,8}-[0-9K]{1}$', run):
        return False, "❌ Formato de RUN inválido. Debe ser: 12345678-9 o 12345678-K"
    
    return True, run

def validar_contraseña_segura(contraseña, max_caracteres=30):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad
    """
    if len(contraseña) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if len(contraseña) > max_caracteres:
        return False, f"La contraseña no puede tener más de {max_caracteres} caracteres"
    
    if not re.search(r'[A-Z]', contraseña):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    if not re.search(r'[a-z]', contraseña):
        return False, "La contraseña debe contener al menos una minúscula"
    
    if not re.search(r'\d', contraseña):
        return False, "La contraseña debe contener al menos un número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
        return False, "La contraseña debe contener al menos un carácter especial (!@#$%^&* etc.)"
    
    return True, "Contraseña válida"

def input_contraseña_segura():
    """
    Solicita una contraseña y valida que cumpla con los requisitos de seguridad
    """
    while True:
        contraseña = input("Ingrese contraseña: ")
        es_valida, mensaje = validar_contraseña_segura(contraseña, 30)  # ← Agregar el límite
        
        if es_valida:
            # Confirmar contraseña
            confirmacion = input("Confirme la contraseña: ")
            if contraseña == confirmacion:
                return contraseña
            else:
                print("❌ Las contraseñas no coinciden. Intente nuevamente.\n")
        else:
            print(f"❌ {mensaje}. Intente nuevamente.\n")

def validar_texto(valor, campo="valor", max_caracteres=30):
    """
    Valida que el string contenga solo letras, espacios y algunos caracteres especiales
    con límite mínimo y máximo
    """
    if not valor.strip():
        return False, f"❌ El {campo} no puede estar vacío"
    
    # Permitir letras, espacios, acentos, ñ, y algunos caracteres especiales comunes
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$', valor):
        return False, f"❌ El {campo} solo puede contener letras y espacios"
    
    if len(valor.strip()) < 2:
        return False, f"❌ El {campo} debe tener al menos 2 caracteres"
    
    if len(valor.strip()) > max_caracteres:
        return False, f"❌ El {campo} no puede tener más de {max_caracteres} caracteres"
    
    return True, "✅ Válido"

def validar_telefono(telefono):
    """
    Valida que el teléfono tenga exactamente 8 dígitos (sin contar el +569)
    """
    telefono_limpio = telefono.strip()
    
    if not telefono_limpio:
        return False, "❌ El teléfono no puede estar vacío"
    
    # Remover espacios, guiones, paréntesis si el usuario los ingresa
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono_limpio)
    
    # Validar que tenga exactamente 8 dígitos
    if not re.match(r'^\d{8}$', telefono_limpio):
        return False, "❌ El teléfono debe tener exactamente 8 dígitos (ej: 12345678)"
    
    return True, telefono_limpio

def validar_direccion(direccion, max_caracteres=20):
    """
    Valida que la dirección contenga texto y números con límite máximo
    """
    if not direccion.strip():
        return False, "❌ La dirección no puede estar vacía"
    
    if len(direccion.strip()) < 5:
        return False, "❌ La dirección debe tener al menos 5 caracteres"
    
    if len(direccion.strip()) > max_caracteres:
        return False, f"❌ La dirección no puede tener más de {max_caracteres} caracteres"
    
    # Verificar que tenga al menos una letra y un número
    if not re.search(r'[a-zA-Z]', direccion) or not re.search(r'\d', direccion):
        return False, "❌ La dirección debe contener texto y números (ej: Av. Principal 123)"
    
    return True, "✅ Dirección válida"

# ========== VALIDACIONES EMPLEADO ==========

def listAllEmpleados():
    print("\n=== LISTADO DE EMPLEADOS ===")
    resultado = EmpleadoDTO().listarEmpleados()
    if len(resultado) > 0:
        for emp in resultado:
            print(emp)
    else:
        print("No hay empleados registrados")

def validateFindEmpleado():
    run = input("Ingrese el RUN del empleado a buscar: ")
    if run == "":
        print("RUN incorrecto")
        return validateFindEmpleado()
    else:
        resu = EmpleadoDTO().buscarEmpleado(run)
        if resu is not None:
            print(f"Resultado: {resu}")
        else:
            print("Empleado no encontrado")

def validaDelEmpleado():
    run = input("Ingrese el RUN del empleado a eliminar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validaDelEmpleado()
    
    
    resu = EmpleadoDTO().buscarEmpleado(run)
    
    if resu is not None:
        print("Datos -->", resu)
        respuesta = input("¿Está seguro de la eliminación? [s/n]: ")
        if respuesta.lower() == "s":  
            print(EmpleadoDTO().eliminarEmpleado(run))
        else:
            print("Eliminación cancelada")
    else:
        print("Empleado no encontrado")



def validateUpdateEmpleado():
    while True:
        try:
            print("\n--- ACTUALIZAR EMPLEADO ---")
            run = input("Ingrese el RUN del empleado a modificar (o '0' para volver): ").strip()
            
            if run == '0':
                print("Volviendo al menú anterior...")
                break
            
            if len(run) == 0:
                print("❌ Debe ingresar un RUN")
                continue
            
            es_valido, run_limpio = validar_run(run)
            if not es_valido:
                print(run_limpio)  # Mensaje de error
                continue
            run = run_limpio  # Usar RUN limpio (K reemplazado si aplica)

            resu = EmpleadoDTO().buscarEmpleado(run)
            
            if resu is None:
                print("❌ Empleado no encontrado")
                continuar = input("¿Buscar otro empleado? (S/N): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                continue
            
            print("Datos actuales -->", resu)
            
            # Obtener datos actuales
            nombre_actual = resu.getNombre()
            apellido_actual = resu.getApellido()
            cargo_actual = resu.getCargo()
            clave_actual = resu.getPassword()
            
            # Solicitar nuevo nombre con validación
            while True:
                nombre_input = input(f"Ingrese nuevo nombre [{nombre_actual}]: ").strip()
                if nombre_input == "":
                    nombre = nombre_actual
                    break
                es_valido, mensaje = validar_texto(nombre_input, "nombre")
                if es_valido:
                    nombre = nombre_input
                    break
                print(mensaje)
            
            # Solicitar nuevo apellido con validación
            while True:
                apellido_input = input(f"Ingrese nuevo apellido [{apellido_actual}]: ").strip()
                if apellido_input == "":
                    apellido = apellido_actual
                    break
                es_valido, mensaje = validar_texto(apellido_input, "apellido")
                if es_valido:
                    apellido = apellido_input
                    break
                print(mensaje)
            
            # Solicitar nuevo cargo con validación
            cargos_permitidos = ['gerente', 'empleado']
            while True:
                print(f"\nCargos permitidos: {', '.join(cargos_permitidos)}")
                cargo_input = input(f"Ingrese nuevo cargo [{cargo_actual}]: ").strip().lower()
                
                if cargo_input == "":
                    cargo = cargo_actual
                    break
                
                if cargo_input in cargos_permitidos:
                    cargo = cargo_input
                    break
                
                print(f"❌ Cargo inválido. Debe ser uno de: {', '.join(cargos_permitidos)}")
            
            # Manejo de contraseña
            print(f"\n--- Actualización de Contraseña ---")
            print("• Presione Enter para mantener la contraseña actual")
            print("• O ingrese una nueva contraseña con los requisitos de seguridad")
            print("--------------------------------\n")
            
            nueva_clave_input = input("Ingrese nueva contraseña (Enter para mantener actual): ").strip()
            
            if nueva_clave_input == "":
                clave = clave_actual
                print("✅ Contraseña actual mantenida")
            else:
                es_valida, mensaje = validar_contraseña_segura(nueva_clave_input)
                if es_valida:
                    confirmacion = input("Confirme la nueva contraseña: ").strip()
                    if nueva_clave_input == confirmacion:
                        clave = nueva_clave_input
                        print("✅ Contraseña actualizada correctamente")
                    else:
                        print("❌ Las contraseñas no coinciden. Se mantendrá la contraseña actual.")
                        clave = clave_actual
                else:
                    print(f"❌ {mensaje}. Se mantendrá la contraseña actual.")
                    clave = clave_actual
            
            # Mostrar resumen y confirmar
            print(f"\n--- RESUMEN DE CAMBIOS ---")
            print(f"RUN: {run}")
            print(f"Nombre: {nombre_actual} → {nombre}")
            print(f"Apellido: {apellido_actual} → {apellido}")
            print(f"Cargo: {cargo_actual} → {cargo}")
            print("Contraseña: " + ("Actualizada" if nueva_clave_input else "Mantenida"))
            print("---------------------------")
            
            confirmar = input("¿Confirmar actualización? (S/N): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Actualización cancelada")
                continuar = input("¿Actualizar otro empleado? (S/N): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                continue
            
            # Ejecutar actualización

            resultado = EmpleadoDTO().actualizarEmpleado(run, nombre, apellido, cargo, clave)
            print(f"✅ {resultado}")
            
            # Preguntar si quiere actualizar otro
            otro = input("¿Actualizar otro empleado? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break

def validateAddEmpleado():
    while True:  # Bucle principal para permanecer en la función
        try:
            print("\n--- AGREGAR EMPLEADO ---")
            run = input("Ingrese RUN del empleado (o '0' para volver): ").strip()
            
            # Opción para salir
            if run == '0':
                print("Volviendo al menú anterior...")
                break
            
            if len(run) == 0:
                print("❌ Debe ingresar un RUN")
                continue  # Vuelve al inicio del bucle
            
            # Validar formato básico de RUN
            es_valido, run_limpio = validar_run(run)
            if not es_valido:
                print(run_limpio)  # Mensaje de error
                continue
            run = run_limpio  # Usar RUN limpio (K reemplazado si aplica)
            
            # Verificar si el empleado ya existe
            resu = EmpleadoDTO().buscarEmpleado(run)
            
            if resu is not None:
                print(f"❌ El empleado con RUN {run} ya existe:")
                print(f"   {resu}")
                continue
            
            # Solicitar nombre (SOLO TEXTO)
            while True:
                nombre = input("Ingrese nombre: ").strip()
                es_valido, mensaje = validar_texto(nombre, "nombre")
                if es_valido:
                    break
                print(mensaje)
            
            # Solicitar apellido (SOLO TEXTO)
            while True:
                apellido = input("Ingrese apellido: ").strip()
                es_valido, mensaje = validar_texto(apellido, "apellido")
                if es_valido:
                    break
                print(mensaje)
            
            # Solicitar código
            while True:
                try:
                    codigo_input = input("Ingrese código: ").strip()
                    if codigo_input == '':  # Permitir campo opcional?
                        codigo = 0
                        break
                    
                    codigo = int(codigo_input)
                    if codigo <= 0:
                        print("❌ El código debe ser un número positivo")
                        continue
                    break
                except ValueError:
                    print("❌ El código debe ser un número válido")
            
            # Solicitar cargo
            cargos_permitidos = ['gerente', 'empleado']
            while True:
                print(f"\nCargos permitidos: {', '.join(cargos_permitidos)}")
                cargo = input("Ingrese cargo: ").strip().lower()
                
                if cargo == '':
                    print("❌ Debe seleccionar un cargo")
                    continue
                
                if cargo not in cargos_permitidos:
                    print(f"❌ Cargo inválido. Debe ser uno de: {', '.join(cargos_permitidos)}")
                    continue
                break
            
            # Solicitar contraseña
            print("\n--- Requisitos de Contraseña ---")
            print("• Mínimo 8 caracteres")
            print("• Al menos una mayúscula y una minúscula") 
            print("• Al menos un número")
            print("• Al menos un carácter especial (!@#$%^&* etc.)")
            print("--------------------------------\n")
            
            clave = input_contraseña_segura()
            
            # Confirmar creación
            print(f"\n--- RESUMEN DEL NUEVO EMPLEADO ---")
            print(f"RUN: {run}")
            print(f"Nombre: {nombre} {apellido}")
            print(f"Código: {codigo}")
            print(f"Cargo: {cargo}")
            print("-----------------------------------")
            
            confirmar = input("¿Confirmar creación? (S/N): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Creación cancelada")
                continue
            
            # Crear empleado
            
            resultado = EmpleadoDTO().agregarEmpleado(run, nombre, apellido, codigo, cargo, clave)
            print(f"✅ {resultado}")
            
            # Preguntar si quiere agregar otro
            otro = input("¿Agregar otro empleado? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break





# ========== VALIDACIONES CLIENTE ==========

def listAllClientes():
    print("\n=== LISTADO DE CLIENTES ===")
    resultado = ClienteDTO().listarClientes()
    if len(resultado) > 0:
        for cli in resultado:
            print(cli)
    else:
        print("No hay clientes registrados")

def validateFindCliente():
    run = input("Ingrese el RUN del cliente a buscar: ")
    if run == "":
        print("RUN incorrecto")
        return validateFindCliente()
    else:
        resu = ClienteDTO().buscarCliente(run)
        if resu is not None:
            print(f"Resultado: {resu}")
        else:
            print("Cliente no encontrado")

def validaDelCliente():
    run = input("Ingrese el RUN del cliente a eliminar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validaDelCliente()
    
    resu = ClienteDTO().buscarCliente(run)
    
    if resu is not None:
        print("Datos -->", resu)
        respuesta = input("¿Está seguro de la eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            
            print(ClienteDTO().eliminarCliente(run))
        else:
            print("Eliminación cancelada")
    else:
        print("Cliente no encontrado")

def validateAddCliente():
    while True:
        try:
            print("\n--- AGREGAR CLIENTE ---")
            run = input("Ingrese RUN del cliente (o '0' para volver): ").strip()
            
            if run == '0':
                print("Volviendo al menú anterior...")
                break
                
            if len(run) == 0:
                print("❌ Debe ingresar un RUN")
                continue
            
            es_valido, run_limpio = validar_run(run)
            if not es_valido:
                print(run_limpio)  # Mensaje de error
                continue
            run = run_limpio  # Usar RUN limpio (K reemplazado si aplica)
            
            # Verificar si el cliente ya existe
            resu = ClienteDTO().buscarCliente(run)
            
            if resu is not None:
                print(f"❌ El cliente con RUN {run} ya existe:")
                print(f"   {resu}")
                continue
            
            # Solicitar nombre (solo texto)
            while True:
                nombre = input("Ingrese nombre: ").strip()
                es_valido, mensaje = validar_texto(nombre, "nombre")
                if es_valido:
                    break
                print(mensaje)
            
            # Solicitar apellido (solo texto)
            while True:
                apellido = input("Ingrese apellido: ").strip()
                es_valido, mensaje = validar_texto(apellido, "apellido")
                if es_valido:
                    break
                print(mensaje)
            
            # Solicitar teléfono (8 dígitos)
            while True:
                telefono_input = input("Ingrese teléfono (+569): ").strip()
                es_valido, mensaje = validar_telefono(telefono_input)
                if es_valido:
                    telefono = mensaje  # mensaje contiene el teléfono limpio
                    break
                print(mensaje)
            
            # Solicitar dirección (texto y números)
            while True:
                direccion = input("Ingrese dirección: ").strip()
                es_valido, mensaje = validar_direccion(direccion)
                if es_valido:
                    break
                print(mensaje)
            
            # Confirmar creación
            print(f"\n--- RESUMEN DEL NUEVO CLIENTE ---")
            print(f"RUN: {run}")
            print(f"Nombre: {nombre} {apellido}")
            print(f"Teléfono: +569{telefono}")
            print(f"Dirección: {direccion}")
            print("-----------------------------------")
            
            confirmar = input("¿Confirmar creación? (S/N): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Creación cancelada")
                continue
            
            resultado = ClienteDTO().agregarCliente(run, nombre, apellido, telefono, direccion)
            print(f"✅ {resultado}")
            
            # Preguntar si quiere agregar otro
            otro = input("¿Agregar otro cliente? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break

def validateUpdateCliente():
    while True:
        try:
            print("\n--- ACTUALIZAR CLIENTE ---")
            run = input("Ingrese el RUN del cliente a modificar (o '0' para volver): ").strip()
            
            if run == '0':
                print("Volviendo al menú anterior...")
                break
                
            if len(run) == 0:
                print("❌ Debe ingresar un RUN")
                continue
            
            es_valido, run_limpio = validar_run(run)
            if not es_valido:
                print(run_limpio)  # Mensaje de error
                continue
            run = run_limpio  # Usar RUN limpio (K reemplazado si aplica)
            
            resu = ClienteDTO().buscarCliente(run)
            
            if resu is None:
                print("❌ Cliente no encontrado")
                continuar = input("¿Buscar otro cliente? (S/N): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                continue
            
            print("Datos actuales -->", resu)
            
            # Obtener datos actuales
            nombre_actual = resu.getNombre()
            apellido_actual = resu.getApellido()
            telefono_actual = resu.getTelefono()
            direccion_actual = resu.getDireccion()
            
            # Solicitar nuevo nombre
            while True:
                nombre_input = input(f"Ingrese nuevo nombre [{nombre_actual}]: ").strip()
                if nombre_input == "":
                    nombre = nombre_actual
                    break
                es_valido, mensaje = validar_texto(nombre_input, "nombre")
                if es_valido:
                    nombre = nombre_input
                    break
                print(mensaje)
            
            # Solicitar nuevo apellido
            while True:
                apellido_input = input(f"Ingrese nuevo apellido [{apellido_actual}]: ").strip()
                if apellido_input == "":
                    apellido = apellido_actual
                    break
                es_valido, mensaje = validar_texto(apellido_input, "apellido")
                if es_valido:
                    apellido = apellido_input
                    break
                print(mensaje)
            
            # Solicitar nuevo teléfono
            while True:
                telefono_input = input(f"Ingrese nuevo teléfono (+569) [{telefono_actual}]: ").strip()
                if telefono_input == "":
                    telefono = telefono_actual
                    break
                es_valido, mensaje = validar_telefono(telefono_input)
                if es_valido:
                    telefono = mensaje  # teléfono limpio
                    break
                print(mensaje)
            
            # Solicitar nueva dirección
            while True:
                direccion_input = input(f"Ingrese nueva dirección [{direccion_actual}]: ").strip()
                if direccion_input == "":
                    direccion = direccion_actual
                    break
                es_valido, mensaje = validar_direccion(direccion_input)
                if es_valido:
                    direccion = direccion_input
                    break
                print(mensaje)
            
            # Mostrar resumen y confirmar
            print(f"\n--- RESUMEN DE CAMBIOS ---")
            print(f"RUN: {run}")
            print(f"Nombre: {nombre_actual} → {nombre}")
            print(f"Apellido: {apellido_actual} → {apellido}")
            print(f"Teléfono: {telefono_actual} → +569{telefono}")
            print(f"Dirección: {direccion_actual} → {direccion}")
            print("---------------------------")
            
            confirmar = input("¿Confirmar actualización? (S/N): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Actualización cancelada")
                continuar = input("¿Actualizar otro cliente? (S/N): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                continue

            resultado = ClienteDTO().actualizarCliente(run, nombre, apellido, telefono, direccion)
            print(f"✅ {resultado}")
            
            # Preguntar si quiere actualizar otro
            otro = input("¿Actualizar otro cliente? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break

# ========== VALIDACIONES VEHÍCULO ==========

def listAllVehiculos():
    print("\n=== LISTADO DE VEHÍCULOS ===")
    resultado = VehiculoDTO().listarVehiculos()
    if len(resultado) > 0:
        for veh in resultado:
            print(veh)
    else:
        print("No hay vehículos registrados")

def listVehiculosDisponibles():
    print("\n=== VEHÍCULOS DISPONIBLES ===")
    resultado = VehiculoDTO().listarVehiculosDisponibles()
    if len(resultado) > 0:
        for veh in resultado:
            print(veh)
    else:
        print("No hay vehículos disponibles")

def validateFindVehiculo():
    patente = input("Ingrese la patente del vehículo a buscar: ")
    if patente == "":
        print("Patente incorrecta")
        return validateFindVehiculo()
    else:
      
        vehiculo_buscar = Vehiculo(patente, "", "", 0, 0, "")
        resu = VehiculoDTO().buscarVehiculo(vehiculo_buscar)
        if resu is not None:
            print(f"Resultado: {resu}")
        else:
            print("Vehículo no encontrado")

def validaDelVehiculo():
    patente = input("Ingrese la patente del vehículo a eliminar: ")
    if len(patente) == 0:
        print("Debe ingresar una patente")
        return validaDelVehiculo()
    
    vehiculo_buscar = Vehiculo(patente, "", "", 0, 0, "")
    resu = VehiculoDTO().buscarVehiculo(vehiculo_buscar)
    
    if resu is not None:
        print("Datos -->", resu)
        respuesta = input("¿Está seguro de la eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            vehiculo_eliminar = Vehiculo(patente, "", "", 0, 0, "")
            print(VehiculoDTO().eliminarVehiculo(vehiculo_eliminar))
        else:
            print("Eliminación cancelada")
    else:
        print("Vehículo no encontrado")

def validateUpdateVehiculo():
    patente = input("Ingrese la patente del vehículo a modificar: ")
    if len(patente) == 0:
        print("Debe ingresar una patente")
        return validateUpdateVehiculo()
    
    vehiculo_buscar = Vehiculo(patente, "", "", 0, 0, "")
    resu = VehiculoDTO().buscarVehiculo(vehiculo_buscar)
    
    if resu is not None:
        print("Datos actuales -->", resu)
        marca = input("Ingrese nueva marca: ")
        modelo = input("Ingrese nuevo modelo: ")
        año = int(input("Ingrese nuevo año: "))
        precio = float(input("Ingrese nuevo precio: "))
        disponible = input("Ingrese estado [disponible/arrendado]: ")
        
        vehiculo_actualizar = Vehiculo(patente, marca, modelo, año, precio, disponible)
        print(VehiculoDTO().actualizarVehiculo(vehiculo_actualizar))
    else:
        print("Vehículo no encontrado")

def validateAddVehiculo():
    patente = input("Ingrese patente del vehículo: ")
    if len(patente) == 0:
        print("Debe ingresar una patente")
        return validateAddVehiculo()
    
    vehiculo_buscar = Vehiculo(patente, "", "", 0, 0, "")
    resu = VehiculoDTO().buscarVehiculo(vehiculo_buscar)
    
    if resu is not None:
        print("Vehículo ya existe -->", resu)
    else:
        marca = input("Ingrese marca: ")
        modelo = input("Ingrese modelo: ")
        año = int(input("Ingrese año: "))
        precio = float(input("Ingrese precio: "))
        
        vehiculo_nuevo = Vehiculo(patente, marca, modelo, año, precio, "disponible")
        print(VehiculoDTO().agregarVehiculo(vehiculo_nuevo))

# ========== VALIDACIONES ARRIENDO ==========

def listAllArriendos():
    print("\n=== LISTADO DE ARRIENDOS ===")
    resultado = ArriendoDTO().listarArriendos()
    if len(resultado) > 0:
        for arr in resultado:
            print(arr)
    else:
        print("No hay arriendos registrados")

def validateFindArriendo():
    numArriendo = int(input("Ingrese el número de arriendo a buscar: "))
   
    arriendo_buscar = Arriendo(numArriendo, None, None, 0, None, None, None)
    resu = ArriendoDTO().buscarArriendo(arriendo_buscar)
    if resu is not None:
        print(f"Resultado: {resu}")
    else:
        print("Arriendo no encontrado")

def validateAddArriendo():
    print("\n=== NUEVO ARRIENDO ===")
    numArriendo = int(input("Ingrese número de arriendo: "))
    
  
    arriendo_buscar = Arriendo(numArriendo, None, None, 0, None, None, None)
    resu = ArriendoDTO().buscarArriendo(arriendo_buscar)
    
    if resu is not None:
        print("Arriendo ya existe -->", resu)
    else:
        fechaInicio = input("Ingrese fecha inicio (YYYY-MM-DD): ")
        fechaEntrega = input("Ingrese fecha entrega (YYYY-MM-DD): ")
        costoTotal = float(input("Ingrese costo total: "))
        run_cliente = input("Ingrese RUN del cliente: ")
        run_empleado = input("Ingrese RUN del empleado: ")
        patente_vehiculo = input("Ingrese patente del vehículo: ")
        
       
        cliente = Cliente(run_cliente, "", "", "", "")
        empleado = Empleado(run_empleado, "", "", 0, "", "")
        vehiculo = Vehiculo(patente_vehiculo, "", "", 0, 0, "")
        
        arriendo_nuevo = Arriendo(numArriendo, fechaInicio, fechaEntrega, costoTotal, cliente, empleado, vehiculo)
        print(ArriendoDTO().agregarArriendo(arriendo_nuevo))

def validaDelArriendo():
    print("\n=== ELIMINAR ARRIENDO ===")
    try:
        numArriendo = int(input("Ingrese número de arriendo a eliminar: "))
    except ValueError:
        print("❌ Debe ingresar un número válido")
        return
    
  
    arriendo_buscar = Arriendo(numArriendo, None, None, 0, None, None, None)
    arriendo = ArriendoDTO().buscarArriendo(arriendo_buscar)
    
    if arriendo:
        print(f"Datos del arriendo: {arriendo}")
        respuesta = input("¿Confirmar eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            resultado = ArriendoDTO().eliminarArriendo(arriendo)
            print(resultado)
    else:
        print("❌ Arriendo no encontrado")

# ========== VALIDACIÓN LOGIN ==========
def input_password(mensaje="Ingrese contraseña: "):
    print(mensaje, end='', flush=True)
    contraseña = ""
    while True:
        tecla = msvcrt.getch()
        if tecla == b'\r':  # Enter
            print()
            break
        elif tecla == b'\x08':  # Backspace
            if contraseña:
                contraseña = contraseña[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            contraseña += tecla.decode('utf-8')
            sys.stdout.write('*')
            sys.stdout.flush()
    return contraseña


def validarLogin():
    run = input("Ingrese RUN(sin puntos y con guion ): ")
    clave = input_password("Ingrese contraseña: ")
    
    
    empleado_login = Empleado(run, "", "", 0, "", clave)  
    resultado = EmpleadoDTO().validarLogin(empleado_login)
    return resultado

# ========== MENÚS ==========


def menuEmpleados(empleado):
    while True:
        print("\n=== GESTIÓN DE EMPLEADOS ===")
        print("1. Listar Empleados")
        
        if empleado.getCargo().strip().lower() == 'gerente':
            print("2. Agregar Empleado")
            print("3. Eliminar Empleado")
            print("4. Actualizar Empleado")
            print("5. Buscar Empleado")
            print("6. Volver al Menú Principal")
        else:
            print("2. Volver al Menú Principal")
        
        opc = input("Ingrese una opción: ")
        
        if empleado.getCargo().strip().lower() == 'gerente':
            if opc == "1":
                listAllEmpleados()
            elif opc == "2":
                validateAddEmpleado()
            elif opc == "3":
                validaDelEmpleado()
            elif opc == "4":
                validateUpdateEmpleado()
            elif opc == "5":
                validateFindEmpleado()
            elif opc == "6":
                return "6"
            else:
                print("Opción no válida")
        else:
            if opc == "1":
                listAllEmpleados()
            elif opc == "2":
                return "6"
            else:
                print("Opción no válida")

def menuClientes():
    while True:
        print("\n=== Gestión de Clientes ===")
        print("1. Listar clientes")
        print("2. Agregar cliente")
        print("3. Eliminar Cliente")
        print("4. Actualizar Cliente")
        print("5. Buscar Cliente")
        print("6. salir")
        opc = input("Seleccione una opción: ")

        if opc == "1":
            listAllClientes()
        elif opc == "2":
            validateAddCliente()
        elif opc == "3":
            validaDelCliente()
        elif opc == "4":
            validateUpdateCliente()
        elif opc == "5":
            validateFindCliente()
        elif opc == "6":
            break            
        else:
            print("Opción no válida.")

def menuVehiculos():
    while True:
        print("\n=== Gestión de Vehiculos ===")
        print("1. Listar vehiculos")
        print("2. Agregar vehiculo")
        print("3. Eliminar vehiculo")
        print("4. Actualizar vehiculo")
        print("5. Buscar vehiculo")
        print("6. salir")
        opc = input("Seleccione una opción: ")

        if opc == "1":
            listAllVehiculos()
        elif opc == "2":
            validateAddVehiculo()
        elif opc == "3":
            validaDelVehiculo()
        elif opc == "4":
            validateUpdateVehiculo()
        elif opc == "5":
            validateFindVehiculo()        
        elif opc == "6":
            break  
        else:
            print("Opción no válida.")

def menuArriendos():
    while True:
        print("\n=== Gestión de Arriendos ===")
        print("1. Listar arriendos")
        print("2. Agregar arriendo")
        print("3. Eliminar ariendo")
        print("4. Buscar arriendo")
        print("5. salir")
        opc = input("Seleccione una opción: ")

        if opc == "1":
            listAllArriendos()
        elif opc == "2":
            validateAddArriendo()
        elif opc == "3":
            validaDelArriendo()
        elif opc == "4":
            validateFindArriendo()
        elif opc == "5":
            break         
        else:
            print("Opción no válida.")

def menuPrincipal(empleado):
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Gestión de Clientes")
        print("2. Gestión de Vehículos")
        print("3. Gestión de Arriendos")
        print("4. Gestión de Empleados")
        print("5. Salir")
        
        opc = input("Seleccione una opción: ")

        if opc == "1":
            menuClientes()
        elif opc == "2":
            menuVehiculos()
        elif opc == "3":
            menuArriendos()
        elif opc == "4":
            opc_emp = menuEmpleados(empleado)
            if opc_emp == "6":
                continue
        elif opc == "5":
            print(" Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")