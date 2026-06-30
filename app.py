from flask import Flask, render_template, request, redirect
from database import crear_tabla, insertar_productos_ejemplo, obtener_productos, agregar_producto
import os

app = Flask(__name__)

crear_tabla()
insertar_productos_ejemplo()

UPLOAD_FOLDER = "static/imagenes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def inicio():
    categoria = request.args.get("categoria")
    productos = obtener_productos(categoria)
    return render_template("index.html", productos=productos, categoria=categoria)

@app.route("/admin")
def admin():
    productos = obtener_productos()
    return render_template("admin.html", productos=productos)

@app.route("/admin/agregar", methods=["POST"])
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

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    