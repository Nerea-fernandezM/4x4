from flask import Flask, render_template
import generate_connection

app = Flask(__name__)

@app.route("/")
def index():
    # Llamar a tu función que genera los grupos de palabras
    choices = generate_connection.generate()

    # Adaptar el diccionario al formato que espera el frontend
    all_groups = []
    for name, words in choices.items():
        all_groups.append({
            "name": name,
            "words": words
        })

    # Renderizar la plantilla y pasar los datos
    return render_template("index.html", allGroups=all_groups)

if __name__ == "__main__":
    app.run(debug=True)
