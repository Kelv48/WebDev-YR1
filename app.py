from flask import Flask, session, render_template, redirect, url_for, g, request
from flask_session import Session
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SearchForm, RegistrationForm, LoginForm, Emp_ManagementForm, Product_ManagementForm, New_ProductForm, New_EmployeeForm, New_ServiceForm, AccountForm, ReviewForm
from forms import SupportForm, BlogForm, ResearchForm, ProfileForm
from functools import wraps
from random import randint


# user_id = admin
# password = admin1

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "i-am-a-secret"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login_status", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/", methods=["GET", "POST"])            #Index page and the location of the search function
def index():
    search_form = SearchForm()
    user = g.user
    profile_info = None
    # Runs the search function anytime it is validated on any page
    if search_form.validate_on_submit():
        search = search_form.search.data
        search = search.lower()
        search = '%' + search + '%'
        db = get_db()
        products = db.execute("""SELECT * FROM products WHERE name like ?;""", (search,)).fetchall()
        services = db.execute("""SELECT * FROM services WHERE name like ?;""", (search,)).fetchall()
        return render_template("products.html", products=products, search_form=search_form, services=services)
    else:
        # The id's for the db products and services
        choices = [12, 10, 54, 32, 1, 2, 7, 100, 20, 30, 34, 19, 3, 4, 5, 99, 88,
        60, 61, 62, 63, 64, 65, 66]
        # Picks a random id from the list
        memory = []
        pick = choices[randint(0, 23)]
        products = []
        db = get_db()
        profile_info = db.execute("""SELECT * FROM profile WHERE user_id = ?;""",(user,)).fetchone()
        if profile_info is not None:
            profile_info = profile_info
        else:
            profile_info = None
        #Saves the pick to memory to try ensure no duplicates 
        memory.append(pick)
        #Ensures that only 3 products will be chosen
        while len(products) < 3:            #This is for a randomized catalog on home page loading which allows you to go directly to
                                            #random pages
            product = db.execute("""SELECT * FROM products WHERE product_id = ?;""", (pick,)).fetchone()
            service = db.execute("""SELECT * FROM services WHERE product_id = ?;""", (pick,)).fetchone()
            if product is not None:
                new_pick = choices[randint(0, 23)]  #Picking a new item and comparing with the previous item
                while new_pick in memory:             #Changes the pick if ite in memory
                    new_pick = choices[randint(0, 23)]  
                pick = new_pick
                products.append(product)               #appends the dict product to the list products
            else:
                new_pick = choices[randint(0, 23)]      #The same as above but for services
                while new_pick == pick:         
                    new_pick = choices[randint(0, 23)]
                pick = new_pick
                products.append(service)
        return render_template("index.html", search_form=search_form, products=products, profile_info=profile_info)


@app.route("/catalog")              
def catalog():
    db = get_db()
    #Gets everything from products and services and displays all of it
    products = db.execute("""SELECT * FROM products;""").fetchall()
    services = db.execute("""SELECT * FROM services;""").fetchall()
    search_form = SearchForm()
    return render_template("catalog.html", products=products, search_form=search_form, services=services)

@app.route("/product_catalog")  
def product_catalog():
    #Gets all products and displays them
    db = get_db()
    products = db.execute("""SELECT * FROM products;""").fetchall()
    search_form = SearchForm()
    return render_template("catalog.html", products=products, search_form=search_form)

@app.route("/service_catalog")    
def service_catalog():
    #Gets all services and displays them
    db = get_db()
    services = db.execute("""SELECT * FROM services;""").fetchall()
    search_form = SearchForm()
    return render_template("catalog.html", services=services, search_form=search_form)
    

@app.route("/login_status", methods=["GET","POST"])     
def login_status():
    password=None
    search_form = SearchForm()
    register_form = RegistrationForm()
    login_form = LoginForm()
    #This is for login/registering
    if login_form.validate_on_submit():
        user_id = login_form.user_id.data
        password = login_form.password.data
        db = get_db()
        user_id_check = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?;""", (user_id,)).fetchone()
        if user_id_check is None:
            login_form.user_id.errors.append("No such user!")
        elif not check_password_hash(user_id_check["password"], password):
            login_form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                 next_page = url_for("index")
            return redirect(next_page)
    if register_form.validate_on_submit():
        user_id = register_form.user_id.data
        password = register_form.password.data
        password2 = register_form.password2.data
        db = get_db()
        user_id_check = db.execute("""SELECT * FROM users
                                      WHERE user_id =?;""", (user_id,)).fetchone()
        if user_id_check is not None:
            register_form.user_id.errors.append("User id is already taken, please try another!")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                          VALUES (?, ?);""",
                          (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login_status"))
    return render_template("sign_in_status.html", register_form=register_form, login_form=login_form, search_form=search_form)  


@app.route("/admin", methods=["GET", "POST"])               #The login for admin is user_id = admin
@login_required                                                                    #password = admin1
def admin():
    #If you are not admin send you back to index this check is in all admin routes
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    return render_template("admin.html", search_form=search_form)


@app.route("/logout")       #Logs out the user
def logout():
    session.clear()
    return redirect( url_for("index") )

@app.route("/modify_login", methods=["GET", "POST"])
@login_required
def modify():
    #Allows standard users not admin to change their user_id
    account_form = AccountForm()
    search_form = SearchForm()
    user = g.user
    #Fetches the user_id and checks if its admin
    #If it is the admin is redirected to index
    if user == "admin":
        return redirect(url_for ("index"))
    #Else it gets the db and displays a form
    db = get_db()
    if account_form.validate_on_submit():
        #Takes the users new id for checking
        new_id = account_form.new_user_id.data
        #Checks if the id already exists
        user_id_check = db.execute("""SELECT * FROM users
                                      WHERE user_id =?;""", (new_id,)).fetchone()
        #If the id is admin produce an error                             
        if new_id == "admin":
            account_form.new_user_id.errors.append("It is not possible to choose this name")
        #If the id is same as last produce error
        elif new_id == user:
            account_form.new_user_id.errors.append("Your new user_id cannot be the same as your current id")
        #If id is already taken produce an error
        elif user_id_check is not None:
            account_form.new_user_id.errors.append("User id is already taken, please try another!")
        #Else update the id and redirect to index
        else:
            g.user = new_id
            db.execute("""UPDATE users set user_id = ? WHERE user_id = ?;""", (new_id, user))
            db.execute("""UPDATE profile set user_id = ? WHERE user_id = ?;""", (new_id, user))
            db.commit()
            return render_template("index.html", search_form=search_form)
    return render_template("myaccount.html", account_form=account_form, search_form=search_form)

@app.route("/my_profile_setup", methods=["GET", "POST"])
@login_required
def my_profile_setup():
    search_form = SearchForm()
    profile_form = ProfileForm()
    db = get_db()
    user = g.user
    if user == "admin":
        return redirect(url_for ("index"))
    if profile_form.validate_on_submit():
        nickname = profile_form.nickname.data
        age = profile_form.age.data
        bio = profile_form.bio.data
        #Sets up the users profile
        db.execute("""INSERT INTO profile (user_id, nickname, age, bio)
                          VALUES (?, ?, ?, ?);""",
                          (user, nickname, age, bio))
        db.commit()
        return redirect( url_for("index"))
    return render_template("my_profile_setup.html", search_form=search_form, profile_form=profile_form)

@app.route("/my_profile", methods=["GET", "POST"])
@login_required
def my_profile():
    search_form = SearchForm()
    suggestion_2 = None
    suggestion_1 = None
    db = get_db()
    user = g.user
    if user == "admin":
        return redirect(url_for ("index"))
    #Gets info relating to the users profile including reviews, wishlist and cart
    profile = db.execute("""SELECT * FROM profile WHERE user_id = ?;""", (user,)).fetchone()
    reviews = db.execute("""SELECT * FROM reviews WHERE user_id = ?;""", (user,)).fetchall()
    cart = db.execute("""SELECT * FROM cart WHERE user_id = ?;""", (user,)).fetchall()
    wishlist = db.execute("""SELECT * FROM wishlist WHERE user_id = ?;""", (user,)).fetchall()
    choices = [12, 10, 54, 32, 1, 2, 7, 100, 20, 30, 34, 19, 3, 4, 5, 99, 88,
        60, 61, 62, 63, 64, 65, 66]
    # Picks a random id from the list
    memory = []
    pick = choices[randint(0, 23)]
    products = []
    db = get_db()
    memory.append(pick)
    #Ensures that only 3 products will be chosen
    while len(products) < 4:            #This is for a randomized catalog on home page loading which allows you to go directly to
                                            #random pages
        product = db.execute("""SELECT * FROM products WHERE product_id = ?;""", (pick,)).fetchone()
        service = db.execute("""SELECT * FROM services WHERE product_id = ?;""", (pick,)).fetchone()
        if product is not None:
            new_pick = choices[randint(0, 23)]  #Picking a new item and comparing with the previous item
            while new_pick in memory:             #Changes the pick if ite in memory
                new_pick = choices[randint(0, 23)]  
            pick = new_pick
            suggestion_1 = product
            products.append(product)               #appends the dict product to the list products
        else:
            new_pick = choices[randint(0, 23)]      #The same as above but for services
            while new_pick == pick:         
                new_pick = choices[randint(0, 23)]
            pick = new_pick
            suggestion_2 = service
            products.append(service)
    #Picks the same item twice if the other is none
    if suggestion_2 == None:
        suggestion_2 = product
    if suggestion_1 == None:
        suggestion_1 = service
    return render_template("my_profile.html", search_form=search_form, profile=profile, reviews=reviews,
    cart=cart, wishlist=wishlist, suggestion_1=suggestion_1, suggestion_2=suggestion_2)

@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    search_form = SearchForm()
    profile_form = ProfileForm()
    db = get_db()
    user = g.user
    if user == "admin":
        return redirect(url_for ("index"))
    if profile_form.validate_on_submit():
        nickname = profile_form.nickname.data
        age = profile_form.age.data
        bio = profile_form.bio.data
        #Takes in new info from the form and allows the user to update their profile
        db.execute("""UPDATE profile set user_id = ?, nickname = ?, age = ?, bio = ? 
        WHERE user_id = ?;""",(user, nickname, age, bio, user))
        db.commit()
        return redirect( url_for("my_profile"))
    return render_template("my_profile_setup.html", search_form=search_form, profile_form=profile_form)


@app.route("/product/<int:product_id>")     #This page shows individual products/services after clicking on them
def product(product_id):
    service = None
    cart = None
    wishlist = None
    review_form = ReviewForm()
    search_form = SearchForm()
    db = get_db()
    #Checks if its a product or service using the id
    product = db.execute("""SELECT * FROM products
                         WHERE product_id = ?;""", (product_id,)).fetchone()
    service = db.execute("""SELECT * FROM services
                         WHERE product_id =?;""", (product_id,)).fetchone()
    
    #checking for reviews and calculating the rating when loading a product
    reviews = db.execute("""SELECT * FROM reviews WHERE product_id = ?;""", (product_id,)).fetchall()
    scores = db.execute("""SELECT SUM(score) FROM reviews WHERE product_id = ?;""", (product_id,)).fetchone()
    count = db.execute("""SELECT COUNT(review) FROM reviews WHERE product_id = ?;""", (product_id,)).fetchone()
    scores = scores["SUM(score)"]
    count = count["COUNT(review)"]
    #Ensuring the it doesn't attempt to divide nothing and produce an error
    if scores != None and count != None:
        score = scores // count
    else:
        score = 0
    #checking if the product is already in the users cart/wishlist
    if g.user is not None:
        user = g.user
        cart = db.execute("""SELECT * FROM cart WHERE product_id = ? and user_id = ?;""", (product_id, user)).fetchone() 
        wishlist = db.execute("""SELECT * FROM wishlist WHERE product_id = ? and user_id = ?;""", (product_id, user)).fetchone()
        return render_template("products.html", product=product, search_form=search_form, 
            service=service, review_form=review_form, reviews=reviews, score=score, cart=cart, wishlist=wishlist)   
    else:   
        return render_template("products.html", product=product, search_form=search_form, 
    service=service, review_form=review_form, reviews=reviews, score=score, cart=cart, wishlist=wishlist)


@app.route("/review/<int:product_id>", methods=["GET", "POST"])
@login_required
def review(product_id):
    user = g.user
    review_form = ReviewForm()
    db = get_db()
    if review_form.validate_on_submit():
        #If the user enters a review takes the info from it inserts it to the db and redirects to the product page
        review = review_form.review.data
        score = review_form.score.data
        db.execute("""INSERT INTO reviews (user_id, product_id, review, score)
                      VALUES (?, ?, ?, ?);""",
                      (user, product_id, review, score))
        db.commit()
    return redirect( url_for('product', product_id=product_id))


#Admin settings relating to products
@app.route("/catalog_management")           
@login_required
def catalog_management():
    if g.user != "admin":
        return redirect( url_for("index"))
    db = get_db()
    #Shows a catalog that when you go into the product/service pages gives admin choices update/delete
    products = db.execute("""SELECT * FROM products;""").fetchall()
    services = db.execute("""SELECT * FROM services;""").fetchall()
    search_form = SearchForm()
    return render_template("catalog_management.html", products=products, search_form=search_form, services=services)

@app.route("/product_management/<int:product_id>")
@login_required
def product_management(product_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    db = get_db()
    #Displays a page that allows the admin to edit a product/service
    product = db.execute("""SELECT * FROM products
                         WHERE product_id = ?;""", (product_id,)).fetchone()
    service = db.execute("""SELECT * FROM services
                         WHERE product_id =?;""", (product_id,)).fetchone()
    return render_template("product_management.html", product=product, search_form=search_form, service=service)

@app.route("/update_product/<int:product_id>", methods=["GET", "POST"])     #This updates product/service information in the database
@login_required
def update_product(product_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    product_form = Product_ManagementForm()
    #Produces a form that allows the admin to update the details of the chosen product
    if product_form.validate_on_submit():
        new_price = product_form.price.data
        new_description = product_form.description.data
        db = get_db()
        #Updates the database at the current id
        db.execute("""UPDATE products SET price = ? WHERE product_id = ?;""", (new_price, product_id))
        db.execute("""UPDATE products SET description = ? WHERE product_id = ?;""", (new_description, product_id))

        db.execute("""UPDATE services SET price = ? WHERE product_id = ?;""", (new_price, product_id))
        db.execute("""UPDATE services SET description = ? WHERE product_id = ?;""", (new_description, product_id))

        db.commit()
        #Takes you back to the catalog upon completion
        return redirect( url_for('product_management', product_id=product_id, search_form=search_form))
    return render_template("product_update.html", search_form=search_form, product_form=product_form)

@app.route("/delete_product/<int:product_id>")                                
@login_required
def delete_product(product_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    db = get_db()
    #This deletes product/service information in the database
    db.execute("""DELETE FROM products WHERE product_id = ?;""", (product_id,))
    db.execute("""DELETE FROM services WHERE product_id = ?;""", (product_id,))
    db.commit()
    return redirect( url_for('catalog_management', search_form=search_form))

@app.route("/new_product", methods=["GET", "POST"])
@login_required
def new_product():
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    new_product_form = New_ProductForm()
    #Allows the admin to add new products to the DB
    if new_product_form.validate_on_submit():
        price = new_product_form.price.data
        description = new_product_form.description.data
        stock = new_product_form.stock.data
        name = new_product_form.name.data
        image = 'static/images/placeholder.png'
        db = get_db()
        db.execute("""INSERT INTO products (price, description, stock, name, img)
                      VALUES (?, ?, ?, ?, ?);""",
                      (price, description, stock, name, image))
        db.commit()
        return redirect( url_for('catalog_management'))
    return render_template("product_new.html", search_form=search_form, new_product_form=new_product_form)

@app.route("/new_service", methods=["GET", "POST"])
@login_required
def new_service():
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    new_service_form = New_ServiceForm()
    #Allows the admin to add new services to the DB
    if new_service_form.validate_on_submit():
        price = new_service_form.price.data
        description = new_service_form.description.data
        name = new_service_form.name.data
        image = 'static/images/placeholder.png'
        db = get_db()
        db.execute("""INSERT INTO services (price, description, name, img)
                      VALUES (?, ?, ?, ?);""",
                      (price, description, name, image))
        db.commit()
        return redirect( url_for('catalog_management'))
    return render_template("service_new.html", search_form=search_form, service_form=new_service_form)



@app.route("/cart")        
@login_required
def cart():
    search_form = SearchForm()
    db = get_db()
    user = g.user
    #Displays the cart of the currently signed in user
    products = db.execute("""SELECT * FROM cart WHERE user_id = ?;""", (user,)).fetchall()
    return render_template("cart.html", search_form=search_form, products=products)

@app.route("/wishlist")
@login_required
def wishlist():
    search_form = SearchForm()
    db = get_db()
    user = g.user
    #Displays the wishlist of the currently signed in user
    products = db.execute("""SELECT * FROM wishlist WHERE user_id = ?;""", (user,)).fetchall()
    product = None
    return render_template("wishlist.html", search_form=search_form, products=products, product=product)

@app.route("/add_to_cart/<int:product_id>")     #This adds to cart
@login_required
def add_to_cart(product_id):
    db = get_db()
    user = g.user
    #Allows the user to add to their cart
    #Checks if the item is already in the users cart/wishlist
    info = db.execute("""SELECT quantity FROM cart where product_id = ? and user_id = ?;""", (product_id, user)).fetchone()
    wishlist = db.execute("""SELECT * FROM wishlist WHERE product_id = ? and user_id = ?;""", (product_id, user)).fetchone()
    if wishlist is not None:
        db.execute("""DELETE FROM wishlist WHERE product_id = ? and user_id = ?;""",(product_id, user))
        #If its in their wishlist delete it from there when they add it to their cart
    if info is not None:
        #If the item is already in their cart get the amount of the item
        quantity = info["quantity"]
        quantity = int(quantity)
    cart = db.execute("""SELECT * FROM cart where product_id = ? and user_id = ?;""", (product_id, user)).fetchone()
    #Gets all details at a specific id
    product = db.execute("""SELECT * FROM products
                                WHERE product_id = ?;""", (product_id,)).fetchone()
    service = db.execute("""SELECT * FROM services
                                WHERE product_id = ?;""", (product_id,)).fetchone()
    if product is not None:
        #If its a product
        name = product["name"]
        image = product["img"]
        price = product["price"]
    else:
        #If its a service
        name = service["name"]
        image = service["img"]
        price = service["price"]
    if cart is None:
        #If the item is not already in their cart insert it and set quantity to 1
        db.execute("""INSERT INTO cart (user_id, product_id, quantity, name, price, image)
                      VALUES (?, ?, ?, ?, ?, ?);""", (user, product_id, 1, name, price, image))
        db.commit()
    else:
        #if it is add one to quantity and update the db
        quantity = quantity + 1
        db.execute("""UPDATE cart set quantity = ?, name = ?, price = ?, image = ? WHERE product_id = ? and user_id =?;""", (quantity, name, price, image, product_id, user))
        db.commit()
        #Send them to their cart
    return redirect( url_for("cart"))

@app.route("/add_to_wishlist/<int:product_id>")    
@login_required
def add_to_wishlist(product_id):
    db = get_db()
    user = g.user
    #Gets the details of the product/service
    product = db.execute("""SELECT * FROM products
                                WHERE product_id = ?;""", (product_id,)).fetchone()
    service = db.execute("""SELECT * FROM services
                                WHERE product_id = ?;""", (product_id,)).fetchone()
    if product is not None:
        #If its a product
        name = product["name"]
        image = product["img"]
    else:
        #If its a service
        name = service["name"]
        image = service["img"]
        #Put the item into their wishlist
    db.execute("""INSERT INTO wishlist (user_id, product_id, name, image)
                      VALUES (?, ?, ?, ?);""", (user, product_id, name, image))
    db.commit()
    #Show them their wishlist
    return redirect( url_for("wishlist"))


@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    db = get_db()
    user = g.user
    #Gets the quantity of the item
    info = db.execute("""SELECT quantity FROM cart where product_id = ?;""", (product_id,)).fetchone()
    if info is not None:
        #If its in the cart
        quantity = info["quantity"]
        quantity = int(quantity)
        #Gets the details on products/services
        product = db.execute("""SELECT * FROM products
                                WHERE product_id = ?;""", (product_id,)).fetchone()
        service = db.execute("""SELECT * FROM services
                                WHERE product_id = ?;""", (product_id,)).fetchone()
        if product is not None:
            #If its a product
            name = product["name"]
            image = product["img"]
            price = product["price"]
        else:
            #If its a service
            name = service["name"]
            image = service["img"]
            price = service["price"]
        if quantity > 1:
            #If the quantity is greater than 1
            #Update the db taking 1 from quantity each time
            quantity = quantity - 1
            db.execute("""UPDATE cart set quantity = ?, name = ?, price = ?, image = ? WHERE product_id = ? and user_id =?;""", (quantity, name, price, image, product_id, user))
            db.commit()
            return redirect( url_for("cart"))
        elif quantity == 1:
            #If there is only 1 left remove it from cart
            db.execute("""DELETE FROM cart WHERE product_id = ? and user_id = ?;""", (product_id, user))
            db.commit()
            return redirect( url_for("cart"))

@app.route("/remove_from_wishlist/<int:product_id>")
@login_required
def remove_wishlist(product_id):
    db = get_db()
    user = g.user
    #Deletes the products from the wishlist
    db.execute("""DELETE FROM wishlist WHERE product_id = ? and user_id = ?;""", (product_id, user))
    db.commit()
    return redirect( url_for("wishlist"))

@app.route("/checkout")             #try get new code for cart maybe store the data into a database if you run the route for checkout
@login_required
def checkout():
    search_form = SearchForm()    
    db = get_db()
    data = db.execute("""SELECT * FROM cart;""").fetchall()
    user = g.user
    #Gets the data on all items in the users cart
    for products in data:
        price = products["price"]
        name = products["name"]
        image = products["image"]
        quantity = products["quantity"]
        product_id = products["product_id"]
        #Sums up the price of each item
        item_price = int(price) * int(quantity)
        #Checks if the item is already in checkout
        test = db.execute("""SELECT * FROM checkout WHERE product_id = ?;""", (product_id,)).fetchone()
        if test is None:
            #Inserts the item into checkout
            db.execute("""INSERT INTO checkout (user_id, product_id, quantity, name, price, item_price, image)
                      VALUES (?, ?, ?, ?, ?, ?, ?);""", (user, product_id, quantity, name, price, item_price, image))
            db.commit()
        else:
            #Updates the checkout
            db.execute("""UPDATE checkout set quantity = ?, name = ?, price = ?, item_price = ?, image = ? 
            WHERE product_id = ? and user_id = ?;""", (quantity, name, price, item_price, image, product_id, user))
            #Gets the checkout and the totals to display them for the user
        checkout = db.execute("""SELECT * FROM checkout""")
        totals = db.execute("""SELECT SUM(item_price) FROM checkout""").fetchone()
    return render_template("checkout.html", search_form=search_form, products=checkout, totals=totals)

@app.route("/remove/<int:product_id>")
@login_required
def remove(product_id):
    db = get_db()
    #Deletes products from cart and checkout
    db.execute("""DELETE FROM cart WHERE product_id = ?;""", (product_id,))
    db.execute("""DELETE FROM checkout WHERE product_id = ?;""", (product_id,))
    db.commit()
    return redirect( url_for("cart" ))

@app.route("/purchase")
@login_required
def purchase():
    db = get_db()
    data = db.execute("""SELECT * FROM checkout;""").fetchall()
    user = g.user
    #Gets info on items in checkout
    for products in data:
        name = products["name"]
        image = products["image"]
        quantity = products["quantity"]
        product_id = products["product_id"]
        test = db.execute("""SELECT * FROM orders WHERE product_id = ? and user_id = ?;""", (product_id, user)).fetchone()
        #Checks if the items are already in orders
        if test is None:
            #If not inserts them into orders
            db.execute("""INSERT INTO orders (user_id, product_id, quantity, name, image)
                      VALUES (?, ?, ?, ?, ?);""", (user, product_id, quantity, name, image))
            db.commit()
        else:
            #If they are update the values
            db.execute("""UPDATE orders set quantity = ?, name = ?, image = ? WHERE product_id = ? and user_id = ?;""", (quantity, name, image, product_id, user))
            db.commit()
        #Deletes everything from cart and checkout upon purchasing
        db.execute("""DELETE FROM cart WHERE user_id = ?;""", (user,))
        db.execute("""DELETE FROM checkout WHERE user_id = ?;""", (user,))
        db.commit()
    return redirect(url_for("index"))


@app.route("/orders")
@login_required
def orders():
    db = get_db()
    search_form = SearchForm()
    user = g.user
    #Shows the user their orders
    orders = db.execute("""SELECT * FROM orders WHERE user_id =?;""", (user,)).fetchall()
    return render_template("orders.html", orders=orders, search_form=search_form)


@app.route("/Employees")       
@login_required
def employees():
    if g.user != "admin":
        return redirect( url_for("index"))
    #This is a catalog of all employees currently working 
    db = get_db()
    employees = db.execute("""SELECT * FROM employees ORDER BY name;""").fetchall()
    search_form = SearchForm()
    return render_template("all_employees.html", employees=employees, search_form=search_form)

@app.route("/Employee/<int:employee_id>")       
@login_required
def employee(employee_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    db = get_db()
    #This shows an individual employee and opens up the option to modify it
    employee = db.execute("""SELECT * FROM employees
                         WHERE employee_id = ?;""", (employee_id,)).fetchone()
    return render_template("employee.html", employee=employee, search_form=search_form)

@app.route("/Employee-management/<int:employee_id>", methods=["GET", "POST"])   
@login_required
def employee_management(employee_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    form = Emp_ManagementForm()
    #This route changes the job/department of the employee
    if form.validate_on_submit():
        new_job_description = form.job_description.data
        new_department = form.department.data
        db = get_db()
        #Updates the db and redirects the admin to the modified employee
        db.execute("""UPDATE employees SET job_description = ? WHERE employee_id = ?;""", (new_job_description, employee_id))
        db.execute("""UPDATE employees SET department = ? WHERE employee_id = ?;""", (new_department, employee_id))
        db.commit()
        return redirect( url_for('employee', employee_id=employee_id))
    return render_template("employee_management.html", search_form=search_form, form=form)

@app.route("/new_employee", methods=["GET", "POST"])                
@login_required
def new_employee():
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    new_employee_form = New_EmployeeForm()
    #Adds new employees to the database
    if new_employee_form.validate_on_submit():
        name = new_employee_form.name.data
        age = new_employee_form.age.data
        department = new_employee_form.department.data
        job_description = new_employee_form.job_description.data
        #Sets a default image
        image = 'static/images/employees/placeholder.png'
        db = get_db()
        db.execute("""INSERT INTO employees (name, age, department, job_description, img)
                      VALUES (?, ?, ?, ?, ?);""",
                      (name, age, department, job_description, image))
        db.commit()
        #Inserts the data into the db
        return redirect( url_for('employees'))
    return render_template("employee_new.html", search_form=search_form, employee_form=new_employee_form)

@app.route("/delete_employee/<int:employee_id>")                                 #This deletes employee information in the database
@login_required
def delete_employee(employee_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    db = get_db()
    #Deletes a specific employee from the db
    db.execute("""DELETE FROM employees WHERE employee_id = ?;""", (employee_id,))
    db.commit()
    return redirect( url_for('employees', search_form=search_form))

@app.route("/R_and_D")      #This shows all current R&D projects
def Research_and_development():
    search_form = SearchForm()
    db = get_db()
    research = db.execute("""SELECT * FROM research""").fetchall()
    return render_template("research.html", search_form=search_form, research=research)

@app.route("/add_R_and_D", methods=["GET", "POST"])  
@login_required
def new_Research():
    if g.user != "admin":
        return redirect( url_for("index"))
    research_form = ResearchForm()
    search_form = SearchForm()
    if research_form.validate_on_submit():
        name = research_form.project_name.data
        start = research_form.started.data
        desc = research_form.description.data
        db = get_db()
        #Allows an admin to create new R&D projects
        db.execute("""INSERT INTO research (project_name, started, description)
                      VALUES (?, ?, ?);""",
                      (name, start, desc))
        db.commit()
        return redirect( url_for('Research_and_development'))
    return render_template("research_new.html", search_form=search_form, research_form=research_form)

@app.route("/admin_orders")
@login_required
def admin_orders():
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    db = get_db()
    #Shows the admin all current orders
    orders = db.execute("SELECT * FROM orders;").fetchall()
    return render_template("admin_orders.html", search_form=search_form, orders=orders)

@app.route("/delivered/<int:product_id>/<user_id>")
@login_required
def orders_delivered(product_id, user_id):
    if g.user != "admin":
        return redirect( url_for("index"))
    db = get_db()
    #Deletes a product from a users orders once confirmed delivered by the admin
    db.execute("""DELETE FROM orders WHERE product_id = ? and user_id = ?;""", (product_id, user_id))
    db.commit()
    return redirect( url_for("admin_orders"))

#These are for the footer and additional resources section
# This code is for the support functionality of the web page
@app.route("/support", methods=["GET", "POST"])
def support():
    search_form = SearchForm()
    support_form = SupportForm()
    if support_form.validate_on_submit():
        user = g.user
        if user is not None:
            #If the user is signed in allows them to make support queries
            question = support_form.support.data
            db = get_db()
            db.execute("""INSERT INTO support (user_id, question)
                        VALUES (?, ?);""",
                      (user, question))
            db.commit()
            return redirect( url_for('index'))
        else:
            return redirect( url_for('login_status'))
    return render_template("support.html", search_form=search_form, support_form=support_form)

@app.route("/admin_support")
def admin_support():
    if g.user != "admin":
        return redirect( url_for("index"))
    search_form = SearchForm()
    db = get_db()
    #Shows the admin all current support queries
    tickets = db.execute("""SELECT * FROM support;""").fetchall()
    return render_template("admin_support.html", tickets=tickets, search_form=search_form)

# This code is for the about section of the page
@app.route("/about")
def about():
    search_form = SearchForm()
    db = get_db()
    #Shows the main employees to users
    team = db.execute("""SELECT * FROM employees WHERE img != 'static/images/employees/placeholder.png';""").fetchall()
    return render_template("about.html", search_form=search_form, team=team)

@app.route("/careers")
def careers():
    search_form = SearchForm()
    db = get_db()
    #Shows the careers offered
    careers = db.execute("""SELECT department, job_description FROM employees;""").fetchall()
    return render_template("about.html", search_form=search_form, careers=careers)


@app.route("/blog", methods=["GET", "POST"])
@login_required
def blog():
    search_form = SearchForm()
    blog_form = BlogForm()
    db = get_db()
    blog = db.execute("""SELECT * FROM blog;""").fetchall()
    if blog_form.validate_on_submit():
        post = blog_form.post.data
        user = g.user
        #Allows user to post on the blog board
        db.execute("""INSERT INTO blog (user_id, post)
                      VALUES (?, ?);""",
                      (user, post))
        db.commit()
        return redirect(url_for('blog'))
    return render_template("blog.html", search_form=search_form, blog=blog, blog_form=blog_form)

@app.route("/frequently_asked_questions")
def frequent():
    search_form = SearchForm()
    db = get_db()
    #Shows the users all current support queries in the form of an FAQ
    questions = db.execute("""SELECT * FROM support;""").fetchall()
    return render_template("faq.html", search_form=search_form, questions=questions)

#Custom error handlers to replace chrome defaults
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found. Please check if there was an error with how the link was typed up.</p>"

@app.errorhandler(405)
def handle_exception(e):
    return "<h1>405 Method not Allowed</h1><p>The server has received the request but rejected the specific HTTP method used please try again</p>"

@app.errorhandler(500)
def handle_exception(e):
    return "<h1>500 Internal Server Error</h1><p>The server encountered an unexpected condition that prevented it from fulfilling the request</p>"

@app.errorhandler(403)
def handle_exception(e):
    return "<h1>403 Forbidden</h1><p>The request you have made is forbidden</p>"
