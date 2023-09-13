DROP TABLE IF EXISTS products;

CREATE TABLE products 
(
    product_id INTEGER PRIMARY KEY,
    price REAL NOT NULL,
    description TEXT NOT NULL,
    stock INTEGER,
    name TEXT NOT NULL,
    img BLOB
);

INSERT INTO products (product_id, price, description, stock, name, img)
VALUES
    (12, 1200, "Mid range gaming pc with an aio cooler", 14, "Gaming-Pc-Ryzen-5 5600x", 'static/images/AioPC.jpg'),
    (10, 900, "Mid range gaming pc with an air cooler", 14, "Gaming-Pc-Ryzen-5 5600", 'static/images/Air-Cooler-PC.jpg'),
    (54, 2000, "High end gaming pc with an 8 core cpu and an aio", 14, "Gaming-Pc-Ryzen-7 5800x", 'static/images/GamingPc.jpg'),
    (32, 350, 'A 27" 1440p Gaming monitor with a 144Hz refresh rate', 14, "Viewsonic VX2705", 'static/images/ViewSonic-Monitor.jpg'),
    (1, 250, 'A 24" 1080p Gaming monitor with a 144Hz refresh rate', 14, "HP X24c Gaming Monitor", 'static/images/HP-X24c-Gaming-Monitor.jpg'),
    (2, 59.99, "A keyboard and mouse bundle great with any pc", 14, "Daewood Gaming Bundle", 'static/images/Keyboard+Mouse-Set.jpg'),
    (7, 650, "New MSI RTX 3070 Suprim X, was used to mine crypto for a small bit only 6 months", 14, "MSI RTX 3070 GPU", 'static/images/RTX-3070-GPU-New.jpg'),
    (100, 250, "A 8-core cpu perfect for multi-media and gaming", 14, "Ryzen 7 5800x", 'static/images/Ryzen-7-5800x.jpg'),
    (20, 69.99, "A black xbox controller", 14, "Xbox Contoller-Black", 'static/images/Xbox-Controller-Black.jpg'),
    (30, 69.99, "A white xbox controller with built in bluetooth", 14, "Xbox Controller-White", 'static/images/Xbox-Controller-White.jpg'),
    (34, 24999.99, "A bitcoin mining rig for ethusiasts", 14, "Bitcoin Mining Rig", 'static/images/bitcoin-server.jpg'),
    (19, 2000, "A very old brick phone that doubles as a weapon", 14, "Brick Phone", 'static/images/brick.jpg'),
    (3, 250, "A modern smartphone for everyday useage", 14, "Motorola Smart Phone", 'static/images/motorola.jpg'),
    (4, 10000, "A server rig for hosting your minecraft session", 14, "A Server", 'static/images/server.jpg'),
    (5, 1000, "A bundle of slightly used phones", 14, "Slightly Used Phones", 'static/images/slightly-used.jpg'),
    (99, 90, "A clasic xbox 360", 14, "Xbox 360 Console", 'static/images/xbox-360.jpg'),
    (88,350, "A new xbox series s console", 14, "Xbox Series S", 'static/images/xbox-series-s.jpg');

DROP TABLE IF EXISTS services;

CREATE TABLE services 
(
    product_id INTEGER PRIMARY KEY,
    price REAL NOT NULL,
    description TEXT NOT NULL,
    name TEXT NOT NULL,
    img BLOB
);

INSERT INTO services (product_id, price, description, name, img)
VALUES
    (60, 25, "We offer an authentication service to try and protect your business' or personal information from password theft", "Authentication Service", 'static/images/authentication.jpg' ),
    (61, 40, "We offer a cload storage sytem that allows you instant acces to your files", "Cloud Storage", 'static/images/cloud-storage.jpg' ),
    (62, 200, "We offer data processing service to help aleviate the strain on smaller businesses", "Data Processing", 'static/images/Data-process.png' ),
    (63, 35, "We offer a laptop hire service for personal or business uses", "Laptop Hire", 'static/images/laptop-hire.jpg' ),
    (64, 100, "We have an office available to rent out by other companies", "Office Rental Service", 'static/images/office.jpg' ),
    (65, 1000, "We offer a server hosting service where we will host either web servers or data servers", "Server Hosting", 'static/images/server-hosting.png' ),
    (66, 8.99, "We offer a vpn server to protect your data and keep you safe while using a public wifi connection", "VPN Service", 'static/images/vpn.jpg' );

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT,
    password TEXT NOT NULL
);

-- User_id = admin, password = admin1
INSERT INTO users (user_id, password) 
VALUES
    ("admin", "pbkdf2:sha256:260000$0Hp3LK4P9rMbN90L$5f7b596dab296a93ec11983ecb8806d48fea71752df6742c85c6b1612404f31f");
    
DROP TABLE IF EXISTS profile;

CREATE TABLE profile
(
    user_id TEXT,
    nickname TEXT,
    age INTEGER,
    bio TEXT
);


DROP TABLE IF EXISTS employees;

CREATE TABLE employees
(
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    department TEXT NOT NULL,
    job_description TEXT NOT NULL,
    img BLOB
);

INSERT INTO employees (name, age, department, job_description, img)
VALUES
    ("John Nobody", 39, "Finance", "A finance manager in charge of VPN services", 'static/images/employees/John.jpg'),
    ("Dylan Gregs", 44, "IT", "A software engineer in the service department working with VPN services", 'static/images/employees/Dylan.jpg'),
    ("Kyle Jam", 20, "IT", "A product deployment manager", 'static/images/employees/Kyle.jpg'),
    ("Mary", 29, "Management", "The regional supervisor in charge of the Cork work district", 'static/images/employees/Mary.jpg'),
    ("Mx", 45, "R & D", "In charge of R&D since 2012", 'static/images/employees/Max.jpg'),
    ("Paul", 39, "IT", "A software engineer in the service department working on data services", 'static/images/employees/Paul.jpg'),
    ("Peter McSwindler", 18, "Finance", "An accountant in charge of ensuring that we dont have to pay all taxes", 'static/images/employees/Peter.jpg'),
    ("Gregory", 22, "IT", "A software engineer", 'static/images/employees/placeholder.png'),
    ("Jimmy", 44, "Finance", "An accountant", 'static/images/employees/placeholder.png'),
    ("Mark", 21, "IT", "A software engineer", 'static/images/employees/placeholder.png'),
    ("Larry", 54, "R & D", "Product deployment manager", 'static/images/employees/placeholder.png'),
    ("Richard", 32, "IT", "A software engineer", 'static/images/employees/placeholder.png'),
    ("Chad", 19, "Finance", "A finance manager in charge of all services", 'static/images/employees/placeholder.png'),
    ("Timmy", 30, "IT", "A software engineer working with services", 'static/images/employees/placeholder.png'),
    ("Jamal Barada", 26, "R & D", "A software engineer in charge of srvice integration", 'static/images/employees/placeholder.png'),
    ("Franklin", 22, "IT", "A software engineer", 'static/images/employees/placeholder.png'),
    ("Amy", 23, "Finance", "A financial analysts", 'static/images/employees/placeholder.png'),
    ("Jessica", 34, "IT", "A software engineer", 'static/images/employees/placeholder.png'),
    ("Gary Oak", 17, "Finance", "A finance manager in charge of rental services", 'static/images/employees/placeholder.png'),
    ("Liz", 43, "IT", "A software engineer in the service department", 'static/images/employees/placeholder.png');



DROP TABLE IF EXISTS research;

CREATE TABLE research
(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    started TEXT,
    description TEXT NOT NULL
);

INSERT INTO research (project_name, started, description)
VALUES 
     ("Data effectiveness", '2022-12-23', "Attepting to make the processing of data more effective"),
     ("The cost saving project", '2022-12-10', "Research by the finance department into cost saving methods");

DROP TABLE IF EXISTS cart;

CREATE TABLE cart
(
    user_id TEXT ,
    product_id INTEGER ,
    quantity INTEGER NOT NULL,
    name TEXT,
    price REAL,
    image BLOB
);

DROP TABLE IF EXISTS checkout;

CREATE TABLE checkout
(
    user_id TEXT ,
    product_id INTEGER ,
    quantity TEXT NOT NULL,
    name TEXT,
    price REAL,
    item_price,
    image BLOB
);

DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(
    user_id TEXT,
    product_id INTEGER,
    quantity INTEGER,
    name TEXT,
    image BLOB
);

DROP TABLE IF EXISTS wishlist;

CREATE TABLE wishlist
(
    user_id TEXT,
    product_id INTEGER,
    name TEXT,
    image BLOB
);

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews
(   
    user_id TEXT,
    product_id INTEGER,
    review TEXT,
    score INTEGER
);

DROP TABLE IF EXISTS support;

CREATE TABLE support
(   
    user_id TEXT NOT NULL,
    question TEXT
);

DROP TABLE IF EXISTS blog;

CREATE TABLE blog
(   
    user_id TEXT NOT NULL,
    post TEXT
);
