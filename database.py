import sqlite3

def conectar():
    return sqlite3.connect("productos.db")

def crear_tabla():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            imagen TEXT NOT NULL,
            descripcion TEXT,
            medidas TEXT
        )
    """)
    con.commit()
    con.close()

def insertar_productos_ejemplo():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        productos = [
            ("Sillón moderno", 85000, "Living", "sillon.jpg", "Sillón tapizado en tela premium con estructura de madera maciza.", "Alto: 90cm | Ancho: 80cm | Prof: 75cm"),
            ("Mesa de comedor", 120000, "Comedor", "mesa.jpg", "Mesa de comedor en madera de roble con terminación al agua.", "Alto: 75cm | Ancho: 160cm | Prof: 90cm"),
            ("Cama matrimonial", 95000, "Dormitorio", "cama.jpg", "Cama con cabecero tapizado y patas de madera natural.", "Alto: 110cm | Ancho: 160cm | Prof: 200cm"),
            ("Biblioteca", 60000, "Estudio", "biblioteca.jpg", "Biblioteca de 5 estantes en melamina blanca con zócalo.", "Alto: 180cm | Ancho: 90cm | Prof: 30cm"),
            ("Silla de escritorio", 45000, "Estudio", "silla.jpg", "Silla ergonómica con altura regulable y ruedas deslizantes.", "Alto: 90-110cm | Ancho: 60cm | Prof: 60cm"),
            ("Sofá 3 cuerpos", 150000, "Living", "sofa.jpg", "Sofá de 3 cuerpos tapizado en cuero ecológico color gris.", "Alto: 85cm | Ancho: 210cm | Prof: 90cm"),
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, categoria, imagen, descripcion, medidas) VALUES (?, ?, ?, ?, ?, ?)",
            productos
        )
        con.commit()
    con.close()

def obtener_productos(categoria=None):
    con = conectar()
    cursor = con.cursor()
    if categoria:
        cursor.execute("SELECT * FROM productos WHERE categoria = ?", (categoria,))
    else:
        cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    con.close()
    return productos
def agregar_producto(nombre, precio, categoria, imagen, descripcion, medidas):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, categoria, imagen, descripcion, medidas) VALUES (?, ?, ?, ?, ?, ?)",
        (nombre, precio, categoria, imagen, descripcion, medidas)
    )
    con.commit()
    con.close()
if __name__ == "__main__":
    crear_tabla()
    insertar_productos_ejemplo()
    print("Base de datos lista!")