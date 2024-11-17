-- This file should contain table definitions for the database.
-- SET search_path TO <path_name>;

DROP TABLE IF EXISTS FACT_Transaction;
DROP TABLE IF EXISTS DIM_Truck;
DROP TABLE IF EXISTS DIM_Payment_Method;

-- Create DIM_Payment_Method table
CREATE TABLE DIM_Payment_Method (
    payment_method_id SMALLINT PRIMARY KEY,
    payment_method VARCHAR(50) NOT NULL
);

-- Create DIM_Truck table
CREATE TABLE DIM_Truck (
    truck_id SMALLINT PRIMARY KEY,
    truck_name TEXT NOT NULL,
    truck_description TEXT,
    has_card_reader BOOLEAN NOT NULL,
    fsa_rating SMALLINT
);

-- Create FACT_Transaction table
CREATE TABLE FACT_Transaction (
    transaction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    truck_id SMALLINT NOT NULL,
    payment_method_id SMALLINT NOT NULL,
    total FLOAT NOT NULL,
    at TIMESTAMP NOT NULL,
    FOREIGN KEY (truck_id) REFERENCES DIM_Truck (truck_id),
    FOREIGN KEY (payment_method_id) REFERENCES DIM_Payment_Method (payment_method_id)
);

INSERT INTO DIM_Truck (truck_id, truck_name, truck_description, has_card_reader, fsa_rating) VALUES
(1, 'Burrito Madness', 'An authentic taste of Mexico.', TRUE, 4),
(2, 'Kings of Kebabs', 'Locally-sourced meat cooked over a charcoal grill.', TRUE, 2),
(3, 'Cupcakes by Michelle', 'Handcrafted cupcakes made with high-quality, organic ingredients.', TRUE, 5),
(4, 'Hartmann''s Jellied Eels', 'A taste of history with this classic English dish.', TRUE, 4),
(5, 'Yoghurt Heaven', 'All the great tastes, but only some of the calories!', TRUE, 4),
(6, 'SuperSmoothie', 'Pick any fruit or vegetable, and we''ll make you a delicious, healthy, multi-vitamin shake. Live well; live wild.', FALSE, 3);

INSERT INTO DIM_Payment_Method (payment_method_id, payment_method) VALUES
(1, 'cash'),
(2, 'card');