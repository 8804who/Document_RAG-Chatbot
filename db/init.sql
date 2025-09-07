CREATE TABLE IF NOT EXISTS google_oauth (
	email VARCHAR(100) PRIMARY KEY,
	name VARCHAR(100),
	refresh_token VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS chat_log (
	id SERIAL PRIMARY KEY,
	email VARCHAR(100),
	query VARCHAR(5000),
	answer VARCHAR(5000),
	created_at TIMESTAMP,
	FOREIGN KEY (email) REFERENCES google_oauth(email)
);

CREATE TABLE IF NOT EXISTS session_id (
	email VARCHAR(100) PRIMARY KEY,
	session_id VARCHAR(100),
	FOREIGN KEY (email) REFERENCES google_oauth(email)
);