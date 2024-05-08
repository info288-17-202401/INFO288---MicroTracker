
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
    -- coordinates GEOMETRY(Point, 4326) NOT NULL,  -- Use 'Point' instead of 'POINT'
    coordinates POINT NOT NULL,  -- Use 'Point' instead of 'POINT'
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