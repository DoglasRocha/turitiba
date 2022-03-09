from crypt import methods
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
from datetime import datetime

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


def update_likes_in_all_locations():
    
    for id_ in db.get_all_locations_id():
        
        update_likes_count(id_[0])
        

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
    
    update_likes_in_all_locations()
    
    sample = db.get_locations_samples()
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
        
    data = location_data(location_name).get_json()
    has_liked = user_has_liked(session.get('username'), location_name)
    
    return render_template('location.html', data=data, user_has_liked=has_liked)


def user_has_liked(username: str, location_route: str) -> bool:
    
    if not (username):
        return False
    
    user_id = db.get_user_id(username)[0]
    location_id = db.get_location_id(location_route)[0]    
    has_register = db.search_for_like_in_location(user_id, location_id)

    if not (has_register):
        return False
    
    return has_register[2]


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
        'route': info[5],
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


@app.route('/manage-likes/<location>', methods=['POST'])
@login_required
def manage_likes(location: str) -> str:
    
    user_id = db.get_user_id(session['username'])[0]
    location_id = db.get_location_id(location)[0]
    
    user_has_register = db.search_for_like_in_location(user_id, location_id)
    
    if (user_has_register):
        
        has_liked = user_has_register[2]
        if (has_liked):
        
            unlike_location(user_id, location_id)
            update_likes_count(location_id)
            return ''
        
        
        like_location(user_id, location_id)
        update_likes_count(location_id)
        return ''
        
    
    insert_like(user_id, location_id)
    update_likes_count(location_id)
    
    return ''


def unlike_location(user_id: int, location_id: int) -> None:
    
    db.unlike_location(user_id, location_id)
    

def like_location(user_id: int, location_id: int) -> None:
    
    db.like_location(user_id, location_id)
    

def insert_like(user_id: str, location_id: int) -> None:
    
    db.insert_like_in_location(user_id, location_id)
    
    
def update_likes_count(location_id: int) -> None:
    
    likes_count = db.get_likes_in_location(location_id)[0]
    
    db.update_likes_in_location(location_id, likes_count)


@app.route('/get-likes/<location_route>')
def get_likes_from_location(location_route: str) -> int:
    
    location_id = db.get_location_id(location_route)[0]
    likes = db.get_likes_in_location(location_id)[0]
    
    return jsonify({'likes': likes})


@app.route('/comment/<location_route>', methods=['POST'])
@login_required
def comment(location_route: str) -> None:
    
    redirect_route = f'/location/{location_route}'
    user_comment = request.form.get('comment')
    user_id = db.get_user_id(session['username'])[0]
    location_id = db.get_location_id(location_route)[0]
    date = datetime.now()
    
    db.insert_comment_in_location(
        user_comment, 
        user_id, 
        location_id, 
        date
    )
    
    return redirect(redirect_route)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return f'Name: {e.name}, code: {e.code}'
    

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
    