import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('GUMROAD_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('GUMROAD_DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello World!'


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
    product_id: str = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    rating: float = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Review('{self.rating}', '{self.description}')"


if __name__ == '__main__':
    app.run()
