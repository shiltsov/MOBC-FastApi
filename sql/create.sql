CREATE TABLE dogs
(
    pk          int NOT NULL,
    name        VARCHAR(64) not null,
    kind        VARCHAR(64) not null
);

INSERT INTO dogs(pk, name, kind) 
VALUES 
    (0,'Bob','terrier'),
    (1,'Marli', 'bulldog'),
    (2,'Snoopy', 'dalmatian'),
    (3,'Rex', 'dalmatian'),
    (4,'Pongo', 'dalmatian'),
    (5,'Tillman', 'bulldog'),
    (6,'Uga', 'bulldog');

CREATE TABLE timestamps
(
    id          int,
    timestamp   int
);

INSERT INTO timestamps(id, timestamp)
VALUES
    (0, 12), (1,10)

