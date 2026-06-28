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
            imagen TEXT NOT NULL
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
            ("Sillón moderno", 85000, "Living", "sillon.jpg"),
            ("Mesa de comedor", 120000, "Comedor", "mesa.jpg"),
            ("Cama matrimonial", 95000, "Dormitorio", "cama.jpg"),
            ("Biblioteca", 60000, "Estudio", "biblioteca.jpg"),
            ("Silla de escritorio", 45000, "Estudio", "silla.jpg"),
            ("Sofá 3 cuerpos", 150000, "Living", "sofa.jpg"),
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, categoria, imagen) VALUES (?, ?, ?, ?)",
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

if __name__ == "__main__":
    crear_tabla()
    insertar_productos_ejemplo()
    print("Base de datos lista!")