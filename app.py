import os
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('GUMROAD_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('GUMROAD_DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/')
def render_mvp():
    product = Product.query.filter_by(id=1).first()
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.date.desc())
    average = round(np.mean([review.rating for review in product.reviews]), 0)
    session['product_id'] = product.id
    return render_template("reviews.html", product=product, average=average, reviews=reviews)

@app.route('/create-review', methods=['GET', 'POST'])
def create_review_mvp():
    star = request.args.get('star', 0, type=float)
    description = request.args.get('description', 0, type=str)

    review = Review (
        rating=star,
        description=description,
        product_id=session["product_id"]
    )

    db.session.add(review)
    db.session.commit()
    return redirect(url_for("render_mvp"))


@dataclass
class Product(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    reviews: list = db.relationship('Review', backref='product', lazy=True)

    def __repr__(self):
        return f"Product('{self.name}')"

@dataclass
class Review(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    date: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id: int = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    rating: float = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Review('{self.rating}', '{self.description}')"


if __name__ == '__main__':
    app.run()
