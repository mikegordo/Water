from flask import (
    render_template, request, redirect, url_for
)

from water.auth import login_required
from water.db import get_db
from water.views.blueprint import bp


@bp.route('/', methods=('GET',))
@login_required
def index():
    db = get_db()
    pots = db.execute(
        'SELECT * FROM pot p ORDER BY p.id'
    ).fetchall()
    return render_template('water/index.html', pots=pots)


@bp.route('/pots', methods=('GET',))
@login_required
def pots_index():
    db = get_db()
    pots = db.execute(
        'SELECT * FROM pot p ORDER BY p.id'
    ).fetchall()
    return render_template('water/pots.html', pots=pots)


@bp.route('/pots/edit/<int:pot_id>', methods=('GET', 'POST'))
@login_required
def pots_edit(pot_id):
    db = get_db()
    pot = db.execute('SELECT * FROM pot WHERE id = ?', (pot_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        moisture_value = request.form['moisture_value']
        water_value = request.form['water_value']
        db.execute(
            'UPDATE "pot" SET "name" = ?, "description" = ?, '
            '"moisture_value" = ?, "water_value" = ? WHERE id = ?',
            (name, description, moisture_value, water_value, pot_id)
        )
        db.commit()
        return redirect(url_for('water.pots_index'))

    return render_template('water/pots_edit.html', pot=pot)


@bp.route('/pots/delete/<int:pot_id>', methods=('GET', 'POST'))
@login_required
def pots_delete(pot_id):
    db = get_db()
    pot = db.execute('SELECT * FROM pot WHERE id = ?', (pot_id,)).fetchone()

    if request.method == 'POST':
        db.execute(
            'DELETE FROM "pot" WHERE id = ?',
            (pot_id,)
        )
        db.commit()
        return redirect(url_for('water.pots_index'))

    return render_template('water/pots_delete.html', pot=pot)


@bp.route('/pots/create', methods=('GET', 'POST'))
@login_required
def pots_add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        moisture_value = request.form['moisture_value']
        water_value = request.form['water_value']
        db = get_db()
        db.execute(
            'INSERT INTO "pot" ("name", "description", "moisture_value", "water_value") '
            'VALUES (?, ?, ?, ?)',
            (name, description, moisture_value, water_value)
        )
        db.commit()
        pot = db.execute('SELECT id FROM "pot" WHERE name = ?', (name,)).fetchone()
        return redirect(url_for('water.pots_edit', pot_id=pot['id']))

    return render_template('water/pots_create.html')
