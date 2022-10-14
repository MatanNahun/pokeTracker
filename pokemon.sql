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

-- SELECT name, (weight) FROM pokemons WHERE weight = All (SELECT MAX(weight) FROM pokemons)

-- SELECT name FROM pokemons WHERE type = "grass"

-- SELECT pokemons_trainers.trainer FROM pokemons, pokemons_trainers WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons.name = "gengar"

-- SELECT pokemons.name FROM pokemons_trainers, pokemons WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons_trainers.trainer = "Loga"