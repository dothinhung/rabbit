from flask import *
import mlab
from models.user import User

app = Flask(__name__)

app.secret_key = 'a super secret key'

mlab.connect()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        form = request.form
        uname = form['uname']
        password = form['password']

        users = User.objects(uname=uname, password=password)

        if not users:
            return "Sai usename or password"
        else:
            session['logged_in'] = True
            session['user_id'] = str(users[0].id)
            return "Vào trang cá nhân"

@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template('sign-up.html')
    elif request.method == "POST":
        form = request.form
        fname = form['fname']
        email = form['email']
        uname = form['uname']
        password = form['password']

        new_user = User(
            fname = fname,
            email = email,
            uname = uname,
            password = password
        )

        new_user.save()
        # sẽ cho redirect vào trang chủ luôn
        return "Bạn đã đk thành công"

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
  app.run(debug=True)
 