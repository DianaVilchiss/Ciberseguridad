from flask import Flask, render_template, request
from lxml import etree

app = Flask(__name__)

usuarios_sql = [{"usuario":"admin","password":"1234"}]

usuarios_nosql = [
    {"usuario":"admin","password":"1234"},
    {"usuario":"user","password":"123"}
]

@app.route("/")
def index():
    return render_template("index.html")


# SQL Injection
@app.route("/sql", methods=["GET","POST"])
def sql():

    if request.method == "POST":

        user = request.form["usuario"]
        password = request.form["password"]

        query = f"SELECT * FROM usuarios WHERE usuario='{user}' AND password='{password}'"

        print(query)

        if "' OR '1'='1" in query:
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        for u in usuarios_sql:
            if u["usuario"] == user and u["password"] == password:
                return render_template("resultado.html",
                tipo="ok",
                icono="✔",
                titulo="Acceso concedido",
                mensaje="Inicio de sesión correcto.")

        return render_template("resultado.html",
        tipo="error",
        icono="✖",
        titulo="Acceso denegado",
        mensaje="Credenciales incorrectas.")

    return render_template("sql.html")


# NoSQL Injection
@app.route("/nosql", methods=["GET","POST"])
def nosql():

    if request.method == "POST":

        user = request.form["usuario"]
        password = request.form["password"]

        if "$ne" in password:
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        for u in usuarios_nosql:
            if u["usuario"] == user and u["password"] == password:
                return render_template("resultado.html",
                tipo="ok",
                icono="✔",
                titulo="Acceso concedido",
                mensaje="Inicio de sesión correcto.")

        return render_template("resultado.html",
        tipo="error",
        icono="✖",
        titulo="Acceso denegado",
        mensaje="Credenciales incorrectas.")

    return render_template("nosql.html")


# LDAP Injection
@app.route("/ldap", methods=["GET","POST"])
def ldap():

    if request.method == "POST":

        user = request.form["usuario"]
        password = request.form["password"]

        filtro = "(&(uid=" + user + ")(password=" + password + "))"
        print("Filtro LDAP:", filtro)

        if user == "admin" and password == "1234":
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        if "*)(uid=*" in user:
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        return render_template("resultado.html",
        tipo="error",
        icono="✖",
        titulo="Acceso denegado",
        mensaje="Credenciales incorrectas.")

    return render_template("ldap.html")


# XPath Injection
@app.route("/xpath", methods=["GET","POST"])
def xpath():

    if request.method == "POST":

        user = request.form["usuario"]
        password = request.form["password"]

        tree = etree.parse("usuarios.xml")

        query = "//usuario[nombre/text()='" + user + "' and password/text()='" + password + "']"
        resultado = tree.xpath(query)

        print(query)

        if "' or '1'='1" in query:
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        if resultado:
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        return render_template("resultado.html",
        tipo="error",
        icono="✖",
        titulo="Acceso denegado",
        mensaje="Credenciales incorrectas.")

    return render_template("xpath.html")


# GraphQL Injection
@app.route("/graphql", methods=["GET","POST"])
def graphql():

    if request.method == "POST":

        user = request.form["usuario"]
        password = request.form["password"]

        query = f'''
        query {{
            login(username:"{user}", password:"{password}") {{
                id
            }}
        }}
        '''

        print(query)

        if user == "admin" and password == "1234":
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        if "users" in user:
            return render_template("resultado.html",
            tipo="ok",
            icono="✔",
            titulo="Acceso concedido",
            mensaje="Inicio de sesión correcto.")

        return render_template("resultado.html",
        tipo="error",
        icono="✖",
        titulo="Acceso denegado",
        mensaje="Credenciales incorrectas.")

    return render_template("graphql.html")


if __name__ == "__main__":
    app.run(debug=True)