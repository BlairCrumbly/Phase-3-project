# lib/helpers.py

def helper_1():
    print("Performing useful function#1.")


def exit_program():
    print("Goodbye!")
    exit()




from datetime import datetime

class Helpers:
    def get_valid_date(self, prompt, required=True, must_be_after=None):
        """
        Get a valid date from user input.
        
        Args:
            prompt (str): The prompt to display to the user
            required (bool): Whether a value is required or can be skipped
            must_be_after (date): If provided, the entered date must be after this date
            
        Returns:
            date or None: The validated date, or None if not required and left blank
        """
        while True:
            date_str = input(prompt).strip()
            
            # If not required and input is empty, return None
            if not required and not date_str:
                return None
                
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Check if date must be after a specific date
                if must_be_after and parsed_date < must_be_after:
                    print(f"Date must be after {must_be_after}. Please enter a valid date.")
                    continue
                    
                return parsed_date
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    def validate_numeric_id(self, id_str, entity_name="item"):
        """
        Validate that the given string is a valid numeric ID.
        
        Args:
            id_str (str): The ID string to validate
            entity_name (str): The name of the entity for error messages
            
        Returns:
            int or None: The ID as an integer, or None if invalid
        """
        try:
            return int(id_str)
        except ValueError:
            print(f"Invalid {entity_name} ID. Please enter a numeric value.")
            return None
    
    def confirm_action(self, prompt):
        """
        Confirm an action with the user.
        
        Args:
            prompt (str): The confirmation prompt
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        response = input(f"{prompt} (Y/N): ").strip().upper()
        return response == "Y"
    
    def format_status(self, status):
        """
        Format a job status for display with appropriate colors.
        
        Args:
            status (str): The job status
            
        Returns:
            str: The formatted status with color formatting
        """
        status_colors = {
            "applied": "blue",
            "pending": "yellow",
            "rejected": "red",
            "offer": "green"
        }
        
        color = status_colors.get(status.lower(), "white")
        return f"[{color}]{status}[/{color}]"