from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_cliente import ClienteDTO
from controlador.dto_vehiculo import VehiculoDTO
from controlador.dto_arriendo import ArriendoDTO
from dao.dao_arriendo import daoArriendo
from modelo.empleado import Empleado
from modelo.cliente import Cliente
from modelo.vehiculo import Vehiculo
from modelo.arriendo import Arriendo

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
        # CORREGIDO: Usar constructor (NO setRun)
        empleado_buscar = Empleado(run, "", "", 0, "", "")
        resu = EmpleadoDTO().buscarEmpleado(empleado_buscar)
        if resu is not None:
            print(f"Resultado: {resu}")
        else:
            print("Empleado no encontrado")

def validaDelEmpleado():
    run = input("Ingrese el RUN del empleado a eliminar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validaDelEmpleado()
    
    # CORREGIDO: Usar constructor
    empleado_buscar = Empleado(run, "", "", 0, "", "")
    resu = EmpleadoDTO().buscarEmpleado(empleado_buscar)
    
    if resu is not None:
        print("Datos -->", resu)
        respuesta = input("¿Está seguro de la eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            empleado_eliminar = Empleado(run, "", "", 0, "", "")
            print(EmpleadoDTO().eliminarEmpleado(empleado_eliminar))
        else:
            print("Eliminación cancelada")
    else:
        print("Empleado no encontrado")

def validateUpdateEmpleado():
    run = input("Ingrese el RUN del empleado a modificar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateUpdateEmpleado()
    
    empleado_buscar = Empleado(run, "", "", 0, "", "")
    resu = EmpleadoDTO().buscarEmpleado(empleado_buscar)
    
    if resu is not None:
        print("Datos actuales -->", resu)
        nombre = input("Ingrese nuevo nombre: ")
        apellido = input("Ingrese nuevo apellido: ")
        cargo = input("Ingrese nuevo cargo: ")
        clave = input("Ingrese nueva contraseña: ")
        
        # CORREGIDO: Constructor con todos los datos
        empleado_actualizar = Empleado(run, nombre, apellido, 0, cargo, clave)
        print(EmpleadoDTO().actualizarEmpleado(empleado_actualizar))
    else:
        print("Empleado no encontrado")

def validateAddEmpleado():
    run = input("Ingrese RUN del empleado: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateAddEmpleado()
    
    empleado_buscar = Empleado(run, "", "", 0, "", "")
    resu = EmpleadoDTO().buscarEmpleado(empleado_buscar)
    
    if resu is not None:
        print("Empleado ya existe -->", resu)
    else:
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        codigo = int(input("Ingrese código: "))
        cargo = input("Ingrese cargo: ")
        clave = input("Ingrese contraseña: ")
        
        empleado_nuevo = Empleado(run, nombre, apellido, codigo, cargo, clave)
        print(EmpleadoDTO().agregarEmpleado(empleado_nuevo))

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
        # CORREGIDO: Usar constructor
        cliente_buscar = Cliente(run, "", "", "", "")
        resu = ClienteDTO().buscarCliente(cliente_buscar)
        if resu is not None:
            print(f"Resultado: {resu}")
        else:
            print("Cliente no encontrado")

def validaDelCliente():
    run = input("Ingrese el RUN del cliente a eliminar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validaDelCliente()
    
    cliente_buscar = Cliente(run, "", "", "", "")
    resu = ClienteDTO().buscarCliente(cliente_buscar)
    
    if resu is not None:
        print("Datos -->", resu)
        respuesta = input("¿Está seguro de la eliminación? [s/n]: ")
        if respuesta.lower() == "s":
            cliente_eliminar = Cliente(run, "", "", "", "")
            print(ClienteDTO().eliminarCliente(cliente_eliminar))
        else:
            print("Eliminación cancelada")
    else:
        print("Cliente no encontrado")

def validateUpdateCliente():
    run = input("Ingrese el RUN del cliente a modificar: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateUpdateCliente()
    
    cliente_buscar = Cliente(run, "", "", "", "")
    resu = ClienteDTO().buscarCliente(cliente_buscar)
    
    if resu is not None:
        print("Datos actuales -->", resu)
        nombre = input("Ingrese nuevo nombre: ")
        apellido = input("Ingrese nuevo apellido: ")
        telefono = input("Ingrese nuevo teléfono: ")
        direccion = input("Ingrese nueva dirección: ")
        
        cliente_actualizar = Cliente(run, nombre, apellido, telefono, direccion)
        print(ClienteDTO().actualizarCliente(cliente_actualizar))
    else:
        print("Cliente no encontrado")

def validateAddCliente():
    run = input("Ingrese RUN del cliente: ")
    if len(run) == 0:
        print("Debe ingresar un RUN")
        return validateAddCliente()
    
    cliente_buscar = Cliente(run, "", "", "", "")
    resu = ClienteDTO().buscarCliente(cliente_buscar)
    
    if resu is not None:
        print("Cliente ya existe -->", resu)
    else:
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        telefono = input("Ingrese teléfono: ")
        direccion = input("Ingrese dirección: ")
        
        cliente_nuevo = Cliente(run, nombre, apellido, telefono, direccion)
        print(ClienteDTO().agregarCliente(cliente_nuevo))

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
        # CORREGIDO: Usar constructor
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
    # CORREGIDO: Usar constructor
    arriendo_buscar = Arriendo(numArriendo, None, None, 0, None, None, None)
    resu = ArriendoDTO().buscarArriendo(arriendo_buscar)
    if resu is not None:
        print(f"Resultado: {resu}")
    else:
        print("Arriendo no encontrado")

def validateAddArriendo():
    print("\n=== NUEVO ARRIENDO ===")
    numArriendo = int(input("Ingrese número de arriendo: "))
    
    # Verificar si ya existe
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
        
        # Crear objetos para las relaciones
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
    
    # CORREGIDO: Usar DTO en lugar de DAO directo
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

def validarLogin():
    run = input("Ingrese RUN: ")
    clave = input("Ingrese contraseña: ")
    
    # CORREGIDO: Constructor con TODOS los parámetros requeridos
    empleado_login = Empleado(run, "", "", 0, "", clave)  # ✅ TODOS LOS PARÁMETROS
    resultado = EmpleadoDTO().validarLogin(empleado_login)
    return resultado

# ========== MENÚS ==========
# (Los menús se mantienen igual - solo interfaz de usuario)

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