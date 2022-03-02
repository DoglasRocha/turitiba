from helpers import login_required
from new_user import NewUser
from log_user import LogUser
from update_user import UpdateUser
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
db = DBManager('./turitiba.db')

@app.route('/')
def index():
    '''Gets samples of the 10 most famous locations from the DB, then
    renders the template, passing the sample as argument.'''
    
    data = sample().get_json()
    
    return render_template('index.html', sample=data) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Deals with the login. If receives a request with the GET 
    method, just renders the login screen.
    Else, clears the cookies, gets the username and the password from
    the form, uses LogUser class to do error checking, writes the 
    cookies with the username if all the tests are past successfully,
    flash all the messages from the object and redirect to the correct
    route. If all is successfull, goes to the main route, if not, stays
    in the login route. 
    '''
    
    if request.method == 'GET':
        
        return render_template('login.html')
    
    session.clear()
    
    username = request.form.get('username') or ''
    password = request.form.get('password') or ''
    
    # error checking
    user = LogUser(username, password, db)
    
    if user.is_all_okay():
        session['username'] = username
        
    # flash messages
    for message in user.get_messages():
        flash(message)
        
    return redirect(user.get_redirection())


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''''
    Deals with the user registration.
    If receives a request with the GET method, just renders the register
    screen.
    If not, gets the data from the registration form, do error checking
    using the NewUser class. If all the test are past successfully, sends
    the new user data to the DB.
    Then, flashes all the messages from the object and redirects to the
    correct route. If the user is successfully registered, redirects to
    the login route, else, stays in the registration route.
    '''
    
    if request.method == 'GET':
        
        return render_template('register.html')
    
    # gets data from form
    name = request.form.get('name') or ''
    email = request.form.get('email') or ''
    username = request.form.get('username') or ''
    password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm-password') or ''
    
    # error checking
    user = NewUser(name, email, username, password, confirm_password,
                   db)
    
    if user.is_all_okay():
        user.send_to_db()
    
    # flash and redirect
    for message in user.get_messages():
        flash(message)
        
    return redirect(user.get_redirection())


@app.route('/user/<username>')
@login_required
def user(username: str):
    
    user_info = db.get_user_info(username)
    info = {
        'username': username,
        'name': user_info[0],
        'email': user_info[1]
    }
    
    return render_template('user.html', info=info)


@app.route('/update-user/<username>', methods=['POST'])
@login_required
def update_user(username):
    
    name = request.form.get('name') or ''
    email = request.form.get('email') or ''
    current_password = request.form.get('old-password') or ''
    new_password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm-password') or ''
    
    # error checking
    user = UpdateUser(name, email, username, current_password,
                      new_password, confirm_password, db)
    
    if user.is_all_okay():
        user.update_user_in_db()
        
    # flash messages
    for message in user.get_messages():
        flash(message)
        
    return redirect(user.get_redirection())


@app.route('/sample')
def sample():
    
    sample = db.get_locations_samples()
    print(sample)
    names = []
    paths = []
    url_names = []
    
    for name, path in sample:
        if name not in names:
            names.append(name)
            paths.append(path)
            url_names.append(name.lower().replace(' ', '-'))
    
    organized_sample = []
    for name, path, url_name in zip(names, paths, url_names):
        organized_sample.append({
            'name': name,
            'path': path,
            'url_name': url_name
        })
        
    return jsonify(organized_sample[:10])


@app.route('/location/<location_name>')
def location(location_name: str):
    
    if location_name == 'ópera-de-arame':
        normalized_name = 'Ópera de Arame'

    else:
        normalized_name = location_name.replace('-', ' ')
        
    data = location_data(normalized_name).get_json()
    
    return render_template('location.html', data=data)


@app.route('/location-data/<location_name>')
def location_data(location_name: str):
    
    info, photos = db.get_location_data(location_name)
    
    normalized_photos = []
    for photo in photos:
        normalized_photos.append('.' + photo[0])
        
    data = {
        'name': info[0],
        'description': info[1],
        'likes': info[2],
        'maps_link': info[3],
        'info': info[4],
        'photos': normalized_photos
    }
    
    return jsonify(data)


@app.route('/logout', methods=['POST'])
def logout():
    
    callback = request.args.get('callback')
    session.clear()
    flash('Deslogado com sucesso!')
    
    return redirect(f'/{callback}')
    
    
@app.route('/main')
def main():
    
    return redirect('/')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return f'Name: {e.name}, code: {e.code}'
    

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)