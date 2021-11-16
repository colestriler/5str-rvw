
MVP: https://gumroad-backend.herokuapp.com/

V2: http://gumroad-fe.s3-website-us-east-1.amazonaws.com/

### Important files

- `app.py`: API endpoints & database schema for MVP & V2
- `/templates/reviews.html`: HTML & jQuery for MVP
- `/static/style.css`: CSS for MVP
- `/v2-react-app/src/App.tsx`: front-end code & API fetches for V2

### Tech stack
Flask, jQuery/React, SQLAlchemy, Postgres

Server hosted on Heroku.

React app hosted on S3.

### API Design
The **MVP front-end** is rendered server side and relies on two methods: `render_mvp()` and `create_review_mvp()`. The `render_mvp()` method renders a HTML template along with product & review data. When a new review is created, the jQuery function inside `reviews.html` calls the `create_review_mvp()` endpoint, adds the review to the database, then re-renders the `render_mvp()` method with the updated list of reviews.

The **V2 front-end** makes three fetch calls to the API: `getProduct`, `getReviews`, and `createReview`. These hit the respective `get_product_v2()`, `get_reviews_v2`, and `create_review_v2()` API endpoints. One key thing to note here is that once `create_review_v2()` actually creates the review, it returns a method call to `get_reviews_v2` which updates the React app with the latest list of reviews without needing to refresh the page.

### Database design
I created a one-to-many relationship between the `Product` and `Review` tables. One product can have many reviews.

To interact with the database in Python, I use the SQLAlchemy ORM.

Even though the MVP only supports whole number reviews, I used the same schema for both the MVP and V2 and stored the reviews as floats.

### React front-end
I used yarn to create a new [Create React App](https://create-react-app.dev/docs/getting-started/) using Typescript.

The major libraries I used are: Material UI, Axios, and Formik.

### Reflecting
For the MVP, I mainly focused on functionality and spent very little time on design -- like most MVPs! I did spend a bit more effort styling the V2 app and even made it mobile compatible.

If I were to go back and work on this some more, I'd put more effort into design.

I'd also spend a bit more time thinking about where I can re-use code between the MVP & V2, specifically when it comes to querying review data for a given product. There were some parts of the code which repeated similar logic, and I think there is opportunity to reduce a bit of this.

I did consider using a document database instead of a relational database. I think a document database would be sufficient for this specific app, but my worry would be that it might be harder to scale later on if you ever wanted to access the reviews without querying all the associated product data (or even other types of data that are added in the future). Plus, reviews will almost always be related to some parent object. So I stuck with a relational database.






