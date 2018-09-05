from flask import *
import mlab
from models.user import User, Body
import datetime

app = Flask(__name__)

app.secret_key = 'a super secret key'

mlab.connect()

@app.route('/')
def index():
    # print(user_id)
    if "logged_in" in session:
        if session['logged_in'] == True:
            return render_template('index2.html', full_name = session['user_name'], user_id = session['user_id'])
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
            session['user_id'] = str(users[0].id)
            # for user in users:
            session['user_name'] = str(users[0].fname)
                # session['user_id']
            return  render_template('index2.html', full_name = session['user_name'], user_id = session['user_id'])



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
        return redirect(url_for('login'))

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
        time = datetime.datetime.now
        bmi = int(weight) / (int(height) ** 2) *10000
        if bmi < 18.5:
            bmi_type = "underweight"
        elif 18.5 <= bmi < 25:
            bmi_type = "normal"
        elif 25 <= bmi < 30:
            bmi_type = "overweight"
        else:
            bmi_type = "obese"

        if "logged_in" in session:
            session['user_bmi'] = int(bmi)
            user_id = session['user_id']
            new_body = Body(
                time = time,
                weight = weight,
                height = height,
                bmi = bmi,
                user_id = user_id,
                bmi_type = bmi_type
            )
            new_body.save()
            all_body = Body.objects(user_id = user_id)
            return render_template ('individual.html', all_body = all_body, full_name = session['user_name'])
        else:
            if bmi < 18.5:
                return render_template('underweight.html') 
            elif 18.5 <= bmi < 25:
                return render_template('normal.html')
            elif 25 <= bmi:
                return render_template('overweight.html')

############################ LOG-OUT #####################
@app.route('/logout')
def log_out():
    del session['logged_in']
    return redirect(url_for('index'))


@app.route('/individual/<user_id>')
def individual(user_id):
    if "logged_in" in session:
        all_body = Body.objects(user_id = user_id)
        return render_template('individual.html', all_body = all_body)
    else:
        return redirect(url_for('login'))

######################### MENU ###############################
@app.route('/menu')
def menu():
    return render_template('menu1.html')

@app.route('/detox')
def detox():
    return render_template('detox1.html')

@app.route('/get-lean')
def getlean():
    if "logged_in" in session:
        bmi = session['user_bmi'] 

        if bmi < 18.5:
            return render_template('underweight2.html', full_name = session['user_name']) 
        elif 18.5 <= bmi < 25:
            return render_template('normal2.html', full_name = session['user_name'])
        else:
            return render_template('overweight2.html', full_name = session['user_name'])
    else:
        return render_template(url_for('login'))

if __name__ == '__main__':
  app.run(debug=True)
 