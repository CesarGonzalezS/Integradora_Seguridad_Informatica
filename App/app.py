from flask import Flask, render_template, request, session
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


#Enviar mensaje
def cifrar_cesar(mensaje, desplazamiento):
    resultado = ''
    for char in mensaje:
        if char.isalpha():
            # Determinar si es una letra mayúscula o minúscula
            inicio = ord('A') if char.isupper() else ord('a')
            # Aplicar el cifrado César
            resultado += chr((ord(char) - inicio + desplazamiento) % 26 + inicio)
        else:
            # Mantener caracteres no alfabéticos sin cambios
            resultado += char
    return resultado

#Iniciar HTML 
@app.route('/')
def index():
    return render_template('index.html')


#Funcion de inicar con nombre y que tipo de cifrado
@app.route('/chat', methods=['POST'])
def chat():
    nombre_usuario = request.form['nombre_usuario']
    tipo_cifrado = request.form['tipo_cifrado']
    session['nombre_usuario'] = nombre_usuario
    session['tipo_cifrado'] = tipo_cifrado
    return render_template('chat.html', nombre_usuario=nombre_usuario, tipo_cifrado=tipo_cifrado)

# Enviar mensaje cifrado aplicando el cifrado 
@socketio.on('message')
def handle_message(data):
    nombre_usuario = session.get('nombre_usuario', 'Invitado')
    tipo_cifrado = session.get('tipo_cifrado', 'Sin cifrado')

    # Obtener el desplazamiento desde el tipo de cifrado
    desplazamiento = int(tipo_cifrado) if tipo_cifrado.isdigit() else 0

    # Cifrar el mensaje con el cifrado César
    mensaje_cifrado = cifrar_cesar(data['message'], desplazamiento)

    print(f'Received message from {nombre_usuario}: {data["message"]}')
    print(f'Mensaje cifrado: {mensaje_cifrado}')

    # Emitir el mensaje cifrado
    socketio.emit('message', {'message': f'{nombre_usuario}: {mensaje_cifrado}'})


#Funcion para decifrar el metodo cesar
@socketio.on('descifrar')
def handle_descifrar(data):
    tipo_descifrado = data['tipo_descifrado']

    # Obtener el desplazamiento desde el tipo de descifrado
    desplazamiento = int(tipo_descifrado) if tipo_descifrado.isdigit() else 0

    print(f'Tipo de descifrado: {tipo_descifrado}')
    print(f'Mensaje cifrado a descifrar: {data["message"]}')

    # Descifrar el mensaje con el cifrado César
    mensaje_descifrado = cifrar_cesar(data['message'], -desplazamiento)

    print(f'Descifrado message: {mensaje_descifrado}')

    # Emitir el mensaje descifrado
    socketio.emit('descifrado', {'message': f'Descifrado: {mensaje_descifrado}'})

if __name__ == '__main__':
    #Ejecutar la apliacion en el puerto predeterminado por Socketio
    socketio.run(app)

    
    
    #socketio.run(app, host='192.168.0.16', port=5000)
