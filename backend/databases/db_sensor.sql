
CREATE DATABASE db_sensor WITH  TABLESPACE = pg_default IS_TEMPLATE = False;
\c db_sensor

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
\c db_sensor
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
\c db_sensor

CREATE TABLE microbus_sensor (
    patent VARCHAR PRIMARY KEY,
    line INTEGER NOT NULL
);

CREATE TABLE microbus_state (
    id SERIAL PRIMARY KEY,
    patent VARCHAR NOT NULL,
    date DATE NOT NULL,
    velocity FLOAT NOT NULL,
    passengers INTEGER NOT NULL,
    -- date DATE NOT NULL = NOW(),
    -- Use 'Point' instead of 'POINT' because POINT gets error
    coordinates GEOMETRY(Point, 4326) NOT NULL,  
    currently BOOLEAN NOT NULL,
    FOREIGN KEY (patent) REFERENCES microbus_sensor(patent)
);

-- Creamos una función genérica para actualizar el estado 'currently'
CREATE OR REPLACE FUNCTION update_currently()
RETURNS TRIGGER AS $$
-- DECLARE
--     current_timestamp TIMESTAMP WITH TIME ZONE := NOW();
BEGIN
    -- Obtenemos el nombre de la tabla afectada
    EXECUTE format('UPDATE %I SET currently = FALSE WHERE currently = TRUE AND patent = %L', TG_TABLE_NAME, NEW.patent);
    NEW.currently = TRUE;
    -- NEW.date = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creamos un trigger genérico para la tabla 'ubication'
CREATE TRIGGER update_currently_estado_microbus
BEFORE INSERT ON microbus_state
FOR EACH ROW
EXECUTE FUNCTION update_currently();


CREATE DATABASE db_sensor2 WITH  TABLESPACE = pg_default IS_TEMPLATE = False;
\c db_sensor2

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
\c db_sensor2
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
\c db_sensor2

CREATE TABLE microbus_sensor (
    patent VARCHAR PRIMARY KEY,
    line INTEGER NOT NULL
    -- line INTEGER NOT NULL,
);

CREATE TABLE microbus_state (
    id SERIAL PRIMARY KEY,
    patent VARCHAR NOT NULL,
    date DATE NOT NULL,
    velocity FLOAT NOT NULL,
    passengers INTEGER NOT NULL,
    -- date DATE NOT NULL = NOW(),
    -- Use 'Point' instead of 'POINT' because POINT gets error
    coordinates GEOMETRY(Point, 4326) NOT NULL,  
    currently BOOLEAN NOT NULL,
    FOREIGN KEY (patent) REFERENCES microbus_sensor(patent)
);

-- Creamos una función genérica para actualizar el estado 'currently'
CREATE OR REPLACE FUNCTION update_currently()
RETURNS TRIGGER AS $$
-- DECLARE
--     current_timestamp TIMESTAMP WITH TIME ZONE := NOW();
BEGIN
    -- Obtenemos el nombre de la tabla afectada
    EXECUTE format('UPDATE %I SET currently = FALSE WHERE currently = TRUE AND patent = %L', TG_TABLE_NAME, NEW.patent);
    NEW.currently = TRUE;
    -- NEW.date = current_timestamp;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creamos un trigger genérico para la tabla 'ubication'
CREATE TRIGGER update_currently_estado_microbus
BEFORE INSERT ON microbus_state
FOR EACH ROW
EXECUTE FUNCTION update_currently();