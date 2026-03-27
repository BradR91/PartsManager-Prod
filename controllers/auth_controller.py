import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from repositories import UserRepository, RoleRepository

auth_bp = Blueprint('auth', __name__)


def is_logged_in():
    return 'username' in session


@auth_bp.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('parts.list'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = UserRepository.authenticate(username, password)
        if user:
            session['username'] = user.Username
            session['role_id'] = user.RoleID
            return redirect(url_for('parts.list'))
        else:
            flash('Wrong username or password', 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = int(request.form['role_id'])
        
        if len(username) <6 or len(password) < 6:
            flash('Username and password must be at least 6 characters long', 'error')
            return redirect(url_for('auth.register'))
        
        if not re.search(r'^[A-Za-z]', password) or not re.search(r'\d', password):
            flash('Password must have letters and numbers.', 'error')
            return redirect(url_for('auth.register'))
        
        if UserRepository.get_by_username(username):
            flash('Username already exists', 'error')
        else:
            UserRepository.create(username, password, role_id)
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
    
    roles = RoleRepository.get_all()
    return render_template('register.html', roles=roles)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
