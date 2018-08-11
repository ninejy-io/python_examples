# coding: utf-8
from flask import Flask, url_for
from flask import request, redirect
from flask import render_template, g, jsonify
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from utils import user_register, check_user
from utils import User
from utils import DockerManager
from utils import get_all_images_info
from utils import record_image_info
from utils import delete_image_info
from forms import LoginForm
from gevent import monkey, pywsgi
monkey.patch_all()


app = Flask(__name__, static_url_path='/static')
app.CSRF_ENABLED = True
app.secret_key = "Akjdhgs,dyG/c!msd*csd$mNL7&N%nm@cdl=dnccnTvfgh"
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)
dm = DockerManager()


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/admin/register/', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if user_register(user, pwd):
            return redirect(url_for('login'))
        return render_template('register.html')
    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            flash('%s  %s  %s' % (form.user.data, form.pwd.data, form.remember_me.data))
        user = request.form.get('user', '')
        pwd = request.form.get('pwd', '')
        res = check_user(user, pwd)
        if res:
            user = User()
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', msg=u'用户名或密码错误')
    return render_template('login.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/images/')
@login_required
def images():
    images = get_all_images_info()
    return render_template('images.html', images=images)


@app.route('/build/', methods=['GET', 'POST'])
@login_required
def build():
    if request.method == 'POST':
        data = request.values.to_dict()
        image = dm.build_image(**data)
        if image != 'error':
            record_image_info(data['tag'].split(':')[1], image)
        return jsonify({'result': image})
    return render_template('build.html')


@app.route('/pull/', methods=['GET', 'POST'])
@login_required
def pull():
    if request.method == 'POST':
        temp = request.form.get('name')
        if ':' in temp:
            name, tag = temp.split(':')
        else:
            name, tag = temp, None
        image = dm.pull_image(name, tag)
        return jsonify({'result': image})
    return render_template('pull.html')


@app.route('/push/', methods=['POST'])
@login_required
def push():
    temp = request.form.get('name')
    if ':' in temp:
        repository, tag = temp.split(':')
    else:
        repository, tag = temp, None
    dm.push_image(repository, tag)
    return 'ok'


@app.route('/delete/')
@login_required
def delete():
    image = request.args.get('name')
    try:
        dm.remove_image(**{'image': image, 'force': True})
        delete_image_info(image)
    except Exception:
        pass
    return 'ok'


@app.route('/all_images/')
def all_images():
    images = dm.get_images()
    return render_template('all_images.html', images=images)


@app.route('/delete2/')
@login_required
def delete2():
    image = request.args.get('name')
    try:
        dm.remove_image(**{'image': image, 'force': True})
    except Exception:
        pass
    return 'ok'


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 9999), app)
    server.serve_forever()
