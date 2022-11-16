CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY,
    region_id INTEGER NOT NULL,
    city_name TEXT NOT NULL,
    FOREIGN KEY(region_id) REFERENCES regions(id)
);

CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	second_name TEXT NOT NULL,
	patronymic TEXT,
	region_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    phone TEXT,
    email TEXT,
    FOREIGN KEY(region_id) REFERENCES regions(id)
    FOREIGN KEY(city_id) REFERENCES cities(id)
);