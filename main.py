# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1: Return first and last names and job titles for all employees in Boston
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName, e.jobTitle
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2: Find offices that have zero employees
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    GROUP BY o.officeCode
    HAVING COUNT(e.employeeNumber) = 0
""", conn)

# STEP 3: Return employees' first/last name, city/state of office, ordered by first and last name
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4: Return customers who have NOT placed orders - contact info and sales rep employee number
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5: Report of customer contacts with payment info, sorted by amount descending
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6: Identify employees whose customers have average credit limit over 90k
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numCustomers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numCustomers DESC
""", conn)

# STEP 7: Product name and count of orders (numorders) and total units (totalunits)
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(DISTINCT o.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY totalunits DESC
""", conn)

# STEP 8: Product name, code, and total number of customers (numpurchasers)
df_total_customers = pd.read_sql("""
    SELECT DISTINCT p.productName, p.productCode, COUNT(DISTINCT c.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    JOIN customers c ON o.customerNumber = c.customerNumber
    GROUP BY p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9: Count of customers per office
df_customers = pd.read_sql("""
    SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode
""", conn)

# STEP 10: Employee info for those who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    JOIN products p ON od.productCode = p.productCode
    WHERE p.productCode IN (
        SELECT p2.productCode
        FROM products p2
        JOIN orderdetails od2 ON p2.productCode = od2.productCode
        JOIN orders o2 ON od2.orderNumber = o2.orderNumber
        GROUP BY p2.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    )
""", conn)

# Close the connection
conn.close()

conn.close()