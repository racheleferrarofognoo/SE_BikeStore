
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
    def get_category():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from category """
        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_prodotti_per_categoria(cat):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from product p
                    where p.category_id = %s """
        cursor.execute(query, (cat,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_connessioni(cat, data_inizio, data_fine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ with productSales as (
                    select p.id, count(distinct oi.order_id) as num_vendite
                    from product p 
                    join order_item oi on p.id = oi.product_id 
                    join `order` o on oi.order_id = o.id 
                    where o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.id
                )
                select p1.id as product1, p2.id as product2, 
                p1.num_vendite as vendite1, p2.num_vendite as vendite2,
                (p1.num_vendite + p2.num_vendite ) as peso
                from productSales p1, productSales p2
                where p1.id < p2.id """
        cursor.execute(query, (data_inizio, data_fine, cat))

        for row in cursor:
            results.append({'product1':row['product1'],
                            'product2':row['product2'] ,
                            'vendite1':row['vendite1'],
                            'vendite2':row['vendite2'],
                            'peso': row['peso']})

        cursor.close()
        conn.close()
        return results
