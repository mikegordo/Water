DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS pot;
DROP TABLE IF EXISTS moisture;
DROP TABLE IF EXISTS water;

CREATE TABLE "user"
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL,
    token    TEXT,
    created  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pot
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT          NOT NULL UNIQUE,
    description    TEXT,
    water_value    INTEGER       NOT NULL,
    moisture_value DECIMAL(8, 6) NOT NULL DEFAULT 99.9,
    created        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE moisture
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pot_id      INTEGER         NOT NULL,
    value       DECIMAL(8, 6)   NOT NULL,
    description TEXT,
    created     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pot_id) REFERENCES pot (id)
);

CREATE TABLE water
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pot_id      INTEGER   NOT NULL,
    value       INTEGER   NOT NULL,
    description TEXT,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pot_id) REFERENCES pot (id)
);

