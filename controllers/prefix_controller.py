from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from repositories import PrefixRepository, PartRepository

prefix_bp = Blueprint('prefix', __name__, url_prefix='/prefixes')


def is_logged_in():
    return 'username' in session


def is_admin():
    return session.get('role_id') == 2


@prefix_bp.route('/create', methods=['GET', 'POST'])
def create():
    if not is_logged_in():
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        part_id = int(request.form['part_id'])
        prefix = request.form['prefix']
        
        try:
            PrefixRepository.create(part_id, prefix)
            flash('Prefix created successfully!', 'success')
            return redirect(url_for('parts.list'))
        except Exception as e:
            flash(f'Error creating prefix: {str(e)}', 'error')
    
    parts = PartRepository.get_all()
    return render_template('create_prefix.html', parts=parts)


@prefix_bp.route('/delete/<int:prefix_id>', methods=['POST'])
def delete(prefix_id):
    if not is_logged_in() or not is_admin():
        flash('Only admins can delete prefixes!', 'error')
        return redirect(url_for('parts.list'))
    
    if PrefixRepository.delete(prefix_id):
        flash('Prefix deleted successfully!', 'success')
    else:
        flash('Error deleting prefix', 'error')
    
    return redirect(url_for('parts.list'))
