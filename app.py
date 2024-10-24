from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Conexión a la base de datos
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'  
    'SERVER=localhost;'                  
    'DATABASE=desarrollowebFP;'              
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Ruta para listar clientes
@app.route('/clientes')
def listar_clientes():
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=clientes)

# Ruta para crear un cliente (formulario)
@app.route('/crear_cliente')
def crear_cliente():
    return render_template('crear_cliente.html')

# Ruta para agregar un cliente (método POST)
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    tipo_cliente = request.form['tipo_cliente']
    
    cursor.execute("INSERT INTO Clientes (nombre, direccion, telefono, tipo_cliente) VALUES (?, ?, ?, ?)", 
                   (nombre, direccion, telefono, tipo_cliente))
    conn.commit()
    
    return redirect(url_for('listar_clientes'))

# Cerrar la conexión al finalizar
@app.teardown_appcontext
def close_connection(exception):
    if 'conn' in locals():
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
