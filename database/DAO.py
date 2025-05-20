from database.DB_connect import DBConnect
from model.retailer import Retailer
from model.sales import Sales


class DAO():
    @staticmethod
    def getPaesi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """select distinct Country 
                    from go_retailers gr 
                    group by Country asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()

        return result
    @staticmethod
    def getRetailers():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from go_retailers gr"""

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()

        return result
    @staticmethod
    def getRetailersPaese(paese):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from go_retailers gr 
                    where gr.Country  = %s """

        cursor.execute(query, (paese, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getEdges(r1, r2 ,anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select gr1.Retailer_code as rc1, gr2.Retailer_code as rc2, count(distinct gds2.Product_number) as peso
                    from go_daily_sales gds1, go_daily_sales gds2, (select distinct * 
                    from go_retailers gr 
                    where gr.Country  = %s) gr1, (select distinct * 
                    from go_retailers gr 
                    where gr.Country  = %s) gr2
                    where gds1.Product_number = gds2.Product_number and 
                    gds1.Retailer_code < gds2.Retailer_code and gds2.Retailer_code = gr2.Retailer_code 
                    and gds1.Retailer_code = gr1.Retailer_code and 
                    year(gds2.`Date`) = year(gds1.`Date`) and year(gds2.`Date`) = %s
                    group by gds1.Retailer_code, gds2.Retailer_code  """

        cursor.execute(query, (r1, r2, anno))

        for row in cursor:
            result.append(Sales(**row))

        cursor.close()
        conn.close()

        return result
