from functions import *
from exceptions import CredentialError,ButtonError
from flask import Flask, render_template, request, redirect, url_for, session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def user_logged_in():
    if 'user-data' in session:
        return True
    return False
def display_template(filename, **context):              #function which standardizes rendering templates and their arguments
    if user_logged_in():                                        #checking if user is logged into session for displaying log off button
        return render_template(filename,logged_in = True,**context)
    elif request.endpoint not in ['login', 'register','outcome']:       #redirect to login page if user isn't logged in, with endpoint exceptions
        return redirect(url_for('login'))                                      
    else:                                                               #if the user is logged in, render template with arguments
        return render_template(filename, **context)
        
@app.route('/')
def hello():                                        #route which redirects to login when app is first launched
    return redirect(url_for('login'))

@app.errorhandler(Exception)                                #error handling function supplied by Flask, modified to return all exceptions caught within the application
def handle_exception(exception):
    error_message = f"Error encountered: {str(exception)}"          #outcome page can be any sort of message, so the contents are parameterized
    return redirect(url_for('outcome',message=error_message,outcome="Error"))     #redirect to outcome page, which returns the content

@app.route('/outcome')
def outcome():
    message = request.args.get('message')
    outcome = request.args.get('outcome')
    if user_logged_in():
        destination = 'home'
    else:
        destination = 'login'
    arguments = {'message':message,
                 'outcome':outcome,
                 'destination':destination}
    return display_template("outcome.html",**arguments)             #passes all the arguments to display_template

@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()                                     #everytime the login page is accessed, the session is cleared so that it can be updated if a different user needs to log in
    if request.method == "POST":
        login_uname = request.form.get('login-username','')            #if a POST request is triggered, retrieve the fields from the form and validate their values in auth.py
        login_pword = request.form.get('login-password','')
        session['user-data'] = login_user(login_uname, login_pword)                #if this line is reached, there weren't any errors logging in, so the user found is assigned to the session 
        return redirect(url_for("home"))            #redirect to the home route
    return display_template("login.html")       #when the login page is routed to by the hello() function, there is no POST request, so the login page just needs to be rendered

@app.route("/register", methods=["POST", "GET"]) #the register page is triggered by an <a> tag in the login page html
def register():                                     #function for registering a new user
    if request.method == "POST":
            username = request.form.get('register-username','')  #obtain username value from form
            password = request.form.get('register-password','')
            admin_token = request.form.get('admin-token','')  #obtain password value from form
            create_user(username, password, admin_token)
            session['user-data'] = login_user(username,password)
            return redirect(url_for("home")) 
    else:
        return display_template("register.html") #display register screen
    
@app.route("/home", methods=["POST","GET"])
def home():
    session_data = session.get('user-data',{}) #check if the session contains user-data, if it does the user is logged in
    booladmin = bool(session_data[3]) #return the admin integer as a boolean to determine which functions to display the user
    username = str(session_data[1]) #return the username as parameter for tempalte
    if booladmin:
        return display_template("functions-admin.html",username=username) #admin user
    else:
        return display_template("functions-user.html",username=username) #regular user
    
@app.route("/add_record",methods=["POST","GET"])
def add_record():
    if request.method == "POST":
        name = request.form['owner-name'] 
        location = request.form['property-location']        #get all form values from request.form
        value = request.form['property-value']
        username = session.get('user-data',{})[1]
        outcome_message = append(name,location,value,username)  #output message from append function
        return redirect(url_for('outcome',message=outcome_message,outcome="Record Added")) #if the user gets this far, the append was successful, so return a succesful outcome message
    else:
        return display_template("record-create.html")

@app.route("/display_record",methods=["POST","GET"])
def display_record():
    if request.method == "POST":
        if 'search-btn' in request.form and (mortgage_id:=request.form.get('mortgage-id','').strip()):                #determine whether the user wants to display all records or just search individual records
            result = read(mortgage_id,False)              #the parameters for function.read() are different depending on which button is clicked
            return display_template("results.html",results=result)
        elif 'display-all-btn' in request.form:
            result = read(None,True) #search all records
            return display_template("results.html",results=result)      
        raise ButtonError #if the user clicks neither the search nor the display all button, throws an error, unless its the return home button
    return display_template("record-display.html") #display display record template
        
@app.route("/update_record",methods=["POST","GET"])
def update_record():
    if request.method == "POST":
        mortgage_id = request.form.get('mortgage-id','').strip() 
        read(mortgage_id,False)
        columns = {k: v for k, v in request.form.items() if k in {'name', 'location', 'value'} and v.strip()}
        if not columns:
            raise ValueError("No values provided for update")  
        update_outcome = update(mortgage=mortgage_id, **columns)
        return redirect(url_for('outcome',message=update_outcome,outcome="Updated Record"))
    return display_template("record-update.html") #display update record template
    
@app.route("/delete_record",methods=["POST","GET"])
def delete_record():
    if user_logged_in() & bool(session.get('user-data',{})[3]):
        if request.method == "POST":
            mortgage_id = request.form.get('mortgage-id','').strip()
            read(mortgage_id,False)
            delete_outcome = delete(mortgage_id)   #delete function
            return redirect(url_for('outcome',message=delete_outcome,outcome="Deleted Record"))
        return display_template("record-delete.html") #display delete record template
    else:
        raise CredentialError("To access the delete record page, you must be an admin") 