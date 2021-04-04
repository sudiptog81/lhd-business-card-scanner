import os
from flask import (
    Flask,
    request,
    redirect,
    render_template,
    flash,
)
from helper import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def create_app():
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', default='octocat')
    return app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            flash('Only images allowed', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join('.', file.filename))
            emails, numbers = parse_card(os.path.join('.', file.filename))
            return render_template('main/index.html', emails=emails, numbers=numbers)
    return render_template('main/index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
