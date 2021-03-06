from flask      import session, render_template, redirect, url_for
from flask_mail import Message
from subprocess import call
import json

# Formatea la fecha
def date_format(date):
    months = ["Enero", "Febrero", "Marzo", "Abril",
             "Mayo", "Junio", "Julio", "Agosto",
             "Septiembe", "Octubre", "Noviembre", "Diciembre"]
             
    month = months[date.month - 1]
    
    return "{} de {} del {}".format(date.day, month, date.year)
    
def send_email(user_email, username, app, mail):
    msg = Message("REGISTRO EXITOSO",
        sender     = app.config["MAIL_USERNAME"],
        recipients = [user_email])
    msg.html = render_template("email.html", username=username)
    mail.send(msg)

def check_login(username):
    if "username" in session:
        username = session["username"]
        return True
    return False

def create_session(username, user_id):
    session["username"] = username
    session["user_id"]  = user_id

# Elimina un comentario
def delete_comment(Comment, db, id_, flash):
    comment = Comment.query.filter_by(id=id_).first()
    db.session.delete(comment)
    db.session.commit()

    success_message = "Comentario eliminado"
    flash(success_message)

# Actualiza un comentario
def comment_update(Comment, db, id_, comment_text, flash):
    comment = Comment.query.filter_by(id=id_).first()
    comment.text = comment_text
    db.session.commit()

    success_message = "Comentario actualizado"
    flash(success_message)

def set_config():        
    
    with open("config.json") as json_data:
        d = json.load(json_data)
    
    print("1- Localhost")
    print("2- Pythonanywhere")
    print("3- Heroku")
    opc = int(input("Choose of the options above: "))

    if opc == 1:
        return d["localhost"]
    elif opc == 2:
        return d["pythonanywhere"]
    elif opc == 3:
        return d["heroku"]
    else:
        return None
