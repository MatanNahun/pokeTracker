-- CREATE DATABASE pokeTracker;


USE pokeTracker;

-- CREATE TABLE pokemons(
--     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255),
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

-- CREATE TABLE pokemon_types(
--     name VARCHAR(255),
--     poke_type VARCHAR(255),
--     PRIMARY KEY(name, poke_type)
-- );

-- select * FROM pokemons_trainers;

INSERT INTO pokemons VALUES(132, "yanma", {pokemon["height"]}, {pokemon["weight"]} );