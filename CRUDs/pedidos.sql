CREATE TABLE pedidos(
    id              INTEGER PRIMARY KEY,
    cliente_id      INTEGER NOT NULL REFERENCES clientes(id),
    valor_total     DECIMAL(10,2) NOT NULL,
    status          VARCHAR(20) NOT NULL
); 