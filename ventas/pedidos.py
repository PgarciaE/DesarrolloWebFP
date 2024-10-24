# ventas/pedidos.py
import pyodbc

def crear_pedido(cliente_id, detalles):
    # Conectar a la base de datos
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'  
        'SERVER=localhost;'                  
        'DATABASE=desarrollowebFP;'              
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    # Insertar el nuevo pedido en la tabla de pedidos
    cursor.execute("INSERT INTO Pedidos (cliente_id, detalles) VALUES (?, ?)", 
                   (cliente_id, detalles))
    conn.commit()

    cursor.close()
    conn.close()
