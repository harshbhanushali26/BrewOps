import json
import os
from datetime import datetime
from utils.display import print_success, print_error, print_warning

class SessionManager:
    def __init__(self, session_file="data/cafe_session.json"):
        self.session_file = session_file
        self.session_duration = 1800  # 30 minutes in seconds
        
    def create_session(self, username):
        """Create a new session after successful login"""
        session_data = {
            "username": username,
            "login_time": datetime.now().isoformat(),
            "session_time": self.session_duration,
            "status": "active"
        }
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            print_success(f"Session created for {username}")
            return True
        except Exception as e:
            print_error(f"Error creating session: {e}")
            return False
    
    def check_existing_session(self):
        """Check if valid session exists on app startup"""
        if not os.path.exists(self.session_file):
            return None
            
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is still valid
            login_time = datetime.fromisoformat(session_data["login_time"])
            current_time = datetime.now()
            elapsed = (current_time - login_time).total_seconds()
            
            if elapsed >= self.session_duration:
                self.clear_session()
                return None
            
            return session_data
            
        except Exception as e:
            print_error(f"Error reading session: {e}")
            self.clear_session()
            return None
    
    def check_session_on_main_menu(self):
        """Check session when returning to main menu"""
        if not os.path.exists(self.session_file):
            return False
            
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            login_time = datetime.fromisoformat(session_data["login_time"])
            current_time = datetime.now()
            elapsed = (current_time - login_time).total_seconds()
            remaining = self.session_duration - elapsed
            
            # Check if session expired
            if remaining <= 0:
                print("\n" + "="*50)
                print_error("SESSION EXPIRED")
                print_warning("Please login again to continue.")
                print("="*50 + "\n")
                self.clear_session()
                return False
            
            # Show warnings
            elif remaining <= 60:  # 1 minute warning
                print_warning(f"\nWARNING: Session expires in {int(remaining)} seconds!")
                print_warning("Please save your work and prepare to login again.\n")
                
            elif remaining <= 300:  # 5 minute warning
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                print_warning(f"\nWARNING: Session expires in {mins}:{secs:02d}")
                print_warning("Please complete your current task soon.\n")
            
            return True
            
        except Exception as e:
            print_error(f"Error checking session: {e}")
            self.clear_session()
            return False
    
    def clear_session(self):
        """Clear/delete session file"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                print("Session cleared.")
        except Exception as e:
            print_error(f"Error clearing session: {e}")
    
    def get_current_user(self):
        """Get current logged in user"""
        if not os.path.exists(self.session_file):
            return None
            
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            return session_data.get("username")
        except:
            return None
