-- Crear la base de datos
DROP DATABASE IF EXISTS 4thewords_prueba_robinson_ramirez;
CREATE DATABASE 4thewords_prueba_robinson_ramirez
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE 4thewords_prueba_robinson_ramirez;

-- Tabla: province
CREATE TABLE province (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO province (id, name) VALUES
(1, 'Cundinamarca'), (2, 'Antioquia'), (3, 'Choco'),
(4, 'Boyaca'), (5, 'Casanare');

-- Tabla: canton
CREATE TABLE canton (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    province_id INT NOT NULL,
    FOREIGN KEY (province_id) REFERENCES province(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO canton (id, name, province_id) VALUES
(1, 'Bogota', 1), (2, 'Medellin', 1), (3, 'Barranquilla', 1),
(4, 'Cali', 2), (5, 'Tunja', 2), (6, 'Cartagena', 2),
(7, 'Santa Marta', 3), (8, 'Valledupar', 3), (9, 'Monteria', 3),
(10, 'Pasto', 4), (11, 'Pereira', 4), (12, 'Villavicencio', 4),
(13, 'Quito', 5), (14, 'Cucuta', 5), (15, 'Mocoa', 5);


-- Tabla: district
CREATE TABLE district (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    canton_id INT NOT NULL,
    FOREIGN KEY (canton_id) REFERENCES canton(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO district (id, name, canton_id) VALUES
(1, 'Chia', 1), (2, 'Cajica', 2), (3, 'Cota', 3),
(4, 'Tunjuelito', 4), (5, 'Facatativa', 5), (6, 'Fomeque', 6),
(7, 'Tocancipa', 7), (8, 'Zipaquira', 8), (9, 'Suesca', 9),
(10, 'Soacha', 10), (11, 'Mosquera', 11), (12, 'Madrid', 12),
(13, 'Girardot', 13), (14, 'Melgar', 14), (15, 'Espinal', 15);


-- Tabla: category
CREATE TABLE category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO category (id, name) VALUES
(1, 'Terror'), (2, 'Romance'), (3, 'Fantasia'), (4, 'Historia'), (5, 'Misterio');



