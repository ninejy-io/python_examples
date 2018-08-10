
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import config
from models import User, Question, Comment
from exts import db
from decorators import login_rquired

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        "questions": Question.query.order_by("-create_time").all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phonenum = request.form.get('phonenum')
        password = request.form.get('password')
        user = User.query.filter(User.phonenum==phonenum,User.password==password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return jsonify({"msg": "手机号码或者密码错误."})


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phonenum = request.form.get("phonenum")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        user = User.query.filter(User.phonenum==phonenum).first()
        if user:
            return jsonify({"msg": "该手机号码已被注册,请更换手机号码."})
        else:
            if password != password2:
                return jsonify({"msg": "两次输入密码不同,请核对后重试."})
            else:
                user = User(phonenum=phonenum,username=username,password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_rquired
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    _question = Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html', question=_question)


@app.route('/comment/', methods=['POST'])
@login_rquired
def comment():
    content = request.form.get('content')
    question_id = request.form.get('question_id')
    _comment = Comment(content=content)
    
    user_id = session['user_id']
    user = User.query.filter(User.id==user_id).first()
    _comment.author = user

    question = Question.query.filter(Question.id==question_id).first()
    _comment.question = question

    db.session.add(_comment)
    db.session.commit()

    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            return {"user": user}
    else:
        return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)