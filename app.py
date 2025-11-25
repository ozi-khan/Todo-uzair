from flask import Flask,render_template,request,redirect
from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
#we use Sqlalchemy to change Database through python. it is an orm maper.
#DATABASE:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db=SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
         
    def __repr__(self):
        return f"{self.sno} - {self.title}"

    
   

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method=="POST":
        title=(request.form["title"])  # we have to pass this these title and in file.html by giving them a name .
        desc=(request.form["desc"]) # it gets the value from flask..
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template("file.html",myfile=alltodo) #here my file is the variable which we are passing to html file for jinja templating.
  

@app.route("/show")
def show():
    alltodo=Todo.query.all()
    print (alltodo)
    return "your file"

@app.route("/update/<int:sno>",methods=["GET","POST"] )
def update(sno):
    if request.method=="POST":
        title=(request.form["title"])
        desc=(request.form["desc"])
        todo=Todo.query.filter_by(sno=sno).first() #(sno=sno ) means give me that query whose sno is equal to updates sno
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo) 

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    
if __name__=="__main__":
    app.run(debug=True , port=2000)