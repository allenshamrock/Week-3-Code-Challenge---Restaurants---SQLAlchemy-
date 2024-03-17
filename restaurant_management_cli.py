import sqlite3

class Restaurants:
    def __init__(self,id,name,price):
        self.id = id
        self.name = name
        self.price = price

    def restaurant_reviews(self,db_name):
        cursor = db_name.cursor()
        cursor.execute("SELECT * FROM reviews WHERE restaurant_id= ?",(self.id))
        reviews = cursor.fetchall()
        return reviews
    
    def customers_reviews(self,db_name):
        cursor = db_name.cursor()
        cursor.execute("SELECT * FROM customers INNER JOIN reviews ON customer_id = reviews.customer_id WHERE reviews.restaurant_id = ?",(self.id))
        customers =  cursor.fetchall()
        return customers
    @classmethod
    def add_restaurant(cls,db_name,name,price):
        cursor = db_name.cursor()
        cursor.execute("INSERT INTO restaurants(name,price) VALUES (?,?)",(name,price))
        db_name.commit()

class Customers:
    def __init__(self,id, first_name, last_name):
        self.first_name = first_name,
        self.last_name = last_name
        self.id = id
    
    def customer_review(self,db_name):
        cursor = db_name.cursor()
        cursor.execute("SELECT * FROM reviews WHERE customer.id = ?",(self.id))
        reviews = cursor.fetchall()
        return reviews
    
    def restaurants_reviewed_by_customer(self,db_name):
        cursor = db_name.cursor()
        cursor.execute("SELECT * FROM restaurants INNER JOIN reviews ON restaurant.id = reviews.restaurant_id WHERE reviews.customer_id = ?",(self.id))
        restaurants = cursor.fetchall()
        return restaurants 
    
    @classmethod
    def add_customer(cls,db_name,first_name,last_name):
        cursor = db_name.cursor()
        cursor.execute("INSERT INTO customers(first_name,last_name) VALUES (?,?)",(first_name,last_name))
        db_name.commit()

class Reviews:
    def __init__(self,star_ratings,customer_id,restaurant_id):
        self.star_ratings = star_ratings
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id

    
    def customer(self,db_name):
        cursor = db_name.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = ?",(self.customer_id))
        customer = cursor.fetchone()
        return customer if customer else None
    
    def restaurant(self,db_name):
        cursor = db_name.cursor()
        cursor.execute("SELECT * FROM restaurants WHERE restaurant_id =?",(self.restaurant_id))
        restaurant = cursor.fetchone()
        return restaurant if restaurant else None

class RestaurantManagement:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants(
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       price INTEGER
            )
''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                       customer_id INTEGER PRIMARY KEY,
                       first_name TEXT,
                       last_name TEXT
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

  
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants(
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       price INTEGER
            )
''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                       customer_id INTEGER,
                       first_name TEXT,
                       last_name TEXT
            )
''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews(
                       id INTEGER PRIMARY KEY,
                       star_rating INTEGER,
                       customer_id INTEGER,
                       restaurant_id INTEGER,
                       FOREIGN KEY(customer_id) REFERENCES customers(id),
                       FOREIGN KEY(retaurant_id) REFERENCES restaurants(id)
            )
''')
        self.conn.commit()

    def add_restaurant_review(self,restaurant_id, customer_id, star_rating):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reviews(restaurant_id,customer_id,star_rating) VALUES(?,?,?)", (customer_id,restaurant_id,star_rating))
        self.conn.commit()
        print("Restaurant review added successfully ")

       
    def add_customer_review(self,restaurant_id,customer_id,star_rating):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reviews(restaurant_id,customer_id,star_rating) VALUES (?,?,?)",(restaurant_id,customer_id,star_rating))
        self.conn.commit()
        print("Customer review added succesfully")
    

    def get_review_by_id(self,review_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reviews WHERE id = ?",(review_id))
        return cursor.fetchone()
    

if __name__ == '__main__':
   
    # restaurant1 = Restaurants(1, "Canopy cafe", 2)
    # restaurant2 = Restaurants(2, "About thyme", 3)

    # customer1 = Customers(1, "Allen", "Shamrock")
    # customer2 = Customers(2, "Leonard", "Omusula")

    # review1 = Reviews(5, 1, 1)  
    # review2 = Reviews(4, 2, 2)  

   
    management = RestaurantManagement("restaurant_manager.db")

    # Add restaurants
    # management.add_restaurant_review(restaurant1.id, customer1.id, review1.star_ratings)
    # management.add_restaurant_review(restaurant2.id, customer2.id, review2.star_ratings)

    # Add customers

    Customers.add_customer(management.conn, "Allen", "Shamrock")
    Customers.add_customer(management.conn, "Leonard", "Omusula")
    Restaurants.add_restaurant(management.conn,"Canopy cafe", 2)
    Restaurants.add_restaurant(management.conn,"About thyme", 3)
    management.add_customer_review(1, 1, 5)
    management.add_customer_review(2, 2, 4)
   
