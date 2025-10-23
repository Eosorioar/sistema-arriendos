from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_cliente import ClienteDTO
from controlador.dto_vehiculo import VehiculoDTO
from controlador.dto_arriendo import ArriendoDTO
from dao.dao_arriendo import daoArriendo
from utils.encoder import Encoder

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
    run = input("Ingrese el RUN del empleado a modificar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateUpdateEmpleado()
    
    resu = EmpleadoDTO().buscarEmpleado(run)
    if resu is not None:
        print("Datos actuales -->", resu)
        nombre = input("Ingrese nuevo nombre: ")
        apellido = input("Ingrese nuevo apellido: ")
        cargo = input("Ingrese nuevo cargo: ")
        clave = input("Ingrese nueva contraseña: ")
        
        print(EmpleadoDTO().actualizarEmpleado(run, nombre, apellido, cargo, clave))
    else:
        print("Empleado no encontrado")

def validateAddEmpleado():
    run = input("Ingrese RUN del empleado: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateAddEmpleado()
    
    resu = EmpleadoDTO().buscarEmpleado(run)
    if resu is not None:
        print("Empleado ya existe -->", resu)
    else:
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        codigo = int(input("Ingrese código: "))
        cargo = input("Ingrese cargo: ")
        clave = input("Ingrese contraseña: ")
        
        print(EmpleadoDTO().agregarEmpleado(run, nombre, apellido, codigo, cargo, clave))

# ========== VALIDACIONES CLIENTE ==========

def listAllClientes():
    print("\n=== LISTADO DE CLIENTES ===")
    resultado = ClienteDTO().listarClientes()  # ← Esto ahora consulta la BD directamente
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

def validateUpdateCliente():
    run = input("Ingrese el RUN del cliente a modificar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateUpdateCliente()
    
    resu = ClienteDTO().buscarCliente(run)
    if resu is not None:
        print("Datos actuales -->", resu)
        nombre = input("Ingrese nuevo nombre: ")
        apellido = input("Ingrese nuevo apellido: ")
        telefono = input("Ingrese nuevo teléfono: ")
        direccion = input("Ingrese nueva dirección: ")
        
        print(ClienteDTO().actualizarCliente(run, nombre, apellido, telefono, direccion))
    else:
        print("Cliente no encontrado")

def validateAddCliente():
    run = input("Ingrese RUN del cliente: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateAddCliente()
    
    resu = ClienteDTO().buscarCliente(run)
    if resu is not None:
        print("Cliente ya existe -->", resu)
    else:
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        telefono = input("Ingrese teléfono: ")
        direccion = input("Ingrese dirección: ")
        
        print(ClienteDTO().agregarCliente(run, nombre, apellido, telefono, direccion))

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
        resu = VehiculoDTO().buscarVehiculo(patente)
        if resu is not None:
            print(f"Resultado: {resu}")
        else:
            print("Vehículo no encontrado")

def validaDelVehiculo():
    patente = input("Ingrese la patente del vehículo a eliminar: ")
    if len(patente) == 0:
        print("Debe ingresar una patente")
        return validaDelVehiculo()
    
    resu = VehiculoDTO().buscarVehiculo(patente)
    if resu is not None:
        print("Datos -->", resu)
        respuesta = input("¿Está seguro de la eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            print(VehiculoDTO().eliminarVehiculo(patente))
        else:
            print("Eliminación cancelada")
    else:
        print("Vehículo no encontrado")

def validateUpdateVehiculo():
    patente = input("Ingrese la patente del vehículo a modificar: ")
    if len(patente) == 0:
        print("Debe ingresar una patente")
        return validateUpdateVehiculo()
    
    resu = VehiculoDTO().buscarVehiculo(patente)
    if resu is not None:
        print("Datos actuales -->", resu)
        marca = input("Ingrese nueva marca: ")
        modelo = input("Ingrese nuevo modelo: ")
        año = int(input("Ingrese nuevo año: "))
        precio = float(input("Ingrese nuevo precio: "))
        disponible = input("Ingrese estado [disponible/arrendado]: ")
        
        print(VehiculoDTO().actualizarVehiculo(patente, marca, modelo, año, precio, disponible))
    else:
        print("Vehículo no encontrado")

def validateAddVehiculo():
    patente = input("Ingrese patente del vehículo: ")
    if len(patente) == 0:
        print("Debe ingresar una patente")
        return validateAddVehiculo()
    
    resu = VehiculoDTO().buscarVehiculo(patente)
    if resu is not None:
        print("Vehículo ya existe -->", resu)
    else:
        marca = input("Ingrese marca: ")
        modelo = input("Ingrese modelo: ")
        año = int(input("Ingrese año: "))
        precio = float(input("Ingrese precio: "))
        
        print(VehiculoDTO().agregarVehiculo(patente, marca, modelo, año, precio))

# ========== VALIDACIONES ARRIENDO ==========

def listAllArriendos():
    print("\n=== LISTADO DE ARRIENDOS ===")
    resultado = ArriendoDTO().listarArriendos()
    if len(resultado) > 0:
        print(resultado)
        for arr in resultado:
            print(arr)
    else:
        print("No hay arriendos registrados")

def validateFindArriendo():
    numArriendo = int(input("Ingrese el número de arriendo a buscar: "))
    resu = ArriendoDTO().buscarArriendo(numArriendo)
    if resu is not None:
        print(f"Resultado: {resu}")
    else:
        print("Arriendo no encontrado")

def validateAddArriendo():
    print("\n=== NUEVO ARRIENDO ===")
    numArriendo = int(input("Ingrese número de arriendo: "))
    
    # Verificar si ya existe
    resu = ArriendoDTO().buscarArriendo(numArriendo)
    if resu is not None:
        print("Arriendo ya existe -->", resu)
    else:
        fechaInicio = input("Ingrese fecha inicio (YYYY-MM-DD): ")
        fechaEntrega = input("Ingrese fecha entrega (YYYY-MM-DD): ")
        costoTotal = float(input("Ingrese costo total: "))
        run_cliente = input("Ingrese RUN del cliente: ")
        run_empleado = input("Ingrese RUN del empleado: ")
        patente_vehiculo = input("Ingrese patente del vehículo: ")
        
        print(ArriendoDTO().agregarArriendo(numArriendo, fechaInicio, fechaEntrega, costoTotal, run_cliente, run_empleado, patente_vehiculo))

def validaDelArriendo():
    print("\n=== ELIMINAR ARRIENDO ===")
    try:
        numArriendo = int(input("Ingrese número de arriendo a eliminar: "))
    except ValueError:
        print("❌ Debe ingresar un número válido")
        return
    
    # Buscar el arriendo primero para mostrar datos
    dao = daoArriendo()
    arriendo = dao.findArriendo(numArriendo)
    
    if arriendo:
        print(f"Datos del arriendo: #{arriendo[0]} - Cliente: {arriendo[5]} {arriendo[6]}")
        respuesta = input("¿Confirmar eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            resultado = dao.deleteArriendo(numArriendo)
            print(resultado)
    else:
        print("❌ Arriendo no encontrado")
# ========== VALIDACIÓN LOGIN ==========

def validarLogin():
    run = input("Ingrese RUN: ")
    clave = input("Ingrese contraseña: ")
    resultado = EmpleadoDTO().validarLogin(run, clave)
    return resultado

# ========== MENÚS ==========

def menuEmpleados(empleado):
    """
    Menú de gestión de empleados con validación de permisos
    """
    while True:
        print("\n=== GESTIÓN DE EMPLEADOS ===")
        print("1. Listar Empleados")
        
        # Solo el gerente puede realizar operaciones CRUD completas
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
                return "6"  # Indicar que quiere volver
            else:
                print("Opción no válida")
        else:
            # Para empleados no gerentes
            if opc == "1":
                listAllEmpleados()
            elif opc == "2":
                return "6"  # Volver al menú principal
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
# ========== INICIALIZACIÓN ==========


def menuPrincipal(empleado):
    """
    Menú principal del sistema que recibe el empleado logueado
    """
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
            # Pasar el empleado al menú de empleados para validar permisos
            opc_emp = menuEmpleados(empleado)
            if opc_emp == "6":  # Volver
                continue
        elif opc == "5":
            print(" Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")