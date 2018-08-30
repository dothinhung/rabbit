from flask import *
import mlab
from models.user import User

app = Flask(__name__)

app.secret_key = 'a super secret key'

mlab.connect()

@app.route('/')
def index():
    # print(user_id)
    if "logged_in" in session:
        if session['logged_in'] == True:
            return render_template('index2.html', full_name = session['user_name'])
    else:
        return render_template('index.html')

#################### LOGIN #######################
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
            # session['user_id'] = str(users[0].id)
            for user in users:
                session['user_name'] = user['fname']
            return redirect(url_for('index'))



#################### SIGN-UP #########################
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
        return redirect(url_for('individual'))

######################## BLOG ###########################
@app.route('/blog')
def blog():
    return render_template('blog.html')


######################### BMI ########################
@app.route('/bmi', methods=["GET", "POST"])
def bmi():
    if request.method == "GET":
        return render_template('check.html')
    elif request.method == "POST":
        form = request.form
        weight = form['weight']
        height = form['height']

        height = int(height) / 100
        bmi = int(weight) / (height ** 2)

        if bmi < 18.5:
            return render_template('underweight.html') 
        elif 18.5 <= bmi < 25:
            return render_template('normal.html')
        elif 25 <= bmi < 30:
            return render_template('overweight.html')
        elif bmi > 30:
            return render_template('obese.html') 

############################ LOG-OUT #####################
@app.route('/logout')
def log_out():
    del session['logged_in']
    return redirect(url_for('index'))


@app.route('/individual')
def individual():
    print(session)
    if "logged_in" in session:
        if session['logged_in'] == True:
            return render_template('individual.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
  app.run(debug=True)
 