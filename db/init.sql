CREATE TABLE user_table (
	username VARCHAR(20) PRIMARY KEY,
	password VARCHAR(60) NOT NULL,
	email VARCHAR(100) NOT NULL
);

CREATE TABLE chat_log (
	id SERIAL PRIMARY KEY,
	username VARCHAR(20),
	query VARCHAR(500),
	answer VARCHAR(500),
	created_at TIMESTAMP,
	FOREIGN KEY (username) REFERENCES user_table(username)
);