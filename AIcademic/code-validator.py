import re
from datetime import datetime

def verify_code(code):
    """
    Verifies if the given code matches the expected format and checks its authenticity.
    
    Parameters:
    - code (str): The code to verify.

    Returns:
    - tuple: (bool, str) A tuple containing a boolean for validity and a message for feedback.
    """
    # Define the regex pattern to match the generated code format
    pattern = r"^AI-EDU-(\d+)-([a-z0-9]{10})$"
    
    match = re.match(pattern, code)
    if match:
        timestamp_str, random_str = match.groups()
        try:
            # Convert timestamp to datetime for verification
            timestamp = int(timestamp_str)
            code_date = datetime.fromtimestamp(timestamp / 1000.0)
            
            # Check if the code was generated within a certain period (e.g., within the last 7 days)
            current_time = datetime.now()
            if (current_time - code_date).days <= 7:
                return True, f"Code is valid and was generated on {code_date}."
            else:
                return False, "Code is invalid: It was generated too long ago."
        except ValueError:
            return False, "Invalid timestamp format in the code."
    else:
        return False, "Invalid code format."

while True:
    # Prompt the user to input a student code
    student_code = input("Please enter the student's code: ")
    
    # Verify the entered code
    is_valid, message = verify_code(student_code)
    print(message)

    # Ask if the user wants to verify another code or quit
    choice = input("Would you like to verify another code? Enter (N)ew or (Q)uit: ").strip().lower()
    if choice == 'q':
        print("Exiting the program. Goodbye!")
        break
    elif choice != 'n':
        print("Invalid input. Exiting the program.")
        break
