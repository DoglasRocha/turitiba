from helpers import login_required
from new_user import NewUser
from log_user import LogUser
from update_user import UpdateUser
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from db_manager import DBManager
from datetime import datetime
from reader import Reader
from os import getenv
from like import Like

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
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db manager
db = DBManager(getenv('DB_PATH'))


def update_likes_in_all_locations():
    '''Function that updates the likes count in all locations.
    Firstly, gets the ids of all locations, then iterates over 
    the ids and triggers other function that updates the likes count
    in a determinate location'''
    
    all_ids = Reader.get_all_ids_from_locations(db)
    
    for id_ in all_ids:
        
        update_likes_count(id_)
        

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
    '''Gets the user data from the DB.
    Receives the username as argument.
    Renders the template
    of the user screen, passing the user data as argument'''
    
    user_info = Reader.get_user_info(db, username)
    
    return render_template('user.html', info=user_info)


@app.route('/update-user/<username>', methods=['POST'])
@login_required
def update_user(username):
    '''Updates the user data in the DB.
    Receives the username as argument.
    First, gets all the
    data from the form, then delegates the update to the
    UpdateUser class, that checks for errors and checks
    what information needs to be updated'''
    
    # gets data from the form
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
    '''Returns a JSON with a sample with size 10.
    First, updates the likes from all locations (ranking
    system), then gets the sample from the DB and
    return the "jsonification" of the sample.'''
    
    update_likes_in_all_locations()
    
    sample = Reader.get_locations_sample(db, 10)
        
    return jsonify(sample)


@app.route('/location/<location_route>')
def location(location_route: str):
    '''Renders the location template.
    Receives the location route as argument.
    First, gets the data from the location, using the location_data
    function, then checks if the user has liked the location,
    then gets all the comments from the location.
    Returns the rendered template, passing the data, the user like 
    and the comments as arguments
    '''
        
    data = location_data(location_route).get_json()
    has_liked = user_has_liked(session.get('username'), location_route)
    comments = Reader.get_comments_from_location(db, location_route)
    
    return render_template('location.html', 
                           data=data, 
                           user_has_liked=has_liked,
                           comments=comments)


@app.route('/location-data/<location_route>')
def location_data(location_route: str):
    '''Returns a JSON with the data from a location.
    Receives the location route as argument.
    Gets the location data from the DB and then
    returns the "jsonification" of it'''
    
    data = Reader.get_location_data(db, location_route)
    
    return jsonify(data)


def user_has_liked(username: str, location_route: str) -> bool:
    '''Returns a boolean that indicates if the user has
    or has not liked a location.
    Takes the username and the location route as arguments.
    If the user is not logged in, just returns False (guard clause).
    Then, checks in the DB if the user has liked and return the info.
    '''
    
    if not (username):
        return False
    
    return Reader.user_has_liked(db, username, location_route)


@app.route('/logout', methods=['POST'])
def logout():
    '''Logs out the user.
    First, gets the callback page, then clear the cookies, flashes
    the user log out message and then redirects to the callback route.'''
    
    callback = request.args.get('callback')
    session.clear()
    flash('Deslogado com sucesso!')
    
    return redirect(f'/{callback}')
    
    
@app.route('/main')
def main():
    '''Just an auxiliary route that redirects to the "/" route.'''
    
    return redirect('/')


@app.route('/manage-likes/<location_route>', methods=['POST'])
@login_required
def manage_likes(location_route: str) -> str:
    '''
    Route responsible for managing the likes in a location.
    Receives the route of the location as argument.
    Delegates the logic to the Like object.
    '''
    
    user_id = Reader.get_user_id(db, session['username'])
    location_id = Reader.get_location_id(db, location_route)
    
    like_manager = Like(db, user_id, location_id, session['username'],
                        location_route)
    
    like_manager.set_action().action()
    return '', 200
    
    
def update_likes_count(location_id: int) -> None:
    
    likes_count = Reader.get_likes_in_location(db, location_id)
    
    db.update_likes_in_location(location_id, likes_count)


@app.route('/get-likes/<location_route>')
def get_likes_from_location(location_route: str) -> int:
    
    location_id = Reader.get_location_id(db, location_route)
    likes = Reader.get_likes_in_location(db, location_id)
    
    return jsonify({'likes': likes})


@app.route('/comment/<location_route>', methods=['POST'])
@login_required
def comment(location_route: str) -> None:
    
    redirect_route = f'/location/{location_route}'
    user_comment = request.form.get('comment')
    user_id = Reader.get_user_id(db, session['username'])
    location_id = Reader.get_location_id(db, location_route)
    date = datetime.now()
    
    db.insert_comment_in_location(
        user_comment, 
        user_id, 
        location_id, 
        date
    )
    
    return redirect(redirect_route)

@app.route('/delete-comment/<location_route>', methods=['POST'])
def delete_comment(location_route: str) -> None:
    
    user_id = Reader.get_user_id(db, session['username'])
    location_id = Reader.get_location_id(db, location_route)
    comment = request.form.get('comment')
    
    db.delete_comment(user_id, location_id, comment)
    
    return redirect(f'/location/{location_route}')


@app.route('/search')
def search():
    
    user_search = request.args.get('q') or ''
    
    result = Reader.search(db, user_search)
    
    return render_template('search.html', search=result)


@app.route('/search-bar')
def search_bar():
    
    user_search = request.args.get('q') or ''
    
    result = Reader.search_names(db, user_search)
    return jsonify(result)
    

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return f'Name: {e.name}, code: {e.code}'
    

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
    