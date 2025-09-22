import random
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import hashlib
import threading
import time
import math

class ThemeManager:
    """Manage dark and light themes"""
    def __init__(self):
        self.current_theme = "dark"  # Default to dark mode
        
    def get_colors(self):
        if self.current_theme == "dark":
            return {
                'primary': '#0f172a',      # slate-900
                'secondary': '#1e293b',    # slate-800
                'accent': '#3b82f6',       # blue-500
                'success': '#10b981',      # emerald-500
                'warning': '#f59e0b',      # amber-500
                'danger': '#ef4444',       # red-500
                'light': '#1e293b',        # slate-800
                'white': '#0f172a',        # slate-900
                'text': '#f8fafc',         # slate-50
                'text_light': '#94a3b8',   # slate-400
                'border': '#374151',       # gray-700
                'input_bg': '#374151',     # gray-700
                'card_bg': '#1e293b',      # slate-800
                'hover': '#334155'         # slate-700
            }
        else:  # light theme
            return {
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
                'input_bg': '#ffffff',
                'card_bg': '#ffffff',
                'hover': '#f3f4f6'         # gray-100
            }
    
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"

class VisualEffects:
    """2.5D visual effects and styling"""
    @staticmethod
    def apply_card_style(widget, bg_color, shadow=True):
        """Apply 2.5D card styling"""
        if shadow:
            widget.configure(relief='raised', bd=2, 
                           highlightbackground='gray', highlightthickness=1)
        else:
            widget.configure(relief='flat', bd=0)
        widget.configure(bg=bg_color)
    
    @staticmethod
    def apply_button_style(widget, bg_color, text_color):
        """Apply 2.5D button styling"""
        widget.configure(
            relief='raised',
            bd=3,
            bg=bg_color,
            fg=text_color,
            activebackground=bg_color,
            activeforeground=text_color,
            font=("Arial", 12, "bold")
        )
    
    @staticmethod
    def apply_input_style(widget, bg_color, text_color, border_color):
        """Apply 2.5D input styling"""
        widget.configure(
            relief='sunken',
            bd=2,
            bg=bg_color,
            fg=text_color,
            insertbackground=text_color,
            highlightbackground=border_color,
            highlightthickness=1
        )

class HandVisualizer:
    """Hand gesture visualizations"""
    @staticmethod
    def get_hand_visual(choice, is_computer=False):
        """Get visual representation of hand gesture"""
        if is_computer:
            prefix = "🤖 "
        else:
            prefix = "👤 "
        
        visuals = {
            'rock': prefix + "✊",      # Closed fist
            'paper': prefix + "✋",     # Open hand
            'scissors': prefix + "✌️"   # Peace sign/scissors
        }
        return visuals.get(choice, "❓")

class InlineNotification:
    """Inline notification system"""
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.notification_frame = None
        
    def show(self, message, msg_type="info", duration=3000):
        """Show inline notification"""
        colors = self.theme_manager.get_colors()
        
        # Remove existing notification
        if self.notification_frame:
            self.notification_frame.destroy()
        
        # Create notification frame
        self.notification_frame = tk.Frame(self.parent, height=40)
        self.notification_frame.pack(fill='x', pady=(10, 0))
        self.notification_frame.pack_propagate(False)
        
        # Style based on message type
        if msg_type == "success":
            bg_color = colors['success']
            icon = "✅"
        elif msg_type == "error":
            bg_color = colors['danger']
            icon = "❌"
        elif msg_type == "warning":
            bg_color = colors['warning']
            icon = "⚠️"
        else:
            bg_color = colors['accent']
            icon = "ℹ️"
        
        # Apply 2.5D styling
        VisualEffects.apply_card_style(self.notification_frame, bg_color)
        
        # Notification content
        content_frame = tk.Frame(self.notification_frame, bg=bg_color)
        content_frame.pack(expand=True, fill='both', padx=15, pady=8)
        
        icon_label = tk.Label(content_frame, text=icon, font=("Arial", 14),
                             bg=bg_color, fg=colors['white'])
        icon_label.pack(side='left', padx=(0, 10))
        
        msg_label = tk.Label(content_frame, text=message, font=("Arial", 11, "bold"),
                            bg=bg_color, fg=colors['white'])
        msg_label.pack(side='left', expand=True, anchor='w')
        
        # Auto-hide notification
        self.parent.after(duration, self.hide)
    
    def hide(self):
        """Hide notification"""
        if self.notification_frame:
            self.notification_frame.destroy()
            self.notification_frame = None

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

class SplashScreen:
    """Animated splash screen with developer logo and credits"""
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.alpha = 0.0
        self.phase = "logo"  # logo -> credits -> complete
        self.fade_speed = 0.05
        
        # Setup splash window
        self.setup_splash()
        self.start_animation()
    
    def setup_splash(self):
        """Setup the splash screen window"""
        self.root.title("Rock Paper Scissors")
        self.root.geometry("800x600")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 400
        y = (self.root.winfo_screenheight() // 2) - 300
        self.root.geometry(f"800x600+{x}+{y}")
        
        # Create main container
        self.container = tk.Frame(self.root, bg='#000000')
        self.container.pack(fill='both', expand=True)
        
        # Developer logo phase
        self.logo_frame = tk.Frame(self.container, bg='#000000')
        self.logo_frame.pack(fill='both', expand=True)
        
        # Company/Developer logo
        logo_container = tk.Frame(self.logo_frame, bg='#000000')
        logo_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Animated logo with glowing effect
        self.logo_label = tk.Label(logo_container, text="⚡", 
                                  font=("Arial", 120, "bold"),
                                  fg='#3b82f6', bg='#000000')
        self.logo_label.pack(pady=(0, 20))
        
        self.company_label = tk.Label(logo_container, text="BUET CSE", 
                                     font=("Arial", 28, "bold"),
                                     fg='#ffffff', bg='#000000')
        self.company_label.pack(pady=(0, 10))
        
        self.tagline_label = tk.Label(logo_container, text="Crafting Digital Experiences", 
                                     font=("Arial", 14),
                                     fg='#94a3b8', bg='#000000')
        self.tagline_label.pack()
        
        # Credits phase (initially hidden)
        self.credits_frame = tk.Frame(self.container, bg='#000000')
        
        credits_container = tk.Frame(self.credits_frame, bg='#000000')
        credits_container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.credits_title = tk.Label(credits_container, text="GAME CREDITS", 
                                     font=("Arial", 32, "bold"),
                                     fg='#10b981', bg='#000000')
        self.credits_title.pack(pady=(0, 40))
        
        credits_info = [
            ("Lead Developer", "Kazi Abir"),
            ("UI/UX Designer", "Kazi Abir"),
            ("Game Logic", "Kazi Abir"),
            ("Animation", "Kazi Abir")
        ]
        
        for role, name in credits_info:
            role_frame = tk.Frame(credits_container, bg='#000000')
            role_frame.pack(pady=8)
            
            role_label = tk.Label(role_frame, text=role, 
                                 font=("Arial", 14, "bold"),
                                 fg='#f59e0b', bg='#000000')
            role_label.pack()
            
            name_label = tk.Label(role_frame, text=name, 
                                 font=("Arial", 12),
                                 fg='#ffffff', bg='#000000')
            name_label.pack()
        
        # Thank you message
        thanks_label = tk.Label(credits_container, text="Thank you for playing!", 
                               font=("Arial", 16, "italic"),
                               fg='#94a3b8', bg='#000000')
        thanks_label.pack(pady=(30, 0))
    
    def start_animation(self):
        """Start the splash screen animation sequence"""
        self.fade_in_logo()
    
    def fade_in_logo(self):
        """Fade in the developer logo"""
        self.alpha += self.fade_speed
        
        if self.alpha >= 1.0:
            self.alpha = 1.0
            # Hold logo for 2 seconds, then fade out
            self.root.after(2000, self.fade_out_logo)
        else:
            self.update_logo_opacity()
            self.root.after(50, self.fade_in_logo)
    
    def fade_out_logo(self):
        """Fade out the developer logo"""
        self.alpha -= self.fade_speed
        
        if self.alpha <= 0.0:
            self.alpha = 0.0
            self.logo_frame.pack_forget()
            self.credits_frame.pack(fill='both', expand=True)
            self.fade_in_credits()
        else:
            self.update_logo_opacity()
            self.root.after(50, self.fade_out_logo)
    
    def fade_in_credits(self):
        """Fade in the credits screen"""
        self.alpha += self.fade_speed
        
        if self.alpha >= 1.0:
            self.alpha = 1.0
            # Hold credits for 3 seconds, then fade out
            self.root.after(3000, self.fade_out_credits)
        else:
            self.update_credits_opacity()
            self.root.after(50, self.fade_in_credits)
    
    def fade_out_credits(self):
        """Fade out the credits screen"""
        self.alpha -= self.fade_speed
        
        if self.alpha <= 0.0:
            self.alpha = 0.0
            # Animation complete, show main login screen
            self.on_complete()
        else:
            self.update_credits_opacity()
            self.root.after(50, self.fade_out_credits)
    
    def update_logo_opacity(self):
        """Update logo opacity for fade effect"""
        # Simulate fade by adjusting colors
        logo_intensity = int(59 + (123 - 59) * self.alpha)  # Blue component
        text_intensity = int(255 * self.alpha)
        tagline_intensity = int(148 + (163 - 148) * self.alpha)
        
        self.logo_label.config(fg=f"#{logo_intensity:02x}{130:02x}{246:02x}")
        self.company_label.config(fg=f"#{text_intensity:02x}{text_intensity:02x}{text_intensity:02x}")
        self.tagline_label.config(fg=f"#{tagline_intensity:02x}{163:02x}{184:02x}")
    
    def update_credits_opacity(self):
        """Update credits opacity for fade effect"""
        # Simulate fade by adjusting colors
        title_intensity_g = int(16 + (185 - 16) * self.alpha)  # Green component for title
        title_intensity_b = int(129 + (185 - 129) * self.alpha)
        
        role_intensity = int(245 * self.alpha)  # Amber for roles
        role_intensity_g = int(158 * self.alpha)
        role_intensity_b = int(11 * self.alpha)
        
        text_intensity = int(255 * self.alpha)  # White for names
        thanks_intensity = int(148 + (163 - 148) * self.alpha)  # Gray for thanks
        
        self.credits_title.config(fg=f"#{16:02x}{title_intensity_g:02x}{title_intensity_b:02x}")
        
        # Update all role labels
        for widget in self.credits_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                text = grandchild.cget('text')
                                if text in ["Lead Developer", "UI/UX Designer", "Game Logic", "Animation", "Quality Assurance"]:
                                    grandchild.config(fg=f"#{role_intensity:02x}{role_intensity_g:02x}{role_intensity_b:02x}")
                                elif text != "GAME CREDITS" and text != "Thank you for playing!":
                                    grandchild.config(fg=f"#{text_intensity:02x}{text_intensity:02x}{text_intensity:02x}")
                                elif text == "Thank you for playing!":
                                    grandchild.config(fg=f"#{thanks_intensity:02x}{163:02x}{184:02x}")

class AnimationManager:
    """Enhanced animation manager with fade effects"""
    def __init__(self, root):
        self.root = root
        self.animations = {}
        
    def fade_in(self, widget, duration=300, callback=None):
        """Smooth fade in animation"""
        if callback:
            self.root.after(duration, callback)
    
    def smooth_button_press(self, button, callback=None):
        """Smooth button press animation"""
        original_relief = button.cget('relief')
        original_bd = button.cget('bd')
        
        # Simple press effect
        button.config(relief='sunken', bd=1)
        self.root.after(80, lambda: button.config(relief=original_relief, bd=original_bd))
        
        if callback:
            self.root.after(100, callback)
    
    def subtle_highlight(self, widget, duration=500):
        """Subtle highlight effect"""
        # Just a simple visual feedback without excessive movement
        original_relief = widget.cget('relief')
        widget.config(relief='raised')
        self.root.after(duration, lambda: widget.config(relief=original_relief))
    
    def fade_transition(self, from_widget, to_widget, duration=1000, callback=None):
        """Smooth fade transition between widgets"""
        steps = 20
        step_time = duration // steps
        
        def transition_step(step):
            if step <= steps:
                # Simple transition by hiding/showing widgets
                if step == steps // 2:
                    from_widget.pack_forget()
                    to_widget.pack(fill='both', expand=True)
                self.root.after(step_time, lambda: transition_step(step + 1))
            elif callback:
                callback()
        
        transition_step(0)

class HelpSystem:
    """Help and instructions system"""
    def __init__(self, root, theme_manager):
        self.root = root
        self.theme_manager = theme_manager
    
    def show_help(self):
        """Display help window with game instructions"""
        colors = self.theme_manager.get_colors()
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Game Instructions")
        help_window.geometry("600x500")
        help_window.configure(bg=colors['light'])
        help_window.transient(self.root)
        help_window.grab_set()
        help_window.resizable(True, True)
        
        # Center window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - 300
        y = (help_window.winfo_screenheight() // 2) - 250
        help_window.geometry(f"600x500+{x}+{y}")
        
        # Header
        header = tk.Frame(help_window, bg=colors['accent'], height=60, relief='raised', bd=2)
        header.pack(fill='x', padx=5, pady=5)
        header.pack_propagate(False)
        
        tk.Label(header, text="❓ Game Instructions & Help", font=("Arial", 18, "bold"),
                bg=colors['accent'], fg=colors['white']).pack(expand=True)
        
        # Scrollable content
        main_frame = tk.Frame(help_window, bg=colors['light'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame, bg=colors['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Help content
        content = tk.Frame(scrollable_frame, bg=colors['white'], padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        help_sections = [
            ("🎮 How to Play", [
                "• Choose Rock, Paper, or Scissors",
                "• Rock beats Scissors",
                "• Paper beats Rock", 
                "• Scissors beats Paper",
                "• Same choice = Tie"
            ]),
            ("⌨️ Keyboard Shortcuts", [
                "• R - Choose Rock",
                "• P - Choose Paper",
                "• S - Choose Scissors",
                "• H - Open High Scores",
                "• Ctrl+R - Reset Game",
                "• Ctrl+Q - Quit Game"
            ]),
            ("🏆 Scoring System", [
                "• Win a round: +1 point",
                "• Win streak: Consecutive wins",
                "• High scores are saved per user",
                "• Guest scores are not saved"
            ]),
            ("🎨 Features", [
                "• Dark/Light theme toggle",
                "• Hand gesture visualizations",
                "• Achievement notifications",
                "• Game history tracking",
                "• User account system"
            ]),
            ("👤 Account System", [
                "• Create account to save progress",
                "• Login to access your scores",
                "• Guest mode for quick play",
                "• Secure password hashing"
            ])
        ]
        
        for title, items in help_sections:
            section_frame = tk.Frame(content, bg=colors['card_bg'], relief='raised', bd=2)
            section_frame.pack(fill='x', pady=10, padx=5)
            
            tk.Label(section_frame, text=title, font=("Arial", 14, "bold"),
                    bg=colors['card_bg'], fg=colors['text']).pack(anchor='w', padx=15, pady=(10, 5))
            
            for item in items:
                tk.Label(section_frame, text=item, font=("Arial", 11),
                        bg=colors['card_bg'], fg=colors['text_light'], anchor='w').pack(anchor='w', padx=25, pady=2)
            
            tk.Frame(section_frame, height=10, bg=colors['card_bg']).pack()
        
        # Close button
        close_btn = tk.Button(help_window, text="Close", font=("Arial", 12, "bold"),
                             bg=colors['secondary'], fg=colors['white'],
                             relief='raised', bd=2, padx=20, pady=8, cursor='hand2',
                             command=help_window.destroy)
        close_btn.pack(pady=10)

class LoginScreen:
    """Enhanced login screen with splash screen integration"""
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.users_file = "users.json"
        self.current_user = None
        self.theme_manager = ThemeManager()
        self.animation_manager = AnimationManager(root)
        self.help_system = HelpSystem(root, self.theme_manager)
        
        # Form data preservation
        self.preserved_data = {}
        
        # Start with splash screen
        self.show_splash_screen()
    
    def show_splash_screen(self):
        """Show animated splash screen before login"""
        self.splash = SplashScreen(self.root, self.on_splash_complete)
    
    def on_splash_complete(self):
        """Called when splash screen animation completes"""
        # Clear splash screen and show welcome screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Add a short delay for smooth transition
        self.root.after(500, self.setup_welcome_screen)
    
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
    
    def preserve_form_data(self):
        """Preserve form data before theme toggle"""
        if hasattr(self, 'username_entry') and self.username_entry.winfo_exists():
            self.preserved_data['username'] = self.username_entry.get()
        if hasattr(self, 'password_entry') and self.password_entry.winfo_exists():
            self.preserved_data['password'] = self.password_entry.get()
        if hasattr(self, 'reg_username_entry') and self.reg_username_entry.winfo_exists():
            self.preserved_data['reg_username'] = self.reg_username_entry.get()
        if hasattr(self, 'reg_password_entry') and self.reg_password_entry.winfo_exists():
            self.preserved_data['reg_password'] = self.reg_password_entry.get()
        if hasattr(self, 'reg_confirm_entry') and self.reg_confirm_entry.winfo_exists():
            self.preserved_data['reg_confirm'] = self.reg_confirm_entry.get()
    
    def restore_form_data(self):
        """Restore form data after theme toggle"""
        self.root.after(100, self._restore_data_delayed)
    
    def _restore_data_delayed(self):
        """Delayed restoration to ensure widgets are created"""
        if hasattr(self, 'username_entry') and 'username' in self.preserved_data:
            self.username_entry.insert(0, self.preserved_data['username'])
        if hasattr(self, 'password_entry') and 'password' in self.preserved_data:
            self.password_entry.insert(0, self.preserved_data['password'])
        if hasattr(self, 'reg_username_entry') and 'reg_username' in self.preserved_data:
            self.reg_username_entry.insert(0, self.preserved_data['reg_username'])
        if hasattr(self, 'reg_password_entry') and 'reg_password' in self.preserved_data:
            self.reg_password_entry.insert(0, self.preserved_data['reg_password'])
        if hasattr(self, 'reg_confirm_entry') and 'reg_confirm' in self.preserved_data:
            self.reg_confirm_entry.insert(0, self.preserved_data['reg_confirm'])
    
    def setup_welcome_screen(self):
        """Enhanced welcome screen with fade-in effect"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        colors = self.theme_manager.get_colors()
        
        self.root.title("Rock Paper Scissors - Welcome")
        self.root.geometry("900x700")
        self.root.configure(bg=colors['primary'])
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main container with fade-in effect
        main_frame = tk.Frame(self.root, bg=colors['primary'])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Apply fade-in animation
        self.animation_manager.fade_in(main_frame, 800)
        
        # Top control bar
        control_bar = tk.Frame(main_frame, bg=colors['primary'])
        control_bar.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Right side controls
        right_controls = tk.Frame(control_bar, bg=colors['primary'])
        right_controls.pack(side='right')
        
        help_btn = tk.Button(right_controls, text="❓", font=("Arial", 12, "bold"),
                            command=self.help_system.show_help)
        VisualEffects.apply_button_style(help_btn, colors['warning'], colors['white'])
        help_btn.pack(side='left', padx=(0, 10))
        
        theme_btn = tk.Button(right_controls, text="🌙 Dark" if self.theme_manager.current_theme == "light" else "☀️ Light",
                             font=("Arial", 10, "bold"), 
                             command=self.toggle_theme)
        VisualEffects.apply_button_style(theme_btn, colors['secondary'], colors['text'])
        theme_btn.pack(side='left')
        
        # Create animated background
        bg_container = tk.Frame(main_frame, bg=colors['primary'])
        bg_container.grid(row=1, column=0, sticky="nsew")
        bg_container.columnconfigure(0, weight=1)
        bg_container.rowconfigure(0, weight=1)
        
        self.bg_canvas = tk.Canvas(bg_container, bg=colors['primary'], highlightthickness=0)
        self.bg_canvas.grid(row=0, column=0, sticky="nsew")
        
        self.animated_bg = AnimatedBackground(self.bg_canvas)
        
        # Welcome content overlay with enhanced entrance
        content_frame = tk.Frame(self.bg_canvas, bg=colors['card_bg'], padx=40, pady=40)
        VisualEffects.apply_card_style(content_frame, colors['card_bg'])
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Enhanced title with welcome animation
        title_label = tk.Label(content_frame, text="🎮 ROCK PAPER SCISSORS 🎮", 
                              font=("Arial", 32, "bold"), 
                              fg=colors['accent'], bg=colors['card_bg'])
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(content_frame, text="Ultimate Gaming Experience", 
                                 font=("Arial", 16), 
                                 fg=colors['text_light'], bg=colors['card_bg'])
        subtitle_label.pack(pady=(0, 30))
        
        # Welcome message after splash
        welcome_msg = tk.Label(content_frame, text="Welcome! Choose your adventure below:", 
                              font=("Arial", 14), 
                              fg=colors['text'], bg=colors['card_bg'])
        welcome_msg.pack(pady=(0, 20))
        
        # Button group with staggered appearance
        button_frame = tk.Frame(content_frame, bg=colors['card_bg'])
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(button_frame, text="🔑 Login", 
                             font=("Arial", 16, "bold"), width=15,
                             command=self.show_login_form)
        VisualEffects.apply_button_style(login_btn, colors['accent'], colors['white'])
        login_btn.pack(side='left', padx=15, pady=10)
        
        register_btn = tk.Button(button_frame, text="📝 Register", 
                                font=("Arial", 16, "bold"), width=15,
                                command=self.show_register_form)
        VisualEffects.apply_button_style(register_btn, colors['success'], colors['white'])
        register_btn.pack(side='left', padx=15, pady=10)
        
        # Guest play option
        guest_btn = tk.Button(content_frame, text="👤 Play as Guest", 
                             font=("Arial", 14), 
                             command=lambda: self.login_as_guest())
        VisualEffects.apply_button_style(guest_btn, colors['secondary'], colors['text'])
        guest_btn.pack(pady=(20, 0))
        
        # Powered by label (subtle branding)
        powered_label = tk.Label(content_frame, text="Powered by NEXUS GAMES", 
                                font=("Arial", 9), 
                                fg=colors['text_light'], bg=colors['card_bg'])
        powered_label.pack(pady=(30, 0))
    
    def toggle_theme(self):
        """Toggle theme with form data preservation"""
        self.preserve_form_data()
        self.theme_manager.toggle_theme()
        
        # Refresh current screen
        if hasattr(self, 'current_screen'):
            if self.current_screen == 'login':
                self.show_login_form()
            elif self.current_screen == 'register':
                self.show_register_form()
            else:
                self.setup_welcome_screen()
        else:
            self.setup_welcome_screen()
        
        self.restore_form_data()
    
    def show_login_form(self):
        """Fixed login form with proper layout"""
        self.current_screen = 'login'
        if hasattr(self, 'animated_bg'):
            self.animated_bg.stop()
        
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        colors = self.theme_manager.get_colors()
        self.root.configure(bg=colors['light'])
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main container
        main_container = tk.Frame(self.root, bg=colors['light'])
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.columnconfigure(0, weight=1)
        
        # Control bar
        control_bar = tk.Frame(main_container, bg=colors['light'])
        control_bar.pack(fill='x', pady=(0, 20))
        
        right_controls = tk.Frame(control_bar, bg=colors['light'])
        right_controls.pack(side='right')
        
        help_btn = tk.Button(right_controls, text="❓", font=("Arial", 10, "bold"),
                            command=self.help_system.show_help)
        VisualEffects.apply_button_style(help_btn, colors['warning'], colors['white'])
        help_btn.pack(side='left', padx=(0, 10))
        
        theme_btn = tk.Button(right_controls, text="🌙 Dark" if self.theme_manager.current_theme == "light" else "☀️ Light",
                             font=("Arial", 10, "bold"), 
                             command=self.toggle_theme)
        VisualEffects.apply_button_style(theme_btn, colors['secondary'], colors['text'])
        theme_btn.pack(side='left')
        
        # Header
        header_frame = tk.Frame(main_container, bg=colors['primary'], height=100, padx=20, pady=20)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        VisualEffects.apply_card_style(header_frame, colors['primary'])
        
        tk.Label(header_frame, text="🔑 User Login", font=("Arial", 24, "bold"),
                bg=colors['primary'], fg=colors['accent']).pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(main_container, bg=colors['card_bg'], padx=50, pady=40)
        form_frame.pack(fill='x')
        VisualEffects.apply_card_style(form_frame, colors['card_bg'])
        
        # Notification area
        self.login_notification = InlineNotification(form_frame, self.theme_manager)
        
        # Input fields
        tk.Label(form_frame, text="Username:", font=("Arial", 14, "bold"),
                bg=colors['card_bg'], fg=colors['text']).pack(anchor='w', pady=(20, 5))
        
        username_container = tk.Frame(form_frame, bg=colors['input_bg'], padx=15, pady=12)
        username_container.pack(fill='x', pady=(0, 20))
        VisualEffects.apply_card_style(username_container, colors['input_bg'])
        
        self.username_entry = tk.Entry(username_container, font=("Arial", 14), bd=0, 
                                      bg=colors['input_bg'], fg=colors['text'])
        self.username_entry.pack(fill='x')
        
        tk.Label(form_frame, text="Password:", font=("Arial", 14, "bold"),
                bg=colors['card_bg'], fg=colors['text']).pack(anchor='w', pady=(0, 5))
        
        password_container = tk.Frame(form_frame, bg=colors['input_bg'], padx=15, pady=12)
        password_container.pack(fill='x', pady=(0, 25))
        VisualEffects.apply_card_style(password_container, colors['input_bg'])
        
        self.password_entry = tk.Entry(password_container, font=("Arial", 14), bd=0, show='*',
                                      bg=colors['input_bg'], fg=colors['text'])
        self.password_entry.pack(fill='x')
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=colors['card_bg'])
        btn_frame.pack(fill='x', pady=20)
        
        login_submit_btn = tk.Button(btn_frame, text="Login", font=("Arial", 14, "bold"),
                                    command=self.process_login)
        VisualEffects.apply_button_style(login_submit_btn, colors['accent'], colors['white'])
        login_submit_btn.pack(side='left', padx=(0, 15), pady=5)
        
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 14),
                            command=self.setup_welcome_screen)
        VisualEffects.apply_button_style(back_btn, colors['secondary'], colors['text'])
        back_btn.pack(side='left', pady=5)
        
        # Focus and bindings
        self.username_entry.focus_set()
        self.root.bind('<Return>', lambda e: self.process_login())
    
    def show_register_form(self):
        """Fixed registration form with proper layout"""
        self.current_screen = 'register'
        if hasattr(self, 'animated_bg'):
            self.animated_bg.stop()
        
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        colors = self.theme_manager.get_colors()
        self.root.configure(bg=colors['light'])
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main container
        main_container = tk.Frame(self.root, bg=colors['light'])
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.columnconfigure(0, weight=1)
        
        # Control bar
        control_bar = tk.Frame(main_container, bg=colors['light'])
        control_bar.pack(fill='x', pady=(0, 20))
        
        right_controls = tk.Frame(control_bar, bg=colors['light'])
        right_controls.pack(side='right')
        
        help_btn = tk.Button(right_controls, text="❓", font=("Arial", 10, "bold"),
                            command=self.help_system.show_help)
        VisualEffects.apply_button_style(help_btn, colors['warning'], colors['white'])
        help_btn.pack(side='left', padx=(0, 10))
        
        theme_btn = tk.Button(right_controls, text="🌙 Dark" if self.theme_manager.current_theme == "light" else "☀️ Light",
                             font=("Arial", 10, "bold"), 
                             command=self.toggle_theme)
        VisualEffects.apply_button_style(theme_btn, colors['secondary'], colors['text'])
        theme_btn.pack(side='left')
        
        # Header
        header_frame = tk.Frame(main_container, bg=colors['success'], height=100, padx=20, pady=20)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        VisualEffects.apply_card_style(header_frame, colors['success'])
        
        tk.Label(header_frame, text="📝 Create Account", font=("Arial", 24, "bold"),
                bg=colors['success'], fg=colors['white']).pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(main_container, bg=colors['card_bg'], padx=50, pady=40)
        form_frame.pack(fill='x')
        VisualEffects.apply_card_style(form_frame, colors['card_bg'])
        
        # Notification area
        self.register_notification = InlineNotification(form_frame, self.theme_manager)
        
        # Input fields
        fields = [
            ("Username:", "reg_username_entry"),
            ("Password:", "reg_password_entry"),
            ("Confirm Password:", "reg_confirm_entry")
        ]
        
        for i, (label_text, attr_name) in enumerate(fields):
            tk.Label(form_frame, text=label_text, font=("Arial", 14, "bold"),
                    bg=colors['card_bg'], fg=colors['text']).pack(anchor='w', pady=(15 if i > 0 else 20, 5))
            
            input_container = tk.Frame(form_frame, bg=colors['input_bg'], padx=15, pady=12)
            input_container.pack(fill='x', pady=(0, 10))
            VisualEffects.apply_card_style(input_container, colors['input_bg'])
            
            entry = tk.Entry(input_container, font=("Arial", 14), bd=0,
                           bg=colors['input_bg'], fg=colors['text'],
                           show='*' if 'password' in attr_name else '')
            entry.pack(fill='x')
            setattr(self, attr_name, entry)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=colors['card_bg'])
        btn_frame.pack(fill='x', pady=25)
        
        register_submit_btn = tk.Button(btn_frame, text="Create Account", font=("Arial", 14, "bold"),
                                       command=self.process_registration)
        VisualEffects.apply_button_style(register_submit_btn, colors['success'], colors['white'])
        register_submit_btn.pack(side='left', padx=(0, 15), pady=5)
        
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 14),
                            command=self.setup_welcome_screen)
        VisualEffects.apply_button_style(back_btn, colors['secondary'], colors['text'])
        back_btn.pack(side='left', pady=5)
        
        # Focus and bindings
        self.reg_username_entry.focus_set()
        self.root.bind('<Return>', lambda e: self.process_registration())
    
    def process_login(self):
        """Process login with inline notifications"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.login_notification.show("Please fill in all fields!", "error")
            return
        
        users = self.load_users()
        hashed_password = self.hash_password(password)
        
        if username in users and users[username]['password'] == hashed_password:
            self.current_user = username
            self.login_notification.show(f"Welcome back, {username}! Loading game...", "success")
            self.root.after(1500, lambda: self.on_login_success(username))
        else:
            self.login_notification.show("Invalid username or password!", "error")
    
    def process_registration(self):
        """Process registration with inline notifications"""
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        if not username or not password or not confirm:
            self.register_notification.show("Please fill in all fields!", "error")
            return
        
        if password != confirm:
            self.register_notification.show("Passwords don't match!", "error")
            return
        
        if len(password) < 4:
            self.register_notification.show("Password must be at least 4 characters!", "warning")
            return
        
        users = self.load_users()
        
        if username in users:
            self.register_notification.show("Username already exists!", "error")
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
        self.register_notification.show(f"Account created! Welcome, {username}! Loading game...", "success")
        self.root.after(2000, lambda: self.on_login_success(username))
    
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
        self.theme_manager = ThemeManager()
        self.animation_manager = AnimationManager(root)
        self.help_system = HelpSystem(root, self.theme_manager)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Game state
        self.player_score = 0
        self.computer_score = 0
        self.current_streak = 0
        self.total_games = 0
        self.total_wins = 0
        self.animation_active = False
        
        # Start with login screen (which will show splash first)
        self.login_screen = LoginScreen(root, self.on_login_success)
    
    def on_login_success(self, username):
        """Called when user successfully logs in with transition effect"""
        self.current_user = username
        self.load_user_scores()
        
        # Add transition effect before showing main UI
        transition_frame = tk.Frame(self.root, bg='#000000')
        transition_frame.pack(fill='both', expand=True)
        
        loading_label = tk.Label(transition_frame, text="Loading Game...", 
                                font=("Arial", 24, "bold"),
                                fg='#3b82f6', bg='#000000')
        loading_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Show main UI after short delay
        self.root.after(1500, lambda: [transition_frame.destroy(), self.setup_ui(), self.setup_keyboard_bindings()])
    
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
        """Clean achievement popup without excessive animations"""
        colors = self.theme_manager.get_colors()
        
        achievement = tk.Toplevel(self.root)
        achievement.title("Achievement!")
        achievement.geometry("380x220")
        achievement.resizable(False, False)
        achievement.configure(bg=colors['success'])
        achievement.transient(self.root)
        achievement.grab_set()
        
        # Center the popup
        achievement.update_idletasks()
        x = (achievement.winfo_screenwidth() // 2) - 190
        y = (achievement.winfo_screenheight() // 2) - 110
        achievement.geometry(f"380x220+{x}+{y}")
        
        # Main container
        container = tk.Frame(achievement, bg=colors['success'], padx=25, pady=25, 
                           relief='raised', bd=4)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Icon
        icon = tk.Label(container, text="🏆", font=("Arial", 36), 
                       bg=colors['success'], fg=colors['white'])
        icon.pack(pady=(0, 15))
        
        # Title
        title_label = tk.Label(container, text=title, font=("Arial", 16, "bold"),
                              bg=colors['success'], fg=colors['white'])
        title_label.pack(pady=(0, 8))
        
        # Message
        msg_label = tk.Label(container, text=message, font=("Arial", 12),
                            bg=colors['success'], fg=colors['white'])
        msg_label.pack(pady=(0, 20))
        
        # Button
        btn = tk.Button(container, text="Awesome!", font=("Arial", 12, "bold"),
                       bg=colors['white'], fg=colors['success'],
                       relief='raised', bd=3, padx=25, pady=10, cursor='hand2',
                       command=achievement.destroy)
        btn.pack()
        
        # Auto-close
        achievement.after(4000, achievement.destroy)

    def show_high_scores(self):
        """High scores window with fixed styling"""
        colors = self.theme_manager.get_colors()
        
        hs_window = tk.Toplevel(self.root)
        hs_window.title(f"High Scores - {self.current_user}")
        hs_window.geometry("500x450")
        hs_window.configure(bg=colors['light'])
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
        
        # Header with enhanced styling
        header = tk.Frame(hs_window, bg=colors['primary'], height=60, relief='raised', bd=2)
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        header.pack_propagate(False)
        
        header_label = tk.Label(header, text=f"🏆 {self.current_user}'s High Scores", font=("Arial", 18, "bold"),
                               bg=colors['primary'], fg=colors['white'])
        header_label.pack(expand=True)
        
        # Main content container
        main_content = tk.Frame(hs_window, bg=colors['light'])
        main_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_content.columnconfigure(0, weight=1)
        main_content.rowconfigure(0, weight=1)
        
        # Content area with enhanced card styling
        content = tk.Frame(main_content, bg=colors['card_bg'], padx=20, pady=20, 
                          relief='raised', bd=2)
        content.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        content.columnconfigure(0, weight=1)
        
        # Stats cards with improved layout
        stats_frame = tk.Frame(content, bg=colors['card_bg'])
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        stats_frame.columnconfigure(0, weight=1)
        
        stats = [
            ("🔥 Best Streak", self.high_scores['best_streak']),
            ("🎯 Total Wins", self.high_scores['total_wins']),
            ("🎮 Total Games", self.high_scores['total_games']),
            ("📊 Win Rate", f"{self.high_scores['win_percentage']:.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=colors['accent'], relief='raised', bd=2)
            card.grid(row=i, column=0, sticky="ew", pady=3, padx=2)
            card.columnconfigure(0, weight=1)
            card.columnconfigure(1, weight=0)
            
            left_label = tk.Label(card, text=label, font=("Arial", 12),
                                 bg=colors['accent'], fg=colors['white'], 
                                 anchor='w', padx=15, pady=8)
            left_label.grid(row=0, column=0, sticky="ew")
            
            right_label = tk.Label(card, text=str(value), font=("Arial", 12, "bold"),
                                  bg=colors['accent'], fg=colors['white'], 
                                  anchor='e', padx=15, pady=8)
            right_label.grid(row=0, column=1, sticky="e")
        
        # Current session
        if self.player_score + self.computer_score > 0:
            session_frame = tk.Frame(content, bg=colors['card_bg'], relief='sunken', bd=1)
            session_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20), padx=2)
            
            session_title = tk.Label(session_frame, text="Current Session", font=("Arial", 12, "bold"),
                                    bg=colors['card_bg'], fg=colors['text'])
            session_title.pack(pady=(10, 5))
            
            session_text = f"Wins: {self.player_score} | Losses: {self.computer_score} | Streak: {self.current_streak}"
            session_label = tk.Label(session_frame, text=session_text, font=("Arial", 10),
                                    bg=colors['card_bg'], fg=colors['text_light'])
            session_label.pack(pady=(0, 10))
        
        # Enhanced buttons with proper alignment
        btn_frame = tk.Frame(hs_window, bg=colors['light'])
        btn_frame.grid(row=2, column=0, sticky="ew", pady=15)
        
        # Center the buttons properly
        btn_container = tk.Frame(btn_frame, bg=colors['light'])
        btn_container.pack(expand=True)
        
        if self.current_user != "Guest":
            reset_btn = tk.Button(btn_container, text="Reset Scores", font=("Arial", 10, "bold"),
                                 bg=colors['danger'], fg=colors['white'],
                                 relief='raised', bd=2, padx=15, pady=8, cursor='hand2',
                                 command=lambda: self.reset_high_scores(hs_window))
            reset_btn.pack(side='left', padx=5)
        
        close_btn = tk.Button(btn_container, text="Close", font=("Arial", 10, "bold"),
                             bg=colors['secondary'], fg=colors['white'],
                             relief='raised', bd=2, padx=15, pady=8, cursor='hand2',
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
        """Smooth button animation without vibration"""
        if self.animation_active:
            return
        
        self.animation_active = True
        
        def reset_animation():
            self.animation_active = False
        
        self.animation_manager.smooth_button_press(button, reset_animation)

    def setup_ui(self):
        """Main UI with enhanced entrance animations"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        colors = self.theme_manager.get_colors()
        self.root.title(f"Rock Paper Scissors - {self.current_user}")
        self.root.configure(bg=colors['light'])
        
        # Create scrollable main container with fade-in
        self.scrollable_container = ScrollableFrame(self.root, bg=colors['light'])
        self.scrollable_container.grid(row=0, column=0, sticky="nsew")
        
        # Apply entrance animation
        self.animation_manager.fade_in(self.scrollable_container, 600)
        
        # Main container inside scrollable frame
        main_container = self.scrollable_container.scrollable_frame
        main_container.columnconfigure(0, weight=1)
        
        # Clean header with controls
        header_section = tk.Frame(main_container, bg=colors['primary'], height=100, 
                                 padx=20, pady=15, relief='raised', bd=3)
        header_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_section.columnconfigure(1, weight=1)
        header_section.pack_propagate(False)
        
        # Control buttons in header
        controls_frame = tk.Frame(header_section, bg=colors['primary'])
        controls_frame.grid(row=0, column=0, sticky="nw")
        
        help_btn = tk.Button(controls_frame, text="❓", font=("Arial", 10, "bold"),
                            command=self.help_system.show_help)
        VisualEffects.apply_button_style(help_btn, colors['warning'], colors['white'])
        help_btn.pack(side='left', padx=(0, 5))
        
        theme_btn = tk.Button(controls_frame, text="🌙 Dark" if self.theme_manager.current_theme == "light" else "☀️ Light",
                             font=("Arial", 10, "bold"), 
                             command=self.toggle_theme)
        VisualEffects.apply_button_style(theme_btn, colors['secondary'], colors['text'])
        theme_btn.pack(side='left')
        
        # Centered title
        title_container = tk.Frame(header_section, bg=colors['primary'])
        title_container.grid(row=0, column=1, sticky="")
        
        title_label = tk.Label(title_container, text="🎮 Rock Paper Scissors", 
                              font=("Arial", 26, "bold"), 
                              bg=colors['primary'], fg=colors['accent'])
        title_label.pack()
        
        user_label = tk.Label(title_container, text=f"Playing as: {self.current_user}", 
                             font=("Arial", 13), 
                             bg=colors['primary'], fg=colors['text_light'])
        user_label.pack()
        
        # Score card
        score_card = tk.Frame(main_container, bg=colors['card_bg'], padx=25, pady=20,
                             relief='raised', bd=3)
        score_card.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        score_card.columnconfigure(0, weight=1)
        
        score_title = tk.Label(score_card, text="Current Game", font=("Arial", 16, "bold"),
                              bg=colors['card_bg'], fg=colors['text'])
        score_title.pack(pady=(0, 15))
        
        self.score_label = tk.Label(score_card, 
                                   text=f"Player {self.player_score} - {self.computer_score} Computer",
                                   font=("Arial", 20, "bold"), 
                                   bg=colors['card_bg'], fg=colors['accent'])
        self.score_label.pack()
        
        self.streak_label = tk.Label(score_card, text=f"🔥 Current Streak: {self.current_streak}",
                                    font=("Arial", 14), 
                                    bg=colors['card_bg'], fg=colors['warning'])
        self.streak_label.pack(pady=(8, 0))
        
        # Game buttons section
        button_section = tk.Frame(main_container, bg=colors['card_bg'], padx=25, pady=25,
                                 relief='raised', bd=3)
        button_section.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        button_section.columnconfigure(0, weight=1)
        
        button_title = tk.Label(button_section, text="Make Your Move", font=("Arial", 16, "bold"),
                               bg=colors['card_bg'], fg=colors['text'])
        button_title.pack(pady=(0, 8))
        
        hint_label = tk.Label(button_section, text="Click buttons or press R/P/S keys", 
                             font=("Arial", 12), 
                             bg=colors['card_bg'], fg=colors['text_light'])
        hint_label.pack(pady=(0, 20))
        
        # Button container
        button_container = tk.Frame(button_section, bg=colors['card_bg'])
        button_container.pack()
        
        # Game buttons with clean styling
        self.rock_btn = tk.Button(button_container, text="🪨\nRock", 
                                 font=("Arial", 18, "bold"), width=10, height=4,
                                 command=lambda: self.make_choice('rock'))
        VisualEffects.apply_button_style(self.rock_btn, '#ef4444', colors['white'])
        self.rock_btn.grid(row=0, column=0, padx=15, pady=10)
        
        self.paper_btn = tk.Button(button_container, text="📄\nPaper", 
                                  font=("Arial", 18, "bold"), width=10, height=4,
                                  command=lambda: self.make_choice('paper'))
        VisualEffects.apply_button_style(self.paper_btn, '#3b82f6', colors['white'])
        self.paper_btn.grid(row=0, column=1, padx=15, pady=10)
        
        self.scissors_btn = tk.Button(button_container, text="✂️\nScissors", 
                                     font=("Arial", 18, "bold"), width=10, height=4,
                                     command=lambda: self.make_choice('scissors'))
        VisualEffects.apply_button_style(self.scissors_btn, '#10b981', colors['white'])
        self.scissors_btn.grid(row=0, column=2, padx=15, pady=10)
        
        # Results section with hand visualizations
        results_section = tk.Frame(main_container, bg=colors['card_bg'], padx=25, pady=20,
                                  relief='raised', bd=3)
        results_section.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        results_section.columnconfigure(0, weight=1)
        
        results_title = tk.Label(results_section, text="Game Results", font=("Arial", 16, "bold"),
                                bg=colors['card_bg'], fg=colors['text'])
        results_title.pack(pady=(0, 20))
        
        # Hand visualization frame
        visual_frame = tk.Frame(results_section, bg=colors['card_bg'])
        visual_frame.pack(pady=10)
        
        # Player hand visualization
        self.player_visual_frame = tk.Frame(visual_frame, bg=colors['input_bg'], padx=20, pady=15,
                                           relief='sunken', bd=2)
        self.player_visual_frame.grid(row=0, column=0, padx=20)
        
        tk.Label(self.player_visual_frame, text="You", font=("Arial", 12, "bold"),
                bg=colors['input_bg'], fg=colors['text']).pack()
        
        self.player_hand_label = tk.Label(self.player_visual_frame, text="👤 Ready", 
                                         font=("Arial", 24), bg=colors['input_bg'])
        self.player_hand_label.pack(pady=5)
        
        # VS label
        vs_frame = tk.Frame(visual_frame, bg=colors['card_bg'])
        vs_frame.grid(row=0, column=1, padx=30)
        
        vs_label = tk.Label(vs_frame, text="VS", font=("Arial", 20, "bold"),
                           bg=colors['card_bg'], fg=colors['accent'])
        vs_label.pack()
        
        # Computer hand visualization
        self.computer_visual_frame = tk.Frame(visual_frame, bg=colors['input_bg'], padx=20, pady=15,
                                             relief='sunken', bd=2)
        self.computer_visual_frame.grid(row=0, column=2, padx=20)
        
        tk.Label(self.computer_visual_frame, text="Computer", font=("Arial", 12, "bold"),
                bg=colors['input_bg'], fg=colors['text']).pack()
        
        self.computer_hand_label = tk.Label(self.computer_visual_frame, text="🤖 Ready", 
                                           font=("Arial", 24), bg=colors['input_bg'])
        self.computer_hand_label.pack(pady=5)
        
        # Winner display
        self.winner_label = tk.Label(results_section, text="", font=("Arial", 16, "bold"),
                                    bg=colors['card_bg'])
        self.winner_label.pack(pady=15)
        
        # Enhanced history section
        history_frame = tk.Frame(results_section, bg=colors['card_bg'])
        history_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        history_title = tk.Label(history_frame, text="Recent Games", font=("Arial", 13, "bold"),
                                bg=colors['card_bg'], fg=colors['text'])
        history_title.pack(anchor='w', pady=(0, 8))
        
        # Text widget container with enhanced styling
        text_container = tk.Frame(history_frame, bg=colors['card_bg'], relief='sunken', bd=2)
        text_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        text_frame = tk.Frame(text_container, bg=colors['input_bg'])
        text_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        self.history_text = tk.Text(text_frame, font=("Arial", 10), height=6,
                                   bg=colors['input_bg'], fg=colors['text'],
                                   relief='flat', bd=0, wrap=tk.WORD)
        self.history_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.history_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons
        control_section = tk.Frame(main_container, bg=colors['light'])
        control_section.grid(row=4, column=0, pady=25)
        
        buttons = [
            ("📊 High Scores", self.show_high_scores, colors['warning']),
            ("🔄 Reset", self.reset_game, colors['danger']),
            ("🚪 Logout", self.logout, colors['secondary']),
            ("❌ Quit", self.quit_game, colors['primary'])
        ]
        
        for i, (text, command, bg_color) in enumerate(buttons):
            btn = tk.Button(control_section, text=text, font=("Arial", 12, "bold"),
                           command=command)
            VisualEffects.apply_button_style(btn, bg_color, colors['white'])
            btn.grid(row=0, column=i, padx=8)
        
        # Add bottom padding for scrolling
        bottom_padding = tk.Frame(main_container, bg=colors['light'], height=50)
        bottom_padding.grid(row=5, column=0, sticky="ew")
    
    def toggle_theme(self):
        """Toggle theme and refresh UI"""
        self.theme_manager.toggle_theme()
        self.setup_ui()
        self.setup_keyboard_bindings()
    
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
        """Clean play round with smooth animations"""
        computer_choice = self.get_computer_choice()
        winner = self.get_winner(player_choice, computer_choice)
        colors = self.theme_manager.get_colors()
        
        # Update hand visualizations with subtle animation
        player_visual = HandVisualizer.get_hand_visual(player_choice, False)
        computer_visual = HandVisualizer.get_hand_visual(computer_choice, True)
        
        # Subtle highlight for hand changes
        self.animation_manager.subtle_highlight(self.player_visual_frame, 300)
        self.animation_manager.subtle_highlight(self.computer_visual_frame, 300)
        
        self.player_hand_label.config(text=player_visual)
        self.computer_hand_label.config(text=computer_visual)
        
        # Update scores and display result
        won_round = False
        if winner == 'player':
            self.player_score += 1
            self.winner_label.config(text="🎉 You Win This Round! 🎉", fg=colors['success'])
            result_text = "Win"
            won_round = True
        elif winner == 'computer':
            self.computer_score += 1
            self.winner_label.config(text="💻 Computer Wins This Round!", fg=colors['danger'])
            result_text = "Loss"
        else:
            self.winner_label.config(text="🤝 It's a Tie Game!", fg=colors['accent'])
            result_text = "Tie"
        
        # Update high scores
        self.update_high_scores(won_round)
        
        # Update displays
        self.score_label.config(text=f"Player {self.player_score} - {self.computer_score} Computer")
        self.streak_label.config(text=f"🔥 Current Streak: {self.current_streak}")
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M")
        choice_emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        history_entry = f"[{timestamp}] {choice_emojis[player_choice]} vs {choice_emojis[computer_choice]} - {result_text}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
        # Color-code the entry
        if won_round:
            self.history_text.tag_add("win", "end-2l linestart", "end-2l lineend")
            self.history_text.tag_config("win", foreground=colors['success'])
        elif winner == 'computer':
            self.history_text.tag_add("loss", "end-2l linestart", "end-2l lineend")
            self.history_text.tag_config("loss", foreground=colors['danger'])
        else:
            self.history_text.tag_add("tie", "end-2l linestart", "end-2l lineend")
            self.history_text.tag_config("tie", foreground=colors['accent'])

    def reset_game(self):
        """Reset the current game session with confirmation"""
        if messagebox.askyesno("Reset Game", "Reset the current game session?"):
            self.player_score = 0
            self.computer_score = 0
            self.current_streak = 0
            self.total_games = 0
            self.total_wins = 0
            
            # Update displays
            self.score_label.config(text=f"Player {self.player_score} - {self.computer_score} Computer")
            self.streak_label.config(text=f"🔥 Current Streak: {self.current_streak}")
            self.player_hand_label.config(text="👤 Ready")
            self.computer_hand_label.config(text="🤖 Ready")
            self.winner_label.config(text="")
            self.history_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Game Reset", "Game has been reset! Good luck! 🍀")

    def quit_game(self):
        """Quit the game with confirmation"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

    def logout(self):
        """Logout and return to welcome screen with transition"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Show logout transition
            transition_frame = tk.Frame(self.root, bg='#000000')
            transition_frame.pack(fill='both', expand=True)
            
            logout_label = tk.Label(transition_frame, text="Logging out...", 
                                   font=("Arial", 24, "bold"),
                                   fg='#f59e0b', bg='#000000')
            logout_label.place(relx=0.5, rely=0.5, anchor='center')
            
            # Return to login screen after delay
            self.root.after(1000, lambda: [
                transition_frame.destroy(),
                setattr(self, 'current_user', None),
                LoginScreen(self.root, self.on_login_success)
            ])

def main():
    """Main function to start the application"""
    root = tk.Tk()
    game = RockPaperScissorsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()