from flask import Flask, render_template, request, redirect, url_for
from models import Tarea
import db

app = Flask(__name__) #En app se encuentra el servidor web de Flask

@app.route("/")   #Ruta de la raíz de la app
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    return render_template("index.html", lista_de_tareas=todas_las_tareas) #Hace referencia al fichero raiz de html

@app.route("/crear-tarea", methods=["POST"])
def crear():
    tarea = Tarea(contenido=request.form["contenido_tarea"], hecha=False)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id_tarea=id).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id_tarea=id).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/editar-tarea/<id>", methods=["POST"])
def editar(id):
    tarea = db.session.query(Tarea).filter_by(id_tarea=id).first()
    tarea.contenido= request.form["contenido_tarea"]
    db.session.commit()
    return redirect(url_for("home"))





if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
