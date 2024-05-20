import mysql.connector
from decouple import config
import pytz
from datetime import datetime
class MyDbEnty:
    
    
    def get_hora():      
        colombia_timezone = pytz.timezone("America/Bogota")
        hora_colombia = datetime.now(colombia_timezone)
        return hora_colombia  
    @staticmethod
    def conectar_con_bd():
        try:
            conectar = mysql.connector.connect(
                host=config('MYSQL_HOST'),
                user=config('MYSQL_USER'),
                password=config('MYSQL_PASSWORD'),
                database=config('MYSQL_DATABASE'),
                collation='utf8mb4_general_ci'
            )
            print('**********************************************************************')
            print('  Conexión Exitosa a: ', config('MYSQL_DATABASE'),MyDbEnty.get_hora())
            print('**********************************************************************')
            return conectar
        except mysql.connector.Error as ex:
            print('Error: ', ex)
 
    def kill_conexion(self, connection):
        try:
            
            if  connection:
                connection.close()
                print('**********************************************************************')
                print('  Conexión Finalizada: ', config('MYSQL_DATABASE'),MyDbEnty.get_hora())
                print('**********************************************************************')
            else:
                print('Connection is closed')    
                
        except Exception as e:
            print ('Error: ' , e)  
            
            
         