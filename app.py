from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs']=False
db=SQLAlchemy(app)
app.app_context().push()




class Todo(db.Model):
      SNo=db.Column(db.Integer, primary_key=True)
      Title=db.Column(db.String(200), nullable=False)
      desc=db.Column(db.String(200), nullable=True)
      date=db.Column(db.DateTime, default=datetime.utcnow)

      def __repr__(self) -> str:
           return f"{self.SNo} - {self.Title}"

@app.route('/',methods=['GET', "POST"])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        

        todo=Todo(Title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    
    return render_template('index.html', alltodo=alltodo)
    #return 'Hello, World!'




@app.route('/update/<int:SNo>', methods=['GET', 'POST'])
def update_todo(SNo):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(SNo=SNo).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')


    todo=Todo.query.filter_by(SNo=SNo).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:SNo>')
def delete_todo(SNo):
    todo= Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True)