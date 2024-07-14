import tkinter as tk
from tkinter import messagebox
import cv2 as cv
import numpy as np
import PoseDetector as pd
import cx_Oracle

class PoseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pose Detection App")
        self.user_id = None
        self.login_screen()

    def login_screen(self):
        self.clear_window()
        self.root.geometry("800x600")
        self.root.configure(bg='#2E2E2E')

        tk.Label(self.root, text="Pose Detection App", font=("Helvetica", 18), bg='#2E2E2E', fg='white').pack(pady=20)

        tk.Label(self.root, text="Email", bg='#2E2E2E', fg='white').pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password", bg='#2E2E2E', fg='white').pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login, bg='#0078D7', fg='white').pack(pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            # Initialize Oracle client library
            cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_14")
            print("Oracle client initialized successfully.")

            # Construct DSN (Data Source Name)
            dsn = cx_Oracle.makedsn("db-oracle02.pjwstk.edu.pl", 1521, service_name="baza.pjwstk.edu.pl")
            print(f"DSN: {dsn}")

            # Establish connection
            conn = cx_Oracle.connect(user="s30942", password="oracle12", dsn=dsn)
            print("Connected to Oracle Database!")

            c = conn.cursor()

            # Execute query
            c.execute("SELECT id FROM PROFILE WHERE email=:email AND password=:password",
                      {'email': email, 'password': password})
            result = c.fetchone()
            conn.close()

            if result:
                self.user_id = result[0]
                self.main_screen()
            else:
                messagebox.showerror("Error", "Invalid email or password")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", f"Failed to connect to the database: {e}")
            print(f"Database Error: {e}")

    def main_screen(self):
        self.clear_window()
        self.root.geometry("800x600")
        self.root.configure(bg='#2E2E2E')

        top_frame = tk.Frame(self.root, bg='#2E2E2E')
        top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        app_name = tk.Label(top_frame, text="Pose Detection App", font=("Helvetica", 16), bg='#2E2E2E', fg='white')
        app_name.pack(side=tk.LEFT, padx=10, pady=10)

        profile_button = tk.Label(top_frame, text="Profile", font=("Helvetica", 14), bg='#2E2E2E', fg='white', cursor="hand2")
        profile_button.pack(side=tk.RIGHT, padx=10, pady=10)
        profile_button.bind("<Button-1>", self.show_profile)

        self.middle_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        button_font = ("Helvetica", 14)
        button_bg = '#4E4E4E'
        button_fg = 'white'

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_rowconfigure(2, weight=1)

        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(2, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)

        self.bicep_button = tk.Button(self.middle_frame, text="Bicep Curl", command=lambda: self.start_exercise("Bicep curl"),
                                      font=button_font, bg=button_bg, fg=button_fg, anchor='sw')
        self.bicep_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.legs_button = tk.Button(self.middle_frame, text="Legs", command=lambda: self.start_exercise("Legs"),
                                     font=button_font, bg=button_bg, fg=button_fg, anchor='sw')
        self.legs_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


    def show_profile(self, event=None):
        self.clear_window()
        self.root.geometry("1200x900")
        self.root.configure(bg='#2E2E2E')

        top_frame = tk.Frame(self.root, bg='#2E2E2E')
        top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        app_name = tk.Label(top_frame, text="Profile", font=("Helvetica", 16), bg='#2E2E2E', fg='white')
        app_name.pack(side=tk.LEFT, padx=10, pady=10)

        profile_button = tk.Label(top_frame, text="Back to Main", font=("Helvetica", 14), bg='#2E2E2E', fg='white', cursor="hand2")
        profile_button.pack(side=tk.RIGHT, padx=10, pady=10)
        profile_button.bind("<Button-1>", lambda event: self.main_screen())

        self.middle_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        button_font = ("Helvetica", 14)
        button_bg = '#4E4E4E'
        button_fg = 'white'

        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(2, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)

        last_workout_button = tk.Button(self.middle_frame, text="Last workout", command=self.show_last_workout,
                                        font=button_font, bg=button_bg, fg=button_fg, anchor='sw')
        last_workout_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        details_button = tk.Button(self.middle_frame, text="Details", command=self.show_details,
                                   font=button_font, bg=button_bg, fg=button_fg, anchor='sw')
        details_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def show_last_workout(self):
        self.clear_window()  # Clear the window before displaying last workout info

        try:
            # Construct DSN (Data Source Name)
            dsn = cx_Oracle.makedsn("db-oracle02.pjwstk.edu.pl", 1521, service_name="baza.pjwstk.edu.pl")

            # Establish connection
            conn = cx_Oracle.connect(user="s30942", password="oracle12", dsn=dsn)
            print("Connected to Oracle Database!")

            c = conn.cursor()

            c.execute("""
                        SELECT w.WorkoutTime, e.Name, t.Reps
                        FROM Workout w
                        JOIN Training t ON w.Training_id = t.id
                        JOIN Exercise e ON t.Exercise_id = e.id
                        WHERE w.Profile_id = :profile_id
                        AND TRUNC(w.WorkoutTime) = (SELECT MAX(TRUNC(WorkoutTime)) FROM Workout WHERE Profile_id = :profile_id)
                    """, {'profile_id': self.user_id})

            rows = c.fetchall()

            if rows:
                info = "Last workouts:\n"
                current_date = None
                for row in rows:
                    workout_time, exercise_name, reps = row
                    info += f"\nWorkout Date: {workout_time.date()}\n"
                    current_date = workout_time.date()
                    info += f"Workout time: {workout_time}\nExercise: {exercise_name}\nReps: {reps}\n\n"

            tk.Button(self.root, text="Back to Profile", command=self.show_profile,
                      font=("Helvetica", 14), bg='#0078D7', fg='white').pack(pady=10)
            conn.close()
        except cx_Oracle.DatabaseError as e:
            print(f"Database Error: {e}")
            info = "No workout data available due to database error."

        self.display_info(info)

    def display_info(self, info):
        info_label = tk.Label(self.root, text=info, font=("Helvetica", 14), bg='#2E2E2E', fg='white')
        info_label.pack(expand=True)

    def show_goals(self):
        self.clear_window()
        self.display_info("Goals information...")
        back_button = tk.Button(self.root, text="Back to Profile", command=self.show_profile, font=("Helvetica", 14),
                                bg='#0078D7', fg='white')
        back_button.pack(pady=10)

    def show_details(self):
        self.clear_window()

        try:
            # Construct DSN (Data Source Name)
            dsn = cx_Oracle.makedsn("db-oracle02.pjwstk.edu.pl", 1521, service_name="baza.pjwstk.edu.pl")

            # Establish connection
            conn = cx_Oracle.connect(user="s30942", password="oracle12", dsn=dsn)
            print("Connected to Oracle Database!")

            c = conn.cursor()

            # Fetch profile details from the database
            c.execute("SELECT p.profile_name, p.name, p.email, p.phone, status.experience "
                      "FROM PROFILE p "
                      "join STATUS ON status.id = status_id "
                      "WHERE p.id=:id",
                      {'id': self.user_id})
            details = c.fetchone()

            if details:
                info = f"Profile Name: {details[0]}\nName: {details[1]}\nEmail: {details[2]}\nPhone: {details[3]}\nExperience: {details[4]}"
            else:
                info = "No profile details available."

            conn.close()
        except cx_Oracle.DatabaseError as e:
            print(f"Database Error: {e}")
            info = "Failed to retrieve profile details due to a database error."

        self.display_info(info)

        back_button = tk.Button(self.root, text="Back to Profile", command=self.show_profile,
                                font=("Helvetica", 14), bg='#0078D7', fg='white')
        back_button.pack(pady=10)

    def start_exercise(self, exercise):
        self.exercise = exercise
        self.count = 0
        self.direction = 0
        self.detector = pd.PoseDetector()
        self.cap = cv.VideoCapture(0)  # Change to your video source
        self.process_video()

    def process_video(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            return

        frame = self.detector.findPose(frame, False)
        lmList = self.detector.findPosition(frame, False)

        if len(lmList) != 0:
            if self.exercise == "Bicep curl":
                angle = self.detector.findAngle(frame, 12, 14, 16)
                per = np.interp(angle, (140, 80), (0, 100))
                if per == 100:
                    if self.direction == 0:
                        self.count += 0.5
                        self.direction = 1
                if per == 0:
                    if self.direction == 1:
                        self.count += 0.5
                        self.direction = 0
                cv.putText(frame, str(int(self.count - 0.5)), (50, 150), cv.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 2)
            elif self.exercise == "Legs":
                angle = self.detector.findAngle(frame, 23, 25, 27)
                per = np.interp(angle, (140, 80), (0, 100))
                if per == 100:
                    if self.direction == 0:
                        self.count += 0.5
                        self.direction = 1
                if per == 0:
                    if self.direction == 1:
                        self.count += 0.5
                        self.direction = 0

        cv.imshow("Pose Detection", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv.destroyAllWindows()
            return

        self.root.after(10, self.process_video)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PoseApp(root)
    root.mainloop()
