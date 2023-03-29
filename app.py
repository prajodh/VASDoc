from flask import Flask, render_template,redirect ,request,send_file,session, url_for , g
from flask_wtf import FlaskForm
import os
import requests
from dotenv import load_dotenv
load_dotenv() 
from File_Decryption import decrypt_data
import datetime
from File_upload import File_upload
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

from wtforms.validators import InputRequired
from Decrypt_file import Decrypt
import bcrypt
from pymongo import MongoClient
from Profile import Profile

cl = MongoClient("mongodb://localhost:27017")
db = cl["userdata"]
collections = db["userdata"]

proj_id = '2My7MeE7GYEYXbYCpx9BTZpYd4m'
proj_secret = 'a14627536a3deddd62467e42bf6a900b' 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'F:/VasDoc/VASDoc/static/_files/'
app.config['UPLOAD_FOLDERR'] = 'F:/VasDoc/VASDoc/static/_files/'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'user-system'
# app.config['MONGO_DBNAME'] = 'VasDoc'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017'
# mysql = MySQL(app)
# mongodb+srv://vasdoc:vasdoc1234@cluster0.1ssyf7f.mongodb.net/test
# mongodb+srv://vasdoc:vasdoc1234@cluster0.1ssyf7f.mongodb.net/?retryWrites=true&w=majority

# mongo = PyMongo(app)
# db  = mongo.db


gateway="https://ipfs.io/ipfs/"
items = {}
dir_name = 'F:/VasDoc/VASDoc/static/_files/'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Submit")

@app.before_request
def before_request():
    if "username" in session:
        g.username = session["username"]


app.register_blueprint(File_upload,url_prefix = "")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

app.register_blueprint(Decrypt,url_prefix="")

app.register_blueprint(Profile, url_prefix = "/login/")

@app.route('/download')
def file_download():
    file ="encrypted.txt"
    return send_file(file,as_attachment=True)

@app.route('/login',methods = ['GET','POST'])
def login():
    form = UploadFileForm()
    # users = mongo.db.users
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        login_user = db.userdata.find_one({'name' : request.form['username']})
        
        if login_user:
            # if check_password_hash(request.form['password'], login_user['password']):
            if  bcrypt.checkpw(request.form['password'].encode("utf-8"),login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for("Profile.profile") )
            return "invalid user"


    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     username = request.form['username']
    #     password = request.form['password']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username,password))
    #     user = cursor.fetchone()
    #     if user:
    #         # session['loggedin'] = True
    #         # session['name'] = user['name']
    #         return render_template('File_upload.html')
    return render_template('login.html')

@app.route('/register',methods = ['GET','POST'])
def register():

    if request.method == 'POST' :
        
        # existing_user = db.userdata.find_one({'name' : request.form['name']})
        existing_user = None
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # hashpass = generate_password_hash(request.form['password'])
            # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8') , bcrypt.gensalt())
            db.userdata.insert_one({'name' : request.form['name'] , 'password' : hashpass , 'email' : request.form['email']})
            return redirect('/login')
        else:
            print(existing_user)
            return "USer exists"
    return render_template('register.html')


    #     user = request.form['name']
    #     username = request.form['username']
    #     password = request.form['password']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM user WHERE username = % s',(username,))
    #     account = cursor.fetchone()
    #     if account :
    #         msg  ="Account exists"
    #     else:
    #         cursor.execute('INSERT INTO user VALUES (% s,% s,% s)',(username,password,user))
    #         mysql.connection.commit()
    #         print("into register")
    #         return render_template('login.html')
    # return render_template('register.html')

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("index"))


if __name__ == '__main__':
  app.run(host='0.0.0.0',debug= True)


































  # @app.route('/', methods=['GET',"POST"])
# @app.route('/file_upload', methods=['GET',"POST"])
# def file_upload():
#     form = UploadFileForm()
#     if form.validate_on_submit(): 
#         username = request.form.get("username")
        
#         file = form.file.data # First grab the file
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
#         directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR'])
#         files = os.listdir(directory)
#         files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
#         recent_file = files[0]
#         print("this is ",recent_file)
#         for f in files:
#             files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
#             recent_file = files[0]
#             item = open(dir_name + recent_file, 'rb')
#             items[f] = item
#         response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=true&wrap-with-directory=false",
#                          auth=(proj_id, proj_secret),files=items)
#         # print(result)
#         dec = json.JSONDecoder()
#         i = 0
#         while i < 1:
#             data, s = dec.raw_decode(response.text[i:])
#             i += s + 1
#             if data['Name'] == '':
#                 data['Name'] = 'Folder CID'
#             print("%s: %s" % (data['Name'], data['Hash']))
#             x = data["Hash"]
#             with open("public.pem","rb") as f:
#                 publicKey = rsa.PublicKey.load_pkcs1(f.read())
#             encrypted_data = encrypt_data(data['Hash'],publicKey)

#             # https://VASDoc.infura-ipfs.io/ipfs/

#         # return "<h2>Click this link{}</h2>".format(x)
#             # https://VASDoc.infura-ipfs.io/ipfs/
#             print(encrypted_data)
            
#             # return redirect("https://VASDoc.infura-ipfs.io/ipfs/"+x)
#             return render_template('file_download.html')
#     return render_template('file_upload.html', form=form)



# @app.route('/decrypt_file',methods=['GET',"POST"])
# def decrypt_file():    
#     if request.method == 'POST':
#         file = request.files['file_name1']
#         # print(file.stream.read())
#         x = b""
#         x = file.stream.read()
#         x.decode()
#         print(x)
        
#         filename = secure_filename(file.filename)
#         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         new_filename = f"{timestamp}_{filename}"
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],new_filename))
#         with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],new_filename), "wb") as f:
#             f.write(x)
        
#         file = request.files['file_name2']
#         filename = secure_filename(file.filename)
#         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M"+"611")
#         new_filename = f"{timestamp}_{filename}"
        
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],new_filename))
        
#         directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR'])
#         data = (decrypt_data(directory))
#         print(data)  
             
#         return redirect("https://VASDoc.infura-ipfs.io/ipfs/"+data)
#     return  render_template("decrypt_file.html")