CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);

CREATE TABLE Order_Items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);


WITH Customer_Category_Spending AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.email,
        p.category,
        SUM(oi.quantity * oi.price_per_unit) AS total_spent,
        ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY SUM(oi.quantity * oi.price_per_unit) DESC) AS rn
    FROM
        Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN Order_Items oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY
        c.customer_id, c.customer_name, c.email, p.category
)
SELECT
    customer_id,
    customer_name,
    email,
    total_spent,
    category as most_purchased_category
FROM
    Customer_Category_Spending
WHERE
    rn = 1
Order BY total_spent DESC
 limit 5;
