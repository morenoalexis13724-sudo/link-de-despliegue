from flask import Flask, request, render_template, redirect, jsonify
import pymysql
import os

sample_app = Flask(__name__)


def conectar():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "servidor-bd"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "adso_db"),
        cursorclass=pymysql.cursors.DictCursor
    )


@sample_app.after_request
def agregar_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@sample_app.route("/")
def home():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM aprendices")
    aprendices = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", aprendices=aprendices)


@sample_app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre_completo"]
    documento = request.form["numero_documento"]
    ficha = request.form["ficha"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO aprendices
        (nombre_completo, numero_documento, ficha)
        VALUES (%s, %s, %s)
        """,
        (nombre, documento, ficha)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@sample_app.route("/estado")
def estado():
    try:
        conn = conectar()
        conn.close()
        return "Conexión exitosa a la base de datos"
    except Exception as e:
        return f"Error de conexión a la base de datos: {e}", 500


@sample_app.route("/api/aprendices", methods=["GET"])
def obtener_aprendices():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aprendices")
    aprendices = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(aprendices)


@sample_app.route("/api/aprendices", methods=["POST"])
def crear_aprendiz():
    datos = request.get_json()

    nombre = datos["nombre_completo"]
    documento = datos["numero_documento"]
    ficha = datos["ficha"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO aprendices
        (nombre_completo, numero_documento, ficha)
        VALUES (%s, %s, %s)
        """,
        (nombre, documento, ficha)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Aprendiz registrado correctamente"
    }), 201


if __name__ == "__main__":
    sample_app.run(
        host="0.0.0.0",
        port=5050,
        debug=True
    )