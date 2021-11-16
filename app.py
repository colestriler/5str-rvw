import os
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('GUMROAD_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('GUMROAD_DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/')
def render_mvp():
    """
    Called by MVP and renders the front-end template for the MVP
    with relevant product and review data.
    """
    product = Product.query.filter_by(id=1).first()
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.date.desc()).all()
    average = get_review_average(product, 0)
    session['product_id'] = product.id
    return render_template("reviews.html", product=product, average=average, reviews=reviews)

@app.route('/create-review', methods=['GET', 'POST'])
def create_review_mvp():
    """
    Called by MVP to create a new review and re-renders
    the page with the updated list of reviews.
    """
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

@app.route('/V2/reviews', methods=['GET', 'POST'])
def get_reviews_v2():
    """
    Called by V2.

    Returns a list of reviews for a specific product.
    """
    product = Product.query.filter_by(id=1).first()
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.date.desc()).all()
    return jsonify(reviews)

@app.route('/V2/product', methods=['GET', 'POST'])
def get_product_v2():
    """
    Called by V2 to fetch product data.
    Returns:
        - JSON: product data
    """
    product = Product.query.filter_by(id=1).first()
    response = {
        "id": product.id,
        "product_name" : product.name,
        "average": get_review_average(product, 1)
    }
    return jsonify(response)

def get_review_average(product, decimal_points):
    """
    Calculates a product's average review.
    """
    return round(np.mean([review.rating for review in product.reviews]), decimal_points)

@app.route('/V2/create-review', methods=['GET', 'POST'])
def create_review_v2():
    """
    Called by V2 to create a new review.
    Returns:
        - list of reviews
    """
    rating = request.get_json()['rating']
    description = request.get_json()['description']
    product_id = request.get_json()['product_id']

    review = Review(
        rating=rating,
        description=description,
        product_id=product_id
    )

    db.session.add(review)
    db.session.commit()
    return get_reviews_v2()



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
