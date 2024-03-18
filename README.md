Setup

To run this project, follow these steps:

Set up a virtual environment (optional but recommended):


python3 -m venv venv
source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt


Create a database and set up the tables by running the SQL script provided.

Populate the tables with sample data using the main.py script.

Database Schema

The database schema consists of the following tables:

Restaurants

id (Primary Key)
name (String)
price (Integer)
Customers
id (Primary Key)
first_name (String)
last_name (String)

Reviews

id (Primary Key)
restaurant_id (Foreign Key referencing Restaurants.id)
customer_id (Foreign Key referencing Customers.id)
star_rating (Integer
)
Object Relationship Methods

Review

.customer(): Returns the Customer instance for this review.
.restaurant(): Returns the Restaurant instance for this review.
Restaurant
reviews(): Returns a collection of all the reviews for the restaurant.
.customers(): Returns a collection of all the customers who reviewed the restaurant.
Customer
.reviews(): Returns a collection of all the reviews that the customer has left.
restaurants(): Returns a collection of all the restaurants that the customer has reviewed.
Aggregate and Relationship Methods

Customer

.full_name(): Returns the full name of the customer, with the first name and last name concatenated.
.favorite_restaurant(): Returns the restaurant instance that has the highest star rating from this customer.
add_review(restaurant, rating): Adds a new review for the restaurant with the given rating.
delete_reviews(restaurant): Removes all reviews for the specified restaurant.
Review
f.ull_review(): Returns a string formatted as "Review for {restaurant name} by {customer's full name}: {review star rating} stars."

Restaurant

.fanciest() (class method): Returns one restaurant instance with the highest price.
.all_reviews(): Returns a list of strings with all the reviews for this restaurant formatted as specified.