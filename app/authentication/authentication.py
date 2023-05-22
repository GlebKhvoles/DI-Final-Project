from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.authentication.forms import LoginForm, SignupForm
from app import db
from app.models import User
from app.authentication import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('templates.stocks'))
    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('templates.stocks'))

    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists.')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)
