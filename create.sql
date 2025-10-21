CREATE TABLE user(
  username varchar(16) NOT NULL,
  email varchar(255) DEFAULT NULL,
  password varchar(32) NOT NULL,
  create_time timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(username)
)