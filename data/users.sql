DROP TABLE IF EXISTS users;
CREATE TABLE users(
   username VARCHAR(50) NOT NULL PRIMARY KEY,
   password VARCHAR(24) NOT NULL);

INSERT INTO users(username,password) VALUES ('admin','pASSw0rD*123');
INSERT INTO users(username,password) VALUES ('user1','pASSw0rD*456');
INSERT INTO users(username,password) VALUES ('user2','pASSw0rD*789');
