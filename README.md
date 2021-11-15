
MVP: https://gumroad-backend.herokuapp.com/

### How to navigate

- `app.py` contains the MVP & V2 API and the database schema
- `/templates/reviews.html` contains the html & jQuery for the MVP
- `/static/style.css` contains some simple CSS for the MVP's html


### Database
I set up a Postgres database and created a one-to-many relationship between the Product and Review tables. One product can have many reviews.

To interact with the database in Python, I use the SQLAlchemy ORM.

Even though the MVP only supports whole integer reviews, I used the same schema for both the MVP and V2 and stored the reviews as floats.

I figured a float could be used to represent both whole numbers and decimals. I also considered storing the reviews the same way Stripe stores dollar amounts where $5.00 is represented as the integer 500. But to avoid having to write extra logic to convert these integers to decimals later, I decided this was too much work for such a simple task.


