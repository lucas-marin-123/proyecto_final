CREATE TABLE estadisticas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    papel INT DEFAULT 0,
    plastico INT DEFAULT 0,
    organico INT DEFAULT 0
);