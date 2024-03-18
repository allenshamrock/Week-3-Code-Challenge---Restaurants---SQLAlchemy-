import sqlite3

class Restaurants:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def restaurant_reviews(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM reviews WHERE restaurant_id= ?", (self.id))
        reviews = cursor.fetchall()
        return reviews

    def customers_reviews(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM customers INNER JOIN reviews ON customer_id = reviews.customer_id WHERE reviews.restaurant_id = ?", (self.id))
        customers = cursor.fetchall()
        return customers

    @classmethod
    def add_restaurant(cls, db_name, name, price):
        if not name or not price:
            print("Restaurant has to has a name and price")
        try:
            cursor = db_name.cursor()
            cursor.execute(
                "INSERT INTO restaurants(name,price) VALUES (?,?)", (name, price))
            db_name.commit()

        except sqlite3.IntegrityError:
            print(f"Restaurant {name} already exists")

    @classmethod
    def fanciest_restaurant(cls,db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM  restaurants WHERE price = (SELECT MAX(price)  FROM restaurants)")
        fanciest_restaurant = cursor.fetchone()
        if fanciest_restaurant:
            id, name, price = fanciest_restaurant
            print(fanciest_restaurant)
            return cls(id, name, price)
        else:
            return None
        
    @classmethod
    def all_reviews(cls,db_name):
            cursor = db_name.cursor()
            cursor.execute('''SELECT restaurants.name AS restaurant,
            customers.first_name || " " || customers.last_name AS full_name,
            reviews.star_rating AS rating
            FROM reviews
            INNER JOIN restaurants ON restaurants.id = reviews.restaurant_id
            INNER JOIN customers ON customers.customer_id = reviews.customer_id ''')
            all_reviews = cursor.fetchall()
            all_reviews_of_a_restaurant = []
            for all_review in all_reviews:
                restaurant, full_name, rating = all_review
                all_reviews_of_a_restaurant.append(f"Review for {restaurant} by {full_name}: {rating} stars.")
            all_review = '\n'.join(all_reviews_of_a_restaurant)
            return all_review

class Customers:
    def __init__(self, id, first_name, last_name):
        self.first_name = first_name,
        self.last_name = last_name
        self.id = id

    def customer_review(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM reviews WHERE customer.id = ?", (self.id))
        reviews = cursor.fetchall()
        return reviews

    def restaurants_reviewed_by_customer(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM restaurants INNER JOIN reviews ON restaurant.id = reviews.restaurant_id WHERE reviews.customer_id = ?", (self.id))
        restaurants = cursor.fetchall()
        for restaurant in restaurants:
            return restaurant

    @classmethod
    def add_customer(cls, db_name, first_name, last_name):
        if not first_name or not last_name:
            print("first_name,last_name are required")
        try:
            cursor = db_name.cursor()
            cursor.execute(
                "INSERT INTO customers(first_name,last_name) VALUES (?,?)", (first_name, last_name))
            db_name.commit()

        except sqlite3.IntegrityError:
            print(f"customer {first_name} {last_name} already exists")

    def full_name(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT first_name || ' ' || last_name AS full_name FROM customers WHERE id = ?", (self.id,))
        full_name = cursor.fetchone()
        return full_name[0] if full_name else None

    def favourite_restaurant(self, db_name):
        cursor = db_name.cursor()
        cursor.execute("""SELECT restaurants, reviews.star_rating FROM restaurants
        INNER JOIN reviews 
        ON restaurants.id = reviews.restaurant_id
        WHERE reviews.star_rating = (SELECT MAX(star_rating) FROM reviews)
        AND
        reviews.customer_id = ?
        """, (self.id,))
        fav_restaurant = cursor.fetchone()
        return fav_restaurant

    def add_customer_review(self, db_name, restaurant_id, customer_id, star_rating):
        if not (restaurant_id and customer_id and star_rating):
            print("All parameters are required for adding a review.")
            return

        cursor = db_name.cursor()
        # Check if the customer has already reviewed the restaurant
        cursor.execute(
            "SELECT * FROM reviews WHERE restaurant_id = ? AND customer_id = ?", (restaurant_id, self.id))
        existing_review = cursor.fetchone()
        if existing_review:
            print(
                f"Customer {self.id} has already reviewed restaurant {restaurant_id}.")
            return

        try:
            cursor.execute("INSERT INTO reviews(restaurant_id, customer_id, star_rating) VALUES (?, ?, ?)",
                           (restaurant_id, self.id, star_rating))
            db_name.commit()
            print("Customer review added successfully")
        except sqlite3.IntegrityError:
            print(f"An error occurred while adding the review.")

    def delete_customer_review(self, db_name, restaurant_id):
        cursor = db_name.cursor()
        cursor.execute(
            "DELETE FROM reviews  WHERE restaurant_id =? AND customer_id=?", (restaurant_id, self.id))
        db_name.commit()
        print("Review deleted")


class Reviews:
    def __init__(self,db_name, star_ratings, customer_id, restaurant_id):
        self.star_ratings = star_ratings
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.db_name = db_name

    def customer(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM customers WHERE customer_id = ?", (self.customer_id))
        customer = cursor.fetchone()
        return customer if customer else None

    def restaurant(self, db_name):
        cursor = db_name.cursor()
        cursor.execute(
            "SELECT * FROM restaurants WHERE restaurant_id =?", (self.restaurant_id))
        restaurant = cursor.fetchone()
        return restaurant if restaurant else None

    def full_review(self):
        cursor = self.db_name.cursor()
        cursor.execute(
            '''SELECT restaurants.name AS restaurant,
            customers.first_name || " " || customers.last_name AS full_name,
            reviews.star_rating AS rating
            FROM reviews
            INNER JOIN restaurants ON restaurants.id = reviews.restaurant_id
            INNER JOIN customers ON customers.customer_id = reviews.customer_id
            '''
        )
        reviews = cursor.fetchall()
        full_reviews = []
        for review in reviews:
            restaurant, full_name, rating = review
            full_reviews.append(f"Review for {restaurant} by {full_name}: {rating} stars.")
        return full_reviews



class RestaurantManagement:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants(
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE,
                       price INTEGER
            )
''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                       customer_id INTEGER PRIMARY KEY,
                       first_name TEXT UNIQUE,
                       last_name TEXT UNIQUE
            )
''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews(
                       id INTEGER PRIMARY KEY,
                       star_rating INTEGER,
                       customer_id INTEGER,
                       restaurant_id INTEGER,
                       FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
                       FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
            )
''')
        self.conn.commit()


    def add_restaurant_review(self, restaurant_id, customer_id, star_rating):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reviews(restaurant_id,customer_id,star_rating) VALUES(?,?,?)",
                       (customer_id, restaurant_id, star_rating))
        self.conn.commit()
        print("Restaurant review added successfully ")

    def get_review_by_id(self, review_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id))
        return cursor.fetchone()


if __name__ == '__main__':

    management = RestaurantManagement("restaurant_manager.db")
    # Add customers
    Customers.add_customer(management.conn, "Allen", "Shamrock")
    Customers.add_customer(management.conn, "Anne", "Irungu")
    Customers.add_customer(management.conn, "Brian", "Kiprono")
    Customers.add_customer(management.conn, "Leonard", "Omusula")

    Customers.add_customer(management.conn, "Leonard", "Omusula")
    # Add restaurant
    Restaurants.add_restaurant(management.conn, "Canopy cafe", 2000)
    Restaurants.add_restaurant(management.conn, "About thyme", 3000)
    Restaurants.add_restaurant(management.conn, "Red ginger", 4000)
    Restaurants.add_restaurant(management.conn, "Baobox", 8000)

    # Add review
    customer1 = Customers(1, "Allen", "Shamrock")
    customer2 = Customers(2, "Leonard", "Omusula")
    customer3 = Customers(3, "Brian", "Kiprono")
    customer4 = Customers(4, "Anne", "Irungu")
    customer1.add_customer_review(management.conn, 1, 1, 3)
    customer2.add_customer_review(management.conn, 2, 2, 4)
    customer3.add_customer_review(management.conn, 3, 1, 5)
    customer4.add_customer_review(management.conn, 4, 1, 2.5)
    # Delete review
    customer1 = Customers(1, "Allen", "Shamrock")
    customer1.delete_customer_review(management.conn, 1)

    # full review
    star_ratings = [
        {"customer_id": 1, "restaurant_id": 1, "rating": 4},
        {"customer_id": 2, "restaurant_id": 2, "rating": 5},
        {"customer_id": 3, "restaurant_id": 1, "rating": 3},
    ]
    for rating in star_ratings:
        customer_id = rating["customer_id"]
        restaurant_id = rating["restaurant_id"]
        star_rating = rating["rating"]
        customer = Customers(customer_id, "", "")
        customer.add_customer_review(management.conn, restaurant_id, customer_id, star_rating)

    # Fetch and print full reviews
    full_review = Reviews(management.conn, star_ratings, customer_id, restaurant_id)
    reviews_list = full_review.full_review()
    for review in reviews_list:
        print(review)
    
    # Fancy restaurant
    fanciest_restaurant = Restaurants.fanciest_restaurant(management.conn)
    if fanciest_restaurant:
        print(f"The fanciest restaurant is: {fanciest_restaurant.name}")
    else:
        print("No restaurants found.")

        # All review of a restaurant
    all_review = Restaurants.all_reviews(management.conn)
    print(all_review)

