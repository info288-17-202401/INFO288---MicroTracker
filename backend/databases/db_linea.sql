CREATE DATABASE db_linea;
\c db_linea

CREATE TABLE line (
    number INTEGER PRIMARY KEY,
    color VARCHAR NOT NULL
);

CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL
);

CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    año INTEGER NOT NULL,
    nombre VARCHAR NOT NULL,
    id_marca_fk INTEGER NOT NULL,
    FOREIGN KEY (id_marca_fk) REFERENCES brand(id)
);

CREATE TABLE route (
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL,
    date DATE NOT NULL,
    actual BOOLEAN NOT NULL
);

CREATE TABLE sector (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL
);

CREATE TABLE microbus (
    patent VARCHAR PRIMARY KEY,
    linea_id INTEGER NOT NULL,
    marca_id INTEGER NOT NULL,
    FOREIGN KEY (linea_id) REFERENCES line(number),
    FOREIGN KEY (marca_id) REFERENCES brand(id)
);

CREATE TABLE ubication (
    id SERIAL PRIMARY KEY,
    micro_patent VARCHAR NOT NULL,
    date DATE NOT NULL,
    coordinates POINT NOT NULL,
    actual BOOLEAN NOT NULL,
    FOREIGN KEY (micro_patent) REFERENCES microbus(patent)
);

CREATE TABLE passengers (
    id SERIAL PRIMARY KEY,
    micro_patent VARCHAR NOT NULL,
    number INTEGER NOT NULL,
    date DATE NOT NULL,
    actual BOOLEAN NOT NULL,
    FOREIGN KEY (micro_patent) REFERENCES microbus(patent)
);

CREATE TABLE bus_stop (
    id SERIAL PRIMARY KEY,
    coordinates POINT NOT NULL,
    id_ruta_fk INTEGER NOT NULL,
    FOREIGN KEY (id_ruta_fk) REFERENCES route(id)
);

CREATE TABLE prediction_log_velocity (
    id SERIAL PRIMARY KEY,
    velocidad FLOAT NOT NULL,
    date DATE NOT NULL,
    id_micro_fk VARCHAR NOT NULL,
    actual BOOLEAN NOT NULL,
    FOREIGN KEY (id_micro_fk) REFERENCES microbus(patent)
);