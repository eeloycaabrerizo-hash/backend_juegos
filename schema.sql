-- Tabla de juegos
DROP TABLE IF EXISTS games;

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    anio INTEGER,
    descripcion TEXT,
    imagen TEXT,
    enlace TEXT
);

INSERT INTO games (nombre, anio, descripcion, imagen, enlace) VALUES
('Dinosaur Game', 2014, 'El clásico T-Rex de Google. Salta cactus y esquiva pterodáctilos mientras esperas a que vuelva el internet.', '/Dinosaurio-de-Google.png', 'https://trex-runner.com/'),
('Snake', 1997, 'Controla a una serpiente hambrienta. Come manzanas para crecer, pero cuidado con morderte la cola en el intento.', '/Snake-Google.png', 'https://playsnake.org/'),
('Asteroids', 1979, 'Pilota tu nave en un campo de asteroides. Dispara para destruirlos y sobrevive al caos espacial.', '/Asteroids-Google.png', 'https://freeasteroids.org/'),
('Flappy Bird', 2013, 'Vuela entre las tuberías tocando la pantalla. Un desafío de precisión y paciencia extrema.', '/Flappy-Bird-Google.png', 'https://flappybird.io/'),
('Tres en Raya', 1952, 'El juego clásico de X y O. Intenta alinear tres símbolos antes que tu oponente en el tablero de cuadrícula.', '/Tres-En-Raya-Google.png', 'https://playtictactoe.org/'),
('Ahorcado', 1894, 'Adivina la palabra oculta letra por letra antes de que se complete el dibujo en la horca.', '/Ahorcado-Google.png', 'https://hangmanwordgame.com/'),
('Pac-Man', 1980, 'Come todos los puntos del laberinto mientras esquivas a los fantasmas Blinky, Pinky, Inky y Clyde.', '/Pacman-Google.jpg', 'https://freepacman.org/'),
('Space Invaders', 1978, 'Defiende la Tierra de oleadas de alienígenas descendentes usando tu cañón láser.', '/Space-Invaders-Google.png', 'https://freeinvaders.org/');

-- Tabla de usuarios (para el login)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);