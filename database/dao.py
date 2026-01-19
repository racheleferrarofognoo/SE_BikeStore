from database.DB_connect import DBConnect
from model.Category import Category
from model.Product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_categories():
        risultato = []
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM category"""
        cursor.execute(query)
        for row in cursor:
            risultato.append(Category(**row))

        cursor.close()
        conn.close()
        return risultato

    @staticmethod
    def get_products_by_categories(category):
        risultato = []
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM product
                    WHERE category_id = %s"""
        cursor.execute(query, (category,))
        for row in cursor:
            risultato.append(Product(**row))

        cursor.close()
        conn.close()
        return risultato

    @staticmethod
    def get_sales_by_product(category, inizio, fine):
        risultato = {}
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ select p.id as product_id, count(distinct oi.order_id) as vendite
                    from product p 
                    left join order_item oi on p.id = oi.product_id 
                    left join `order` o on oi.order_id = o.id 
                        and o.order_date between %s and %s
                    where p.category_id = %s
                    group by p.id"""

        cursor.execute(query, (inizio, fine, category))
        for row in cursor:
            risultato[row["product_id"]] = row["vendite"]
        cursor.close()
        conn.close()
        return risultato
