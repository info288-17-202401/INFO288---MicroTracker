CREATE DATABASE db_linea;
\c db_linea

CREATE TABLE line (
    number INTEGER PRIMARY KEY,
    color VARCHAR NOT NULL
);

CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    id_marca_fk INTEGER NOT NULL,
    FOREIGN KEY (id_marca_fk) REFERENCES brand(id)
);

CREATE TABLE route (
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL,
    date DATE NOT NULL,
    currently BOOLEAN NOT NULL
);

CREATE TABLE sector (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE microbus (
    patent VARCHAR PRIMARY KEY,
    line_id INTEGER NOT NULL,
    brand_id INTEGER NOT NULL,
    FOREIGN KEY (line_id) REFERENCES line(number),
    FOREIGN KEY (brand_id) REFERENCES brand(id)
);

CREATE TABLE ubication (
    id SERIAL PRIMARY KEY,
    micro_patent VARCHAR NOT NULL,
    date DATE NOT NULL,
    coordinates POINT NOT NULL,
    currently BOOLEAN NOT NULL,
    FOREIGN KEY (micro_patent) REFERENCES microbus(patent)
);

CREATE TABLE passengers (
    id SERIAL PRIMARY KEY,
    micro_patent VARCHAR NOT NULL,
    number INTEGER NOT NULL,
    date DATE NOT NULL,
    currently BOOLEAN NOT NULL,
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
    velocity FLOAT NOT NULL,
    date DATE NOT NULL,
    id_micro_fk VARCHAR NOT NULL,
    currently BOOLEAN NOT NULL,
    FOREIGN KEY (id_micro_fk) REFERENCES microbus(patent)
);