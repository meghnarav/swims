-- SUPPLIERS
INSERT INTO Supplier (supplier_id, supplier_name, contact_email, phone_number) VALUES
(1,'Arctic Foods','contact@arcticfoods.com','9876543210'),
(2,'Fresh Dairy Co','info@freshdairy.com','9812345670'),
(3,'Polar Treats','sales@polartreats.com','9123456789'),
(4,'Cool Cream Ltd','support@coolcream.com','9988776655'),
(5,'Frozen Valley','contact@frozenvalley.com','9090909090'),
(6,'North Star Supplies','hello@northstar.com','9000011111'),
(7,'Glacier Goods','team@glaciergoods.com','9000022222'),
(8,'Aurora Dairy','service@auroradairy.com','9000033333'),
(9,'Snowflake Distributors','info@snowflake.com','9000044444'),
(10,'Evercold Logistics','support@evercold.com','9000055555');

-- WAREHOUSES
INSERT INTO Warehouse (warehouse_id, location, capacity) VALUES
(1,'Chennai',10000),
(2,'Bangalore',8000),
(3,'Hyderabad',7500),
(4,'Mumbai',12000),
(5,'Delhi',9000),
(6,'Pune',6500),
(7,'Kolkata',7000),
(8,'Ahmedabad',6000);

-- EMPLOYEES
INSERT INTO Employee (employee_id, name, role) VALUES
(1,'Rahul Sharma','Manager'),
(2,'Priya Iyer','Supervisor'),
(3,'Amit Verma','Operator'),
(4,'Sneha Kapoor','Operator'),
(5,'Karan Mehta','Warehouse Staff'),
(6,'Anita Rao','Manager'),
(7,'Vikram Singh','Operator'),
(8,'Meera Joshi','Warehouse Staff'),
(9,'Rohit Nair','Supervisor'),
(10,'Divya Kulkarni','Operator');

-- PERMANENT EMP
INSERT INTO Permanent_Employee (employee_id, monthly_salary, benefits) VALUES
(1,60000,'Health Insurance'),
(2,50000,'Health Insurance'),
(6,65000,'Health + Bonus'),
(9,52000,'Health Insurance');

-- CONTRACT EMP
INSERT INTO Contract_Employee (employee_id, hourly_rate, contract_end_date) VALUES
(3,400,'2026-12-31'),
(4,350,'2026-10-31'),
(5,300,'2026-09-30'),
(7,320,'2026-11-30'),
(8,310,'2026-08-31'),
(10,330,'2027-01-31');

-- PRODUCTS
INSERT INTO Product (product_id, product_name, supplier_id, category, unit_price) VALUES
(1,'Vanilla Ice Cream',1,'Ice Cream',120),
(2,'Chocolate Ice Cream',2,'Ice Cream',130),
(3,'Strawberry Ice Cream',3,'Ice Cream',125),
(4,'Mango Sorbet',4,'Sorbet',110),
(5,'Blueberry Gelato',5,'Gelato',150),
(6,'Butterscotch Cone',1,'Ice Cream',140),
(7,'Pistachio Kulfi',2,'Traditional',160),
(8,'Cookie Crumble Sundae',3,'Ice Cream',170),
(9,'Mint Choco Chip',4,'Ice Cream',135),
(10,'Coffee Gelato',5,'Gelato',155),
(11,'Salted Caramel Cup',6,'Ice Cream',145),
(12,'Lemon Sorbet',7,'Sorbet',115),
(13,'Berry Blast Stick',8,'Ice Cream',125),
(14,'Almond Crunch Bar',9,'Ice Cream',150),
(15,'Sugar-free Vanilla',10,'Diet',130);

-- INVENTORY
INSERT INTO Inventory (product_id, warehouse_id, quantity) VALUES
(1,1,500),
(1,2,300),
(2,1,400),
(3,3,250),
(4,4,350),
(5,5,200),
(2,2,220),
(2,4,180),
(3,1,150),
(3,5,120),
(4,2,260),
(4,5,140),
(5,1,90),
(5,3,80),
(6,1,200),
(6,2,150),
(6,6,100),
(7,3,130),
(7,4,120),
(8,4,160),
(8,5,140),
(9,2,110),
(9,7,90),
(10,5,130),
(10,6,120),
(11,1,95),
(11,8,70),
(12,4,85),
(12,7,65),
(13,3,140),
(13,6,120),
(14,2,75),
(14,5,95),
(15,1,60),
(15,8,55);

-- STOCK TRANSACTIONS
INSERT INTO Stock_Transaction
(transaction_id, transaction_date, transaction_type, product_id, quantity, warehouse_id, employee_id)
VALUES
(1,'2026-01-10','INWARD',1,200,1,3),
(2,'2026-01-12','OUTWARD',2,50,1,4),
(3,'2026-01-15','INWARD',3,150,3,3),
(4,'2026-01-20','OUTWARD',1,70,2,5),
(5,'2026-01-25','INWARD',4,120,4,4),
(6,'2026-02-01','INWARD',2,180,2,7),
(7,'2026-02-03','OUTWARD',3,40,3,8),
(8,'2026-02-05','INWARD',5,90,5,10),
(9,'2026-02-07','OUTWARD',4,60,4,3),
(10,'2026-02-10','INWARD',6,150,1,6),
(11,'2026-02-12','OUTWARD',6,30,2,7),
(12,'2026-02-14','INWARD',7,130,3,8),
(13,'2026-02-16','OUTWARD',7,25,4,4),
(14,'2026-02-18','INWARD',8,160,4,9),
(15,'2026-02-20','OUTWARD',8,35,5,2),
(16,'2026-02-22','INWARD',9,110,2,1),
(17,'2026-02-24','OUTWARD',9,20,7,5),
(18,'2026-02-26','INWARD',10,130,5,6),
(19,'2026-02-28','OUTWARD',10,25,6,10),
(20,'2026-03-02','INWARD',11,95,1,9),
(21,'2026-03-03','OUTWARD',11,15,8,3),
(22,'2026-03-05','INWARD',12,85,4,4),
(23,'2026-03-06','OUTWARD',12,20,7,8),
(24,'2026-03-08','INWARD',13,140,3,2),
(25,'2026-03-09','OUTWARD',13,30,6,7),
(26,'2026-03-11','INWARD',14,95,2,1),
(27,'2026-03-12','OUTWARD',14,25,5,5),
(28,'2026-03-14','INWARD',15,60,1,6),
(29,'2026-03-15','OUTWARD',15,10,8,10),
(30,'2026-03-16','OUTWARD',2,35,4,4);