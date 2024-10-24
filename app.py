from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar flash

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'  
            'SERVER=localhost;'                  
            'DATABASE=desarrollowebFP;'              
            'Trusted_Connection=yes;'
        )
    except pyodbc.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

# Ruta para listar clientes
@app.route('/')
@app.route('/clientes')
def listar_clientes():
    conn = get_db_connection()
    if conn is None:
        flash("Error de conexión a la base de datos", "error")
        return render_template('clientes.html', clientes=[])
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

# Ruta para crear un cliente (formulario)
@app.route('/crear_cliente')
def crear_cliente():
    return render_template('crear_cliente.html')

# Ruta para agregar un cliente (método POST)
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    conn = get_db_connection()
    if conn is None:
        flash("Error de conexión a la base de datos", "error")
        return redirect(url_for('crear_cliente'))
    
    try:
        cursor = conn.cursor()
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        tipo_cliente = request.form['tipo_cliente']
        
        cursor.execute("INSERT INTO Clientes (nombre, direccion, telefono, tipo_cliente) VALUES (?, ?, ?, ?)", 
                       (nombre, direccion, telefono, tipo_cliente))
        conn.commit()
        flash("Cliente agregado exitosamente", "success")
    except pyodbc.Error as e:
        conn.rollback()
        flash(f"Error al agregar cliente: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('listar_clientes'))

# Función para crear un pedido en la base de datos
def crear_pedido(cliente_id, detalles):
    conn = get_db_connection()
    if conn is None:
        flash("Error de conexión a la base de datos", "error")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Pedidos (cliente_id, detalles) VALUES (?, ?)", 
                       (cliente_id, detalles))
        conn.commit()
        flash("Pedido creado exitosamente", "success")
    except pyodbc.Error as e:
        conn.rollback()
        flash(f"Error al crear pedido: {e}", "error")
    finally:
        cursor.close()
        conn.close()

# Ruta para listar pedidos y crear uno nuevo
@app.route('/pedidos', methods=['GET', 'POST'])
def listar_pedidos():
    conn = get_db_connection()
    if conn is None:
        flash("Error de conexión a la base de datos", "error")
        return render_template('pedidos.html', pedidos=[], clientes=[])

    cursor = conn.cursor()

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        detalles = request.form['detalles']
        crear_pedido(cliente_id, detalles)  # Llamar a la función para crear el pedido
        return redirect(url_for('listar_pedidos'))

    cursor.execute("SELECT * FROM Pedidos")  # Cambia esto según tu tabla de pedidos
    pedidos = cursor.fetchall()

    cursor.execute("SELECT * FROM Clientes")  # Obtener la lista de clientes
    clientes = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('pedidos.html', pedidos=pedidos, clientes=clientes)

# Ruta para agregar un pedido (método POST)
@app.route('/agregar_pedido', methods=['POST'])
def agregar_pedido():
    cliente_id = request.form['cliente_id']
    detalles = request.form['detalles']
    crear_pedido(cliente_id, detalles)  # Llamar a la función para crear el pedido
    return redirect(url_for('listar_pedidos'))


# Ruta para listar productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    conn = get_db_connection()
    if conn is None:
        flash("Error de conexión a la base de datos", "error")
        return render_template('productos.html', productos=[])
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos)

# Ruta para crear un producto (formulario)
@app.route('/crear_producto')
def crear_producto():
    return render_template('crear_producto.html')

# Ruta para agregar un producto (método POST)
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    conn = get_db_connection()
    if conn is None:
        flash("Error de conexión a la base de datos", "error")
        return redirect(url_for('crear_producto'))
    
    try:
        cursor = conn.cursor()
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        
        cursor.execute("INSERT INTO Productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)", 
                       (nombre, descripcion, precio, stock))
        conn.commit()
        flash("Producto agregado exitosamente", "success")
    except pyodbc.Error as e:
        conn.rollback()
        flash(f"Error al agregar producto: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('listar_productos'))


if __name__ == '__main__':
    app.run(debug=True)
