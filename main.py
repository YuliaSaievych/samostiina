from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    comment = db.Column(db.Text)
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'  # Замініть на свій URL бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
with app.app_context():
    db.create_all()

class ReviewForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired()])
    comment = TextAreaField('Відгук', validators=[DataRequired()])
    submit = SubmitField('Залишити відгук')
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReviewForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data

        review = Review(name=name, comment=comment)
        db.session.add(review)
        db.session.commit()

        flash('Ваш відгук було збережено!', 'success')
        return redirect(url_for('index'))

    reviews = Review.query.all()

    return render_template('index.html', form=form, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)

