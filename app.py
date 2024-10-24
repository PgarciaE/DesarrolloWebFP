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

if __name__ == '__main__':
    app.run(debug=True)
