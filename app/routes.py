from pip import main
from .import bp as auth 
from .forms import RegisterForm, LoginForm, EditProfileForm
from app.models import User
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import login_user, current_user, logout_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = request.form.get('email').lower()
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash("You have successfully logged in. Welcome!", 'primary')
            return redirect(url_for('homepage.index')) 
        flash('Invalid Email and/or Password', 'danger')         
        return render_template('login.html.j2', form=form,)

    return render_template('login.html.j2',form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash('There was an unexpected Error creating your Account. Please Try Again', 'warning')
            return render_template('register.html.j2', form=form)
        flash('You have registered successfully', 'danger')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html.j2', form = form)

@auth.route('/user_profile', methods=['GET','POST'])
def user_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "first_name":form.first_name.data.title(),
            "last_name":form.last_name.data.title(),
            "email":form.email.data.lower(),
            "password":form.password.data
        }
        user_email = User.query.filter_by(email = form.email.data.lower()).first()
        if user_email and user_email.email != current_user.email:
            flash('Email already in use','warning')
            return redirect(url_for('auth.user_profile'))
        else:
            try:
                current_user.from_dict(new_user_data)
                current_user.save()
                flash('Profile Updated', 'success')
            except: 
                flash('There was an unexpected Error. Please Try Again', 'warning')
                return redirect(url_for('auth.user_profile'))
        return redirect(url_for('homepage.index'))
    return render_template('user_profile.html.j2', form=form)

    from .import bp as homepage 
from .forms import PokeSearch
from app.models import PokeParty, PokeUserJoin
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import  login_required, current_user

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/party', methods=['GET', 'POST'])
@login_required
def party():
    form = PokeSearch()
    
    if request.method == 'POST' and form.validate_on_submit():
        
        search = request.form.get('search')
        
        url = f"https://pokeapi.co/api/v2/pokemon/{search}"
        response = requests.get(url)
        if response.ok:
            user_pokemon = []               
            poke_dict={
                "name":response.json()['forms'][0]['name'],
                "hp":response.json()['stats'][0]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],                
                "sprite": response.json()['sprites']['front_shiny']
                }
            user_pokemon.append(poke_dict)
            if not PokeParty.exists(poke_dict["name"]):
                new_poke = PokeParty()
                new_poke.from_dict(poke_dict)
                new_poke.save()
        

            user = current_user
            user.add_to_team(PokeParty.exists(poke_dict['name']))

            return render_template('pokepage.html.j2', form=form, pokemon_party = user_pokemon)
        else:
            error_string = "Invalid Selection, please try again."
            return render_template('pokepage.html.j2', form=form, error = error_string)
    return render_template('pokepage.html.j2', form=form)
# battle 
@main.route('/pokeparty', methods=['GET'])
@login_required
def pokeparty():
    team = current_user.team
    return render_template('pokeparty.html.j2', team = team)

@main.route('/remove/<int:id>')
@login_required
def remove(id):
    poke = []
    poke = PokeUserJoin.query.get((id, current_user.id))
    poke.remove()
    flash('You said your goodbyes and released this pokemon back into the wild.', 'success')
    return redirect(url_for('homepage.pokeparty'))