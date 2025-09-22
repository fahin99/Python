import random
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import hashlib
import threading
import time

class AnimatedBackground:
    """Animated background for welcome screen"""
    def __init__(self, canvas):
        self.canvas = canvas
        self.shapes = []
        self.animation_running = True
        self.create_shapes()
        self.animate()
    
    def create_shapes(self):
        """Create floating shapes for background animation"""
        for i in range(15):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            size = random.randint(20, 40)
            color = random.choice(['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
            shape_type = random.choice(['oval', 'rect'])
            
            if shape_type == 'oval':
                shape = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            else:
                shape = self.canvas.create_rectangle(x, y, x+size, y+size, fill=color, outline="")
            
            self.shapes.append({
                'id': shape,
                'x': x,
                'y': y,
                'dx': random.choice([-1, 1]) * random.uniform(0.5, 2),
                'dy': random.choice([-1, 1]) * random.uniform(0.5, 2),
                'size': size
            })
    
    def animate(self):
        """Animate the background shapes"""
        if not self.animation_running:
            return
        
        for shape in self.shapes:
            # Update position
            shape['x'] += shape['dx']
            shape['y'] += shape['dy']
            
            # Bounce off edges
            if shape['x'] <= 0 or shape['x'] >= 800 - shape['size']:
                shape['dx'] *= -1
            if shape['y'] <= 0 or shape['y'] >= 600 - shape['size']:
                shape['dy'] *= -1
            
            # Update canvas position
            self.canvas.coords(shape['id'], shape['x'], shape['y'], 
                             shape['x'] + shape['size'], shape['y'] + shape['size'])
        
        # Schedule next animation frame
        self.canvas.after(50, self.animate)
    
    def stop(self):
        """Stop the animation"""
        self.animation_running = False

class LoginScreen:
    """Login and registration screen"""
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.users_file = "users.json"
        self.current_user = None
        
        # CSS colors
        self.colors = {
            'primary': '#1f2937',
            'secondary': '#374151',
            'accent': '#3b82f6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'light': '#f9fafb',
            'white': '#ffffff',
            'text': '#111827',
            'text_light': '#6b7280',
        }
        
        self.setup_welcome_screen()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self, users):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save user data: {e}")
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setup_welcome_screen(self):
        """Setup animated welcome screen"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Rock Paper Scissors - Welcome")
        self.root.geometry("800x600")
        self.root.configure(bg=self.colors['primary'])
        
        # Create animated background
        self.bg_canvas = tk.Canvas(self.root, bg=self.colors['primary'], highlightthickness=0)
        self.bg_canvas.pack(fill='both', expand=True)
        
        self.animated_bg = AnimatedBackground(self.bg_canvas)
        
        # Welcome content overlay
        content_frame = tk.Frame(self.bg_canvas, bg=self.colors['primary'])
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Game title with animation effect
        title_label = tk.Label(content_frame, text="🎮 ROCK PAPER SCISSORS 🎮", 
                              font=("Arial", 28, "bold"), 
                              fg=self.colors['white'], bg=self.colors['primary'])
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(content_frame, text="Ultimate Gaming Experience", 
                                 font=("Arial", 14), 
                                 fg=self.colors['text_light'], bg=self.colors['primary'])
        subtitle_label.pack(pady=(0, 30))
        
        # Login/Register buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(button_frame, text="🔑 Login", 
                             font=("Arial", 14, "bold"), width=15,
                             bg=self.colors['accent'], fg=self.colors['white'],
                             relief='flat', padx=20, pady=10, cursor='hand2',
                             command=self.show_login_form)
        login_btn.pack(side='left', padx=10)
        
        register_btn = tk.Button(button_frame, text="📝 Register", 
                                font=("Arial", 14, "bold"), width=15,
                                bg=self.colors['success'], fg=self.colors['white'],
                                relief='flat', padx=20, pady=10, cursor='hand2',
                                command=self.show_register_form)
        register_btn.pack(side='left', padx=10)
        
        # Guest play option
        guest_btn = tk.Button(content_frame, text="👤 Play as Guest", 
                             font=("Arial", 12), 
                             bg=self.colors['secondary'], fg=self.colors['white'],
                             relief='flat', padx=15, pady=8, cursor='hand2',
                             command=lambda: self.login_as_guest())
        guest_btn.pack(pady=(20, 0))
    
    def show_login_form(self):
        """Show login form"""
        self.animated_bg.stop()
        self.bg_canvas.destroy()
        
        # Login form
        login_frame = tk.Frame(self.root, bg=self.colors['light'], padx=50, pady=50)
        login_frame.pack(expand=True, fill='both')
        
        # Header
        header_frame = tk.Frame(login_frame, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔑 User Login", font=("Arial", 20, "bold"),
                bg=self.colors['primary'], fg=self.colors['white']).pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(login_frame, bg=self.colors['white'], padx=40, pady=40)
        form_frame.pack(expand=True, fill='both')
        
        tk.Label(form_frame, text="Username:", font=("Arial", 12, "bold"),
                bg=self.colors['white'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, relief='flat', bd=10)
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(form_frame, text="Password:", font=("Arial", 12, "bold"),
                bg=self.colors['white'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show='*', relief='flat', bd=10)
        self.password_entry.pack(fill='x', pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['white'])
        btn_frame.pack(fill='x', pady=10)
        
        login_submit_btn = tk.Button(btn_frame, text="Login", font=("Arial", 12, "bold"),
                                    bg=self.colors['accent'], fg=self.colors['white'],
                                    relief='flat', padx=20, pady=8, cursor='hand2',
                                    command=self.process_login)
        login_submit_btn.pack(side='left', padx=(0, 10))
        
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12),
                            bg=self.colors['secondary'], fg=self.colors['white'],
                            relief='flat', padx=20, pady=8, cursor='hand2',
                            command=self.setup_welcome_screen)
        back_btn.pack(side='left')
        
        # Focus on username entry
        self.username_entry.focus_set()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.process_login())
    
    def show_register_form(self):
        """Show registration form"""
        self.animated_bg.stop()
        self.bg_canvas.destroy()
        
        # Registration form
        register_frame = tk.Frame(self.root, bg=self.colors['light'], padx=50, pady=50)
        register_frame.pack(expand=True, fill='both')
        
        # Header
        header_frame = tk.Frame(register_frame, bg=self.colors['success'], height=80)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📝 Create Account", font=("Arial", 20, "bold"),
                bg=self.colors['success'], fg=self.colors['white']).pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(register_frame, bg=self.colors['white'], padx=40, pady=40)
        form_frame.pack(expand=True, fill='both')
        
        tk.Label(form_frame, text="Username:", font=("Arial", 12, "bold"),
                bg=self.colors['white'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        self.reg_username_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, relief='flat', bd=10)
        self.reg_username_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(form_frame, text="Password:", font=("Arial", 12, "bold"),
                bg=self.colors['white'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        self.reg_password_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show='*', relief='flat', bd=10)
        self.reg_password_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12, "bold"),
                bg=self.colors['white'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        self.reg_confirm_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show='*', relief='flat', bd=10)
        self.reg_confirm_entry.pack(fill='x', pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['white'])
        btn_frame.pack(fill='x', pady=10)
        
        register_submit_btn = tk.Button(btn_frame, text="Create Account", font=("Arial", 12, "bold"),
                                       bg=self.colors['success'], fg=self.colors['white'],
                                       relief='flat', padx=20, pady=8, cursor='hand2',
                                       command=self.process_registration)
        register_submit_btn.pack(side='left', padx=(0, 10))
        
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12),
                            bg=self.colors['secondary'], fg=self.colors['white'],
                            relief='flat', padx=20, pady=8, cursor='hand2',
                            command=self.setup_welcome_screen)
        back_btn.pack(side='left')
        
        # Focus on username entry
        self.reg_username_entry.focus_set()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.process_registration())
    
    def process_login(self):
        """Process login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        users = self.load_users()
        hashed_password = self.hash_password(password)
        
        if username in users and users[username]['password'] == hashed_password:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.on_login_success(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    
    def process_registration(self):
        """Process registration"""
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match!")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters!")
            return
        
        users = self.load_users()
        
        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return
        
        # Create new user
        users[username] = {
            'password': self.hash_password(password),
            'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'high_scores': {
                "best_streak": 0,
                "total_wins": 0,
                "total_games": 0,
                "win_percentage": 0.0,
                "last_updated": ""
            }
        }
        
        self.save_users(users)
        self.current_user = username
        messagebox.showinfo("Success", f"Account created successfully! Welcome, {username}!")
        self.on_login_success(username)
    
    def login_as_guest(self):
        """Login as guest user"""
        self.current_user = "Guest"
        self.animated_bg.stop()
        self.on_login_success("Guest")

class ScrollableFrame(tk.Frame):
    """A scrollable frame for the main content"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=kwargs.get('bg', '#f9fafb'))
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get('bg', '#f9fafb'))
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack elements
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.bind_mousewheel()
        
        # Update canvas width when window resizes
        self.canvas.bind('<Configure>', self.on_canvas_configure)
    
    def on_canvas_configure(self, event):
        # Update the scrollable frame width to match canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.find_all()[0], width=canvas_width)
    
    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.users_file = "users.json"
        
        self.root.title("Rock Paper Scissors")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # CSS-inspired color palette (Tailwind CSS colors)
        self.css_colors = {
            'primary': '#1f2937',      # gray-800
            'secondary': '#374151',    # gray-700
            'accent': '#3b82f6',       # blue-500
            'success': '#10b981',      # emerald-500
            'warning': '#f59e0b',      # amber-500
            'danger': '#ef4444',       # red-500
            'light': '#f9fafb',        # gray-50
            'white': '#ffffff',
            'text': '#111827',         # gray-900
            'text_light': '#6b7280',   # gray-500
            'border': '#d1d5db',       # gray-300
            'hover': '#f3f4f6'         # gray-100
        }
        
        # Configure root styling
        self.root.configure(bg=self.css_colors['light'])
        
        # Game state
        self.player_score = 0
        self.computer_score = 0
        self.current_streak = 0
        self.total_games = 0
        self.total_wins = 0
        self.animation_active = False
        
        # Start with login screen
        self.login_screen = LoginScreen(root, self.on_login_success)
    
    def on_login_success(self, username):
        """Called when user successfully logs in"""
        self.current_user = username
        self.load_user_scores()
        self.setup_ui()
        self.setup_keyboard_bindings()
    
    def load_user_scores(self):
        """Load user-specific high scores"""
        if self.current_user == "Guest":
            self.high_scores = {
                "best_streak": 0,
                "total_wins": 0,
                "total_games": 0,
                "win_percentage": 0.0,
                "last_updated": ""
            }
        else:
            try:
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
                    self.high_scores = users.get(self.current_user, {}).get('high_scores', {
                        "best_streak": 0,
                        "total_wins": 0,
                        "total_games": 0,
                        "win_percentage": 0.0,
                        "last_updated": ""
                    })
            except:
                self.high_scores = {
                    "best_streak": 0,
                    "total_wins": 0,
                    "total_games": 0,
                    "win_percentage": 0.0,
                    "last_updated": ""
                }
    
    def save_high_scores(self):
        """Save high scores for current user"""
        if self.current_user == "Guest":
            return  # Don't save guest scores
        
        try:
            users = {}
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
            
            if self.current_user in users:
                users[self.current_user]['high_scores'] = self.high_scores
                
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save high scores: {e}")

    def update_high_scores(self, won_round):
        """Update high scores based on game result"""
        self.total_games += 1
        
        if won_round:
            self.current_streak += 1
            self.total_wins += 1
            if self.current_streak > self.high_scores["best_streak"]:
                self.high_scores["best_streak"] = self.current_streak
                # Show achievement notification
                self.show_achievement("New Best Streak!", f"Congratulations! New record: {self.current_streak} wins!")
        else:
            self.current_streak = 0
        
        self.high_scores["total_wins"] = max(self.high_scores["total_wins"], self.total_wins)
        self.high_scores["total_games"] = max(self.high_scores["total_games"], self.total_games)
        
        if self.total_games > 0:
            win_percentage = (self.total_wins / self.total_games) * 100
            if win_percentage > self.high_scores["win_percentage"]:
                self.high_scores["win_percentage"] = win_percentage
                if self.total_games >= 10:  # Only show for meaningful sample size
                    self.show_achievement("New Best Win Rate!", f"New record: {win_percentage:.1f}%!")
        
        self.high_scores["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_high_scores()
    
    def show_achievement(self, title, message):
        """Modern CSS-styled achievement popup"""
        achievement = tk.Toplevel(self.root)
        achievement.title("Achievement!")
        achievement.geometry("350x200")
        achievement.resizable(False, False)
        achievement.configure(bg=self.css_colors['success'])
        achievement.transient(self.root)
        achievement.grab_set()
        
        # Center the popup
        achievement.update_idletasks()
        x = (achievement.winfo_screenwidth() // 2) - (350 // 2)
        y = (achievement.winfo_screenheight() // 2) - (200 // 2)
        achievement.geometry(f"350x200+{x}+{y}")
        
        # CSS-like container
        container = tk.Frame(achievement, bg=self.css_colors['success'], padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        # Icon
        icon = tk.Label(container, text="🏆", font=("Arial", 30), 
                       bg=self.css_colors['success'], fg=self.css_colors['white'])
        icon.pack(pady=(0, 10))
        
        # Title
        title_label = tk.Label(container, text=title, font=("Arial", 14, "bold"),
                              bg=self.css_colors['success'], fg=self.css_colors['white'])
        title_label.pack(pady=(0, 5))
        
        # Message
        msg_label = tk.Label(container, text=message, font=("Arial", 11),
                            bg=self.css_colors['success'], fg=self.css_colors['white'])
        msg_label.pack(pady=(0, 15))
        
        # Button with CSS-like styling
        btn = tk.Button(container, text="Awesome!", font=("Arial", 10, "bold"),
                       bg=self.css_colors['white'], fg=self.css_colors['success'],
                       relief='flat', padx=20, pady=8, cursor='hand2',
                       command=achievement.destroy)
        btn.pack()
        
        # Auto-close
        achievement.after(4000, achievement.destroy)

    def show_high_scores(self):
        """Fixed CSS-styled high scores window with proper button alignment"""
        hs_window = tk.Toplevel(self.root)
        hs_window.title(f"High Scores - {self.current_user}")
        hs_window.geometry("500x450")
        hs_window.configure(bg=self.css_colors['light'])
        hs_window.transient(self.root)
        hs_window.grab_set()
        hs_window.resizable(True, True)
        
        # Configure grid weights for resizing
        hs_window.columnconfigure(0, weight=1)
        hs_window.rowconfigure(1, weight=1)
        
        # Center window
        hs_window.update_idletasks()
        x = (hs_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (hs_window.winfo_screenheight() // 2) - (450 // 2)
        hs_window.geometry(f"500x450+{x}+{y}")
        
        # Header (CSS-like)
        header = tk.Frame(hs_window, bg=self.css_colors['primary'], height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.pack_propagate(False)
        
        header_label = tk.Label(header, text=f"🏆 {self.current_user}'s High Scores", font=("Arial", 18, "bold"),
                               bg=self.css_colors['primary'], fg=self.css_colors['white'])
        header_label.pack(expand=True)
        
        # Main content container
        main_content = tk.Frame(hs_window, bg=self.css_colors['light'])
        main_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_content.columnconfigure(0, weight=1)
        main_content.rowconfigure(0, weight=1)
        
        # Content area with proper grid
        content = tk.Frame(main_content, bg=self.css_colors['white'], padx=20, pady=20)
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        
        # Stats cards with improved layout
        stats_frame = tk.Frame(content, bg=self.css_colors['white'])
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        stats_frame.columnconfigure(0, weight=1)
        
        stats = [
            ("🔥 Best Streak", self.high_scores['best_streak']),
            ("🎯 Total Wins", self.high_scores['total_wins']),
            ("🎮 Total Games", self.high_scores['total_games']),
            ("📊 Win Rate", f"{self.high_scores['win_percentage']:.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=self.css_colors['accent'], relief='flat')
            card.grid(row=i, column=0, sticky="ew", pady=3)
            card.columnconfigure(0, weight=1)
            card.columnconfigure(1, weight=0)
            
            left_label = tk.Label(card, text=label, font=("Arial", 12),
                                 bg=self.css_colors['accent'], fg=self.css_colors['white'], 
                                 anchor='w', padx=15, pady=8)
            left_label.grid(row=0, column=0, sticky="ew")
            
            right_label = tk.Label(card, text=str(value), font=("Arial", 12, "bold"),
                                  bg=self.css_colors['accent'], fg=self.css_colors['white'], 
                                  anchor='e', padx=15, pady=8)
            right_label.grid(row=0, column=1, sticky="e")
        
        # Current session
        if self.player_score + self.computer_score > 0:
            session_frame = tk.Frame(content, bg=self.css_colors['white'])
            session_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
            
            session_title = tk.Label(session_frame, text="Current Session", font=("Arial", 12, "bold"),
                                    bg=self.css_colors['white'], fg=self.css_colors['text'])
            session_title.pack(pady=(0, 5))
            
            session_text = f"Wins: {self.player_score} | Losses: {self.computer_score} | Streak: {self.current_streak}"
            session_label = tk.Label(session_frame, text=session_text, font=("Arial", 10),
                                    bg=self.css_colors['white'], fg=self.css_colors['text_light'])
            session_label.pack()
        
        # Fixed buttons with proper alignment
        btn_frame = tk.Frame(hs_window, bg=self.css_colors['light'])
        btn_frame.grid(row=2, column=0, sticky="ew", pady=15)
        
        # Center the buttons properly
        btn_container = tk.Frame(btn_frame, bg=self.css_colors['light'])
        btn_container.pack(expand=True)
        
        if self.current_user != "Guest":
            reset_btn = tk.Button(btn_container, text="Reset Scores", font=("Arial", 10, "bold"),
                                 bg=self.css_colors['danger'], fg=self.css_colors['white'],
                                 relief='flat', padx=15, pady=8, cursor='hand2',
                                 command=lambda: self.reset_high_scores(hs_window))
            reset_btn.pack(side='left', padx=5)
        
        close_btn = tk.Button(btn_container, text="Close", font=("Arial", 10, "bold"),
                             bg=self.css_colors['secondary'], fg=self.css_colors['white'],
                             relief='flat', padx=15, pady=8, cursor='hand2',
                             command=hs_window.destroy)
        close_btn.pack(side='left', padx=5)

    def reset_high_scores(self, window):
        """Reset all high scores"""
        if messagebox.askyesno("Reset High Scores", "Are you sure you want to reset all high scores?"):
            self.high_scores = {
                "best_streak": 0,
                "total_wins": 0,
                "total_games": 0,
                "win_percentage": 0.0,
                "last_updated": ""
            }
            self.save_high_scores()
            window.destroy()
            messagebox.showinfo("Reset Complete", "High scores have been reset!")
    
    def setup_keyboard_bindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<r>', lambda e: self.make_choice('rock'))
        self.root.bind('<p>', lambda e: self.make_choice('paper'))
        self.root.bind('<s>', lambda e: self.make_choice('scissors'))
        self.root.bind('<h>', lambda e: self.show_high_scores())
        self.root.bind('<Control-r>', lambda e: self.reset_game())
        self.root.bind('<Control-q>', lambda e: self.quit_game())
        self.root.focus_set()

    def animate_button(self, button):
        """Simple button animation"""
        if self.animation_active:
            return
        
        self.animation_active = True
        original_bg = button.cget('bg')
        button.config(bg=self.css_colors['white'])
        self.root.after(100, lambda: button.config(bg=original_bg))
        self.root.after(150, lambda: setattr(self, 'animation_active', False))

    def setup_ui(self):
        """Setup main UI with CSS-like styling and scrolling"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Rock Paper Scissors - {self.current_user}")
        
        # Create scrollable main container
        self.scrollable_container = ScrollableFrame(self.root, bg=self.css_colors['light'])
        self.scrollable_container.grid(row=0, column=0, sticky="nsew")
        
        # Main container inside scrollable frame
        main_container = self.scrollable_container.scrollable_frame
        main_container.columnconfigure(0, weight=1)
        
        # Header section with user info
        header_section = tk.Frame(main_container, bg=self.css_colors['primary'], height=80)
        header_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_section.columnconfigure(0, weight=1)
        header_section.pack_propagate(False)
        
        title_container = tk.Frame(header_section, bg=self.css_colors['primary'])
        title_container.pack(expand=True, fill='x')
        
        title_label = tk.Label(title_container, text="🎮 Rock Paper Scissors", 
                              font=("Arial", 24, "bold"), 
                              bg=self.css_colors['primary'], fg=self.css_colors['white'])
        title_label.pack()
        
        user_label = tk.Label(title_container, text=f"Playing as: {self.current_user}", 
                             font=("Arial", 12), 
                             bg=self.css_colors['primary'], fg=self.css_colors['text_light'])
        user_label.pack()
        
        # Score card (CSS card component)
        score_card = tk.Frame(main_container, bg=self.css_colors['white'], 
                             relief='flat', padx=20, pady=15)
        score_card.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        score_card.columnconfigure(0, weight=1)
        
        score_title = tk.Label(score_card, text="Current Game", font=("Arial", 14, "bold"),
                              bg=self.css_colors['white'], fg=self.css_colors['text'])
        score_title.pack(pady=(0, 10))
        
        self.score_label = tk.Label(score_card, 
                                   text=f"Player {self.player_score} - {self.computer_score} Computer",
                                   font=("Arial", 18, "bold"), 
                                   bg=self.css_colors['white'], fg=self.css_colors['accent'])
        self.score_label.pack()
        
        self.streak_label = tk.Label(score_card, text=f"🔥 Current Streak: {self.current_streak}",
                                    font=("Arial", 12), 
                                    bg=self.css_colors['white'], fg=self.css_colors['warning'])
        self.streak_label.pack(pady=(5, 0))
        
        # Game buttons section (CSS button group)
        button_section = tk.Frame(main_container, bg=self.css_colors['white'], 
                                 relief='flat', padx=20, pady=20)
        button_section.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        button_section.columnconfigure(0, weight=1)
        
        button_title = tk.Label(button_section, text="Make Your Move", font=("Arial", 14, "bold"),
                               bg=self.css_colors['white'], fg=self.css_colors['text'])
        button_title.pack(pady=(0, 5))
        
        hint_label = tk.Label(button_section, text="Click buttons or press R/P/S keys", 
                             font=("Arial", 10), 
                             bg=self.css_colors['white'], fg=self.css_colors['text_light'])
        hint_label.pack(pady=(0, 15))
        
        # Button container
        button_container = tk.Frame(button_section, bg=self.css_colors['white'])
        button_container.pack()
        
        # Game buttons with proper command binding
        self.rock_btn = tk.Button(button_container, text="🪨\nRock", 
                                 font=("Arial", 16, "bold"), width=8, height=3,
                                 bg='#ef4444', fg=self.css_colors['white'],
                                 relief='flat', cursor='hand2',
                                 command=lambda: self.make_choice('rock'))
        self.rock_btn.grid(row=0, column=0, padx=10)
        
        self.paper_btn = tk.Button(button_container, text="📄\nPaper", 
                                  font=("Arial", 16, "bold"), width=8, height=3,
                                  bg='#3b82f6', fg=self.css_colors['white'],
                                  relief='flat', cursor='hand2',
                                  command=lambda: self.make_choice('paper'))
        self.paper_btn.grid(row=0, column=1, padx=10)
        
        self.scissors_btn = tk.Button(button_container, text="✂️\nScissors", 
                                     font=("Arial", 16, "bold"), width=8, height=3,
                                     bg='#10b981', fg=self.css_colors['white'],
                                     relief='flat', cursor='hand2',
                                     command=lambda: self.make_choice('scissors'))
        self.scissors_btn.grid(row=0, column=2, padx=10)
        
        # Results section (CSS card) - Improved layout
        results_section = tk.Frame(main_container, bg=self.css_colors['white'], 
                                  relief='flat', padx=20, pady=15)
        results_section.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        results_section.columnconfigure(0, weight=1)
        
        results_title = tk.Label(results_section, text="Game Results", font=("Arial", 14, "bold"),
                                bg=self.css_colors['white'], fg=self.css_colors['text'])
        results_title.pack(pady=(0, 15))
        
        # Improved choice display with better formatting
        self.choice_display_frame = tk.Frame(results_section, bg=self.css_colors['white'])
        self.choice_display_frame.pack(pady=(0, 10))
        
        self.choice_display = tk.Label(self.choice_display_frame, text="Ready to play!", 
                                      font=("Arial", 12), 
                                      bg=self.css_colors['white'], fg=self.css_colors['accent'])
        self.choice_display.pack()
        
        # Battle display frame for better alignment
        self.battle_frame = tk.Frame(results_section, bg=self.css_colors['white'])
        self.battle_frame.pack(pady=5)
        
        # Player choice
        self.player_choice_label = tk.Label(self.battle_frame, text="", 
                                           font=("Arial", 16, "bold"),
                                           bg=self.css_colors['white'], fg=self.css_colors['accent'])
        self.player_choice_label.grid(row=0, column=0, padx=10)
        
        # VS label
        self.vs_label = tk.Label(self.battle_frame, text="VS", 
                                font=("Arial", 14, "bold"),
                                bg=self.css_colors['white'], fg=self.css_colors['text_light'])
        self.vs_label.grid(row=0, column=1, padx=20)
        
        # Computer choice
        self.computer_choice_label = tk.Label(self.battle_frame, text="", 
                                             font=("Arial", 16, "bold"),
                                             bg=self.css_colors['white'], fg=self.css_colors['danger'])
        self.computer_choice_label.grid(row=0, column=2, padx=10)
        
        # Winner display
        self.winner_label = tk.Label(results_section, text="", font=("Arial", 14, "bold"),
                                    bg=self.css_colors['white'])
        self.winner_label.pack(pady=(10, 15))
        
        # History section
        history_frame = tk.Frame(results_section, bg=self.css_colors['white'])
        history_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        history_title = tk.Label(history_frame, text="Recent Games", font=("Arial", 11, "bold"),
                                bg=self.css_colors['white'], fg=self.css_colors['text'])
        history_title.pack(anchor='w', pady=(0, 5))
        
        # Text widget with scrollbar
        text_frame = tk.Frame(history_frame, bg=self.css_colors['white'])
        text_frame.pack(fill='both', expand=True)
        
        self.history_text = tk.Text(text_frame, font=("Arial", 9), height=6,
                                   bg='#f9fafb', fg=self.css_colors['text'],
                                   relief='flat', wrap=tk.WORD)
        self.history_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.history_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons with logout option
        control_section = tk.Frame(main_container, bg=self.css_colors['light'])
        control_section.grid(row=4, column=0, pady=20)
        
        high_scores_btn = tk.Button(control_section, text="📊 High Scores", 
                                   font=("Arial", 11, "bold"),
                                   bg=self.css_colors['warning'], fg=self.css_colors['white'],
                                   relief='flat', padx=15, pady=8, cursor='hand2',
                                   command=self.show_high_scores)
        high_scores_btn.grid(row=0, column=0, padx=5)
        
        reset_btn = tk.Button(control_section, text="🔄 Reset", 
                             font=("Arial", 11, "bold"),
                             bg=self.css_colors['danger'], fg=self.css_colors['white'],
                             relief='flat', padx=15, pady=8, cursor='hand2',
                             command=self.reset_game)
        reset_btn.grid(row=0, column=1, padx=5)
        
        logout_btn = tk.Button(control_section, text="🚪 Logout", 
                              font=("Arial", 11, "bold"),
                              bg=self.css_colors['secondary'], fg=self.css_colors['white'],
                              relief='flat', padx=15, pady=8, cursor='hand2',
                              command=self.logout)
        logout_btn.grid(row=0, column=2, padx=5)
        
        quit_btn = tk.Button(control_section, text="❌ Quit", 
                            font=("Arial", 11, "bold"),
                            bg=self.css_colors['primary'], fg=self.css_colors['white'],
                            relief='flat', padx=15, pady=8, cursor='hand2',
                            command=self.quit_game)
        quit_btn.grid(row=0, column=3, padx=5)
        
        # Add bottom padding for scrolling
        bottom_padding = tk.Frame(main_container, bg=self.css_colors['light'], height=50)
        bottom_padding.grid(row=5, column=0, sticky="ew")

    def make_choice(self, choice):
        """Unified method for making a choice (fixes button clicks)"""
        if self.animation_active:
            return
        
        # Animate the appropriate button
        if choice == 'rock':
            self.animate_button(self.rock_btn)
        elif choice == 'paper':
            self.animate_button(self.paper_btn)
        elif choice == 'scissors':
            self.animate_button(self.scissors_btn)
        
        # Play the round
        self.play_round(choice)

    def get_computer_choice(self):
        return random.choice(['rock', 'paper', 'scissors'])
    
    def get_winner(self, player, computer):
        if player == computer:
            return 'tie'
        elif (player == 'rock' and computer == 'scissors') or \
             (player == 'paper' and computer == 'rock') or \
             (player == 'scissors' and computer == 'paper'):
            return 'player'
        else:
            return 'computer'
    
    def play_round(self, player_choice):
        """Play a round of the game with improved display"""
        computer_choice = self.get_computer_choice()
        winner = self.get_winner(player_choice, computer_choice)
        
        # Display choices with better formatting
        choice_emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        
        # Update battle display
        self.player_choice_label.config(text=f"You\n{choice_emojis[player_choice]} {player_choice.title()}")
        self.computer_choice_label.config(text=f"Computer\n{choice_emojis[computer_choice]} {computer_choice.title()}")
        
        # Clear the old choice display text
        self.choice_display.config(text="")
        
        # Update scores and display result
        won_round = False
        if winner == 'player':
            self.player_score += 1
            self.winner_label.config(text="🎉 You Win This Round! 🎉", fg=self.css_colors['success'])
            result_text = "Win"
            won_round = True
        elif winner == 'computer':
            self.computer_score += 1
            self.winner_label.config(text="💻 Computer Wins This Round!", fg=self.css_colors['danger'])
            result_text = "Loss"
        else:
            self.winner_label.config(text="🤝 It's a Tie Game!", fg=self.css_colors['accent'])
            result_text = "Tie"
        
        # Update high scores
        self.update_high_scores(won_round)
        
        # Update display
        self.score_label.config(text=f"Player {self.player_score} - {self.computer_score} Computer")
        self.streak_label.config(text=f"🔥 Current Streak: {self.current_streak}")
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M")
        history_entry = f"[{timestamp}] {choice_emojis[player_choice]} vs {choice_emojis[computer_choice]} - {result_text}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
        # Color-code the entry
        if won_round:
            self.history_text.tag_add("win", "end-2l linestart", "end-2l lineend")
            self.history_text.tag_config("win", foreground=self.css_colors['success'])
        elif winner == 'computer':
            self.history_text.tag_add("loss", "end-2l linestart", "end-2l lineend")
            self.history_text.tag_config("loss", foreground=self.css_colors['danger'])
        else:
            self.history_text.tag_add("tie", "end-2l linestart", "end-2l lineend")
            self.history_text.tag_config("tie", foreground=self.css_colors['accent'])

    def reset_game(self):
        """Reset the current game session"""
        if messagebox.askyesno("Reset Game", "Reset the current game session?"):
            self.player_score = 0
            self.computer_score = 0
            self.current_streak = 0
            self.total_games = 0
            self.total_wins = 0
            
            # Update displays
            self.score_label.config(text=f"Player {self.player_score} - {self.computer_score} Computer")
            self.streak_label.config(text=f"🔥 Current Streak: {self.current_streak}")
            self.choice_display.config(text="Ready to play!")
            self.winner_label.config(text="")
            self.player_choice_label.config(text="")
            self.computer_choice_label.config(text="")
            self.history_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Game Reset", "Game has been reset! Good luck! 🍀")

    def quit_game(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

    def logout(self):
        """Logout and return to welcome screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.login_screen = LoginScreen(self.root, self.on_login_success)

def main():
    root = tk.Tk()
    game = RockPaperScissorsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()