from flask import *
import mlab
from models.user import Body, User
from models.video import Video, Underweight, Yoga, Cardio, Exercise
from youtube_dl import YoutubeDL 
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
        users = User.objects(uname__exact=uname, password__exact=password)
        if len(users) == 0:
            error = 'Wrong username or password! Please try again!'
            return render_template('login.html', error=error)
        else:
            user_id = str(users[0].id)
            full_name = str(users[0].fname)
            session['logged_in'] = True
            session['user_id'] = user_id
            session['user_name'] = full_name
            # for user in users:
            #     session['user_name'] = user['fname']
            current_user = User.objects.with_id(user_id)
            all_body = current_user.bmi_id
            return render_template('individual.html', user_id= user_id, all_body = all_body, full_name = session['user_name'])

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
            password = password,
            bmi_id = []
        )

        new_user.save()
        # sẽ cho redirect vào trang chủ luôn
        return redirect(url_for('login'))


######################### BMI ########################
@app.route('/bmi', methods=["GET", "POST"])
def bmi():
    if request.method == "GET":
        if 'user_name' not in session:
            return redirect(url_for('login'))
        else:
            return render_template('check.html', full_name = session['user_name'])
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
            # session['user_bmi'] = bmi
            user_id = session['user_id']
            new_body = Body(
                time = time,
                weight = weight,
                height = height,
                bmi = bmi,
                bmi_type = bmi_type
            )
            new_body.save()
            new_body.reload()
            # videos = Video.objects()
            # cardios = Cardio.objects()

            current_user = User.objects.with_id(user_id)
            # current_user.update(add_to_set__bmi_id = str(new_body.id))
            # print(new_body)
            # print(current_user)
            current_user.update(push__bmi_id = new_body)
            # return render_template ('individual.html', all_body = current_user.bmi_id, full_name = session['user_name'], user_id = session['user_id'])
            # return "sadasd"
            return redirect(url_for('individual'))
        else:
            videos = Video.objects()
            cardios = Cardio.objects()
            underweights = Underweight.objects()
            yogas = Yoga.objects()
            exercises = Exercise.objects()
            # overweights = Overweight.objects()
            if bmi < 18.5:
                return render_template('underweight.html', bmi = bmi, yogas=yogas, underweights=underweights, full_name = session['user_name']) 
            elif 18.5 <= bmi < 25:
                return render_template('normal.html', bmi = bmi, videos=videos, yogas=yogas, underweights=underweights, full_name = session['user_name'])
            elif 25 <= bmi < 30:
                return render_template('overweight.html', bmi = bmi, videos=videos, cardios=cardios, exercises=exercises,full_name = session['user_name'])
            elif bmi > 30:
                return render_template('obese.html', bmi = bmi, videos=videos, cardios=cardios, exercises=exercises)


############################ LOG-OUT #####################
@app.route('/logout')
def log_out():
    if 'logged_in' in session:
        del session['logged_in']
        return redirect(url_for('index'))
    else:
        return "Bạn chưa đăng nhập"

@app.route('/individual/')
def individual():
    if "logged_in" in session:
        user_id = session["user_id"]
        current_user = User.objects.with_id(user_id)
        all_body = current_user.bmi_id
        return render_template('individual.html', all_body = all_body, full_name = session['user_name'], user_id=user_id)
    else:
        return redirect(url_for('login'))

######################### MENU ###############################
@app.route('/menu')
def menu():
    return render_template('menu1.html',full_name = session['user_name'])

@app.route('/menu-under')
def menu_under():
    return render_template('menu2.html',full_name = session['user_name'])

@app.route('/menu-under1')
def menu_under1():
    return render_template('menu3.html',full_name = session['user_name'])


@app.route('/detox')
def detox():
    return render_template('detox1.html',full_name = session['user_name'])

############################## app thêm video
@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'GET':
        videos = Video.objects()
        cardios = Cardio.objects()
        # overweights = Overweight.objects()
        underweights = Underweight.objects()
        yogas= Yoga.objects()
        exercises = Exercise.objects()
        return render_template('admin.html', videos=videos, cardios=cardios, underweights=underweights, yogas=yogas, exercises=exercises )
    elif request.method == 'POST':
        form = request.form
        link = form['link']
        ydl = YoutubeDL()
        data = ydl.extract_info(link, download=False)

        title = data['title']
        thumbnail = data['thumbnail']
        youtube_id = data['id']
        # duration = data['duration']


        new_ex = Exercise(
                title= title,
                link= link,
                thumbnail= thumbnail,
                youtube_id= youtube_id
                # duration= duration
            )

        new_ex.save()
    
        return redirect(url_for('video'))

# detail to view video
@app.route('/detail/<youtube_id>')
def detail(youtube_id):
    return render_template('detail.html', youtube_id = youtube_id, full_name = session['user_name'], bmi=bmi) 



@app.route('/detox-underweight')
def detox_underweight():
    return render_template('detox2.html')

@app.route('/getlean/<bmi_id>')
def getlean(bmi_id):
    if "logged_in" in session:
        # bmi = session['user_bmi']
        body = Body.objects.with_id(bmi_id)
        
        user = User.objects.with_id(session['user_id'])
        # user_id = session['user_id']
        # print(user_id)
        # get_body = Body.objects(user_id = user_id)
        # print(get_body)
        # bmi = Body.objects.order_by('-user_id').first()
        videos = Video.objects()
        cardios = Cardio.objects()
        yogas = Yoga.objects()
        exercises = Exercise.objects()
        underweights = Underweight.objects()
        if body.bmi < 18.5:
            return render_template('underweight.html', full_name = user.fname, user_id = user.id, bmi = body.bmi, videos=videos, cardios=cardios, yogas=yogas, underweights=underweights) 
        elif 18.5 <= body.bmi < 25:
            return render_template('normal.html', full_name = user.fname, user_id = user.id, bmi = body.bmi, videos=videos, cardios=cardios, yogas=yogas, underweights=underweights)
        elif 25 <= body.bmi < 30: 
            return render_template('overweight.html', full_name = user.fname, user_id = user.id, bmi = body.bmi, videos=videos, cardios=cardios, exercises=exercises)
        else:
            return render_template('obese.html', full_name = user.fname, user_id = user.id, bmi = body.bmi, videos=videos, cardios=cardios, exercises=exercises)
    else:
        return render_template(url_for('login'))



if __name__ == '__main__':
  app.run(debug=True)