from flask import Flask, render_template, request
from database import crear_tabla, insertar_productos_ejemplo, obtener_productos

app = Flask(__name__)

crear_tabla()
insertar_productos_ejemplo()

@app.route("/")
def inicio():
    categoria = request.args.get("categoria")
    productos = obtener_productos(categoria)
    return render_template("index.html", productos=productos, categoria=categoria)


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))