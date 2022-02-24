from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp, template
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from db_manager import DBManager

# configure application
app = Flask(__name__)

# ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ensure responses are not cached
@app.after_request
def after_request(response):

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db manager
db = DBManager('turitiba.db')

@app.route('/')
def index():
    '''Returns the template of the ‘/’ route. '''
    
    return render_template('index.html') 


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        
        return render_template('login.html')
    
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'GET':
        
        return render_template('register.html')
    
    fields = ['name', 'email', 'username', 'password', 
              'confirm-password']
    
    # gets data from form
    name = request.form.get(fields[0])
    email = request.form.get(fields[1])
    username = request.form.get(fields[2])
    password = request.form.get(fields[3])
    confirm_password = request.form.get(fields[4])
    
    # error checking
    if not (len(name) > 0 and ' ' in name):
        
        flash('Nome inválido!!!')
        return redirect('/register')
    
    if not ('@' in email and '.' in email):
        
        flash('E-mail inválido!!!')
        return redirect('/register')
    
    all_emails = db.get_all_emails()
    for mail in all_emails:
        
        if (email == mail[0]):
            
            flash('Este email já foi cadastrado.')
            return redirect('/register')
    
    if not (len(username) > 0 and ' ' not in username):
        
        flash('Nome de usuário inválido!!!')
        return redirect('/register')
    
    all_usernames = db.get_all_usernames()
    for user in all_usernames:
        
        if (username == user[0]):
            
            flash('Este nome de usuário já foi escolhido.')
            return redirect('/register')
    
    if not (len(password) >= 8):
        
        flash('Senha inválida!!!')
        return redirect('/register')
    
    if not (password == confirm_password):
        
        flash('As senhas digitadas não são iguais!!!')
        return redirect('/register')
    
    # add user to tb
    db.add_user_to_db(username.lower(), name, email.lower(), 
                      generate_password_hash(password))
    
    # redirect to main page
    flash('Cadastrado com sucesso!')
    return redirect('/')