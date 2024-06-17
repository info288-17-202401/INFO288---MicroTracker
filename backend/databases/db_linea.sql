
CREATE DATABASE db_linea WITH  TABLESPACE = pg_default IS_TEMPLATE = False;
\c db_linea

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
\c db_linea
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
\c db_linea

--HACER TABLA SECTOR - LINEA
CREATE TABLE line (
    number INTEGER PRIMARY KEY,
    color VARCHAR NOT NULL
    -- Arrreglo de puntos (RUTA)
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
    route GEOMETRY(MultiPoint, 4326) NOT NULL,
    line_id INTEGER NOT NULL,
    FOREIGN KEY (line_id) REFERENCES line(number)
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

CREATE TABLE bus_stop (
    id SERIAL PRIMARY KEY,
    coordinates GEOMETRY(Point, 4326) NOT NULL,
);

CREATE TABLE route_busstop (
    id SERIAL PRIMARY KEY,
    id_ruta_fk INTEGER NOT NULL,
    id_busstop_fk INTEGER NOT NULL,
    FOREIGN KEY (id_ruta_fk) REFERENCES route(id),
    FOREIGN KEY (id_busstop_fk) REFERENCES bus_stop(id)
);