from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from repositories import PartRepository

parts_bp = Blueprint('parts', __name__, url_prefix='/parts')


def is_logged_in():
    return 'username' in session


def is_admin():
    return session.get('role_id') == 2


@parts_bp.route('/')
def list():
    if not is_logged_in():
        return redirect(url_for('auth.login'))
    
    parts = PartRepository.get_all()
    return render_template('parts_list.html', parts=parts, is_admin=is_admin())


@parts_bp.route('/create', methods=['GET', 'POST'])
def create():
    if not is_logged_in():
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        part_no = request.form['part_no']
        part_desc = request.form['part_desc']

        if PartRepository.get_by_part_no(part_no):
            flash(f'Part number "{part_no}" already exists.', 'error')
            return render_template('create_part.html')
        
        try:
            PartRepository.create(part_no, part_desc)
            flash('Part created successfully!', 'success')
            return redirect(url_for('parts.list'))
        except Exception as e:
            flash(f'Error creating part: {str(e)}', 'error')
    
    return render_template('create_part.html')


@parts_bp.route('/update/<int:part_id>', methods=['GET', 'POST'])
def update(part_id):
    if not is_logged_in() or not is_admin():
        flash('Only admins can update parts', 'error')
        return redirect(url_for('auth.login'))
    
    part = PartRepository.get_by_id(part_id)
    if not part:
        flash('Part not found', 'error')
        return redirect(url_for('parts.list'))
    
    if request.method == 'POST':
        part_no = request.form['part_no']
        part_desc = request.form['part_desc']
        
        try:
            PartRepository.update(part_id, part_no, part_desc)
            flash('Part updated successfully!', 'success')
            return redirect(url_for('parts.list'))
        except Exception as e:
            flash(f'Error updating part: {str(e)}', 'error')
    
    return render_template('update_part.html', part=part)


@parts_bp.route('/delete/<int:part_id>', methods=['POST'])
def delete(part_id):
    if not is_logged_in() or not is_admin():
        flash('Only admins can delete parts', 'error')
        return redirect(url_for('parts.list'))
    
    if PartRepository.delete(part_id):
        flash('Part deleted successfully!', 'success')
    else:
        flash('Error deleting part', 'error')
    
    return redirect(url_for('parts.list'))
