from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_cliente import ClienteDTO
from controlador.dto_vehiculo import VehiculoDTO
from controlador.dto_arriendo import ArriendoDTO
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
    VehiculoDTO().cargarVehiculosBase()
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
    #ArriendoDTO().cargarArriendosBase() 
    resultado = ArriendoDTO().cargarArriendosBase()
    if len(resultado) > 0:
        print(resultado)
        #for arr in resultado:
            #print(arr)
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

# ========== VALIDACIÓN LOGIN ==========

def validarLogin():
    run = input("Ingrese RUN: ")
    clave = input("Ingrese contraseña: ")
    resultado = EmpleadoDTO().validarLogin(run, clave)
    return resultado

# ========== MENÚS ==========

def menuPrincipal():
    print("\n=== SISTEMA DE ARRIENDOS ===")
    print("1. Gestión de Empleados")
    print("2. Gestión de Clientes")
    print("3. Gestión de Vehículos")
    print("4. Gestión de Arriendos")
    print("5. Salir")
    opc = int(input("Ingrese una opción: "))
    return opc

def menuEmpleados():
    print("\n=== GESTIÓN DE EMPLEADOS ===")
    print("1. Listar Empleados")
    print("2. Agregar Empleado")
    print("3. Eliminar Empleado")
    print("4. Actualizar Empleado")
    print("5. Buscar Empleado")
    print("6. Volver al Menú Principal")
    opc = int(input("Ingrese una opción: "))
    return opc

def menuClientes():
    print("\n=== GESTIÓN DE CLIENTES ===")
    print("1. Listar Clientes")
    print("2. Agregar Cliente")
    print("3. Eliminar Cliente")
    print("4. Actualizar Cliente")
    print("5. Buscar Cliente")
    print("6. Volver al Menú Principal")
    opc = int(input("Ingrese una opción: "))
    return opc

def menuVehiculos():
    print("\n=== GESTIÓN DE VEHÍCULOS ===")
    print("1. Listar Vehículos")
    print("2. Listar Vehículos Disponibles")
    print("3. Agregar Vehículo")
    print("4. Eliminar Vehículo")
    print("5. Actualizar Vehículo")
    print("6. Buscar Vehículo")
    print("7. Volver al Menú Principal")
    opc = int(input("Ingrese una opción: "))
    return opc

def menuArriendos():
    print("\n=== GESTIÓN DE ARRIENDOS ===")
    print("1. Listar Arriendos")
    print("2. Agregar Arriendo")
    print("3. Buscar Arriendo")
    print("4. Volver al Menú Principal")
    opc = int(input("Ingrese una opción: "))
    return opc

# ========== INICIALIZACIÓN ==========

def inicial():
    # Cargar datos base de todas las entidades
    print("Cargando datos...")
    EmpleadoDTO().cargarEmpleadosBase()
    ClienteDTO().cargarClientesBase()
    VehiculoDTO().cargarVehiculosBase()
    ArriendoDTO().cargarArriendosBase()
    print("Datos cargados exitosamente!")
    
    # Sistema de login
    print("\n=== LOGIN ===")
    empleado = validarLogin()
    if empleado is not None:
        print(f"¡Bienvenido(a) {empleado.getNombre()} {empleado.getApellido()}!")
        mainMenu()
    else:
        print("Credenciales incorrectas")

def mainMenu():
    while True:
        opc = menuPrincipal()
        
        if opc == 1:  # Empleados
            while True:
                opc_emp = menuEmpleados()
                if opc_emp == 1:
                    listAllEmpleados()
                elif opc_emp == 2:
                    validateAddEmpleado()
                elif opc_emp == 3:
                    validaDelEmpleado()
                elif opc_emp == 4:
                    validateUpdateEmpleado()
                elif opc_emp == 5:
                    validateFindEmpleado()
                else:
                    break
                    
        elif opc == 2:  # Clientes
            while True:
                opc_cli = menuClientes()
                if opc_cli == 1:
                    listAllClientes()
                elif opc_cli == 2:
                    validateAddCliente()
                elif opc_cli == 3:
                    validaDelCliente()
                elif opc_cli == 4:
                    validateUpdateCliente()
                elif opc_cli == 5:
                    validateFindCliente()
                else:
                    break
                    
        elif opc == 3:  # Vehículos
            while True:
                opc_veh = menuVehiculos()
                if opc_veh == 1:
                    listAllVehiculos()
                elif opc_veh == 2:
                    listVehiculosDisponibles()
                elif opc_veh == 3:
                    validateAddVehiculo()
                elif opc_veh == 4:
                    validaDelVehiculo()
                elif opc_veh == 5:
                    validateUpdateVehiculo()
                elif opc_veh == 6:
                    validateFindVehiculo()
                else:
                    break
                    
        elif opc == 4:  # Arriendos
            while True:
                opc_arr = menuArriendos()
                if opc_arr == 1:
                    listAllArriendos()
                elif opc_arr == 2:
                    validateAddArriendo()
                elif opc_arr == 3:
                    validateFindArriendo()
                else:
                    break
                    
        elif opc == 5:  # Salir
            print("¡Hasta pronto!")
            break
        else:
            print("Opción inválida")