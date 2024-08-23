from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email, send_simple_message
from . import main
from .forms import NameForm



@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    user_all = User.query.all();
    role_all = Role.query.all();
    print(user_all);
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()                        
        if user is None:
            user_role = Role.query.filter_by(name=form.role.data).first();
            user = User(username=form.name.data, role=user_role);
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False),
                           user_all=user_all, role_all = role_all);
