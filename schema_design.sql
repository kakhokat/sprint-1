-- Создание схемы
CREATE SCHEMA IF NOT EXISTS content;

-- Таблица с фильмами
CREATE TABLE IF NOT EXISTS content.film_work (
    film_id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT CHECK (rating >= 0 AND rating <= 10),
    film_type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица с жанрами
CREATE TABLE IF NOT EXISTS content.genre (
    genre_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT genre_name_unique UNIQUE (name)
);

-- Таблица с персонами (актёры, режиссёры, сценаристы)
CREATE TABLE IF NOT EXISTS content.person (
    person_id UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Связь фильмов и жанров
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    genre_film_id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES content.film_work (film_id) ON DELETE CASCADE,
    genre_id UUID NOT NULL REFERENCES content.genre (genre_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT genre_film_work_unique UNIQUE (film_work_id, genre_id)
);

-- Связь фильмов и персон
CREATE TABLE IF NOT EXISTS content.person_film_work (
    person_film_id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES content.film_work (film_id) ON DELETE CASCADE,
    person_id UUID NOT NULL REFERENCES content.person (person_id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT person_film_work_unique UNIQUE (film_work_id, person_id, role)
);

-- Индексы для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_film_work_title ON content.film_work (title);
CREATE INDEX IF NOT EXISTS idx_genre_name ON content.genre (name);
CREATE INDEX IF NOT EXISTS idx_person_full_name ON content.person (full_name);
CREATE INDEX IF NOT EXISTS idx_person_film_work_role ON content.person_film_work (role);
