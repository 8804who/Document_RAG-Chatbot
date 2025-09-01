CREATE TABLE IF NOT EXISTS google_oauth (
	email VARCHAR(100) PRIMARY KEY,
	name VARCHAR(100),
	refresh_token VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS chat_log (
	id SERIAL PRIMARY KEY,
	email VARCHAR(100),
	query VARCHAR(500),
	answer VARCHAR(500),
	created_at TIMESTAMP,
	FOREIGN KEY (email) REFERENCES google_oauth(email)
);

CREATE TABLE IF NOT EXISTS chat_history (
	session_id VARCHAR(100) PRIMARY KEY,
	context VARCHAR(10000),
	FOREIGN KEY (email) REFERENCES google_oauth(email)
);