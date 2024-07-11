from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

class Base(DeclarativeBase):
  pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    img_url = URLField('Cafe Photo(URL)', validators=[DataRequired()])
    map_url = URLField('Cafe location on google map(URL)', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    socket = StringField('Has Socket(True/False)', validators=[DataRequired()])
    wifi = StringField('Wifi Rating(True/False)', validators=[DataRequired()])
    toilet = StringField('Has Toilet(True/False)', validators=[DataRequired()])
    call_take = StringField('Can Call Take(True/False)', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[float] = mapped_column(String(500), nullable=False)
    location: Mapped[float] = mapped_column(String, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[float] = mapped_column(String, nullable=False)
    coffee_price: Mapped[float] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<Book {self.name}>'
    
with app.app_context():
    db.create_all()

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = Cafe(
            name = form.data['cafe_name'],
            map_url = form.data['map_url'],
            img_url = form.data['img_url'],
            location = form.data['location'],
            has_sockets = bool(form.data['socket']),
            has_toilet = bool(form.data['toilet']),
            has_wifi = bool(form.data['wifi']),
            can_take_calls = bool(form.data['call_take']),
            seats = form.data['seats'],
            coffee_price = form.data['coffee_price'],
        )
        db.session.add(cafe)
        db.session.commit()
        return redirect('/add')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    return render_template('cafes.html', cafes=all_cafes)

if __name__ == '__main__':
    app.run(debug=True)

# <div class="row my-3">
#     <div class="col-xxl-3 d-flex justify-content-center">
#       <img src="{{cafe.img_url}}" height="150px" width="250px" alt="">
#     </div>
#     <div class="col-xxl-9">
#       <h4>{{ cafe.name }}</h4>
#       <p><img class="me-2" src="/static/img/logo.jpg" height="20px" width="20px" alt="">{{ cafe.location }}</p>
#       <a href="{{ cafe.map_url }}"><img class="me-2" src="/static/img/map.png" height="20px" width="20px" alt="">{{ cafe.map_url[:50] }}.....</a>
#     </div>
#   </div>
