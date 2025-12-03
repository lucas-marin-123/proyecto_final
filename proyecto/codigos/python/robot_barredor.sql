CREATE DATABASE clasificacion_residuos;
USE clasificacion_residuos;
CREATE TABLE residuos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    rol VARCHAR(20)
);
CREATE TABLE estadisticas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    papel INT DEFAULT 0,
    plastico INT DEFAULT 0,
    organico INT DEFAULT 0
);
