CREATE DATABASE IF NOT EXISTS arriendos_db;
USE arriendos_db;

-- ==================================================
-- TABLA PERSONA (CLASE BASE PARA HERENCIA)
-- ==================================================
CREATE TABLE IF NOT EXISTS persona (
    run VARCHAR(12) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL
);

-- ==================================================
-- TABLA EMPLEADO (HEREDA DE PERSONA) - CON ROLES
-- ==================================================
CREATE TABLE IF NOT EXISTS empleado (
    run VARCHAR(12) PRIMARY KEY,
    codigo INT UNIQUE NOT NULL,
    cargo VARCHAR(30) NOT NULL CHECK (cargo IN ('gerente', 'empleado')),
    password VARCHAR(255) NOT NULL,
    supervisor_id INT NULL,
    FOREIGN KEY (run) REFERENCES persona(run) ON DELETE CASCADE,
    FOREIGN KEY (supervisor_id) REFERENCES empleado(codigo)
);

-- ==================================================
-- TABLA CLIENTE (HEREDA DE PERSONA)
-- ==================================================
CREATE TABLE IF NOT EXISTS cliente (
    run VARCHAR(12) PRIMARY KEY,
    telefono VARCHAR(15),
    direccion VARCHAR(100),
    FOREIGN KEY (run) REFERENCES persona(run) ON DELETE CASCADE
);

-- ==================================================
-- TABLA VEHICULO (ACTUALIZADA)
-- ==================================================
CREATE TABLE IF NOT EXISTS vehiculo (
    patente VARCHAR(10) PRIMARY KEY,
    marca VARCHAR(30) NOT NULL,
    modelo VARCHAR(30) NOT NULL,
    año INT NOT NULL,
    precio_uf DECIMAL(10,2) NOT NULL,  -- Cambiado de 'precio' a 'precio_uf'
    disponible ENUM('disponible', 'reservado', 'ocupado', 'mantención') DEFAULT 'disponible'  -- 4 estados
);

-- ==================================================
-- TABLA ARRIENDO (PREPARADA PARA API UF)
-- ==================================================
CREATE TABLE IF NOT EXISTS arriendo (
    numArriendo INT AUTO_INCREMENT PRIMARY KEY,
    fechaInicio DATE NOT NULL,
    fechaEntrega DATE NOT NULL,
    costo_total_uf DECIMAL(10,2) NOT NULL,      -- Total en UF
    valor_uf_dia DECIMAL(10,2) NOT NULL,        -- Valor UF usado para cálculo
    costo_total_pesos DECIMAL(12,2) NOT NULL,   -- Total en pesos chilenos
    run_cliente VARCHAR(12) NOT NULL,
    run_empleado VARCHAR(12) NOT NULL,
    patente_vehiculo VARCHAR(10) NOT NULL,
    FOREIGN KEY (run_cliente) REFERENCES cliente(run),
    FOREIGN KEY (run_empleado) REFERENCES empleado(run),
    FOREIGN KEY (patente_vehiculo) REFERENCES vehiculo(patente),
    INDEX idx_fecha_inicio (fechaInicio),
    INDEX idx_cliente (run_cliente)
);

-- ==================================================
-- DATOS DE PRUEBA ACTUALIZADOS
-- ==================================================

-- Insertar gerente por defecto (password: 123)
INSERT IGNORE INTO persona (run, nombre, apellido) VALUES 
('11111111-1', 'Admin', 'Sistema');

INSERT IGNORE INTO empleado (run, codigo, cargo, password, supervisor_id) VALUES 
('11111111-1', 1, 'gerente', '$2b$12$famS.TS49JhZSoV1ZNu7.u5cP1YftpbW4yYlpzGQ5W5s6gw27rlKu', NULL);

-- Insertar empleado normal (password: 123)
INSERT IGNORE INTO persona (run, nombre, apellido) VALUES 
('22222222-2', 'Juan', 'Perez');

INSERT IGNORE INTO empleado (run, codigo, cargo, password, supervisor_id) VALUES 
('22222222-2', 2, 'empleado', '$2b$12$famS.TS49JhZSoV1ZNu7.u5cP1YftpbW4yYlpzGQ5W5s6gw27rlKu', 1);

-- Insertar cliente de prueba
INSERT IGNORE INTO persona (run, nombre, apellido) VALUES 
('33333333-3', 'Maria', 'Gonzalez');

INSERT IGNORE INTO cliente (run, telefono, direccion) VALUES 
('33333333-3', '12345678', 'Calle Principal 123');

-- Insertar vehículos de prueba con precio_uf y diferentes estados
INSERT IGNORE INTO vehiculo (patente, marca, modelo, año, precio_uf, disponible) VALUES 
('AB-CD-12', 'Toyota', 'Corolla', 2022, 1.5, 'disponible'),
('BC-DE-34', 'Honda', 'Civic', 2023, 2.0, 'reservado'),
('CD-EF-56', 'Ford', 'Focus', 2021, 1.2, 'ocupado'),
('DE-FG-78', 'Chevrolet', 'Spark', 2020, 0.8, 'mantención');

-- ==================================================
-- CONSULTAS ÚTILES ACTUALIZADAS
-- ==================================================

-- Ver empleados con información completa
SELECT p.run, p.nombre, p.apellido, e.codigo, e.cargo 
FROM empleado e 
JOIN persona p ON e.run = p.run;

-- Ver clientes con información completa
SELECT p.run, p.nombre, p.apellido, c.telefono, c.direccion 
FROM cliente c 
JOIN persona p ON c.run = p.run;

-- Ver vehículos disponibles para arriendo (disponible + reservado)
SELECT patente, marca, modelo, año, precio_uf, disponible 
FROM vehiculo 
WHERE disponible IN ('disponible', 'reservado');

-- Ver todos los vehículos con estados
SELECT patente, marca, modelo, año, precio_uf, disponible 
FROM vehiculo 
ORDER BY disponible, marca;