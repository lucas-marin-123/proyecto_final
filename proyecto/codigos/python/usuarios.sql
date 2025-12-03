CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    rol VARCHAR(20)
);

INSERT INTO usuarios (nombre, rol) VALUES ('Juan Pérez', 'administrador');
INSERT INTO usuarios (nombre, rol) VALUES ('Ana López', 'operador');
INSERT INTO usuarios (nombre, rol) VALUES ('Carlos Ruiz', 'operador');