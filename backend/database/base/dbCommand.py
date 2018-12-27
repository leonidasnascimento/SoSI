import mysql.connector
from mysql.connector import Error

class DbCommand:
    def Commit(self, strCommand):
        try:
            conn = mysql.connector.connect(host='127.0.0.1',
                                       database='sys',
                                       user='sosi',
                                       password='sosidb')
            if conn.is_connected():
                cursor = conn.cursor()
                rowsAffected = cursor.execute(strCommand)
                
                conn.commit()
        except Error as e:
            print(e + ' - ' + strCommand)
        finally:
            cursor.close()
            conn.close()
            return True

    def CallProcedure(self, strCommand, args):
        try:
            conn = mysql.connector.connect(host='127.0.0.1',
                                       database='sys',
                                       user='sosi',
                                       password='sosidb')
            
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.callproc(strCommand, args)
                
                return True
            return False
        except Error as e:
            print(e)
            pass
        finally:
            cursor.close()
            conn.close()
            pass    


    def Query(self, strCommand):
        try:
            returnObj = tuple
            conn = mysql.connector.connect(host='127.0.0.1',
                                       database='sys',
                                       user='sosi',
                                       password='sosidb')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(strCommand)
                returnObj = cursor.fetchone()
        except Error as e:
            print(e)
            pass
        finally:
            cursor.close()
            conn.close()

            return returnObj
