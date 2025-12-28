# MedSafe: Pharmacy Management & Expiry Alert System 
#### Video Demo:  <URL [HERE](https://youtu.be/NKj8IXGcR28)>
#### Description:

MedSafe: pharmacy Mangement & alert system  
Medsafe is an webapp built for Pharmacies where users can add medicines, sell medicines, See their sales using logbook, users can also change their passwords. 

This project is inspired by Harvard university CS50x course week 9 pset finance.  
https://cs50.harvard.edu/x/psets/9/finance/    

You can access this project by going to
#### Demo link: 
First link: https://project-cs50.onrender.com/  
Second link: https://dasarath.com  

## Tech stack used:  
**1. Frontend:**   
Html, CSS, BootStrap  
**2. Backend:**  
    python using Flask framework  
    Sqlite3 database  
**3. Deployment:**  
   Render
   Namecheap for domain     
      

### Frontend  
This project uses **Html,css and Bootstrap** for frontend.The design of this project is inspired and adapted form **CS50 finance assignment.**   

There are mainly 10 files in templates folder  
**1. layout.html**  
This is the main template for builiding the other pages int this project as this project uses flask so we are using jinja templates for ease of development. This file has nav bar which will be common to all pages. The navbar contains Logo of the project, depending upon the if user is logged in or not it will show differnet nav-bar.  
We have used Bootstraps **class="bg-light border navbar navbar-expand-md navbar-light"** for nav-bar.  
If user is not logged in:
page shows logo on the left and login and register on the right they have anchor tags which take user to their respecitive routes.  

**2. login.html**   
**Main function:** Get login details from the user and submit to **/login**
This page is a child of layout.html which splits out a form to the **"/login"** route via post it has mainly 2 input tags each one for username and pasword respectively. 
Stylized with bootstrap **class="form-control mx-auto w-auto"**
Finally a button is present for submitting the form to "/login route".  

**3. Register html** 
**Main function:** Get registration details from the user and submit to **/register** 
This page is also similar to **login.html** and a child of **layout.html**. This page has 1 form and 3 input tags Which are stylized with this **Boot strap: class="form-control mx-auto w-auto"** this page submits the form to **"/register"**


**4. Index.html**
**Main function:** There are many functions as this is the main index/home page of this project **  
On Navbar:  there are mainly 5 anchor tags namely **Buy medicines, Add money, log book, change password, logut.**  
Every term is self-explinatory here.  
In the main page of the body there are status legends for depending the upon the expiry date of medicine a color tag is given based on the below conditions:    

    RED-TAG if expiry date <= 15 days
    YELLOW-TAG if expiry date <= 1 months   
    GREEN-TAG if expiry date > 2 months  
    GREY-TAG if expired  
    Below that we have the main table which have the following columns **Medicine name, Status, Expiry date	Quantity, Price, TOTAL,	a button to Sell/dispose**  
    And also below the table under the total column we have cash = balance of the current user  
    Total = total of the whole medicine stock + cash  

**5. addmeds.html**  
**Main Function: Is to add medicines into the inventory and submits via post to "/addmeds" route**
This page contains a form with takes 5 inputs from the user namely  
Medicine name  
quantity  
price of 1 med  
purchase date  
Expiry date  

**6. addmoney.html**  
**Main Function: Is to add money into the user account form sent to route "/addmoney" via post**  
This page contains a form and 1 input tags for cash and 1 button for submisson.  

**7.logbook.html**  
**Main Function: This page shows a table of all transactions happend**  
This page has a table with the following columns  
Medicine name, Transaction Type, Amount, Transacted at
Here there are 3 transaction types  
LOSS - Happens when medicines are expired and disposed  
BOUGHT - Happens when we add medicines  
SOLD - happens when we sell medicines  

**8.changepwd.html** 
**Main function:** new password from the user and submit to **/changepwd**
This page is a child of layout.html which splits out a form to the **"/changepwd"** route via post it has mainly 2 input tags each one for pasword and confirmation respectively. 
Stylized with bootstrap **class="form-control mx-auto w-auto"**
Finally a button is present for submitting the form to "/changepwd route".  

**9. dispose.html**  
**Main fuction:** Is to dispose(delete the medicines row) if the medicine is expired.

**10. apology.html**  
**Main function:** Is to show an apology message along with error code with a cat meme to the user if user tries to bypass validation.   


## Backend  
Backend has mainly 3 files app.py, helpers.py and schema.sql  

**1. schema.sql:**  
This file contains the database schema required for the sqlite3 database to work.  

**2. helper.py**  
This file gives useful and very important functions for finding app.py(Main backend logic) to perform well.  
Functions in this file:  
**apology(message,status_code):** this fn takes 2 arguments 1st is message to be shown in apology.html when user tries to bypass server side validation  
2nd message is to send staus_code.  
**login_required**: this function creates a decorator route which is helpful for other routes which need login to access them.
**int(value):"** Converts given value into ₹  
**get_status(expiry_date)**: This function is an improtant function which assings colors to the status depending upon the expiry date.

**3. app.py**  
This is the main backend logic of the program   
First we are going to intiate Configure session to use filesystem (instead of signed cookies) and Configure CS50 Library to use SQLite database.  
If database is not created then we are going to create it using schema.sql.  


**@app.route("/")**
This function displays the index table it gets data from medicines table and passes each row of medicines through a
loop where the medicines get their status using get_status(expiry_date) expiry date.  

**@app.route("/addmeds", methods=["GET", "POST"])**
This route supports both GET and POST:
If GET it displays "addmeds.html"  
if POST we are going to read all the inputs and validate them like if a date type is:
integer-  
if integer is empty  
We are going to check if the integer is a not a string  
not a float or -ve number  

string-  
we are going to validate the input if it empty

dates: 
if purchase_date > today then we will return an apology that "User cannot buy from future"  
elif expire_date <= today because "As We need not to buy expired medicines"  

Then update the database as we are buying we need to reduce the cost of medicines from the current balance from users table and also log the transaction also insert medicines into medicines  
Also a flash alert is shown to them near nav bar as "registered"

**@app.route("/logbook")**  
This shows logbook of transactions it just reads from transactions table and displays them in a neat formatable table.  

**@app.route("/register", methods=["GET", "POST"])**  
This route has 2 methods GET and POST:  
If GET this route shows register.html  
IF POST this route collects the name, password and confirmation and validaties them similar to "/addmeds" route.  

After validation if the user is present then already this route shows apology("Username already exist!!")  

Then if username is new then the username is stored in plain text and password is stored in hash from with the help of "werkzeug.security" module  

If registration is successfull then the user will be 
Also a flash alert is shown to them near nav bar as "registered"
redirected to the index page  


**@app.route("/sell", methods=["POST"])**
This route accepts only POST 
Here we are going to select the medicnies that are expiried  then we are going to get the id of the medicine batch from the user form   
After validating them we are also going to validating the  
id with non-expired medicines.  

Then updating user account balance and logging transactions and deleteing the medicine batch  


**@app.route("/addmoney", methods=["GET","POST"])**  
This route after validating the html form via POST updates the user's balance.  


**@app.route("/changepwd")**
If GET this route spits out changepwd.html 
If POST this route vaidates the data then updates the users table hash with new hash from werkzeug.security fns

*@app.route("/dispose", methods=["POST"])*  
This route is also very similar to the /sell route but /sell add money to our account this route disposes the medicines so it is lose and hence it reduces the money in out account.


**The following routes were adapted from cs50 finance:**  
@app.route("/login", methods=["GET", "POST"])  
@app.route("/logout") 


## Deployment  
The whole flask server is runned on **Render** service and  domain name is bought on **namecheap**.
