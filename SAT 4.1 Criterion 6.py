import customtkinter as ctk
import csv
import os
from tkinter import messagebox

# =========================
# File Constants & Headers
# =========================

GAME_FILE = "games.csv"      # CSV file storing game collection data
USER_FILE = "users.csv"      # CSV file storing user login credentials

# Expected CSV headers for the two files
EXPECTED_HEADER = ["Name", "Platform", "Format"]
USER_HEADER = ["Username", "Password"]

# ============================================================
# CSV Header Auto-fix Functions
# These ensure that the required CSV files exist and have the
# correct header rows. If headers are missing or incorrect,
# they rewrite the files with the correct headers and preserve
# existing data rows.
# ============================================================

def fix_csv_header():
    """
    Ensures GAME_FILE exists with the correct header.
    If missing or incorrect, rewrites header and preserves data.
    """
    if not os.path.exists(GAME_FILE):
        # If the game file doesn't exist, create it and write the header
        with open(GAME_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(EXPECTED_HEADER)
    else:
        # If it exists, check header validity
        with open(GAME_FILE, "r", newline="") as f:
            lines = f.readlines()
        if not lines or lines[0].strip().split(",") != EXPECTED_HEADER:
            # If header is wrong, rewrite header and keep any existing data
            data_lines = lines[1:] if len(lines) > 1 else []
            with open(GAME_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_HEADER)
                for line in data_lines:
                    f.write(line)

def fix_user_header():
    """
    Ensures USER_FILE exists with the correct header.
    If missing or incorrect, rewrites header and preserves data.
    """
    if not os.path.exists(USER_FILE):
        # If the user file doesn't exist, create it and write the header
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(USER_HEADER)
    else:
        # If it exists, check header validity
        with open(USER_FILE, "r", newline="") as f:
            lines = f.readlines()
        if not lines or lines[0].strip().split(",") != USER_HEADER:
            # If header is wrong, rewrite header and keep any existing data
            data_lines = lines[1:] if len(lines) > 1 else []
            with open(USER_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(USER_HEADER)
                for line in data_lines:
                    f.write(line)

# Ensure CSV files are initialized with correct headers before any app logic
fix_csv_header()
fix_user_header()

# =========================
# UI Constants
# =========================
FONT_HEAD = ("Jaldi", 14, "bold")   # Header font
FONT_BODY = ("Jaldi", 14)           # Body font

# Theme colour constants for consistent styling
BG_COLOUR = "#DC46F0"
BTN_COLOUR = "#4B79FA"
ENTRY_COLOUR = "#5263FA"
DROPDOWN_COLOUR = "#3163F9"
FILTER_COLOUR = "#4195EF"
LABEL_COLOUR = "#593cb0"
LIST_BG_COLOUR = "#D9D9D9"

# Dropdown options for platform and format fields
PLATFORMS = ["PC", "Xbox", "PlayStation", "Nintendo", "Other"]
FORMATS = ["Physical", "Digital"]

# ===============================================================
# Main Application Class (GameApp)
# Manages the overall window, user session info, and navigation
# between views ("frames").
# ===============================================================

class GameApp(ctk.CTk):
    def __init__(self):
        """
        Initializes the main application window.
        Handles frame switching and stores the logged-in user.
        """
        super().__init__()
        self.title("Game Collection")
        self.geometry("300x350")
        self.logged_in_user = None  # Username of the session; set on login
        self.switch_frame(LoginPage)  # Start with login frame

    def switch_frame(self, frame_class):
        """
        Replaces the current frame with a new one of type frame_class.
        Used for page navigation.
        """
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

# ===============================================================
# LoginPage Frame
# Handles user login and navigation to registration
# ===============================================================

class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        """
        Login form for existing users. Navigates to registration or main menu.
        """
        super().__init__(master, fg_color=BG_COLOUR)
        master.geometry("300x300")

        ctk.CTkLabel(self, text="Login", font=FONT_HEAD, text_color=LABEL_COLOUR).pack(pady=20)

        # Username entry
        ctk.CTkLabel(self, text="Username:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.username_entry = ctk.CTkEntry(self, font=FONT_BODY, text_color=ENTRY_COLOUR)
        self.username_entry.pack(pady=5)

        # Password entry
        ctk.CTkLabel(self, text="Password:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.password_entry = ctk.CTkEntry(self, font=FONT_BODY, show="*", text_color=ENTRY_COLOUR)
        self.password_entry.pack(pady=5)

        # Login button
        ctk.CTkButton(self, text="Login", command=self.login_user,
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)

        # Navigation to registration page
        ctk.CTkButton(self, text="Register", command=lambda: master.switch_frame(RegisterPage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack()

    def login_user(self):
        """
        Authenticates user credentials.
        If valid, navigates to MainMenuPage.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        with open(USER_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    self.master.logged_in_user = username
                    self.master.switch_frame(MainMenuPage)
                    return
        messagebox.showerror("Error", "Invalid username or password.")

# ===============================================================
# RegisterPage Frame
# Handles new user registration
# ===============================================================

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master):
        """
        Registration form for new users with validation.
        """
        super().__init__(master, fg_color=BG_COLOUR)
        master.geometry("300x350")

        ctk.CTkLabel(self, text="Register", font=FONT_HEAD, text_color=LABEL_COLOUR).pack(pady=20)

        # Username entry
        ctk.CTkLabel(self, text="Username:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.username_entry = ctk.CTkEntry(self, font=FONT_BODY, text_color=ENTRY_COLOUR)
        self.username_entry.pack(pady=5)

        # Password entry
        ctk.CTkLabel(self, text="Password:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.password_entry = ctk.CTkEntry(self, font=FONT_BODY, show="*", text_color=ENTRY_COLOUR)
        self.password_entry.pack(pady=5)

        # Confirm password entry
        ctk.CTkLabel(self, text="Confirm Password:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.confirm_entry = ctk.CTkEntry(self, font=FONT_BODY, show="*", text_color=ENTRY_COLOUR)
        self.confirm_entry.pack(pady=5)

        # Register button
        ctk.CTkButton(self, text="Register", command=self.register_user,
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)

        # Navigation to login page
        ctk.CTkButton(self, text="Back to Login", command=lambda: master.switch_frame(LoginPage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack()

    def register_user(self):
        """
        Registers a new user if username is unique and passwords match.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields are required.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        # Check for existing username
        with open(USER_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    messagebox.showerror("Error", "Username already exists.")
                    return
        # Add new user credentials to file
        with open(USER_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, password])
        messagebox.showinfo("Success", "Registration successful. Please login.")
        self.master.switch_frame(LoginPage)

# ===============================================================
# MainMenuPage Frame
# User dashboard for navigation to other pages
# ===============================================================

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, master):
        """
        Displays main menu options and user info.
        """
        super().__init__(master, fg_color=BG_COLOUR)
        master.geometry("300x350")
        user = master.logged_in_user if master.logged_in_user else "Unknown"

        ctk.CTkLabel(self, text=f"Main Menu\nUser: {user}", font=FONT_HEAD, text_color=LABEL_COLOUR).pack(pady=20)

        # Navigation buttons for different features
        ctk.CTkButton(self, text="View Games", command=lambda: master.switch_frame(ViewGamesPage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)
        ctk.CTkButton(self, text="Input Game Details", command=lambda: master.switch_frame(InputGamePage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)
        ctk.CTkButton(self, text="Delete Entry", command=lambda: master.switch_frame(DeleteGamePage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)
        ctk.CTkButton(self, text="Logout", command=self.logout,
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)
        ctk.CTkButton(self, text="Exit App", command=self.quit,
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)

    def logout(self):
        """
        Logs out the user and returns to login page.
        """
        self.master.logged_in_user = None
        self.master.switch_frame(LoginPage)

# ===============================================================
# ViewGamesPage Frame
# Displays the game collection with filtering
# ===============================================================

class ViewGamesPage(ctk.CTkFrame):
    def __init__(self, master):
        """
        Shows the full game list with platform filters.
        """
        super().__init__(master, fg_color=BG_COLOUR)
        master.geometry("850x550")

        ctk.CTkLabel(self, text="Game List", font=FONT_HEAD, text_color=LABEL_COLOUR).pack(pady=10)

        # Textbox for displaying games
        self.textbox = ctk.CTkTextbox(self, width=750, height=325, font=FONT_BODY, fg_color=LIST_BG_COLOUR)
        self.textbox.pack(pady=10)
        self.display_games("All")  # Default to show all games

        # Filter buttons for platforms
        filter_frame = ctk.CTkFrame(self, fg_color=BG_COLOUR)
        filter_frame.pack(pady=10)

        for platform in ["All"] + PLATFORMS:
            btn_colour = FILTER_COLOUR
            if platform == "Other":
                btn_colour = "#FF6F61"  # Special colour for "Other"
            ctk.CTkButton(filter_frame, text=platform, command=lambda p=platform: self.display_games(p),
                          font=FONT_BODY, fg_color=btn_colour, text_color="white").pack(side="left", padx=5)

        # Navigation back to main menu
        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(MainMenuPage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)

    def display_games(self, platform_filter):
        """
        Populates the textbox with games, filtered by platform.
        """
        self.textbox.delete("1.0", "end")
        with open(GAME_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if platform_filter == "All" or row["Platform"] == platform_filter:
                    self.textbox.insert("end", f"{row['Name']} - {row['Platform']} - {row['Format']}\n")

# ===============================================================
# InputGamePage Frame
# Allows users to add new games to the collection
# ===============================================================

class InputGamePage(ctk.CTkFrame):
    def __init__(self, master):
        """
        Form for adding a new game (name, platform, format).
        """
        super().__init__(master, fg_color=BG_COLOUR)
        master.geometry("300x350")

        ctk.CTkLabel(self, text="Input Game Details", font=FONT_HEAD, text_color=LABEL_COLOUR).pack(pady=10)

        # Game name entry
        ctk.CTkLabel(self, text="Game Name:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.name_entry = ctk.CTkEntry(self, font=FONT_BODY, text_color=ENTRY_COLOUR)
        self.name_entry.pack(pady=5)

        # Platform dropdown
        ctk.CTkLabel(self, text="Platform:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.platform_option = ctk.CTkOptionMenu(self, values=PLATFORMS, font=FONT_BODY,
                                                 dropdown_fg_color=DROPDOWN_COLOUR)
        self.platform_option.pack(pady=5)

        # Format dropdown
        ctk.CTkLabel(self, text="Format:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.format_option = ctk.CTkOptionMenu(self, values=FORMATS, font=FONT_BODY,
                                               dropdown_fg_color=DROPDOWN_COLOUR)
        self.format_option.pack(pady=5)

        # Save button
        ctk.CTkButton(self, text="Save", command=self.save_game,
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)

        # Navigation back to main menu
        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(MainMenuPage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack()

    def save_game(self):
        """
        Saves the new game entry to GAME_FILE if name is provided.
        """
        name = self.name_entry.get()
        platform = self.platform_option.get()
        format_ = self.format_option.get()
        if name:
            with open(GAME_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, platform, format_])
            messagebox.showinfo("Saved", "Game added!")
            self.name_entry.delete(0, "end")
        else:
            messagebox.showerror("Error", "Game name required.")

# ===============================================================
# DeleteGamePage Frame
# Allows users to delete a game entry by name and platform
# ===============================================================

class DeleteGamePage(ctk.CTkFrame):
    def __init__(self, master):
        """
        Form to delete a game entry by specifying name and platform.
        """
        super().__init__(master, fg_color=BG_COLOUR)
        master.geometry("300x350")

        ctk.CTkLabel(self, text="Delete Game Entry", font=FONT_HEAD, text_color=LABEL_COLOUR).pack(pady=10)

        # Game name entry
        ctk.CTkLabel(self, text="Game Name:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.name_entry = ctk.CTkEntry(self, font=FONT_BODY, text_color=ENTRY_COLOUR)
        self.name_entry.pack(pady=5)

        # Platform dropdown
        ctk.CTkLabel(self, text="Platform:", font=FONT_BODY, text_color=LABEL_COLOUR).pack()
        self.platform_option = ctk.CTkOptionMenu(self, values=PLATFORMS, font=FONT_BODY,
                                                 dropdown_fg_color=DROPDOWN_COLOUR)
        self.platform_option.pack(pady=5)

        # Delete button
        ctk.CTkButton(self, text="Delete", command=self.delete_game,
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack(pady=10)

        # Navigation back to main menu
        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(MainMenuPage),
                      font=FONT_BODY, fg_color=BTN_COLOUR).pack()

    def delete_game(self):
        """
        Deletes the specified game entry from GAME_FILE.
        """
        name = self.name_entry.get()
        platform = self.platform_option.get()
        rows = []
        deleted = False
        with open(GAME_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # If row matches both name and platform, skip (delete)
                if row["Name"] == name and row["Platform"] == platform:
                    deleted = True
                else:
                    rows.append(row)
        # Write updated list back to file
        with open(GAME_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=EXPECTED_HEADER)
            writer.writeheader()
            writer.writerows(rows)
        if deleted:
            messagebox.showinfo("Deleted", "Game deleted successfully.")
        else:
            messagebox.showerror("Error", "Game not found.")

# ===============================================================
# Application Entry Point
# Sets appearance mode and launches the main app window
# ===============================================================

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Sets UI to light mode
    app = GameApp()                   # Creates the main application
    app.mainloop()                    # Starts the Tkinter event loop