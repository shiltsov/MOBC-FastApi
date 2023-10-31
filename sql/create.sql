CREATE TABLE dogs
(
    pk          serial primary key,
    name        VARCHAR(64) not null,
    kind        VARCHAR(64) not null
);

INSERT INTO dogs(name, kind) 
VALUES 
    ('Bob','terrier'),
    ('Marli', 'bulldog'),
    ('Snoopy', 'dalmatian'),
    ('Rex', 'dalmatian'),
    ('Pongo', 'dalmatian'),
    ('Tillman', 'bulldog'),
    ('Uga', 'bulldog');