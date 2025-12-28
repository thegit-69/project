-- For creating users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL, 
    cash NUMERIC NOT NULL DEFAULT 10000.00);


-- For creating Medcines table
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL, 
    quantity INTEGER NOT NULL, 
    price INTEGER NOT NULL, 
    purchase_date DATE NOT NULL, 
    expiry_date DATE NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY(user_id) REFERENCES users(id));


-- For creating logbook table
CREATE TABLE logbook (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    med_name TEXT NOT NULL,
    trans_type TEXT NOT NULL,
    amount INTEGER NOT NULL, 
    transacted_at INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP);