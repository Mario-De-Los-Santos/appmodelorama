import mysql.connector

def conecta():
    conn = mysql.connector.connect(
        host="localhost", 
        port="3310", 
        user="root", 
        password="mario19", 
        database="modelorama"
    )
    return conn  
