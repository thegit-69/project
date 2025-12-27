import os

from cs50 import SQL
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///medsafe.db")


# a global variable for storing today
TODAY = date.today()
# TODAY = date(2026,6,12)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # need to show the medicines stock
    meds = db.execute("SELECT name, expiry_date, quantity, price FROM medicines WHERE user_id = ? ORDER BY expiry_date;", session["user_id"])

    net = 0
    for ele in meds:
        ele["TOTAL"] = ele["price"] * ele["quantity"]
        net += ele["TOTAL"]
    # bal = ?
    # curr_bal = current balance a user has and ld = list of dict
    curr_bal_ld = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    bal = curr_bal_ld[0]["cash"]

    total = bal + net
    for ele in meds:
        # default status value
        ele["status"] = "unknown" 
        expiry_str = ele["expiry_date"]
        format = "%Y-%m-%d"

        # Convert the string from html form to a date object
        expiry_date = datetime.strptime(expiry_str, format).date()

        # Finding two_months before expiry if TODAY > two_months => GREEN status
        rdelta = relativedelta(months=2)
        two_months_before = expiry_date - rdelta
        # Finding one_month before expiry => YELLOW status
        rdelta = relativedelta(months=1)
        one_month_before = expiry_date - rdelta
        # Finding 15 days before expiry => RED => STATUS
        rdelta = relativedelta(days=15)
        onefive = expiry_date - rdelta
        # Checking if the medicine is expired
        # if yes then the user must dispose medicine and money is lost as it is a loss
        if TODAY <= two_months_before:
            ele["status"] = "green"
            # we need to send alert how the idk
        elif TODAY <= one_month_before:
            ele["status"] = "yellow"
        elif TODAY < expiry_date:
            ele["status"] = "red"
        elif TODAY >= expiry_date:
            ele["status"] = "expired"
    # return render_template("test.html", two=two_months_before, exp=expiry_date, one=one_month_before, onefive=onefive)
    # we need to implement alert logic
    return render_template("index.html", meds=meds, bal=bal, total=total)



@app.route("/addmeds", methods=["GET", "POST"])
@login_required
def addmeds():
    # adding medicine details to database
    if request.method == "POST":
        medname = request.form.get("name")
        quantity = request.form.get("quantity")
        pricestr = request.form.get("price")
        purchased_date_str = request.form.get("purchase_date")
        expiry_date_str = request.form.get("expiry_date")
        if not medname:
            return apology("Please enter medicine name!!")
        elif not quantity:
            return apology("Please enter quantity!!")
        elif not pricestr:
            return apology("Please enter the price")
        elif not purchased_date_str:
            return apology("Please enter purchase date")
        elif not expiry_date_str:
            return apology("Please enter expiry date")
        try:
            nmeds = int(quantity)
            price = int(pricestr)
        except ValueError:
            return apology("Fractional quantity or prices are not allowed!!")
        if (not quantity.isdigit()):
            return apology("quantity cannot be empty or  -ve")
        elif (not pricestr.isdigit()):
            return apology("Price cannot be empty or  -ve")
        
        format = "%Y-%m-%d"

        # Convert the string from html form to a date object
        purchase_date = datetime.strptime(purchased_date_str, format).date()
        expiry_date = datetime.strptime(expiry_date_str, format).date()

        # validating dates
        if purchase_date > TODAY:
            return apology("You cannot purchase from future")
        elif expiry_date <= TODAY:
            return apology("Dont buy it is expired")
        
        # curr_bal = current balance a user has and ld = list of dict
        curr_bal_ld = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
        bal = curr_bal_ld[0]["cash"]

        # finding the cost of this batch of medcines
        cost = nmeds * price

        if (bal < cost):
            return apology("Low balance!! Add some money into the account")
        
        # inserting the data from form into the medicines table or inserting into the database
        db.execute("INSERT INTO medicines(user_id, name, quantity, price, purchase_date, expiry_date) VALUES(?,?,?,?,?,?);", session["user_id"], medname, nmeds, price, purchase_date,expiry_date)
        
        # Deducting cost from user account bal
        db.execute("UPDATE users set cash = ? WHERE id = ?", bal - cost, session["user_id"])

        # if everthing is successfull we will redirect back to index with added medcines
        flash("Medicines bought!!")
        return redirect("/")
    return render_template("addmeds.html")


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""
#     purchases = db.execute("SELECT symbol, shares, price, purchased_at FROM purchases WHERE user_id = ?", session["user_id"])
#     return render_template("history.html", purchases=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")





@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not name:
            return apology("Please enter username!!")
        elif not password:
            return apology("Please enter password")
        elif (password != confirmation):
            return apology("Passwords do not match")
        try:
            new_user_id = db.execute("INSERT INTO users(username, hash) VALUES(?,?)", name,generate_password_hash(password))
            session["user_id"] = new_user_id
            flash("Registered")
            return redirect("/")
        except ValueError:
            return apology("Username already exist!!")
    return render_template("register.html")


# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     portfolio = db.execute("SELECT DISTINCT(symbol), SUM(shares) AS shares FROM purchases WHERE user_id = ? GROUP BY symbol ORDER BY symbol;", session["user_id"])
#     stocks = []
#     for stock in portfolio:
#         stocks += [stock["symbol"]]
#     if request.method == "POST":
#         symbol = request.form.get("symbol")
#         shares = request.form.get("shares")
#         # nshares is the no. of shares user owns of that symbol
#         if not symbol:
#             return apology("Please select some share symbol to sell!!")
#         elif symbol not in stocks:
#             return apology("Please select some share symbol THAT you own!!!")
#         elif (not shares.isdigit()):
#             return apology("Shares cannot be empty or  -ve")

#         for stock in portfolio:
#             if (symbol == stock["symbol"]):
#                 nshares = stock["shares"]

#         if (int(shares) > nshares):
#             return apology("You don't own that many shares!!")

#         # after the above validation we need to sell
#         # selling shares means reducing shares count and adding the money to the account
#         # first we need to see how much cost 1 share right now
#         # quote = lookup(symbol)
#         price = quote["price"]
#         cost = float(shares) * float(price)
#         # reduce that many shares
#         db.execute("INSERT INTO purchases(user_id,symbol,shares,price) VALUES (?,?,?,?);", session["user_id"], symbol, -int(shares), usd(price))
#         # also add the balance cash in users table
#         curr_bal_ld = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
#         bal = curr_bal_ld[0]["cash"]
#         db.execute("UPDATE users set CASH = ? WHERE id = ?", bal + cost, session["user_id"])
#         flash("Sold!!")
#         return redirect("/")
#     return render_template("sell.html", stocks=stocks)


# Allow users to add additional cash to their account.
@app.route("/addmoney", methods=["GET","POST"])
@login_required
def addbal():
    if request.method == "POST":
        amount = request.form.get("money")
        if not amount:
            return apology("Please enter some value!!")
        elif not amount.isdigit():
            return apology("-ve numbers and charecters are not allowed!!")

        curr_bal_ld = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
        bal = curr_bal_ld[0]["cash"]
        db.execute("UPDATE users set CASH = ? WHERE id = ?", bal + float(amount), session["user_id"])
        flash("Amount added Successfully!!")
        return redirect("/")

    return render_template("addmoney.html")


@app.route("/changepwd", methods=["GET", "POST"])
@login_required
def changepwd():
    if request.method == "POST":
        newpwd = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not newpwd:
            return apology("Password filed cannot be empty")
        elif not confirmation:
            return apology("Confirmation field missing!!")
        elif newpwd != confirmation:
            return apology("Password's don't match!!!")
        db.execute("UPDATE users set hash = ? WHERE id = ?", generate_password_hash(newpwd), session["user_id"])
        flash("Password updated Successfully!!")
        return redirect("/")
    return render_template("changepwd.html")




@app.route("/dispose", methods=["GET", "POST"])
@login_required
def dispose():
    meds = db.execute("SELECT id,name, expiry_date, quantity, price FROM medicines WHERE user_id = ? and expiry_date >= ? ORDER BY expiry_date", session["user_id"], str(TODAY))
    if request.method == "POST":
        id = request.form.get("id")
        if not id:
            return apology("Medicine id cannot be empty Try Again!!")
        
        flag = False
        for ele in meds:
            if int(id) == int(ele["id"]):
                flag = True
        
        if not flag:
            return apology("Id does not exists")

        # also todo reduce that much amount from user account bal 
        # Finding account balance
        curr_bal_ld = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
        bal = curr_bal_ld[0]["cash"]

        # Finding the cost of the loss = price * quantity
        # loss because we are going to lose money as we didn't sale this medicines so waste
        loss = db.execute("SELECT quantity * price AS loss FROM medicines WHERE id = ?", id)
        loss_amount = loss[0]["loss"]
        db.execute("UPDATE users set CASH = ? WHERE id = ?", bal - loss_amount, session["user_id"])
        # deleting that batch of medicines using the medicine is
        db.execute("DELETE FROM medicines WHERE id = ?", id)
        flash("Disposed expired medicines!!")
        return redirect("/")
        
    return render_template("dispose.html", meds=meds,today=str(TODAY))