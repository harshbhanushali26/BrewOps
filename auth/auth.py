import bcrypt
import uuid
from pathlib import Path
from datetime import datetime
import re
from utils.json_io import load_users_data, save_users_data

USERS_FILE = Path("data") / "users.json"

class AuthManager:
    def __init__(self):
        self.users = self.load_users()  # or load from file
        self.current_user = None

        
    def login(self, username, password):
        for user_id, user in self.users.items():
            if user["username"] == username and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                self.current_user = user_id 
                return True, "User Logged-in Successfully!"  # Return boolean
        return False, "Username or password is invalid, try again!"
        
    
    def logout(self):
        self.current_user = None
    
    
    def is_logged_in(self):
        return self.current_user is not None
    
    
    def register_user(self, username, password):
        
        if self._verify_username(username):
            return False, "Username already exists, try another!"
        
        success, msg = self._check_password_strength(password)
        if not success:
            return False, msg
            
        user_id = self._generate_user_id() 
        hashed_password = self._hash_password(password)
        self.users[user_id] = {
            "user_id" : user_id,
            "username" : username,
            "password" : hashed_password,
            "created_at" : datetime.now().isoformat()
        }
        self.save_users(self.users)
        return True, "User Registered successfully"
    
        
    def _generate_user_id(self):
        return f"u_{uuid.uuid4().hex[:8]}"  # u_a1b2c3d4
      
    
    def _hash_password(self, password):
        salt = bcrypt.gensalt() # Generates a random salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) # encode password as bytes
        return hashed_password.decode('utf-8')  # string for JSON
    
    
    def _check_password_strength(self, password):
        # Password validation - at least 8-12 characters, 1 uppercase, 1 lowercase, 1 number
        if len(password) < 8 or len(password) > 12:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"
    
    
    def _check_username_strength(self, username):
        # Username validation - 8–12 characters, at least 1 uppercase, 1 lowercase, 1 number
        if len(username) < 8 or len(username) > 12:
            return False, "Username must be 8-12 characters long."
        if not re.search(r'[A-Z]', username):
            return False, "Must contain at least 1 uppercase letter."
        if not re.search(r'[a-z]', username):
            return False, "Must contain at least 1 lowercase letter."
        if not re.search(r'\d', username):
            return False, "Must contain at least 1 number."
        
        return True, "Valid username!"

    
      
    def _verify_username(self, username):
        if self.users: # for first user 
            for user in self.users.values():
                if user["username"] == username:
                    return True
        return False
    
    
    def load_users(self):
        return load_users_data(USERS_FILE)
    
    
    def save_users(self, users):
        return save_users_data(users, USERS_FILE)
    

 
