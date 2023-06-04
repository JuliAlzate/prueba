from flask import Flask, render_template, request, redirect
import mysql.connector
import re
from flask import Flask, request, jsonify


app = Flask(__name__)

# Conexión a la base de datos
db = mysql.connector.connect(

    user="root",
    password="salo0220",
    database="tiendaonline"
)
def validar_correo(correo):
    # Expresión regular para validar el correo electrónico
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Comprobar si el correo coincide con el patrón
    if re.match(patron, correo):
        return True
    else:
        return False

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        
        if len(nombre) < 3:
            return "El nombre debe tener al menos 3 caracteres."
        if not validar_correo(correo):
            return "Correo electrónico inválido."
        if len(contrasena) < 8:
            return "La contraseña debe tener al menos 8 caracteres."

     
        cursor = db.cursor()
        query = "INSERT INTO usuarios (nombre, correo_electronico, contrasena) VALUES (%s, %s, %s)"
        values = (nombre, correo, contrasena)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return "Registro exitoso. ¡Bienvenido/a!"
    
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    cursor = db.cursor()
    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()

    return jsonify({'usuarios': usuarios})

@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    cursor = db.cursor()
    query = "SELECT * FROM usuarios WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    usuario = cursor.fetchone()
    cursor.close()

    if usuario is None:
        return jsonify({'mensaje': 'Usuario no encontrado'})

    return jsonify({'usuario': usuario})

@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    nombre = data['nombre']
    correo = data['correo']
    contrasena = data['contrasena']

    cursor = db.cursor()
    query = "UPDATE usuarios SET nombre = %s, correo_electronico = %s, contrasena = %s WHERE id = %s"
    values = (nombre, correo, contrasena, id)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Usuario actualizado correctamente'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    cursor = db.cursor()
    query = "DELETE FROM usuarios WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Usuario eliminado correctamente'})
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    precio = data['precio']

    cursor = db.cursor()
    query = "INSERT INTO productos (nombre, descripcion, precio) VALUES (%s, %s, %s)"
    values = (nombre, descripcion, precio)
    cursor.execute(query, values)
    db.commit()

    cursor.close()

    return jsonify({'mensaje': 'Producto creado correctamente'})

@app.route('/productos')  
def productos():
    cursor = db.cursor()
    query = "SELECT * FROM productos"
    cursor.execute(query)
    productos = cursor.fetchall()
    cursor.close()
    return productos

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    cursor = db.cursor()
    query = "SELECT * FROM productos WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    producto = cursor.fetchone()
    cursor.close()

    if producto is None:
        return jsonify({'mensaje': 'Producto no encontrado'})

    return jsonify({'producto': producto})
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    precio = data['precio']

    cursor = db.cursor()
    query = "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s"
    values = (nombre, descripcion, precio, id)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Producto actualizado correctamente'})

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    cursor = db.cursor()
    query = "DELETE FROM productos WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Producto eliminado correctamente'})

@app.route('/pedidos', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    usuario_id = data['usuario_id']
    producto_id = data['producto_id']
    fecha = data['fecha']
    cantidad = data['cantidad']

    cursor = db.cursor()

    # Verificar si el usuario existe
    query = "SELECT * FROM usuarios WHERE id = %s"
    values = (usuario_id,)
    cursor.execute(query, values)
    usuario = cursor.fetchone()

    if usuario is None:
        return jsonify({'mensaje': 'Usuario no encontrado'})

    # Verificar si el producto existe
    query = "SELECT * FROM productos WHERE id = %s"
    values = (producto_id,)
    cursor.execute(query, values)
    producto = cursor.fetchone()

    if producto is None:
        return jsonify({'mensaje': 'Producto no encontrado'})

    # Insertar el nuevo pedido
    query = "INSERT INTO pedidos (usuario_id, producto_id, fecha, cantidad) VALUES (%s, %s, %s, %s)"
    values = (usuario_id, producto_id, fecha, cantidad)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Pedido creado correctamente'})


@app.route('/pedidos', methods=['GET'])
def obtener_pedidos():
    cursor = db.cursor()
    query = "SELECT * FROM pedidos"
    cursor.execute(query)
    pedidos = cursor.fetchall()
    cursor.close()

    return jsonify({'pedidos': pedidos})


@app.route('/pedidos/usuario/<int:usuario_id>', methods=['GET'])
def obtener_pedidos_por_usuario(usuario_id):
    cursor = db.cursor()
    query = "SELECT * FROM pedidos WHERE usuario_id = %s"
    values = (usuario_id,)
    cursor.execute(query, values)
    pedidos = cursor.fetchall()
    cursor.close()

    return jsonify({'pedidos': pedidos})


@app.route('/pedidos/<int:id>', methods=['GET'])
def obtener_pedido(id):
    cursor = db.cursor()
    query = "SELECT * FROM pedidos WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    pedido = cursor.fetchone()
    cursor.close()

    if pedido is None:
        return jsonify({'mensaje': 'Pedido no encontrado'})

    return jsonify({'pedido': pedido})


@app.route('/pedidos/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    data = request.get_json()
    usuario_id = data['usuario_id']
    producto_id = data['producto_id']
    fecha = data['fecha']
    cantidad = data['cantidad']

    cursor = db.cursor()
    query = "UPDATE pedidos SET usuario_id = %s, producto_id = %s, fecha = %s, cantidad = %s WHERE id = %s"
    values = (usuario_id, producto_id, fecha, cantidad, id)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Pedido actualizado correctamente'})


@app.route('/pedidos/<int:id>', methods=['DELETE'])
def eliminar_pedido(id):
    cursor = db.cursor()
    query = "DELETE FROM pedidos WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'mensaje': 'Pedido eliminado correctamente'})

@app.route('/pedidos/usuario/<int:usuario_id>', methods=['GET'])
def obtener_pedidos_por_user(usuario_id):
    cursor = db.cursor()

    # Verificar si el usuario existe
    query = "SELECT * FROM usuarios WHERE id = %s"
    values = (usuario_id,)
    cursor.execute(query, values)
    usuario = cursor.fetchone()

    if usuario is None:
        return jsonify({'mensaje': 'Usuario no encontrado'})

    # Obtener los pedidos del usuario con datos relacionados
    query = """
    SELECT p.id, u.nombre, pr.nombre, pr.descripcion, pr.precio, p.fecha, p.cantidad
    FROM pedidos p
    INNER JOIN usuarios u ON p.usuario_id = u.id
    INNER JOIN productos pr ON p.producto_id = pr.id
    WHERE p.usuario_id = %s
    """
    values = (usuario_id,)
    cursor.execute(query, values)
    pedidos = []
    for pedido in cursor.fetchall():
        pedido_data = {
            'id': pedido[0],
            'nombre_usuario': pedido[1],
            'nombre_producto': pedido[2],
            'descripcion': pedido[3],
            'precio': pedido[4],
            'fecha': pedido[5],
            'cantidad': pedido[6]
        }
        pedidos.append(pedido_data)

    cursor.close()

    return jsonify({'pedidos': pedidos})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo_electronico = data['correo_electronico']
    contrasena = data['contrasena']

    cursor = db.cursor()

    # Verificar las credenciales del usuario
    query = "SELECT * FROM usuarios WHERE correo_electronico = %s AND contrasena = %s"
    values = (correo_electronico, contrasena)
    cursor.execute(query, values)
    usuario = cursor.fetchone()

    cursor.close()

    if usuario is None:
        return jsonify({'mensaje': 'Credenciales inválidas'})

    return jsonify({'mensaje': 'Bienvenido'})

if __name__ == '__main__':
    app.run(debug=True,port=4000)