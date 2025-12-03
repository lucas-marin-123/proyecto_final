CREATE DATABASE clasificacion_residuos;
USE clasificacion_residuos;
CREATE TABLE residuos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- Registros de hace 2 días (ejemplo histórico)
INSERT INTO residuos (tipo, fecha) VALUES ('Papel', '2025-11-18 09:10:00');
INSERT INTO residuos (tipo, fecha) VALUES ('Plastico', '2025-11-18 09:12:30');
INSERT INTO residuos (tipo, fecha) VALUES ('Organico', '2025-11-18 10:05:15');

-- Registros de ayer
INSERT INTO residuos (tipo, fecha) VALUES ('Papel', '2025-11-19 14:20:00');
INSERT INTO residuos (tipo, fecha) VALUES ('Organico', '2025-11-19 14:35:40');
INSERT INTO residuos (tipo, fecha) VALUES ('Plastico', '2025-11-19 15:00:00');
INSERT INTO residuos (tipo, fecha) VALUES ('Plastico', '2025-11-19 15:01:05');

-- Registros de hoy (usando CURRENT_TIMESTAMP)
INSERT INTO residuos (tipo) VALUES ('Papel');
INSERT INTO residuos (tipo) VALUES ('Organico');
INSERT INTO residuos (tipo) VALUES ('Plastico');
INSERT INTO residuos (tipo) VALUES ('Organico');