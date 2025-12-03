CREATE TABLE estadisticas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    papel INT DEFAULT 0,
    plastico INT DEFAULT 0,
    organico INT DEFAULT 0
);
INSERT INTO estadisticas (fecha, papel, plastico, organico) VALUES('2025-11-20', 150, 85, 300);
INSERT INTO estadisticas (fecha, papel, plastico, organico) VALUES('2025-11-21', 180, 110, 320);
INSERT INTO estadisticas (fecha, papel, plastico, organico) VALUES('2025-11-22', 120, 90, 280);
INSERT INTO estadisticas (fecha, papel, plastico, organico) VALUES('2025-11-23', 210, 130, 350);
INSERT INTO estadisticas (fecha, papel, plastico, organico) VALUES('2025-11-24', 165, 75, 310);