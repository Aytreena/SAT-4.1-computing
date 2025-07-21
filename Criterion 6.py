import customtkinter as ctk
import csv
import os
from tkinter import messagebox

# File
GAME_FILE = "games.csv"
EXPECTED_HEADER = ["Name", "Platform", "Format"]

# Auto-fix CSV header function
def fix_csv_header():
    if not os.path.exists(GAME_FILE):
        # Create file with header if doesn't exist
        with open(GAME_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(EXPECTED_HEADER)
    else:
        with open(GAME_FILE, "r", newline="") as f:
            lines = f.readlines()
        # Check if file empty or header invalid
        if not lines or lines[0].strip().split(",") != EXPECTED_HEADER:
            # Rewrite with correct header + existing data (if any)
            data_lines = lines[1:] if len(lines) > 1 else []
            with open(GAME_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_HEADER)
                for line in data_lines:
                    f.write(line)

# Run header fix before app starts
fix_csv_header()

# UI Constants
FONT_HEAD = ("Jaldi", 12, "bold")
FONT_BODY = ("Jaldi", 10)
BG_COLOR = "#7595F9"
BTN_COLOR = "#4B79FA"
ENTRY_COLOR = "#5263FA"
DROPDOWN_COLOR = "#3163F9"
FILTER_COLOR = "#4195EF"
LABEL_COLOR = "#A35AD8"
LIST_BG_COLOR = "#D9D9D9"

PLATFORMS = ["PC", "Xbox", "PlayStation", "Nintendo", "Other"]
FORMATS = ["Physical", "Digital"]


class GameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Collection")
        self.switch_frame(MainMenuPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_COLOR)
        master.geometry("300x350")

        ctk.CTkLabel(self, text="Main Menu", font=FONT_HEAD, text_color=LABEL_COLOR).pack(pady=20)

        ctk.CTkButton(self, text="View Games", command=lambda: master.switch_frame(ViewGamesPage),
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)
        ctk.CTkButton(self, text="Input Game Details", command=lambda: master.switch_frame(InputGamePage),
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)
        ctk.CTkButton(self, text="Delete Entry", command=lambda: master.switch_frame(DeleteGamePage),
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)
        ctk.CTkButton(self, text="Exit App", command=self.quit,
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)

class ViewGamesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_COLOR)
        master.geometry("850x550")

        ctk.CTkLabel(self, text="Game List", font=FONT_HEAD, text_color=LABEL_COLOR).pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=750, height=325, font=FONT_BODY, fg_color=LIST_BG_COLOR)
        self.textbox.pack(pady=10)
        self.display_games("All")

        filter_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        filter_frame.pack(pady=10)

        for platform in ["All"] + PLATFORMS:
            btn_color = FILTER_COLOR
            if platform == "Other":
                btn_color = "#FF6F61"  # Distinct color for "Other"
            ctk.CTkButton(filter_frame, text=platform, command=lambda p=platform: self.display_games(p),
                          font=FONT_BODY, fg_color=btn_color, text_color="white").pack(side="left", padx=5)

        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(MainMenuPage),
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)

    def display_games(self, platform_filter):
        self.textbox.delete("1.0", "end")
        with open(GAME_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if platform_filter == "All" or row["Platform"] == platform_filter:
                    self.textbox.insert("end", f"{row['Name']} - {row['Platform']} - {row['Format']}\n")

class InputGamePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_COLOR)
        master.geometry("300x350")

        ctk.CTkLabel(self, text="Input Game Details", font=FONT_HEAD, text_color=LABEL_COLOR).pack(pady=10)

        ctk.CTkLabel(self, text="Game Name:", font=FONT_BODY, text_color=LABEL_COLOR).pack()
        self.name_entry = ctk.CTkEntry(self, font=FONT_BODY, text_color=ENTRY_COLOR)
        self.name_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Platform:", font=FONT_BODY, text_color=LABEL_COLOR).pack()
        self.platform_option = ctk.CTkOptionMenu(self, values=PLATFORMS, font=FONT_BODY,
                                                 dropdown_fg_color=DROPDOWN_COLOR)
        self.platform_option.pack(pady=5)

        ctk.CTkLabel(self, text="Format:", font=FONT_BODY, text_color=LABEL_COLOR).pack()
        self.format_option = ctk.CTkOptionMenu(self, values=FORMATS, font=FONT_BODY,
                                               dropdown_fg_color=DROPDOWN_COLOR)
        self.format_option.pack(pady=5)

        ctk.CTkButton(self, text="Save", command=self.save_game,
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)

        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(MainMenuPage),
                      font=FONT_BODY, fg_color=BTN_COLOR).pack()

    def save_game(self):
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

class DeleteGamePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_COLOR)
        master.geometry("300x350")

        ctk.CTkLabel(self, text="Delete Game Entry", font=FONT_HEAD, text_color=LABEL_COLOR).pack(pady=10)

        ctk.CTkLabel(self, text="Game Name:", font=FONT_BODY, text_color=LABEL_COLOR).pack()
        self.name_entry = ctk.CTkEntry(self, font=FONT_BODY, text_color=ENTRY_COLOR)
        self.name_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Platform:", font=FONT_BODY, text_color=LABEL_COLOR).pack()
        self.platform_option = ctk.CTkOptionMenu(self, values=PLATFORMS, font=FONT_BODY,
                                                 dropdown_fg_color=DROPDOWN_COLOR)
        self.platform_option.pack(pady=5)

        ctk.CTkButton(self, text="Delete", command=self.delete_game,
                      font=FONT_BODY, fg_color=BTN_COLOR).pack(pady=10)

        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(MainMenuPage),
                      font=FONT_BODY, fg_color=BTN_COLOR).pack()

    def delete_game(self):
        name = self.name_entry.get()
        platform = self.platform_option.get()
        rows = []
        deleted = False
        with open(GAME_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Name"] == name and row["Platform"] == platform:
                    deleted = True
                else:
                    rows.append(row)
        with open(GAME_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=EXPECTED_HEADER)
            writer.writeheader()
            writer.writerows(rows)
        if deleted:
            messagebox.showinfo("Deleted", "Game deleted successfully.")
        else:
            messagebox.showerror("Error", "Game not found.")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = GameApp()
    app.mainloop()
