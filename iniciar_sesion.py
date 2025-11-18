from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "clave_muy_secreta"

# Simulación de base de datos de usuarios
users = {
    "admin@example.com": generate_password_hash("1234")
}

@app.route("/")
def home():
    user = session.get("user")
    return render_template("dashboard.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and check_password_hash(users[email], password):
            session["user"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
