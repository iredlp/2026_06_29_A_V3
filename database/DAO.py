from database.DB_connect import DBConnect
from model.costumer import Customer


class DAO():
    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country 
                from customer c 
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(paese):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                   select distinct c.*
                    from customer c, invoice i 
                    where c.Country =%s
                    and c.CustomerId =i.CustomerId 
                    order by c.FirstName 
                                       """

        cursor.execute(query, (paese,))

        for row in cursor:
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getTotPerCliente(customerId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT COALESCE(SUM(i.Total), 0) AS fatturato
                    FROM invoice i
                    WHERE i.CustomerId = %s       """

        cursor.execute(query, (customerId,))

        for row in cursor:
            results.append(row["fatturato"])

        cursor.close()
        conn.close()
        return float(results[0])

    @staticmethod
    def getArtistiPerCliente(customerId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
           SELECT DISTINCT a.ArtistId
            FROM invoice i, invoiceline il, track t, album al, artist a
            WHERE i.InvoiceId = il.InvoiceId
            AND il.TrackId = t.TrackId
            AND t.AlbumId = al.AlbumId
            AND al.ArtistId = a.ArtistId
            AND i.CustomerId = %s
                    """

        cursor.execute(query, (customerId,))

        risultati = set()
        for row in cursor:
            risultati.add(row["ArtistId"])

        cursor.close()
        conn.close()

        return risultati