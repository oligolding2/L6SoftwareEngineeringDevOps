import sqlite3,random,re
from exceptions import CredentialError, DatabaseError

def check_credentials(username, password):
        login_username = validate_field("username",username,min_length=5,max_length=12,allow_numbers=True)
        login_password = validate_field("password",password,min_length=7,max_length=None,allow_numbers=True)
        return login_username, login_password
    

def validate_field(field_name,value, min_length=0, max_length=50, allow_numbers=False):
        if not value or not value.strip():
            raise ValueError(f"{field_name.capitalize()} cannot be empty.")
        
        value = value.strip()  # Remove leading/trailing spaces
        
        if not allow_numbers and re.match(r'^\d+$', value):
            raise ValueError(f"{field_name.capitalize()} must not contain numeric characters.")
        
        if min_length and len(value) < min_length:
            raise ValueError(f"{field_name.capitalize()} must be at least {min_length} characters long.")
        
        if max_length and len(value) > max_length:
            raise ValueError(f"{field_name.capitalize()} cannot exceed {max_length} characters.")
        
        return value  # Return the cleaned and validated value

def executor(query,args,query_type): #executor function which runs sql queries
        try:
            with sqlite3.connect('static/database.db') as conn:
                cursor = conn.cursor()
                match query_type:
                    case 'login':
                        return cursor.execute(query, args or ()).fetchone()
                    case 'read':
                        return cursor.execute(query, args or ()).fetchall()
                    case 'add' | 'update' |'delete':
                        cursor.execute(query, args or ())
                        conn.commit()
                        return "Success" if query_type != 'delete' else "Record deleted successfully."
        except sqlite3.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")     #raise the error from sqlite3 as a system error so it can be caught by the flask exception handler
        
def append(owner,location,value,user):
        owner = validate_field("owner",owner)
        location = validate_field("location",location)
        value = validate_field("value",value, allow_numbers=True)
        user = validate_field("user",user,allow_numbers=True)
        query = "INSERT INTO mortgage (owner,location,value,inserted_by) VALUES (?,?,?,?)" #create the query for executor
        return executor(query,(owner,location,value,user),'add') #run the query and arguments, with query type add in executor

def read(mortgage_id,search_all):       #function to display records from the database
        query = "SELECT mortgage_id, owner, location, value FROM mortgage"
        args = None

        if not search_all:
            query += " WHERE mortgage_id = ?"
            args = (validate_field("mortgage_id",mortgage_id, allow_numbers=True),)

        result = executor(query, args, 'read')
        if not result:
            raise ValueError(f"No record found for Mortgage ID {mortgage_id}.")
        return result

def update(mortgage_id,name=None,location=None,value=None): #function to update mortgage records
        fields = {'owner': name, 'location': location, 'value': value}
        fields = {key: validate_field(key,value, allow_numbers=(key == 'value')) for key, value in fields.items() if value}

        if not fields:
            raise ValueError("No fields provided for update.")

        query = f"UPDATE mortgage SET {', '.join(f'{k} = ?' for k in fields.keys())} WHERE mortgage_id = ?"
        args = (*fields.values(), mortgage_id)
        return executor(query, args, 'update')

def delete(mortgage_id):        #function to delete records from database
        query = "DELETE FROM mortgage WHERE mortgage_id = ?"        #query for executor
        args = validate_field("mortgage_id",mortgage_id, allow_numbers=True)          #arguments for executor
        return executor(query,(args,),'delete')         #delete record

def create_user(username,password,admin_token):             #function to create user
        new_credentials = check_credentials(username,password)
        admin = 1 if admin_token == "HiQA99999999" else 0

        if admin_token and admin == 0:
            raise CredentialError("Invalid admin token provided.")
        
        user_id = random.randint(0, 9999999)
        query = "INSERT INTO users (user_id, username, password, admin) VALUES (?, ?, ?, ?)"
        return executor(query, (user_id, new_credentials[0], new_credentials[1], admin), 'add')

def login_user(username,password):   
        credentials = check_credentials(username,password)
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        result = executor(query, (credentials[0], credentials[1]), 'login')
        if result:
              return result
        else:
            raise CredentialError("Invalid username and password given - no results found in database.")


    