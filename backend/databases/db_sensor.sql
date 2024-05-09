
CREATE DATABASE db_sensor WITH  TABLESPACE = pg_default IS_TEMPLATE = False;
\c db_sensor

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
\c db_sensor
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
\c db_sensor

CREATE TABLE microbus (
    patent VARCHAR PRIMARY KEY
);

CREATE TABLE ubication (
    id SERIAL PRIMARY KEY,
    micro_patent VARCHAR NOT NULL,
    date DATE NOT NULL,
    -- Use 'Point' instead of 'POINT' because POINT gets error
    coordinates GEOMETRY(Point, 4326) NOT NULL,  
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


CREATE TABLE velocity (
    id SERIAL PRIMARY KEY,
    velocity FLOAT NOT NULL,
    date DATE NOT NULL,
    micro_patent VARCHAR NOT NULL,
    currently BOOLEAN NOT NULL,
    FOREIGN KEY (micro_patent) REFERENCES microbus(patent)
);

-- Creamos una función genérica para actualizar el estado 'currently'
CREATE OR REPLACE FUNCTION update_currently()
RETURNS TRIGGER AS $$
BEGIN
    -- Obtenemos el nombre de la tabla afectada
    EXECUTE format('UPDATE %I SET currently = FALSE WHERE currently = TRUE', TG_TABLE_NAME);
    NEW.currently = TRUE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creamos un trigger genérico para la tabla 'ubication'
CREATE TRIGGER update_currently_ubication
BEFORE INSERT ON ubication
FOR EACH ROW
EXECUTE FUNCTION update_currently();

-- Creamos un trigger genérico para la tabla 'velocity'
CREATE TRIGGER update_currently_velocity
BEFORE INSERT ON velocity
FOR EACH ROW
EXECUTE FUNCTION update_currently();

-- Creamos un trigger genérico para la tabla 'passengers'
CREATE TRIGGER update_currently_passengers
BEFORE INSERT ON passengers
FOR EACH ROW
EXECUTE FUNCTION update_currently();
