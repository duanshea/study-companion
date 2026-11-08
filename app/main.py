import tkinter as tk
import webbrowser
from tkinter import ttk
import json
from datetime import date, datetime
import calendar

def load_progress():
    today = date.today().isoformat()

    try:
        with open("data/progress.json", "r", encoding="utf-8") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        data = {"history": {}, "today": {}}

    if "history" not in data:
        data["history"] = {}

    today_data = data.get("today", {})

    if today_data.get("date") != today:
        today_data = {
            "date": today,
            "cpp_count": 0,
            "linux_count": 0
        }

    data["today"] = today_data

    return data

def save_progress():
    progress_data["today"]["cpp_count"] = cpp_count
    progress_data["today"]["linux_count"] = linux_count

    progress_data["history"][progress_data["today"]["date"]] = {
        "cpp_count": cpp_count,
        "linux_count": linux_count
    }

    with open("data/progress.json", "w", encoding="utf-8") as file:
        json.dump(progress_data, file, indent=4)

# 1. Create the main window
root = tk.Tk()

# 2. Configure the window
root.title("Study Companion")
root.geometry("600x1080")
root.configure(bg="#F5F5F5")

# 3. Create a welcome message
welcome_label = tk.Label(
    root,
    text="Hello, Xiaoyue:)",
    font=("Arial", 18, "bold"),
    bg="#F5F5F5",
    fg="#333333"
)

welcome_label.pack(pady=10,padx = 50)

progress_data = load_progress()

today_data = progress_data["today"]

cpp_count = today_data["cpp_count"]
cpp_target = 3

linux_count = today_data["linux_count"]
linux_target = 5

# Learning tasks section
tasks_label = tk.Label(
    root,
    text="Today's Learning",
    font=("Arial", 14, "bold"),
    bg="#F5F5F5",
    fg="#333333"
)

tasks_label.pack(pady=10)


cpp_label = tk.Label(
    root,
    text=f"C++: {cpp_count}/{cpp_target} questions",
    font=("Arial", 12),
    bg="#F5F5F5",
    fg="#333333"
)
cpp_label.pack(pady=10)

def open_cpp():
    webbrowser.open("https://www.hackerrank.com/domains/cpp")

cpp_button = tk.Button(
    root,
    text="Practice C++",
    command=open_cpp,
    font=("Arial", 11)
)
cpp_button.pack(pady=5)

cpp_progress = ttk.Progressbar(
    root,
    length=250,
    maximum=cpp_target,
    value=cpp_count
)
cpp_progress.pack(pady=10)

def increase_cpp():
    global cpp_count
    if cpp_count < cpp_target:
        cpp_count += 1
        cpp_label.config(
            text=f"C++: {cpp_count}/{cpp_target} questions"
        )


        cpp_progress.config(value=cpp_count)
        save_progress()
        update_calendar()


cpp_add_button = tk.Button(
    root,
    text="+",
    command=increase_cpp,
    font=("Arial", 11)
)
cpp_add_button.pack(pady=5)




linux_label = tk.Label(
    root,
    text=f"Linux: {linux_count}/{linux_target} exercises",
    font=("Arial", 12),
    bg="#F5F5F5",
    fg="#333333"
)
linux_label.pack(pady=10)

def open_linux():
    webbrowser.open("https://www.hackerrank.com/domains/shell")


linux_button = tk.Button(
    root,
    text="Practice Linux",
    command=open_linux,
    font=("Arial", 11)
)
linux_button.pack(pady=5)

linux_progress = ttk.Progressbar(
    root,
    length=250,
    maximum=linux_target,
    value=linux_count
)
linux_progress.pack(pady=10)



def increase_linux():
    global linux_count
    if linux_count < linux_target:
        linux_count += 1
        linux_label.config(
            text=f"Linux: {linux_count}/{linux_target} exercises"
        )

    linux_progress.config(value=linux_count)

    save_progress()
    update_calendar()

linux_add_button = tk.Button(
    root,
    text="+",
    command=increase_linux,
    font=("Arial", 11)
)
linux_add_button.pack(pady=5)

calendar_title = tk.Label(
    root,
    text="Study Calendar",
    font=("Arial", 14, "bold"),
    bg="#F5F5F5",
    fg="#333333"
)
calendar_title.pack(pady=15)

view_year = date.today().year
view_month = date.today().month

month_name = calendar.month_name[view_month]


def previous_month():
    global view_year, view_month

    if view_month == 1:
        view_month = 12
        view_year -= 1
    else:
        view_month -= 1

    show_calendar()


def next_month():
    global view_year, view_month

    if view_month == 12:
        view_month = 1
        view_year += 1
    else:
        view_month += 1

    show_calendar()

month_label = tk.Label(
    root,
    text=f"{month_name} {view_year}",
    font=("Arial", 12, "bold"),
    bg="#F5F5F5",
    fg="#555555"
)
month_nav = tk.Frame(
    root,
    bg="#F5F5F5"
)
month_nav.pack(pady=5)

previous_button = tk.Button(
    month_nav,
    text="←",
    command=previous_month,
    font=("Arial", 11)
)
previous_button.pack(side="left", padx=15)

month_label.pack(side="left", padx=15)

next_button = tk.Button(
    month_nav,
    text="→",
    command=next_month,
    font=("Arial", 11)
)
next_button.pack(side="left", padx=15)



detail_label = tk.Label(
    root,
    text="Click a date to see your study record",
    font=("Arial", 10),
    bg="#F5F5F5",
    fg="#555555"
)
detail_label.pack(pady=10)

calendar_frame = tk.Frame(
    root,
    bg="#F5F5F5"
)
calendar_frame.pack(pady=15, padx=10, fill="x")

calendar_day_labels = {}

def show_day_details(day):
    selected_date = date(view_year, view_month, day)
    date_key = selected_date.isoformat()

    record = progress_data["history"].get(date_key, {})

    cpp_done = record.get("cpp_count", 0)
    linux_done = record.get("linux_count", 0)

    detail_label.config(
        text=f"{date_key}\nC++: {cpp_done}/3    Linux: {linux_done}/5"
    )


def show_calendar():
    # Update month title
    month_name = calendar.month_name[view_month]
    month_label.config(text=f"{month_name} {view_year}")

    # Clear old calendar
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    # Read check-in history
    checked_dates = set()

    for saved_date, record in progress_data["history"].items():
        saved_day = datetime.strptime(saved_date, "%Y-%m-%d").date()

        if saved_day.year == view_year and saved_day.month == view_month:
            if record["cpp_count"] > 0 or record["linux_count"] > 0:
                checked_dates.add(saved_day.day)

    # Display weekdays
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for col, weekday in enumerate(weekdays):
        day_label = tk.Label(
            calendar_frame,
            text=weekday,
            font=("Arial", 10, "bold"),
            bg="#F5F5F5",
            fg="#777777",
            width=5
        )
        day_label.grid(row=0, column=col, padx=3, pady=8)

    # Generate dates
    month_calendar = calendar.monthcalendar(view_year, view_month)

    calendar_day_labels.clear()

    for row, week in enumerate(month_calendar, start=1):
        for col, day in enumerate(week):
            if day != 0:
                day_color = "#C8E6C9" if day in checked_dates else "#FFFFFF"

                day_label = tk.Label(
                    calendar_frame,
                    text=str(day),
                    font=("Arial", 11, "bold") if day in checked_dates else ("Arial", 11),
                    bg=day_color,
                    fg="#2E7D32" if day in checked_dates else "#333333",
                    width=5,
                    height=2
                )

                day_label.grid(row=row, column=col, padx=3, pady=4)

                calendar_day_labels[day] = day_label

                day_label.bind(
                    "<Button-1>",
                    lambda event, d=day: show_day_details(d)
                )


def update_calendar():
    show_calendar()


# Draw calendar for the first time
show_calendar()

# Task 3
project_label = tk.Label(
    root,
    text="Personal Project     0 / 60 minutes",
    font=("Arial", 11),
    bg="#F5F5F5"
)

project_label.pack(pady=8)



# 4. Start the application
root.mainloop()