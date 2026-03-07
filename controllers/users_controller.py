import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from repositories import UserRepository

users_bp = Blueprint('users', __name__, url_prefix='/users')


def is_logged_in():
    return 'username' in session


def is_admin():
    return session.get('role_id') == 2


@users_bp.route('/')
def list():
    if not is_logged_in() or not is_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('parts.list'))

    users = UserRepository.get_all()
    return render_template('manage_users.html', users=users)


@users_bp.route('/update_password/<username>', methods=['POST'])
def update_password(username):
    if not is_logged_in() or not is_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('parts.list'))

    new_password = request.form['new_password']

    if len(new_password) < 6:
        flash('Password must be at least 6 characters long', 'error')
        return redirect(url_for('users.list'))

    if not re.search(r'^[A-Za-z]', new_password) or not re.search(r'\d', new_password):
        flash('Password must have letters and numbers', 'error')
        return redirect(url_for('users.list'))

    if UserRepository.update_password(username, new_password):
        flash(f'Password updated for {username}', 'success')
    else:
        flash(f'User {username} not found', 'error')

    return redirect(url_for('users.list'))


@users_bp.route('/delete/<username>', methods=['POST'])
def delete(username):
    if not is_logged_in() or not is_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('parts.list'))

    if username == session.get('username'):
        flash('You cannot delete your own account', 'error')
        return redirect(url_for('users.list'))

    if UserRepository.delete(username):
        flash(f'User {username} deleted successfully', 'success')
    else:
        flash(f'User {username} not found', 'error')

    return redirect(url_for('users.list'))
