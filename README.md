

## Database
I designed a relational schema (Postgres) and created a one-to-many relationship between the Product and Review tables. One product can have many reviews.

SQLAlchemy is used as the ORM.

I used the same schema for both the MVP and V2.

My initial idea was to create two separate Review tables (i.e.`ReviewMVP` and `ReviewV2`) so that the MVP reviews would be restricted to integers, and the V2 reviews would be floats.

But to limit the overhead, I decided to handle this logic in the XXX route and use the same db for both the MVP and V2. 

I figured a float could be used to represent whole numbers, but an integer couldn't be used to represent decimals.
