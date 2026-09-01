import pandas as pd



df = pd.read_csv(r"C:\Users\ketan\Downloads\blinkit_grocery.csv")
print(df.columns.tolist())

difference_one = df.groupby(["Outlet Type"]).agg(
    outlet_type_sale = ("Sales", "mean")
)

difference_one.reset_index(inplace=True)
difference_one.sort_values(by="outlet_type_sale", ascending=False, inplace=True)
print(difference_one)

difference_two = df.groupby(["Outlet Size"]).agg(
    total_size_sale = ("Sales", "mean")
)

print(difference_two)

difference_three = df.groupby(["Outlet Location Type"]).agg(
    tier_sales = ("Sales", "mean")
)

print(difference_three)

difference_four = df.groupby(["Item Type"]).agg(
    total_type = ("Sales", "mean")
)
print(difference_four)

difference_five = df["Item Visibility"].corr(df["Sales"])
print(difference_five)
    


filtered_results = df[df["Outlet Type"] == "Supermarket Type1"].groupby(["Item Type"]).agg(
    total_type = ("Sales", "mean")
)
print(filtered_results)

df["Item Fat Content"] = df["Item Fat Content"].replace(
    {"low fat" : "Low Fat",  "LF" : "Low Fat", "reg" : "Regular"}
)
print(df["Item Fat Content"])

filter_results = df.groupby("Item Fat Content").agg(
    avg_sales = ("Sales", "mean")
)

print(filter_results)

import sqlite3
import os

db_path = r"C:\Users\ketan\Downloads\blinkit.db"
if os.path.exists(db_path):
    print(db_path)

if not os.path.exists(db_path):
    print("Error")

else:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales LIMIT 10")
    results = cursor.fetchall()
    connection.close()
    print(results)


connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""SELECT "Item Type",AVG(Sales) AS avg_sales, SUM(Sales) AS total_sales FROM sales GROUP BY "Item Type" ORDER BY AVG(Sales) DESC LIMIT 5""")
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""SELECT COUNT (*) AS count_rows FROM sales WHERE "Item Weight" IS NULL""")
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""SELECT "Item Fat Content" AS Original, CASE WHEN "Item Fat Content" = 'reg' THEN 'Regular' WHEN "Item Fat Content" = 'low fat' THEN 'Low Fat' WHEN "Item Fat Content" = 'LF' THEN 'Low Fat' ELSE "Item Fat Content" END AS New FROM sales """)
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""SELECT "Item Type", AVG(Sales) AS avg_sales FROM sales WHERE "Outlet Type" = 'Supermarket Type1' GROUP BY "Item Type" ORDER BY avg_sales DESC LIMIT 3""")
results = cursor.fetchall()
connection.close()
print(results)

DB_path = r"C:\Users\ketan\Downloads\blinkitt.db"
connection = sqlite3.connect(DB_path)
cursor = connection.cursor()
cursor.execute("""SELECT sales."Outlet Identifier", sales."Sales", outlet_managers."Region" FROM outlet_managers INNER JOIN sales ON outlet_managers."Outlet Identifier" = sales."Outlet Identifier" """)
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(DB_path)
cursor = connection.cursor()
cursor.execute("""SELECT SUM(sales."Sales") AS total_sales, outlet_managers."Region" FROM outlet_managers INNER JOIN sales ON outlet_managers."Outlet Identifier" = sales."Outlet Identifier" GROUP BY outlet_managers."Region" """)
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(DB_path)
cursor = connection.cursor()
cursor.execute("""SELECT outlet_managers."Manager Name", AVG(sales."Sales") AS avg_sales, sales."Outlet Identifier" FROM outlet_managers INNER JOIN sales ON outlet_managers."Outlet Identifier" = sales."Outlet Identifier" GROUP BY outlet_managers."Manager Name", sales."Outlet Identifier" ORDER BY avg_sales DESC LIMIT 1 """)
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""SELECT "Outlet Identifier", "Sales", RANK() OVER (PARTITION BY "Outlet Identifier" ORDER BY "Sales") FROM sales LIMIT 5""")
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""SELECT DISTINCT * FROM (SELECT "Item Type", "Sales", DENSE_RANK() OVER (PARTITION BY "Item Type" ORDER BY "Sales" DESC) AS sales_rank FROM sales) ranked WHERE sales_rank = 1 """)
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""WITH ranked AS (SELECT "Sales", "Outlet Identifier", RANK() OVER (PARTITION BY "Outlet Identifier" ORDER BY "Sales" DESC) AS Sales_rank FROM sales) SELECT * FROM ranked WHERE Sales_rank = 1   """)
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute(""" WITH regional_sales AS (SELECT SUM(Sales) AS total_sales, "Item Type", "Outlet Location Type" FROM sales GROUP BY "Outlet Location Type", "Item Type"), ranked AS(SELECT *, RANK() OVER (PARTITION BY "Outlet Location Type" ORDER BY total_sales DESC) AS sales_rank FROM regional_sales) SELECT * FROM ranked WHERE sales_rank = 1""")
results = cursor.fetchall()
connection.close()
print(results)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute(""" WITH cleaned AS (SELECT "Outlet Location Type", "Item Fat Content" AS Original, CASE WHEN "Item Fat Content" = 'reg' THEN 'Regular' WHEN "Item Fat Content" = 'low fat' THEN 'Low Fat' WHEN "Item Fat Content" = 'LF' THEN 'Low Fat' ELSE "Item Fat Content" END AS "Item Fat Content", "Sales" FROM sales), Outlet_Sales AS (SELECT AVG(Sales) AS avg_sales, "Outlet Location Type", "Item Fat Content" FROM cleaned GROUP BY "Outlet Location Type", "Item Fat Content"), ranked AS (SELECT *, RANK() OVER (PARTITION BY "Item Fat Content" ORDER BY avg_sales DESC) AS sales_rank FROM Outlet_Sales) SELECT  * FROM ranked WHERE sales_rank = 1 """)
results = cursor.fetchall()
connection.close()
print(results)
