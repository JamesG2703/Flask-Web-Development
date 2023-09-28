from market import app
from flask import render_template, redirect, url_for, flash, request, make_response
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, ItemForm
from market import db
from flask_login import login_user, logout_user, login_required
from datetime import datetime
import json
import requests

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/graphs')
@login_required
def graph_page():
    # Market price of categories overall graph
    category_price = db.session.query(db.func.sum(Item.price), Item.category).group_by(Item.category).order_by(Item.category).all()
    # Overall market share price status by date
    price_status = db.session.query(db.func.sum(Item.price), Item.date).group_by(Item.date).order_by(Item.date).all()

    category_income = []
    for total_amount, _ in category_price:
        category_income.append(total_amount)

    price_over_time = []
    dates_labels=[]
    for price, date in price_status:
        price_over_time.append(price)
        dates_labels.append(date.strftime("%m-%d-%Y"))

    return render_template('graphs.html', 
    category_price = json.dumps(category_income),
    price_over_time = json.dumps(price_over_time),
    dates_labels = json.dumps(dates_labels))

@app.route('/live_graphs')
@login_required
def live_graph_page():
    return render_template('live_graphs.html')

@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    payload = {}
    headers = {}
    url = "https://demo-live-data.highcharts.com/aapl-ohlcv.json"
    r = requests.get(url, headers=headers, data ={})
    r = r.json()
    return {"res":r}

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Item.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f"You have now successfully created the item {item_to_delete.name}!", category='success')
        return redirect(url_for('market_page'))
    except:
        return 'There was a problem deleting that task'

@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item_to_edit = Item.query.get_or_404(id)

    if request.method == 'POST':
        item_to_edit.name = request.form['name']
        item_to_edit.country_appeal_rate = request.form['country_appeal_rate']
        item_to_edit.category = request.form['category']
        item_to_edit.price = request.form['price']
        item_to_edit.barcode = request.form['barcode']
        item_to_edit.description = request.form['description']

        try:
            db.session.commit()
            flash(f"You have now successfully updated the item {item_to_edit.name}!", category='success')
            return redirect(url_for('market_page'))
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('edit_item.html', item=item_to_edit)

@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    form = ItemForm()
    if form.validate_on_submit():
        item_to_create = Item(name=form.name.data,
                              country_appeal_rate=form.country_appeal_rate.data,
                              category=form.category.data,
                              price=form.price.data,
                              barcode=form.barcode.data,
                              description=form.description.data)
        db.session.add(item_to_create)
        db.session.commit()
        flash(f"You have now successfully created the item {item_to_create.name}!", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an item: {err_msg}', category='danger')

    return render_template('create_item.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user_login = User.query.filter_by(username=form.username.data).first()
        if attempted_user_login and attempted_user_login.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user_login)
            flash(f'Success! You are logged in as: {attempted_user_login.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))