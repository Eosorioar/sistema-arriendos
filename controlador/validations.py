from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_cliente import ClienteDTO
from controlador.dto_vehiculo import VehiculoDTO
from controlador.dto_arriendo import ArriendoDTO
from modelo.empleado import Empleado
from modelo.cliente import Cliente
from modelo.vehiculo import Vehiculo
from modelo.arriendo import Arriendo
from dao.dao_persona import daoPersona 
import msvcrt
import sys 
import re 
from datetime import datetime, timedelta
# ========== VALIDACIONES ENTRADA ==========
def validar_codigo_empleado(codigo_input, empleado_dto):
    """
    Valida que el código sea único y válido
    """
    if not codigo_input.strip():
        return False, "❌ El código no puede estar vacío"
    
    try:
        codigo = int(codigo_input)
        if codigo <= 0:
            return False, "❌ El código debe ser un número positivo mayor a 0"
        
        # Verificar si el código ya existe en la base de datos
        todos_empleados = empleado_dto.listarEmpleados()
        for empleado in todos_empleados:
            if empleado.getCodigo() == codigo:
                return False, f"❌ El código {codigo} ya está en uso por otro empleado"
        
        return True, codigo
    except ValueError:
        return False, "❌ El código debe ser un número válido"
    
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

            # Solicitar código CON VALIDACIÓN (pero permitir mantener el actual)
            codigo_actual = resu.getCodigo()
            while True:
                codigo_input = input(f"Ingrese nuevo código [{codigo_actual}]: ").strip()
                if codigo_input == "":
                    codigo = codigo_actual  # Mantener el código actual
                    break
    
                es_valido, mensaje = validar_codigo_empleado(codigo_input, EmpleadoDTO())
                if es_valido:
                    codigo = mensaje
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
            
            if daoPersona().existePersona(run):
                print(f"❌ El RUN {run} ya existe en el sistema (como empleado o cliente)")
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
                codigo_input = input("Ingrese código: ").strip()
                es_valido, mensaje = validar_codigo_empleado(codigo_input, EmpleadoDTO())
                if es_valido:
                    codigo = mensaje  # mensaje contiene el código validado
                    break
                print(mensaje)
            
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
            if daoPersona().existePersona(run):
                print(f"❌ El RUN {run} ya existe en el sistema (como empleado o cliente)")
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
# ========== VALIDACIONES  DE ENTRADA VEHÍCULO ==========

def validar_patente(patente):
    """
    Valida formato de patente chilena (AA-BB-11 o ABC-D12)
    """
    patente = patente.upper().strip()
    
    if not patente:
        return False, "❌ La patente no puede estar vacía"
    
    if len(patente) > 8:
        return False, "❌ La patente no puede tener más de 8 caracteres"
    
    # Formato antiguo: AA-BB-11 (4 letras + 2 números + 2 guiones)
    # Formato nuevo: ABC-D12 (3 letras + 1 letra + 2 números + 1 guión)
    if not re.match(r'^[A-Z]{2}-[A-Z]{2}-\d{2}$', patente) and \
       not re.match(r'^[A-Z]{3}-[A-Z]{1}\d{2}$', patente):
        return False, "❌ Formato de patente inválido. Ejemplos válidos: AB-CD-12 o ABC-D12"
    
    return True, patente

def validar_marca_vehiculo(marca):
    """
    Valida marca de vehículo
    """
    if not marca.strip():
        return False, "❌ La marca no puede estar vacía"
    
    if len(marca.strip()) > 20:
        return False, "❌ La marca no puede tener más de 20 caracteres"
    
    # Permitir letras, números, espacios y algunos caracteres especiales
    if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$', marca):
        return False, "❌ La marca solo puede contener letras, números y espacios"
    
    return True, marca.strip()

def validar_modelo_vehiculo(modelo):
    """
    Valida modelo de vehículo  
    """
    if not modelo.strip():
        return False, "❌ El modelo no puede estar vacía"
    
    if len(modelo.strip()) > 25:
        return False, "❌ El modelo no puede tener más de 25 caracteres"
    
    # Permitir letras, números, espacios y algunos caracteres especiales
    if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$', modelo):
        return False, "❌ El modelo solo puede contener letras, números y espacios"
    
    return True, modelo.strip()

def validar_año_vehiculo(año):
    """
    Valida año del vehículo (1900 - año_actual+1)
    """
    año_actual = datetime.now().year
    
    if not año.strip():
        return False, "❌ El año no puede estar vacío"
    
    if len(año.strip()) > 4:
        return False, "❌ El año no puede tener más de 4 caracteres"
    
    try:
        año_int = int(año)
        if año_int < 1900 or año_int > año_actual + 1:  # +1 para modelos próximos
            return False, f"❌ El año debe estar entre 1900 y {año_actual + 1}"
        return True, año_int
    except ValueError:
        return False, "❌ El año debe ser un número válido"

def validar_precio_uf(precio):
    """
    Valida precio en UF del vehículo (positivo y realista)
    """
    if not precio.strip():
        return False, "❌ El precio no puede estar vacío"
    
    try:
        precio_float = float(precio)
        if precio_float <= 0:
            return False, "❌ El precio debe ser mayor a 0"
        if precio_float > 100:  # 100 UF como límite realista por día
            return False, "❌ El precio no puede exceder 100 UF por día"
        return True, precio_float
    except ValueError:
        return False, "❌ El precio debe ser un número válido"
    
def validar_estado_vehiculo(estado):
    """
    Valida que el estado del vehículo sea uno de los permitidos
    """
    estados_permitidos = ['disponible', 'reservado', 'ocupado', 'mantención']
    
    if not estado.strip():
        return False, "❌ El estado no puede estar vacío"
    
    estado = estado.strip().lower()
    
    # Validar longitud
    if len(estado) < 5 or len(estado) > 12:
        return False, "❌ El estado debe tener entre 5 y 12 caracteres"
    
    # Validar que solo contenga letras y acentos
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+$', estado):
        return False, "❌ El estado solo puede contener letras"
    
    # Validar que sea uno de los estados permitidos
    if estado not in estados_permitidos:
        estados_str = ", ".join(estados_permitidos)
        return False, f"❌ Estado inválido. Debe ser uno de: {estados_str}"
    
    return True, estado

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

def validateAddVehiculo():
    while True:
        try:
            print("\n--- AGREGAR VEHÍCULO ---")
            patente = input("Ingrese patente del vehículo (o '0' para volver): ").strip()
            
            if patente == '0':
                print("Volviendo al menú anterior...")
                break
                
            # Validar patente
            es_valido, patente_limpia = validar_patente(patente)
            if not es_valido:
                print(patente_limpia)  # Mensaje de error
                continue
            patente = patente_limpia
            
            # Verificar si el vehículo ya existe
            resu = VehiculoDTO().buscarVehiculo(patente)
            if resu is not None:
                print(f"❌ El vehículo con patente {patente} ya existe:")
                print(f"   {resu}")
                continue
            
            # Solicitar marca con validación
            while True:
                marca = input("Ingrese marca: ").strip()
                es_valido, mensaje = validar_marca_vehiculo(marca)
                if es_valido:
                    break
                print(mensaje)
            
            # Solicitar modelo con validación
            while True:
                modelo = input("Ingrese modelo: ").strip()
                es_valido, mensaje = validar_modelo_vehiculo(modelo)
                if es_valido:
                    break
                print(mensaje)
            
            # Solicitar año con validación
            while True:
                año_input = input("Ingrese año: ").strip()
                es_valido, mensaje = validar_año_vehiculo(año_input)
                if es_valido:
                    año = mensaje  # año ya convertido a int
                    break
                print(mensaje)
            
            # Solicitar precio UF con validación
            while True:
                precio_input = input("Ingrese precio por día (UF): ").strip()
                es_valido, mensaje = validar_precio_uf(precio_input)
                if es_valido:
                    precio_uf = mensaje  # precio ya convertido a float
                    break
                print(mensaje)
            
            # Estado por defecto "disponible"
            estado = "disponible"
            
            # Confirmar creación
            print(f"\n--- RESUMEN DEL NUEVO VEHÍCULO ---")
            print(f"Patente: {patente}")
            print(f"Marca: {marca}")
            print(f"Modelo: {modelo}")
            print(f"Año: {año}")
            print(f"Precio por día: {precio_uf} UF")
            print(f"Estado: {estado}")
            print("-----------------------------------")
            
            confirmar = input("¿Confirmar creación? (S/N): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Creación cancelada")
                continue
            
            # Crear vehículo
            resultado = VehiculoDTO().agregarVehiculo(patente, marca, modelo, año, precio_uf, estado)
            print(f"✅ {resultado}")
            
            # Preguntar si quiere agregar otro
            otro = input("¿Agregar otro vehículo? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break

def validateUpdateVehiculo():
    while True:
        try:
            print("\n--- ACTUALIZAR VEHÍCULO ---")
            patente = input("Ingrese la patente del vehículo a modificar (o '0' para volver): ").strip()
            
            if patente == '0':
                print("Volviendo al menú anterior...")
                break
                
            # Validar patente
            es_valido, patente_limpia = validar_patente(patente)
            if not es_valido:
                print(patente_limpia)
                continue
            patente = patente_limpia
            
            resu = VehiculoDTO().buscarVehiculo(patente)
            
            if resu is None:
                print("❌ Vehículo no encontrado")
                continuar = input("¿Buscar otro vehículo? (S/N): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                continue
            
            print("Datos actuales -->", resu)
            
            # Obtener datos actuales
            marca_actual = resu.getMarca()
            modelo_actual = resu.getModelo()
            año_actual = resu.getAño()
            precio_actual = resu.getPrecio()
            estado_actual = resu.getDisponible()
            
            # Solicitar nueva marca
            while True:
                marca_input = input(f"Ingrese nueva marca [{marca_actual}]: ").strip()
                if marca_input == "":
                    marca = marca_actual
                    break
                es_valido, mensaje = validar_marca_vehiculo(marca_input)
                if es_valido:
                    marca = marca_input
                    break
                print(mensaje)
            
            # Solicitar nuevo modelo
            while True:
                modelo_input = input(f"Ingrese nuevo modelo [{modelo_actual}]: ").strip()
                if modelo_input == "":
                    modelo = modelo_actual
                    break
                es_valido, mensaje = validar_modelo_vehiculo(modelo_input)
                if es_valido:
                    modelo = modelo_input
                    break
                print(mensaje)
            
            # Solicitar nuevo año
            while True:
                año_input = input(f"Ingrese nuevo año [{año_actual}]: ").strip()
                if año_input == "":
                    año = año_actual
                    break
                es_valido, mensaje = validar_año_vehiculo(año_input)
                if es_valido:
                    año = mensaje
                    break
                print(mensaje)
            
            # Solicitar nuevo precio UF
            while True:
                precio_input = input(f"Ingrese nuevo precio por día (UF) [{precio_actual}]: ").strip()
                if precio_input == "":
                    precio_uf = precio_actual
                    break
                es_valido, mensaje = validar_precio_uf(precio_input)
                if es_valido:
                    precio_uf = mensaje
                    break
                print(mensaje)
            
            # Solicitar nuevo estado
            while True:
                estado_input = input(f"Ingrese nuevo estado [{estado_actual}]: ").strip()
                if estado_input == "":
                    estado = estado_actual
                    break
                es_valido, mensaje = validar_estado_vehiculo(estado_input)
                if es_valido:
                    estado = mensaje
                    break
                print(mensaje)
            
            # Mostrar resumen y confirmar
            print(f"\n--- RESUMEN DE CAMBIOS ---")
            print(f"Patente: {patente}")
            print(f"Marca: {marca_actual} → {marca}")
            print(f"Modelo: {modelo_actual} → {modelo}")
            print(f"Año: {año_actual} → {año}")
            print(f"Precio UF: {precio_actual} → {precio_uf}")
            print(f"Estado: {estado_actual} → {estado}")
            print("---------------------------")
            
            confirmar = input("¿Confirmar actualización? (S/N): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Actualización cancelada")
                continuar = input("¿Actualizar otro vehículo? (S/N): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                continue
            
            # Ejecutar actualización
            resultado = VehiculoDTO().actualizarVehiculo(patente, marca, modelo, año, precio_uf, estado)
            print(f"✅ {resultado}")
            
            # Preguntar si quiere actualizar otro
            otro = input("¿Actualizar otro vehículo? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break

def validateFindVehiculo():
    while True:
        try:
            print("\n--- BUSCAR VEHÍCULO ---")
            patente = input("Ingrese la patente del vehículo a buscar (o '0' para volver): ").strip()
            
            if patente == '0':
                break
                
            es_valido, patente_limpia = validar_patente(patente)
            if not es_valido:
                print(patente_limpia)
                continue
            
            resu = VehiculoDTO().buscarVehiculo(patente_limpia)
            if resu is not None:
                print(f"✅ Resultado: {resu}")
            else:
                print("❌ Vehículo no encontrado")
            
            otro = input("¿Buscar otro vehículo? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break

def validaDelVehiculo():
    while True:
        try:
            print("\n--- ELIMINAR VEHÍCULO ---")
            patente = input("Ingrese la patente del vehículo a eliminar (o '0' para volver): ").strip()
            
            if patente == '0':
                break
                
            es_valido, patente_limpia = validar_patente(patente)
            if not es_valido:
                print(patente_limpia)
                continue
            
            resu = VehiculoDTO().buscarVehiculo(patente_limpia)
            
            if resu is not None:
                print("Datos del vehículo -->", resu)
                respuesta = input("¿Está seguro de la eliminación? (S/N): ").strip().lower()
                if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                    resultado = VehiculoDTO().eliminarVehiculo(patente_limpia)
                    print(f"✅ {resultado}")
                else:
                    print("❌ Eliminación cancelada")
            else:
                print("❌ Vehículo no encontrado")
            
            otro = input("¿Eliminar otro vehículo? (S/N): ").strip().lower()
            if otro not in ['s', 'si', 'sí', 'y', 'yes']:
                break
                
        except Exception as e:
            print(f"❌ Ocurrió un error: {e}")
            continuar = input("¿Reintentar? (S/N): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                break
from datetime import datetime, timedelta
import re

# ========== VALIDACIONES DE ENTRADA DE ARRIENDO ==========

def determinar_tipo_arriendo(fecha_inicio, fecha_entrega):
    """
    Determina si el arriendo es pasado, presente/mixto, o futuro
    """
    try:
        hoy = datetime.now().date()
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_entrega_dt = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()
        
        if fecha_entrega_dt < hoy:
            return "pasado"    # ✅ Totalmente en el pasado
        elif fecha_inicio_dt > hoy:
            return "futuro"    # ✅ Totalmente en el futuro
        else:
            return "mixto"     # Incluye días pasados/presentes y futuros
        
    except:
        return "futuro"

def obtener_uf_hoy():
    """
    Simula obtener UF de hoy (luego se reemplaza por API)
    """
    return 36000  # Valor fijo para testing

def obtener_uf_fecha_historica(fecha):
    """
    Simula obtener UF histórica (luego se reemplaza por API)
    """
    # Por simplicidad, retorna valores diferentes según el año
    try:
        año = datetime.strptime(fecha, '%Y-%m-%d').year
        if año <= 2020:
            return 28000
        elif año <= 2022:
            return 30000
        elif año <= 2023:
            return 32000
        else:
            return 34000
    except:
        return 35000

def validar_fecha_formato(fecha_str):
    """
    Valida que la fecha tenga formato YYYY-MM-DD
    """
    if not fecha_str.strip():
        return False, "❌ La fecha no puede estar vacía"
    
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True, "✅ Formato de fecha válido"
    except ValueError:
        return False, "❌ Formato de fecha inválido. Debe ser YYYY-MM-DD (ej: 2024-01-15)"

def validar_fechas_arriendo(fecha_inicio_str, fecha_entrega_str):
    """
    Valida lógica de fechas para arriendo (permite fechas pasadas para testing)
    """
    # Validar formato primero
    es_valido, mensaje = validar_fecha_formato(fecha_inicio_str)
    if not es_valido:
        return False, mensaje
    
    es_valido, mensaje = validar_fecha_formato(fecha_entrega_str)
    if not es_valido:
        return False, mensaje
    
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
        
        # ✅ PERMITIR fechas pasadas (para testing con UF histórica)
        # ❌ Solo validar que entrega > inicio
        if fecha_entrega <= fecha_inicio:
            return False, "❌ La fecha de entrega debe ser posterior a la de inicio"
        
        # Máximo 30 días de arriendo
        dias_arriendo = (fecha_entrega - fecha_inicio).days
        if dias_arriendo > 30:
            return False, "❌ El arriendo no puede exceder 30 días"
        if dias_arriendo < 1:
            return False, "❌ El arriendo debe ser de al menos 1 día"
        
        tipo = determinar_tipo_arriendo(fecha_inicio_str)
        
        return True, {
            'dias': dias_arriendo,
            'tipo': tipo,
            'fecha_inicio': fecha_inicio,
            'fecha_entrega': fecha_entrega
        }
        
    except Exception as e:
        return False, f"❌ Error validando fechas: {e}"
    
def validar_disponibilidad_vehiculo(patente, fecha_inicio, fecha_entrega):
    """
    Valida que el vehículo no tenga arriendos superpuestos en las fechas solicitadas
    """
    from dao.dao_arriendo import daoArriendo
    
    try:
        dao = daoArriendo()
        arriendo_superpuesto = dao.tieneArriendosSuperpuestos(patente, fecha_inicio, fecha_entrega)
        
        if arriendo_superpuesto:
            return False, f"❌ El vehículo ya tiene un arriendo en las fechas solicitadas (Arriendo #{arriendo_superpuesto[0]})"
        return True, "✅ Vehículo disponible para las fechas"
        
    except Exception as e:
        return False, f"❌ Error validando disponibilidad: {e}"
    
def validar_vehiculo_disponible(patente, fecha_inicio_str, fecha_entrega_str):
    """
    Valida que el vehículo esté disponible para las fechas solicitadas
    """
    from controlador.dto_vehiculo import VehiculoDTO
    
    try:
        # Validar patente primero
        patente = patente.upper().strip()
        if not patente:
            return False, "❌ La patente no puede estar vacía"
        
        # Verificar que el vehículo existe y está en estado arrendable
        vehiculo_dto = VehiculoDTO()
        vehiculo = vehiculo_dto.buscarVehiculo(patente)
        
        if not vehiculo:
            return False, "❌ Vehículo no encontrado"
        
        estado = vehiculo.getDisponible().lower()
        if estado not in ['disponible', 'reservado']:
            return False, f"❌ El vehículo está {estado}, no se puede arrendar"
        
        # ✅ AGREGAR AQUÍ: Validación de superposición de fechas
        es_disponible, mensaje = validar_disponibilidad_vehiculo(patente, fecha_inicio_str, fecha_entrega_str)
        if not es_disponible:
            return False, mensaje
        
        return True, vehiculo
        
    except Exception as e:
        return False, f"❌ Error validando vehículo: {e}"

def validar_cliente_existente(run_cliente):
    """
    Valida que el cliente exista
    """
    from controlador.dto_cliente import ClienteDTO
    
    try:
        if not run_cliente.strip():
            return False, "❌ El RUN del cliente no puede estar vacío"
        
        cliente_dto = ClienteDTO()
        cliente = cliente_dto.buscarCliente(run_cliente)
        
        if not cliente:
            return False, "❌ Cliente no encontrado"
        
        return True, cliente
        
    except Exception as e:
        return False, f"❌ Error validando cliente: {e}"

def validar_empleado_existente(run_empleado):
    """
    Valida que el empleado exista
    """
    from controlador.dto_empleado import EmpleadoDTO
    
    try:
        if not run_empleado.strip():
            return False, "❌ El RUN del empleado no puede estar vacío"
        
        empleado_dto = EmpleadoDTO()
        empleado = empleado_dto.buscarEmpleado(run_empleado)
        
        if not empleado:
            return False, "❌ Empleado no encontrado"
        
        return True, empleado
        
    except Exception as e:
        return False, f"❌ Error validando empleado: {e}"

def validar_numero_arriendo(num_arriendo_str):
    if not num_arriendo_str.strip():
        return False, "❌ El número de arriendo no puede estar vacío"
    
    try:
        num_arriendo = int(num_arriendo_str)
        if num_arriendo <= 0:
            return False, "❌ El número de arriendo debe ser positivo"
        if num_arriendo > 999999:  
            return False, "❌ El número de arriendo no puede exceder 999999"
        return True, num_arriendo
    except ValueError:
        return False, "❌ El número de arriendo debe ser un número válido"

def calcular_costo_arriendo(vehiculo, dias_arriendo, tipo_arriendo, fecha_inicio=None, fecha_entrega=None):
    """
    Calcula costo según el tipo de arriendo (pasado, mixto, futuro)
    """
    try:
        precio_uf_dia = vehiculo.getPrecio()
        
        if tipo_arriendo == "pasado":
            # ✅ Cálculo REAL con UF histórica
            uf_valor = obtener_uf_fecha_historica(fecha_inicio)
            costo_uf = precio_uf_dia * dias_arriendo
            costo_pesos = costo_uf * uf_valor
            
            return {
                'tipo': 'real',
                'costo_uf': round(costo_uf, 2),
                'costo_pesos': round(costo_pesos, 2),
                'uf_valor': uf_valor,
                'dias': dias_arriendo,
                'precio_uf_dia': precio_uf_dia,
                'estado': 'confirmado',
                'mensaje': f'Cálculo real con UF histórica: ${uf_valor:,.0f}'
            }
        
        elif tipo_arriendo == "futuro":
            # ⏳ Cálculo ESTIMADO con UF actual
            uf_valor = obtener_uf_hoy()
            costo_uf = precio_uf_dia * dias_arriendo
            costo_pesos = costo_uf * uf_valor
            
            return {
                'tipo': 'estimado',
                'costo_uf': round(costo_uf, 2),
                'costo_pesos': round(costo_pesos, 2),
                'uf_valor': uf_valor,
                'dias': dias_arriendo,
                'precio_uf_dia': precio_uf_dia,
                'estado': 'reservado',
                'mensaje': f'⚠️ COTIZACIÓN: Precio calculado con UF de hoy (${uf_valor:,.0f}), sujeto a cambios'
            }
        
        else:  # mixto
            # 🔄 Cálculo MIXTO (parte real + parte estimada)
            uf_valor = obtener_uf_hoy()  # Por simplicidad, usamos UF actual
            costo_uf = precio_uf_dia * dias_arriendo
            costo_pesos = costo_uf * uf_valor
            
            return {
                'tipo': 'mixto',
                'costo_uf': round(costo_uf, 2),
                'costo_pesos': round(costo_pesos, 2),
                'uf_valor': uf_valor,
                'dias': dias_arriendo,
                'precio_uf_dia': precio_uf_dia,
                'estado': 'confirmado',
                'mensaje': f'⚠️ CÁLCULO MIXTO: Incluye días pasados y futuros. Precio con UF actual (${uf_valor:,.0f})'
            }
        
    except Exception as e:
        return None
    
# ========== VALIDACIONES ARRIENDO ==========

def mostrar_resumen_arriendo(datos_arriendo, calculo):
    """
    Muestra resumen completo del arriendo
    """
    print(f"\n--- RESUMEN DEL ARRIENDO ---")
    print(f"Número: {datos_arriendo['num_arriendo']}")
    print(f"Cliente: {datos_arriendo['cliente'].getNombre()} {datos_arriendo['cliente'].getApellido()} ({datos_arriendo['cliente'].getRun()})")
    print(f"Vehículo: {datos_arriendo['vehiculo'].getMarca()} {datos_arriendo['vehiculo'].getModelo()} ({datos_arriendo['vehiculo'].getPatente()})")
    print(f"Empleado: {datos_arriendo['empleado'].getNombre()} {datos_arriendo['empleado'].getApellido()}")
    print(f"Fechas: {datos_arriendo['fecha_inicio']} a {datos_arriendo['fecha_entrega']} ({calculo['dias']} días)")
    print(f"Precio por día: {calculo['precio_uf_dia']} UF")
    print(f"\n--- CÁLCULO ---")
    print(f"Tipo: {calculo['tipo'].upper()}")
    print(f"{calculo['mensaje']}")
    print(f"Costo total: {calculo['costo_uf']} UF (${calculo['costo_pesos']:,.0f} CLP)")
    print(f"Estado: {calculo['estado'].upper()}")
    print("-----------------------------------")

def listAllArriendos():
    """Lista todos los arriendos con formato mejorado"""
    print("\n" + "="*50)
    print("📋 LISTADO COMPLETO DE ARRIENDOS")
    print("="*50)
    
    try:
        resultado = ArriendoDTO().listarArriendos()
        if len(resultado) > 0:
            for i, arr in enumerate(resultado, 1):
                print(f"\n[{i}] {arr}")
        else:
            print("❌ No hay arriendos registrados")
    except Exception as e:
        print(f"❌ Error al listar arriendos: {e}")

def validateFindArriendo():
    """Busca un arriendo por número con validaciones"""
    print("\n" + "="*40)
    print("🔍 BUSCAR ARRIENDO")
    print("="*40)
    
    while True:
        try:
            num_arriendo_str = input("Ingrese el número de arriendo a buscar (o '0' para volver): ").strip()
            
            if num_arriendo_str == '0':
                print("↩️ Volviendo al menú anterior...")
                return
            
            # Validar número de arriendo
            es_valido, resultado = validar_numero_arriendo(num_arriendo_str)
            if not es_valido:
                print(resultado)
                continue
            
            num_arriendo = resultado
            arriendo_dto = ArriendoDTO()
            arriendo = arriendo_dto.buscarArriendo(num_arriendo)
            
            if arriendo is not None:
                print(f"\n✅ ARRIENDO ENCONTRADO:")
                print(f"   Número: {arriendo.getNumArriendo()}")
                print(f"   Fechas: {arriendo.getFechaInicio()} a {arriendo.getFechaEntrega()}")
                print(f"   Costo: ${arriendo.getCostoTotal():,.0f} CLP")
                print(f"   Cliente: {arriendo.getCliente().getNombre()} {arriendo.getCliente().getApellido()}")
                print(f"   Vehículo: {arriendo.getVehiculo().getMarca()} {arriendo.getVehiculo().getModelo()}")
                print(f"   Empleado: {arriendo.getEmpleado().getNombre()} {arriendo.getEmpleado().getApellido()}")
            else:
                print("❌ Arriendo no encontrado")
            
            # Preguntar si quiere buscar otro
            continuar = input("\n¿Buscar otro arriendo? (S/N): ").strip().upper()
            if continuar != 'S':
                break
                
        except ValueError:
            print("❌ Debe ingresar un número válido")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

def validateAddArriendo():
    """Agrega un nuevo arriendo con validaciones completas"""
    print("\n" + "="*50)
    print("🚗 NUEVO ARRIENDO / RESERVA")
    print("="*50)
    
    while True:
        try:
            # 1. Validar número de arriendo (BUCLE INDIVIDUAL)
            print("\n1️⃣  INGRESO DE DATOS BÁSICOS")
            num_arriendo = None
            while num_arriendo is None:
                num_arriendo_str = input("Ingrese número de arriendo (o '0' para volver): ").strip()
                
                if num_arriendo_str == '0':
                    print("↩️ Volviendo al menú anterior...")
                    return
                
                es_valido, resultado = validar_numero_arriendo(num_arriendo_str)
                if es_valido:
                    num_arriendo = resultado
                    
                    # Verificar si el arriendo ya existe
                    arriendo_existente = ArriendoDTO().buscarArriendo(num_arriendo)
                    if arriendo_existente is not None:
                        print(f"❌ El arriendo #{num_arriendo} ya existe:")
                        print(f"   {arriendo_existente}")
                        continuar = input("¿Intentar con otro número? (S/N): ").strip().upper()
                        if continuar == 'S':
                            num_arriendo = None  # Reiniciar bucle
                        else:
                            return
                else:
                    print(resultado)

            # 2. Validar fechas (BUCLE INDIVIDUAL)
            print("\n2️⃣  FECHAS DEL ARRIENDO")
            datos_fechas = None
            while datos_fechas is None:
                fecha_inicio = input("Ingrese fecha inicio (YYYY-MM-DD): ").strip()
                fecha_entrega = input("Ingrese fecha entrega (YYYY-MM-DD): ").strip()
                
                es_valido, resultado_fechas = validar_fechas_arriendo(fecha_inicio, fecha_entrega)
                if es_valido:
                    datos_fechas = resultado_fechas
                else:
                    print(resultado_fechas)

            dias_arriendo = datos_fechas['dias']
            tipo_arriendo = datos_fechas['tipo']

            # 3. Validar cliente (BUCLE INDIVIDUAL)
            print("\n3️⃣  DATOS DEL CLIENTE")
            cliente = None
            while cliente is None:
                run_cliente = input("Ingrese RUN del cliente: ").strip()
                
                es_valido, resultado_cliente = validar_cliente_existente(run_cliente)
                if es_valido:
                    cliente = resultado_cliente
                else:
                    print(resultado_cliente)

            # 4. Validar vehículo (BUCLE INDIVIDUAL)
            print("\n4️⃣  DATOS DEL VEHÍCULO")
            vehiculo = None
            while vehiculo is None:
                patente_vehiculo = input("Ingrese patente del vehículo: ").strip()
                
                es_valido, resultado_vehiculo = validar_vehiculo_disponible(patente_vehiculo, fecha_inicio, fecha_entrega)
                if es_valido:
                    vehiculo = resultado_vehiculo
                else:
                    print(resultado_vehiculo)

            # 5. Validar empleado (BUCLE INDIVIDUAL)
            print("\n5️⃣  DATOS DEL EMPLEADO")
            empleado = None
            while empleado is None:
                run_empleado = input("Ingrese RUN del empleado: ").strip()
                
                es_valido, resultado_empleado = validar_empleado_existente(run_empleado)
                if es_valido:
                    empleado = resultado_empleado
                else:
                    print(resultado_empleado)

            # 6. Calcular costo
            print("\n6️⃣  CÁLCULO DE COSTO")
            calculo = calcular_costo_arriendo(vehiculo, dias_arriendo, tipo_arriendo, fecha_inicio)
            
            if not calculo:
                print("❌ Error al calcular el costo del arriendo")
                continue

            # 7. Mostrar resumen y confirmar
            datos_arriendo = {
                'num_arriendo': num_arriendo,
                'cliente': cliente,
                'vehiculo': vehiculo,
                'empleado': empleado,
                'fecha_inicio': fecha_inicio,
                'fecha_entrega': fecha_entrega
            }
            
            mostrar_resumen_arriendo(datos_arriendo, calculo)
            
            # 8. Confirmar creación
            confirmar = input("\n¿Confirmar creación del arriendo? (S/N): ").strip().upper()
            if confirmar == 'S':
                resultado = ArriendoDTO().agregarArriendo(
                    num_arriendo, fecha_inicio, fecha_entrega, 
                    calculo['costo_pesos'], run_cliente, run_empleado, patente_vehiculo
                )
                print(f"\n{resultado}")
             #9 actualizar estado del vehiculo
            confirmar = input("\n¿Confirmar creación del arriendo? (S/N): ").strip().upper()
            if confirmar == 'S':
                resultado = ArriendoDTO().agregarArriendo(
                    num_arriendo, fecha_inicio, fecha_entrega, 
                    calculo['costo_pesos'], run_cliente, run_empleado, patente_vehiculo
                )
                print(f"\n{resultado}")
    
        # ✅ ACTUALIZAR ESTADO DEL VEHÍCULO (UN SOLO BLOQUE)
            if tipo_arriendo in ['presente', 'mixto', 'futuro']:
                from controlador.dto_vehiculo import VehiculoDTO
                vehiculo_dto = VehiculoDTO()
        
        # Determinar nuevo estado según tipo de arriendo
                if tipo_arriendo in ['presente', 'mixto']:
                    nuevo_estado = 'ocupado'
                else:  # futuro
                    nuevo_estado = 'reservado'
        
        # Obtener datos actuales del vehículo
            vehiculo_actual = vehiculo_dto.buscarVehiculo(patente_vehiculo)
            if vehiculo_actual:
                resultado_vehiculo = vehiculo_dto.actualizarVehiculo(
                    vehiculo_actual.getPatente(),
                    vehiculo_actual.getMarca(),
                    vehiculo_actual.getModelo(),
                    vehiculo_actual.getAño(),
                    vehiculo_actual.getPrecio(),
                    nuevo_estado
                )
                print(f"✅ Estado del vehículo actualizado a: {nuevo_estado}")
            else:
                print("❌ Arriendo cancelado")

            # Preguntar si quiere agregar otro
            continuar = input("\n¿Agregar otro arriendo? (S/N): ").strip().upper()
            if continuar != 'S':
                break

        except KeyboardInterrupt:
            print("\n\n⚠️ Operación cancelada por el usuario")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()

def validateUpdateArriendo():
    """Actualiza un arriendo existente"""
    print("\n" + "="*40)
    print("✏️ ACTUALIZAR ARRIENDO")
    print("="*40)
    
    try:
        num_arriendo_str = input("Ingrese número de arriendo a actualizar (o '0' para volver): ").strip()
        
        if num_arriendo_str == '0':
            print("↩️ Volviendo al menú anterior...")
            return
        
        es_valido, resultado = validar_numero_arriendo(num_arriendo_str)
        if not es_valido:
            print(resultado)
            return
        
        num_arriendo = resultado
        arriendo_dto = ArriendoDTO()
        arriendo = arriendo_dto.buscarArriendo(num_arriendo)
        
        if not arriendo:
            print("❌ Arriendo no encontrado")
            return
        
        print(f"\n📋 Datos actuales del arriendo #{num_arriendo}:")
        print(f"   Fecha inicio: {arriendo.getFechaInicio()}")
        print(f"   Fecha entrega: {arriendo.getFechaEntrega()}")
        print(f"   Costo total: ${arriendo.getCostoTotal():,.0f}")
        print(f"   Cliente: {arriendo.getCliente().getNombre()} {arriendo.getCliente().getApellido()}")
        print(f"   Vehículo: {arriendo.getVehiculo().getMarca()} {arriendo.getVehiculo().getModelo()}")
        
        # Por simplicidad, solo permitimos actualizar fechas
        print("\n🔄 ACTUALIZACIÓN DE FECHAS")
        nueva_fecha_inicio = input(f"Nueva fecha inicio [{arriendo.getFechaInicio()}]: ").strip()
        nueva_fecha_entrega = input(f"Nueva fecha entrega [{arriendo.getFechaEntrega()}]: ").strip()
        
        # Usar valores actuales si no se ingresan nuevos
        if not nueva_fecha_inicio:
            nueva_fecha_inicio = arriendo.getFechaInicio()
        if not nueva_fecha_entrega:
            nueva_fecha_entrega = arriendo.getFechaEntrega()
        
        # Validar nuevas fechas
        es_valido, resultado_fechas = validar_fechas_arriendo(nueva_fecha_inicio, nueva_fecha_entrega)
        if not es_valido:
            print(resultado_fechas)
            return
        
        datos_fechas = resultado_fechas
        dias_arriendo = datos_fechas['dias']
        tipo_arriendo = datos_fechas['tipo']
        
        # Recalcular costo
        vehiculo = arriendo.getVehiculo()
        calculo = calcular_costo_arriendo(vehiculo, dias_arriendo, tipo_arriendo, nueva_fecha_inicio)
        
        if not calculo:
            print("❌ Error al recalcular el costo")
            return
        
        print(f"\n💡 RESUMEN DE CAMBIOS:")
        print(f"   Fechas: {arriendo.getFechaInicio()} → {nueva_fecha_inicio}")
        print(f"           {arriendo.getFechaEntrega()} → {nueva_fecha_entrega}")
        print(f"   Días: {dias_arriendo} días")
        print(f"   Nuevo costo: {calculo['costo_uf']} UF (${calculo['costo_pesos']:,.0f} CLP)")
        print(f"   Tipo: {calculo['tipo']}")
        
        confirmar = input("\n¿Confirmar actualización? (S/N): ").strip().upper()
        if confirmar == 'S':
            # Actualizar el arriendo
            arriendo.setFechaInicio(nueva_fecha_inicio)
            arriendo.setFechaEntrega(nueva_fecha_entrega)
            arriendo.setCostoTotal(calculo['costo_pesos'])
            
            # Aquí necesitaríamos un método updateArriendo en el DTO
            print("✅ Funcionalidad de actualización en desarrollo...")
            # resultado = arriendo_dto.actualizarArriendo(arriendo)
            # print(resultado)
        else:
            print("❌ Actualización cancelada")
            
    except Exception as e:
        print(f"❌ Error al actualizar arriendo: {e}")

def validaDelArriendo():
    """Elimina un arriendo con confirmación"""
    print("\n" + "="*40)
    print("🗑️ ELIMINAR ARRIENDO")
    print("="*40)
    
    try:
        num_arriendo_str = input("Ingrese número de arriendo a eliminar (o '0' para volver): ").strip()
        
        if num_arriendo_str == '0':
            print("↩️ Volviendo al menú anterior...")
            return
        
        es_valido, resultado = validar_numero_arriendo(num_arriendo_str)
        if not es_valido:
            print(resultado)
            return
        
        num_arriendo = resultado
        arriendo_dto = ArriendoDTO()
        arriendo = arriendo_dto.buscarArriendo(num_arriendo)
        
        if arriendo:
            print(f"\n⚠️ DATOS DEL ARRIENDO A ELIMINAR:")
            print(f"   Número: {arriendo.getNumArriendo()}")
            print(f"   Fechas: {arriendo.getFechaInicio()} a {arriendo.getFechaEntrega()}")
            print(f"   Costo: ${arriendo.getCostoTotal():,.0f}")
            print(f"   Cliente: {arriendo.getCliente().getNombre()} {arriendo.getCliente().getApellido()}")
            print(f"   Vehículo: {arriendo.getVehiculo().getMarca()} {arriendo.getVehiculo().getModelo()}")
            
            respuesta = input("\n¿Está seguro de eliminar este arriendo? [s/N]: ").strip().lower()
            if respuesta == 's':
                resultado = arriendo_dto.eliminarArriendo(arriendo)
                print(f"\n{resultado}")
                
                # Liberar el vehículo si estaba ocupado/reservado
                vehiculo = arriendo.getVehiculo()
                if vehiculo.getDisponible() in ['ocupado', 'reservado']:
                    from controlador.dto_vehiculo import VehiculoDTO
                    vehiculo_dto = VehiculoDTO()
                    vehiculo.setDisponible('disponible')
                    vehiculo_dto.actualizarVehiculo(vehiculo)
                    print("✅ Vehículo liberado y marcado como disponible")
            else:
                print("❌ Eliminación cancelada")
        else:
            print("❌ Arriendo no encontrado")
            
    except Exception as e:
        print(f"❌ Error al eliminar arriendo: {e}")


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