from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database import crear_tabla, insertar_productos_ejemplo, obtener_productos, agregar_producto, eliminar_producto, obtener_producto, editar_producto
import os

app = Flask(__name__)
app.secret_key = "muebleria_ja_clave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

USUARIO = "admin"
CONTRASENA = "muebleria123"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

crear_tabla()
insertar_productos_ejemplo()

UPLOAD_FOLDER = "static/imagenes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def inicio():
    categoria = request.args.get("categoria")
    productos = obtener_productos(categoria)
    return render_template("index.html", productos=productos, categoria=categoria)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        if usuario == USUARIO and contrasena == CONTRASENA:
            login_user(User(usuario))
            return redirect("/admin")
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/admin")
@login_required
def admin():
    productos = obtener_productos()
    return render_template("admin.html", productos=productos)

@app.route("/admin/agregar", methods=["POST"])
@login_required
def admin_agregar():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]
    descripcion = request.form["descripcion"]
    medidas = request.form["medidas"]
    imagen = request.files["imagen"]

    nombre_archivo = imagen.filename
    ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
    imagen.save(ruta)

    agregar_producto(nombre, precio, categoria, nombre_archivo, descripcion, medidas)
    return redirect("/admin")

@app.route("/admin/eliminar/<int:id>")
@login_required
def admin_eliminar(id):
    eliminar_producto(id)
    return redirect("/admin")

@app.route("/admin/editar/<int:id>", methods=["GET", "POST"])
@login_required
def admin_editar(id):
    producto = obtener_producto(id)
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        categoria = request.form["categoria"]
        descripcion = request.form["descripcion"]
        medidas = request.form["medidas"]
        editar_producto(id, nombre, precio, categoria, descripcion, medidas)
        return redirect("/admin")
    return render_template("editar.html", producto=producto)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))