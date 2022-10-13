-- CREATE DATABASE pokeTracker;


USE pokeTracker;

-- CREATE TABLE pokemons(
--     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255),
--     type VARCHAR(255),
--     height INT,
--     weight INT
-- );


-- CREATE TABLE trainers(
   
--     name VARCHAR(255),
--     town VARCHAR(255),
--     PRIMARY KEY (name)
-- );


-- CREATE TABLE pokemons_trainers(
--     id_pokemon INT,
--     trainer VARCHAR(255),

--     PRIMARY KEY (id_pokemon, trainer),

--     FOREIGN KEY(id_pokemon) REFERENCES pokemons(id),
--     FOREIGN KEY(trainer) REFERENCES trainers(name)
-- );



-- SELECT * FROM pokemons_trainers;