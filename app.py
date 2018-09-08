from flask import *
import mlab
from models.user import Body, User
from models.video import Video,Cardio
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
            session['user_id'] = str(users[0].id)
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
            
            # videos = Video.objects()
            # cardios = Cardio.objects()

            current_user = User.objects.with_id(user_id)
            # current_user.update(add_to_set__bmi_id = str(new_body.id))
            # print(new_body)
            # print(current_user)
            current_user.update(push__bmi_id = new_body)
            return render_template ('individual.html', all_body = current_user.bmi_id, full_name = session['user_name'])
            # return "sadasd"
        else:
            videos = Video.objects()
            cardios = Cardio.objects()
            if bmi < 18.5:
                return render_template('underweight.html', bmi = bmi, videos=videos, cardios=cardios, full_name = session['user_name']) 
            elif 18.5 <= bmi < 25:
                return render_template('normal.html', bmi = bmi, videos=videos, cardios=cardios, full_name = session['user_name'])
            elif 25 <= bmi:
                return render_template('overweight.html', bmi = bmi, videos=videos, cardios=cardios, full_name = session['user_name'])

############################ LOG-OUT #####################
@app.route('/logout')
def log_out():
    if 'logged_in' in session:
        del session['logged_in']
        return redirect(url_for('index'))
    else:
        return "Bạn chưa đăng nhập"

@app.route('/individual/<user_id>')
def individual(user_id):
    if "logged_in" in session:
        all_body = Body.objects(user_id = user_id)
        return render_template('individual.html', all_body = all_body, full_name = session['user_name'])
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
        return render_template('admin.html', cardios=cardios)
    elif request.method == 'POST':
        form = request.form
        link = form['link']
        ydl = YoutubeDL()
        data = ydl.extract_info(link, download=False)

        title = data['title']
        thumbnail = data['thumbnail']
        youtube_id = data['id']
        duration = data['duration']


        new_cardio = Cardio(
                title= title,
                link= link,
                thumbnail= thumbnail,
                youtube_id= youtube_id,
                duration= duration
            )

        new_cardio.save()
    
        return redirect(url_for('video'))

# detail to view video
@app.route('/detail/<youtube_id>')
def detail(youtube_id):
    return render_template('detail.html', youtube_id = youtube_id) 



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
        if body.bmi < 18.5:
            return render_template('underweight.html', full_name = user.fname, user_id = user.id, bmi = body.bmi) 
        elif 18.5 <= body.bmi < 25:
            return render_template('normal.html', full_name = user.fname, user_id = user.id, bmi = body.bmi)
        else:
            return render_template('overweight.html', full_name = user.fname, user_id = user.id, bmi = body.bmi)
    else:
        return render_template(url_for('login'))



if __name__ == '__main__':
  app.run(debug=True)
 