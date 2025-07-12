# System module for command line arguments and exit functionality
import sys
# PyQt5 application framework for GUI
from PyQt5.QtWidgets import QApplication
# Import the login window UI component
from ui.login_window import LoginWindow
# Import database initialization function
from db.init_db import init_db

def main():
    """
    Main function that initializes the application and starts the GUI.
    """
    # Initialize the database (create tables if they don't exist)
    init_db()
    
    # Create the main PyQt5 application instance
    app = QApplication(sys.argv)
    
    # Create and display the login window
    window = LoginWindow()
    window.show()
    
    # Start the application event loop and exit when closed
    sys.exit(app.exec_())

# Entry point - run main function only if script is executed directly
if __name__ == "__main__":
    main()
