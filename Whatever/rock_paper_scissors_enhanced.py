#!/usr/bin/env python3
"""
Enhanced Rock Paper Scissors Game - Based on Working Simple Version
Adds better styling and features while maintaining stability
"""

import sys
import os
import json
import hashlib
import random
from datetime import datetime

# Handle PyQt version detection
PYQT_VERSION = 6
try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox,
                                QGraphicsOpacityEffect)
    from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
    from PyQt6.QtGui import QIcon, QFont, QPixmap
except ImportError:
    try:
        from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                    QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox,
                                    QGraphicsOpacityEffect)
        from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
        from PyQt5.QtGui import QIcon, QFont, QPixmap
        PYQT_VERSION = 5
    except ImportError:
        print("❌ Neither PyQt6 nor PyQt5 found!")
        sys.exit(1)


class ThemeManager:
    """Manages light and dark themes"""
    def __init__(self):
        self.is_dark_mode = False
        
    def get_theme_colors(self):
        if self.is_dark_mode:
            return {
                'bg_primary': '#1f2937',
                'bg_secondary': '#374151',
                'bg_accent': '#4b5563',
                'text_primary': '#ffffff',
                'text_secondary': '#e5e7eb',
                'text_muted': '#9ca3af',
                'border': '#6b7280',
                'blue': '#3b82f6',
                'blue_hover': '#2563eb',
                'green': '#10b981',
                'green_hover': '#059669',
                'red': '#ef4444',
                'red_hover': '#dc2626',
                'yellow': '#f59e0b',
                'yellow_hover': '#d97706',
                'gray': '#6b7280',
                'gray_hover': '#4b5563'
            }
        else:
            return {
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8fafc',
                'bg_accent': '#e2e8f0',
                'text_primary': '#1f2937',
                'text_secondary': '#374151',
                'text_muted': '#6b7280',
                'border': '#d1d5db',
                'blue': '#3b82f6',
                'blue_hover': '#2563eb',
                'green': '#10b981',
                'green_hover': '#059669',
                'red': '#ef4444',
                'red_hover': '#dc2626',
                'yellow': '#f59e0b',
                'yellow_hover': '#d97706',
                'gray': '#6b7280',
                'gray_hover': '#4b5563'
            }
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode


class EnhancedUserManager:
    """Enhanced user management with better data handling"""
    def __init__(self):
        self.users_file = "users.json"
        self.high_scores_file = "high_scores.json"
        self.current_user = None
        self.users = self.load_users()
        
    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            return True
        except:
            return False
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password):
        if username in self.users:
            if self.users[username]['password'] == self.hash_password(password):
                self.current_user = username
                return True
        return False
    
    def register(self, username, password):
        if username not in self.users:
            self.users[username] = {
                'password': self.hash_password(password),
                'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'wins': 0,
                'losses': 0,
                'ties': 0,
                'games_played': 0,
                'best_streak': 0,
                'current_streak': 0
            }
            self.save_users()
            return True
        return False
    
    def save_game_result(self, result_type):
        """Save game result with compatibility for existing data"""
        if not self.current_user or self.current_user not in self.users:
            return
        
        user_data = self.users[self.current_user]
        
        # Initialize missing fields for compatibility
        if 'games_played' not in user_data:
            user_data['games_played'] = 0
        if 'wins' not in user_data:
            user_data['wins'] = 0
        if 'losses' not in user_data:
            user_data['losses'] = 0
        if 'ties' not in user_data:
            user_data['ties'] = 0
        if 'current_streak' not in user_data:
            user_data['current_streak'] = 0
        if 'best_streak' not in user_data:
            user_data['best_streak'] = 0
        
        # Update stats
        user_data['games_played'] += 1
        
        if result_type == 'win':
            user_data['wins'] += 1
            user_data['current_streak'] += 1
            if user_data['current_streak'] > user_data['best_streak']:
                user_data['best_streak'] = user_data['current_streak']
        elif result_type == 'loss':
            user_data['losses'] += 1
            user_data['current_streak'] = 0
        else:  # tie
            user_data['ties'] += 1
        
        self.save_users()
    
    def get_user_stats(self):
        """Get current user's statistics"""
        if not self.current_user or self.current_user not in self.users:
            return {}
        
        user_data = self.users[self.current_user]
        total_games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        return {
            'games_played': total_games,
            'wins': wins,
            'losses': user_data.get('losses', 0),
            'ties': user_data.get('ties', 0),
            'win_rate': win_rate,
            'current_streak': user_data.get('current_streak', 0),
            'best_streak': user_data.get('best_streak', 0)
        }


class SplashScreen(QWidget):
    """Initial splash screen with logo"""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo/Icon
        logo_label = QLabel("🎮")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 80px; margin: 20px;")
        layout.addWidget(logo_label)
        
        # App name
        title = QLabel("Rock Paper Scissors")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #3b82f6; margin: 10px;")
        layout.addWidget(title)
        
        # Developer info
        dev_label = QLabel("Developed by Code Masters")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        dev_label.setStyleSheet("font-size: 16px; color: #6b7280; margin: 5px;")
        layout.addWidget(dev_label)
        
        # Store references
        self.logo_label = logo_label
        self.title = title
        self.dev_label = dev_label
        
        self.apply_theme()
        
    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        self.setStyleSheet(f"background-color: {colors['bg_secondary']};")
        self.title.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {colors['blue']}; margin: 10px;")
        self.dev_label.setStyleSheet(f"font-size: 16px; color: {colors['text_muted']}; margin: 5px;")


class CreditScreen(QWidget):
    """Credit screen"""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Credits title
        title = QLabel("Credits")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Credits content
        credits_text = """
🎨 UI/UX Design: Code Masters Team
💻 Programming: Python & PyQt
🎮 Game Logic: Enhanced RPS Algorithm
🌟 Special Thanks: Open Source Community
        """
        
        credits_label = QLabel(credits_text.strip())
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(credits_label)
        
        layout.addSpacing(20)
        
        # Version info
        version_label = QLabel("Version 2.0 - Enhanced Edition")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Store references
        self.title = title
        self.credits_label = credits_label
        self.version_label = version_label
        
        self.apply_theme()
        
    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        self.setStyleSheet(f"background-color: {colors['bg_secondary']};")
        self.title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {colors['green']}; margin: 10px;")
        self.credits_label.setStyleSheet(f"font-size: 14px; color: {colors['text_secondary']}; line-height: 1.8;")
        self.version_label.setStyleSheet(f"font-size: 12px; color: {colors['text_muted']}; font-style: italic;")


class WelcomeScreen(QWidget):
    """Welcome screen with sign in/log in options"""
    def __init__(self, user_manager, main_window):
        super().__init__()
        self.user_manager = user_manager
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Theme toggle button
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedSize(80, 30)
        theme_layout.addWidget(self.theme_btn)
        layout.addLayout(theme_layout)
        
        # Title section
        title = QLabel("🎮 Rock Paper Scissors")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Ultimate Gaming Experience")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        description = QLabel("Welcome to the most exciting Rock Paper Scissors game!\nChoose an option below to get started.")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(description)
        
        layout.addSpacing(10)
        
        # Options container
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        options_layout.setSpacing(10)
        options_layout.setContentsMargins(15, 15, 15, 15)
        
        # Log in button
        login_btn = QPushButton("🔑 Log In\nI already have an account")
        login_btn.clicked.connect(self.main_window.show_login)
        login_btn.setFixedHeight(50)
        options_layout.addWidget(login_btn)
        
        # Sign up button
        signup_btn = QPushButton("📝 Sign Up\nCreate a new account")
        signup_btn.clicked.connect(self.main_window.show_register)
        signup_btn.setFixedHeight(50)
        options_layout.addWidget(signup_btn)
        
        layout.addWidget(options_container)
        layout.addStretch()
        
        # Store references for theme updates
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.options_container = options_container
        self.login_btn = login_btn
        self.signup_btn = signup_btn
        
        self.apply_theme()
        
    def toggle_theme(self):
        self.main_window.theme_manager.toggle_theme()
        self.main_window.apply_theme_to_all()
        
    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        
        self.setStyleSheet(f"background-color: {colors['bg_secondary']};")
        
        self.theme_btn.setText("☀️ Light" if self.main_window.theme_manager.is_dark_mode else "🌙 Dark")
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['gray']};
                color: {colors['text_primary']};
                border: none;
                border-radius: 6px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {colors['gray_hover']}; }}
        """)
        
        self.title.setStyleSheet(f"""
            font-size: 24px; 
            font-weight: bold; 
            color: {colors['blue']}; 
            margin: 5px 0;
        """)
        
        self.subtitle.setStyleSheet(f"font-size: 14px; color: {colors['text_muted']}; margin-bottom: 10px; font-style: italic;")
        
        self.description.setStyleSheet(f"font-size: 11px; color: {colors['text_secondary']}; margin-bottom: 15px;")
        
        self.options_container.setStyleSheet(f"""
            QWidget {{
                background: {colors['bg_primary']};
                border-radius: 8px;
            }}
        """)
        
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['blue']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {colors['blue_hover']}; }}
        """)
        
        self.signup_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['green']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {colors['green_hover']}; }}
        """)


class EnhancedLoginScreen(QWidget):
    """Enhanced login screen with glassmorphism styling"""
    def __init__(self, user_manager, main_window):
        super().__init__()
        self.user_manager = user_manager
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        
        # Main glassmorphism container - make it responsive
        glass_container = QWidget()
        glass_container.setMinimumSize(350, 400)
        glass_container.setMaximumSize(450, 500)
        glass_layout = QVBoxLayout(glass_container)
        glass_layout.setSpacing(15)
        glass_layout.setContentsMargins(25, 20, 25, 20)
        
        # Theme toggle button - positioned at top right
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedSize(65, 26)
        theme_layout.addWidget(self.theme_btn)
        glass_layout.addLayout(theme_layout)
        
        # Header section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(3)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Sign in to your account")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        glass_layout.addWidget(header_widget)
        
        # Add some spacing after header
        glass_layout.addSpacing(10)
        
        # Form section
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Username input
        username_label = QLabel("Username")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(40)
        form_layout.addWidget(self.username_input)
        
        # Add small spacing between fields
        form_layout.addSpacing(5)
        
        # Password input
        password_label = QLabel("Password")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password if PYQT_VERSION == 6 else QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        form_layout.addWidget(self.password_input)
        
        glass_layout.addWidget(form_widget)
        
        # Add spacing before buttons
        glass_layout.addSpacing(15)
        
        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.main_window.show_welcome)
        back_btn.setFixedHeight(40)
        button_layout.addWidget(back_btn)
        
        login_btn = QPushButton("Sign In")
        login_btn.clicked.connect(self.login_clicked)
        login_btn.setFixedHeight(40)
        button_layout.addWidget(login_btn)
        
        glass_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        self.status_label.setFixedHeight(20)
        self.status_label.setWordWrap(True)
        glass_layout.addWidget(self.status_label)
        
        # Add stretch to push everything up
        glass_layout.addStretch()
        
        layout.addWidget(glass_container)
        
        # Store references for theme updates
        self.glass_container = glass_container
        self.title = title
        self.subtitle = subtitle
        self.username_label = username_label
        self.password_label = password_label
        self.back_btn = back_btn
        self.login_btn = login_btn
        
        # Connect Enter key
        self.username_input.returnPressed.connect(self.login_clicked)
        self.password_input.returnPressed.connect(self.login_clicked)
        
        self.apply_theme()
        
    def toggle_theme(self):
        self.main_window.theme_manager.toggle_theme()
        self.main_window.apply_theme_to_all()
        
    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        
        # Background gradient and glass styling based on theme
        if self.main_window.theme_manager.is_dark_mode:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #334155)"
            glass_bg = "rgba(45, 55, 72, 0.85)"
            glass_border = "rgba(45, 55, 72, 0.9)"  # Almost invisible border
            text_color = "white"
            label_color = "rgba(255, 255, 255, 0.95)"
            input_bg = "rgba(55, 65, 81, 0.8)"
            input_border = "rgba(75, 85, 99, 0.6)"
            placeholder_color = "rgba(255, 255, 255, 0.5)"
        else:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2)"
            glass_bg = "rgba(255, 255, 255, 0.3)"
            glass_border = "rgba(255, 255, 255, 0.5)"
            text_color = "#1f2937"
            label_color = "#1f2937"
            input_bg = "rgba(255, 255, 255, 0.85)"
            input_border = "rgba(255, 255, 255, 0.7)"
            placeholder_color = "rgba(31, 41, 55, 0.6)"
            
        self.setStyleSheet(f"background: {bg_gradient};")
        
        # Theme toggle button
        self.theme_btn.setText("☀️ Light" if self.main_window.theme_manager.is_dark_mode else "🌙 Dark")
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: {glass_bg};
                color: {text_color};
                border: 1px solid {glass_border};
                border-radius: 13px;
                font-size: 9px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.4);
                color: #1f2937;
            }}
        """)
        
        # Glassmorphism container - remove visible borders in dark mode
        border_style = f"1px solid {glass_border}" if not self.main_window.theme_manager.is_dark_mode else "none"
        self.glass_container.setStyleSheet(f"""
            QWidget {{
                background: {glass_bg};
                border: {border_style};
                border-radius: 18px;
            }}
        """)
        
        # Header styles - better spacing
        self.title.setStyleSheet(f"""
            font-size: 22px; 
            font-weight: bold; 
            color: {text_color};
            margin: 0px;
            padding: 0px;
        """)
        
        self.subtitle.setStyleSheet(f"""
            font-size: 13px; 
            color: {label_color};
            font-weight: 400;
            margin: 0px;
            padding: 0px;
        """)
        
        # Label styles - consistent sizing
        label_style = f"""
            color: {label_color};
            font-size: 12px;
            font-weight: 600;
            margin: 0px 0px 3px 0px;
            padding: 0px;
        """
        self.username_label.setStyleSheet(label_style)
        self.password_label.setStyleSheet(label_style)
        
        # Input styles with better contrast and consistent sizing
        input_style = f"""
            QLineEdit {{
                background: {input_bg};
                border: 1px solid {input_border};
                border-radius: 8px;
                padding: 10px 12px;
                color: {text_color};
                font-size: 13px;
                font-weight: 400;
            }}
            QLineEdit:focus {{
                border: 2px solid #06b6d4;
                background: {"rgba(255, 255, 255, 0.95)" if not self.main_window.theme_manager.is_dark_mode else "rgba(75, 85, 99, 0.9)"};
            }}
            QLineEdit::placeholder {{
                color: {placeholder_color};
            }}
        """
        self.username_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        
        # Button styles - consistent sizing
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background: {glass_bg};
                border: 1px solid {glass_border};
                border-radius: 8px;
                color: {text_color};
                font-size: 13px;
                font-weight: 600;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.4);
                color: #1f2937;
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.3);
            }}
        """)
        
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #06b6d4);
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5855eb, stop:1 #0891b2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #0284c7);
            }
        """)
        
    def login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_message("Please enter both username and password", "error")
            return
            
        if self.user_manager.login(username, password):
            self.show_message(f"Welcome back, {username}! 🎉", "success")
            QTimer.singleShot(1000, self.main_window.show_game)
        else:
            self.show_message("Invalid username or password", "error")
    
    def show_message(self, message, message_type):
        if message_type == "success":
            color = "#22c55e"
            bg_color = "rgba(34, 197, 94, 0.2)"
        else:
            color = "#ef4444"
            bg_color = "rgba(239, 68, 68, 0.2)"
            
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            color: {color}; 
            font-weight: bold; 
            font-size: 12px;
            background: {bg_color};
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        """)
    
    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
        self.status_label.clear()


class EnhancedRegisterScreen(QWidget):
    """Enhanced register screen with glassmorphism styling"""
    def __init__(self, user_manager, main_window):
        super().__init__()
        self.user_manager = user_manager
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        
        # Main glassmorphism container
        glass_container = QWidget()
        glass_container.setFixedSize(380, 520)
        glass_layout = QVBoxLayout(glass_container)
        glass_layout.setSpacing(20)
        glass_layout.setContentsMargins(30, 25, 30, 25)
        
        # Theme toggle button
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedSize(70, 28)
        theme_layout.addWidget(self.theme_btn)
        glass_layout.addLayout(theme_layout)
        
        # Header section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Join the ultimate gaming experience")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        glass_layout.addWidget(header_widget)
        
        # Add some spacing after header
        glass_layout.addSpacing(10)
        
        # Form section
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 5, 0, 5)
        
        # Username input
        username_label = QLabel("Username")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setFixedHeight(40)
        form_layout.addWidget(self.username_input)
        
        # Add small spacing between fields
        form_layout.addSpacing(5)
        
        # Password input
        password_label = QLabel("Password")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password if PYQT_VERSION == 6 else QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        form_layout.addWidget(self.password_input)
        
        # Add small spacing between fields
        form_layout.addSpacing(5)
        
        # Confirm Password input
        confirm_label = QLabel("Confirm Password")
        form_layout.addWidget(confirm_label)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password if PYQT_VERSION == 6 else QLineEdit.Password)
        self.confirm_password_input.setFixedHeight(40)
        form_layout.addWidget(self.confirm_password_input)
        
        glass_layout.addWidget(form_widget)
        
        # Add spacing before buttons
        glass_layout.addSpacing(15)
        
        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.main_window.show_welcome)
        back_btn.setFixedHeight(45)
        button_layout.addWidget(back_btn)
        
        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.register_clicked)
        register_btn.setFixedHeight(45)
        button_layout.addWidget(register_btn)
        
        glass_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        self.status_label.setFixedHeight(25)
        form_layout.addWidget(self.status_label)
        
        glass_layout.addWidget(form_widget)
        layout.addWidget(glass_container)
        
        # Store references for theme updates
        self.glass_container = glass_container
        self.title = title
        self.subtitle = subtitle
        self.username_label = username_label
        self.password_label = password_label
        self.confirm_label = confirm_label
        self.back_btn = back_btn
        self.register_btn = register_btn
        
        # Connect Enter key
        self.username_input.returnPressed.connect(self.register_clicked)
        self.password_input.returnPressed.connect(self.register_clicked)
        self.confirm_password_input.returnPressed.connect(self.register_clicked)
        
        self.apply_theme()
        
    def toggle_theme(self):
        self.main_window.theme_manager.toggle_theme()
        self.main_window.apply_theme_to_all()
        
    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        
        # Background gradient and glass styling based on theme
        if self.main_window.theme_manager.is_dark_mode:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #334155)"
            glass_bg = "rgba(45, 55, 72, 0.85)"
            glass_border = "rgba(45, 55, 72, 0.9)"  # Almost invisible border
            text_color = "white"
            label_color = "rgba(255, 255, 255, 0.95)"
            input_bg = "rgba(55, 65, 81, 0.8)"
            input_border = "rgba(75, 85, 99, 0.6)"
            placeholder_color = "rgba(255, 255, 255, 0.5)"
        else:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2)"
            glass_bg = "rgba(255, 255, 255, 0.3)"
            glass_border = "rgba(255, 255, 255, 0.5)"
            text_color = "#1f2937"
            label_color = "#1f2937"
            input_bg = "rgba(255, 255, 255, 0.85)"
            input_border = "rgba(255, 255, 255, 0.7)"
            placeholder_color = "rgba(31, 41, 55, 0.6)"
            
        self.setStyleSheet(f"background: {bg_gradient};")
        
        # Theme toggle button
        self.theme_btn.setText("☀️ Light" if self.main_window.theme_manager.is_dark_mode else "🌙 Dark")
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: {glass_bg};
                color: {text_color};
                border: 1px solid {glass_border};
                border-radius: 13px;
                font-size: 9px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.4);
                color: #1f2937;
            }}
        """)
        
        # Glassmorphism container - remove visible borders in dark mode
        border_style = f"1px solid {glass_border}" if not self.main_window.theme_manager.is_dark_mode else "none"
        self.glass_container.setStyleSheet(f"""
            QWidget {{
                background: {glass_bg};
                border: {border_style};
                border-radius: 18px;
            }}
        """)
        
        # Header styles - better spacing
        self.title.setStyleSheet(f"""
            font-size: 22px; 
            font-weight: bold; 
            color: {text_color};
            margin: 0px;
            padding: 0px;
        """)
        
        self.subtitle.setStyleSheet(f"""
            font-size: 13px; 
            color: {label_color};
            font-weight: 400;
            margin: 0px;
            padding: 0px;
        """)
        
        # Label styles - consistent sizing
        label_style = f"""
            color: {label_color};
            font-size: 12px;
            font-weight: 600;
            margin: 0px 0px 3px 0px;
            padding: 0px;
        """
        self.username_label.setStyleSheet(label_style)
        self.password_label.setStyleSheet(label_style)
        self.confirm_label.setStyleSheet(label_style)
        
        # Input styles with better contrast and consistent sizing
        input_style = f"""
            QLineEdit {{
                background: {input_bg};
                border: 1px solid {input_border};
                border-radius: 8px;
                padding: 10px 12px;
                color: {text_color};
                font-size: 13px;
                font-weight: 400;
            }}
            QLineEdit:focus {{
                border: 2px solid #06b6d4;
                background: {"rgba(255, 255, 255, 0.95)" if not self.main_window.theme_manager.is_dark_mode else "rgba(75, 85, 99, 0.9)"};
            }}
            QLineEdit::placeholder {{
                color: {placeholder_color};
            }}
        """
        self.username_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        self.confirm_password_input.setStyleSheet(input_style)
        
        # Button styles - consistent sizing
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background: {glass_bg};
                border: 1px solid {glass_border};
                border-radius: 8px;
                color: {text_color};
                font-size: 13px;
                font-weight: 600;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.4);
                color: #1f2937;
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.3);
            }}
        """)
        
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #06b6d4);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #0891b2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #047857, stop:1 #0284c7);
            }
        """)
        
    def register_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not username or not password or not confirm_password:
            self.show_message("Please fill in all fields", "error")
            return
            
        if len(username) < 2:
            self.show_message("Username must be at least 2 characters", "error")
            return
            
        if len(password) < 3:
            self.show_message("Password must be at least 3 characters", "error")
            return
            
        if password != confirm_password:
            self.show_message("Passwords do not match", "error")
            return
            
        if self.user_manager.register(username, password):
            self.user_manager.current_user = username
            self.show_message(f"Account created! Welcome, {username}! 🚀", "success")
            QTimer.singleShot(1000, self.main_window.show_game)
        else:
            self.show_message("Username already exists", "error")
    
    def show_message(self, message, message_type):
        if message_type == "success":
            color = "#22c55e"
            bg_color = "rgba(34, 197, 94, 0.2)"
        else:
            color = "#ef4444"
            bg_color = "rgba(239, 68, 68, 0.2)"
            
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            color: {color}; 
            font-weight: bold; 
            font-size: 12px;
            background: {bg_color};
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        """)
    
    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.status_label.clear()


class StatsScreen(QWidget):
    """Dedicated stats screen instead of dialog"""
    def __init__(self, user_manager, main_window):
        super().__init__()
        self.user_manager = user_manager
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 15, 25, 15)
        
        # Theme toggle button
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedSize(80, 30)
        theme_layout.addWidget(self.theme_btn)
        layout.addLayout(theme_layout)
        
        # Title
        title = QLabel("📊 Player Statistics")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(title)
        
        # Stats container
        stats_container = QWidget()
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stats content
        self.stats_content = QLabel("Loading statistics...")
        self.stats_content.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        stats_layout.addWidget(self.stats_content)
        
        layout.addWidget(stats_container)
        
        # Back button
        back_btn = QPushButton("← Back to Game")
        back_btn.clicked.connect(self.main_window.show_game)
        back_btn.setFixedHeight(40)
        layout.addWidget(back_btn)
        
        layout.addStretch()
        
        # Store references
        self.title = title
        self.stats_container = stats_container
        self.back_btn = back_btn
        
        self.apply_theme()
        
    def toggle_theme(self):
        self.main_window.theme_manager.toggle_theme()
        self.main_window.apply_theme_to_all()
        
    def update_stats(self):
        """Update statistics display"""
        stats = self.user_manager.get_user_stats()
        if stats:
            stats_text = f"""🎮 {self.user_manager.current_user}'s Performance

📊 Total Games: {stats['games_played']}
🏆 Wins: {stats['wins']}
😅 Losses: {stats['losses']}
🤝 Ties: {stats['ties']}

📈 Win Rate: {stats['win_rate']:.1f}%
🔥 Current Streak: {stats['current_streak']}
⭐ Best Streak: {stats['best_streak']}"""
        else:
            stats_text = "No statistics available yet.\nPlay some games to see your stats!"
        
        self.stats_content.setText(stats_text)
        
    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        
        self.setStyleSheet(f"background-color: {colors['bg_secondary']};")
        
        self.theme_btn.setText("☀️ Light" if self.main_window.theme_manager.is_dark_mode else "🌙 Dark")
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['gray']};
                color: {colors['text_primary']};
                border: none;
                border-radius: 6px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {colors['gray_hover']}; }}
        """)
        
        self.title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {colors['yellow']}; margin: 10px 0;")
        
        self.stats_container.setStyleSheet(f"""
            QWidget {{
                background: {colors['bg_primary']};
                border-radius: 8px;
            }}
        """)
        
        self.stats_content.setStyleSheet(f"""
            font-size: 14px; 
            color: {colors['text_secondary']}; 
            line-height: 1.6;
            padding: 10px;
        """)
        
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['blue']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {colors['blue_hover']}; }}
        """)


class EnhancedGameScreen(QWidget):
    """Enhanced game screen with better styling and stats"""
    def __init__(self, user_manager, main_window):
        super().__init__()
        self.user_manager = user_manager
        self.main_window = main_window
        self.player_score = 0
        self.computer_score = 0
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 8, 10, 8)
        
        self.welcome_label = QLabel(f"Welcome, {self.user_manager.current_user}! 🎮")
        header_layout.addWidget(self.welcome_label)
        
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedSize(65, 25)
        header_layout.addWidget(self.theme_btn)
        
        # Stats button
        stats_btn = QPushButton("📊 Stats")
        stats_btn.clicked.connect(self.show_stats)
        stats_btn.setFixedSize(60, 25)
        header_layout.addWidget(stats_btn)
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout_clicked)
        logout_btn.setFixedSize(65, 25)
        header_layout.addWidget(logout_btn)
        
        layout.addWidget(header_widget)
        
        # Game title
        title = QLabel("🎮 Rock Paper Scissors")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        layout.addWidget(title)
        
        # Game buttons
        game_container = QWidget()
        game_layout = QVBoxLayout(game_container)
        game_layout.setContentsMargins(10, 10, 10, 10)
        
        instruction = QLabel("Choose your move:")
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        game_layout.addWidget(instruction)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        choices = [
            ("🪨", "ROCK", "rock", "#ef4444"),
            ("📄", "PAPER", "paper", "#3b82f6"),
            ("✂️", "SCISSORS", "scissors", "#10b981")
        ]
        
        self.game_buttons = []
        for emoji, text, choice, color in choices:
            btn = QPushButton(f"{emoji}\n{text}")
            btn.clicked.connect(lambda checked, c=choice: self.play_game(c))
            btn.setFixedHeight(55)
            btn.choice_color = color
            self.game_buttons.append(btn)
            button_layout.addWidget(btn)
        
        game_layout.addLayout(button_layout)
        layout.addWidget(game_container)
        
        # Result display
        self.result_label = QLabel("Choose your move to start playing!")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        self.result_label.setFixedHeight(60)
        layout.addWidget(self.result_label)
        
        # Score display
        self.score_label = QLabel("Session Score - You: 0 | Computer: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        self.score_label.setFixedHeight(25)
        layout.addWidget(self.score_label)
        
        # Store references for theme updates
        self.header_widget = header_widget
        self.title = title
        self.game_container = game_container
        self.instruction = instruction
        self.stats_btn = stats_btn
        self.logout_btn = logout_btn
        
        self.apply_theme()
        
    def toggle_theme(self):
        self.main_window.theme_manager.toggle_theme()
        self.main_window.apply_theme_to_all()
        
    def show_stats(self):
        """Show dedicated stats screen"""
        self.main_window.show_stats()
    
    def logout_clicked(self):
        """Handle logout"""
        self.user_manager.current_user = None
        self.player_score = 0
        self.computer_score = 0
        self.main_window.show_welcome()

    def apply_theme(self):
        colors = self.main_window.theme_manager.get_theme_colors()
        
        self.setStyleSheet(f"background-color: {colors['bg_secondary']};")
        
        self.header_widget.setStyleSheet(f"""
            QWidget {{
                background: {colors['bg_primary']};
                border-radius: 6px;
            }}
        """)
        
        self.welcome_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {colors['blue']};")
        
        self.theme_btn.setText("☀️ Light" if self.main_window.theme_manager.is_dark_mode else "🌙 Dark")
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['gray']};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {colors['gray_hover']}; }}
        """)
        
        self.stats_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['yellow']};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {colors['yellow_hover']}; }}
        """)
        
        self.logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['red']};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {colors['red_hover']}; }}
        """)
        
        self.title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {colors['text_primary']}; margin: 5px 0;")
        
        self.game_container.setStyleSheet(f"""
            QWidget {{
                background: {colors['bg_primary']};
                border-radius: 8px;
            }}
        """)
        
        self.instruction.setStyleSheet(f"font-size: 12px; color: {colors['text_secondary']}; font-weight: bold; margin-bottom: 8px;")
        
        for btn in self.game_buttons:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {btn.choice_color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {btn.choice_color}dd;
                }}
            """)
        
        self.result_label.setStyleSheet(f"""
            font-size: 12px; 
            color: {colors['text_secondary']}; 
            padding: 10px; 
            background: {colors['bg_primary']};
            border-radius: 6px; 
            font-weight: bold;
        """)
        
        self.score_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {colors['text_primary']}; margin: 5px;")
        
    def update_welcome_message(self):
        """Update welcome message when user changes"""
        if self.user_manager.current_user:
            self.welcome_label.setText(f"Welcome, {self.user_manager.current_user}! 🎮")
        
    def play_game(self, player_choice):
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
        
        # Determine winner
        result_type = None
        if player_choice == computer_choice:
            result = "It's a tie! 🤝"
            result_color = self.main_window.theme_manager.get_theme_colors()['yellow']
            result_type = "tie"
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissors" and computer_choice == "paper"):
            result = "You win! 🎉"
            result_color = self.main_window.theme_manager.get_theme_colors()['green']
            result_type = "win"
            self.player_score += 1
        else:
            result = "Computer wins! 😅"
            result_color = self.main_window.theme_manager.get_theme_colors()['red']
            result_type = "loss"
            self.computer_score += 1
        
        # Save game result
        self.user_manager.save_game_result(result_type)
        
        # Update displays
        emoji_map = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        self.result_label.setText(f"You: {emoji_map[player_choice]} vs Computer: {emoji_map[computer_choice]}\n{result}")
        
        colors = self.main_window.theme_manager.get_theme_colors()
        self.result_label.setStyleSheet(f"""
            font-size: 12px; 
            color: {result_color}; 
            padding: 10px; 
            background: {colors['bg_primary']};
            border-radius: 6px; 
            border: 3px solid {result_color};
            font-weight: bold;
        """)
        
        self.score_label.setText(f"Session Score - You: {self.player_score} | Computer: {self.computer_score}")
        
        # Simple animation effect
        self.animate_result()
        
    def animate_result(self):
        """Simple result animation"""
        try:
            effect = QGraphicsOpacityEffect()
            self.result_label.setGraphicsEffect(effect)
            
            self.pulse_animation = QPropertyAnimation(effect, b"opacity")
            self.pulse_animation.setDuration(500)
            self.pulse_animation.setStartValue(0.3)
            self.pulse_animation.setEndValue(1.0)
            self.pulse_animation.start()
        except:
            pass  # Skip animation if it fails
    
    def show_stats(self):
        """Show dedicated stats screen"""
        self.main_window.show_stats()


class EnhancedMainWindow(QMainWindow):
    """Enhanced main window with better error handling"""
    def __init__(self):
        super().__init__()
        print("🔧 Creating EnhancedMainWindow...")
        
        self.setWindowTitle("Rock Paper Scissors 🎮")
        
        # Set proper window size and make it resizable
        self.setGeometry(100, 100, 500, 400)
        self.setMinimumSize(500, 400)
        self.setMaximumSize(800, 600)
        self.resize(500, 400)
        
        # Ensure proper window flags for controls
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowTitleHint | 
            Qt.WindowType.WindowCloseButtonHint | 
            Qt.WindowType.WindowMinimizeButtonHint | 
            Qt.WindowType.WindowMaximizeButtonHint
            if PYQT_VERSION == 6 else
            Qt.Window | 
            Qt.WindowTitleHint | 
            Qt.WindowCloseButtonHint | 
            Qt.WindowMinimizeButtonHint | 
            Qt.WindowMaximizeButtonHint
        )
        
        # Theme manager
        self.theme_manager = ThemeManager()
        
        # User manager
        self.user_manager = EnhancedUserManager()
        
        # Create stacked widget for screens
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Create screens
        self.splash_screen = SplashScreen(self)
        self.credit_screen = CreditScreen(self)
        self.welcome_screen = WelcomeScreen(self.user_manager, self)
        self.login_screen = EnhancedLoginScreen(self.user_manager, self)
        self.register_screen = EnhancedRegisterScreen(self.user_manager, self)
        self.game_screen = EnhancedGameScreen(self.user_manager, self)
        self.stats_screen = StatsScreen(self.user_manager, self)
        
        # Add screens to stack
        self.stack.addWidget(self.splash_screen)    # Index 0
        self.stack.addWidget(self.credit_screen)    # Index 1
        self.stack.addWidget(self.welcome_screen)   # Index 2
        self.stack.addWidget(self.login_screen)     # Index 3
        self.stack.addWidget(self.register_screen)  # Index 4
        self.stack.addWidget(self.game_screen)      # Index 5
        self.stack.addWidget(self.stats_screen)     # Index 6
        
        # Apply initial theme
        self.apply_theme_to_all()
        
        # Start with splash screen and animation sequence
        self.start_app_sequence()
        
        print("✅ EnhancedMainWindow setup complete")
        
    def start_app_sequence(self):
        """Start the application with splash and credit screens"""
        self.stack.setCurrentIndex(0)  # Show splash screen
        
        # Setup fade animations
        self.setup_fade_animation(self.splash_screen)
        
        # Show splash for 2 seconds, then credit screen
        QTimer.singleShot(2000, self.show_credit_with_fade)
        
    def setup_fade_animation(self, widget):
        """Setup fade in animation for a widget"""
        self.fade_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.fade_effect)
        
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad if PYQT_VERSION == 6 else QEasingCurve.InOutQuad)
        self.fade_animation.start()
        
    def show_credit_with_fade(self):
        """Show credit screen with fade effect"""
        self.stack.setCurrentIndex(1)
        self.setup_fade_animation(self.credit_screen)
        
        # Show credit for 2 seconds, then welcome screen
        QTimer.singleShot(2000, self.show_welcome_with_fade)
        
    def show_welcome_with_fade(self):
        """Show welcome screen with fade effect"""
        self.stack.setCurrentIndex(2)
        self.setup_fade_animation(self.welcome_screen)
        
    def apply_theme_to_all(self):
        """Apply current theme to all screens"""
        colors = self.theme_manager.get_theme_colors()
        self.setStyleSheet(f"QMainWindow {{ background-color: {colors['bg_secondary']}; }}")
        
        # Apply theme to all screens
        self.splash_screen.apply_theme()
        self.credit_screen.apply_theme()
        self.welcome_screen.apply_theme()
        self.login_screen.apply_theme()
        self.register_screen.apply_theme()
        self.game_screen.apply_theme()
        self.stats_screen.apply_theme()
        
    def show_welcome(self):
        print("🏠 Switching to welcome screen")
        self.stack.setCurrentIndex(2)
        
    def show_login(self):
        print("📋 Switching to enhanced login screen")
        self.stack.setCurrentIndex(3)
        self.login_screen.clear_form()
        
    def show_register(self):
        print("📝 Switching to register screen")
        self.stack.setCurrentIndex(4)
        self.register_screen.clear_form()
        
    def show_game(self):
        print("🎮 Switching to enhanced game screen")
        if self.user_manager.current_user:
            self.game_screen.update_welcome_message()
            self.stack.setCurrentIndex(5)
        else:
            print("❌ No user logged in, staying on welcome screen")
            self.show_welcome()
            
    def show_stats(self):
        print("📊 Switching to stats screen")
        self.stack.setCurrentIndex(6)
        self.stats_screen.update_stats()


def main():
    """Enhanced main function with better error handling"""
    print("🚀 Starting Enhanced Rock Paper Scissors Ultimate Gaming Experience...")
    
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    print(f"✅ Application created with PyQt{PYQT_VERSION}")
    print(f"📋 Platform: {app.platformName()}")
    
    # Set application icon if it exists
    icon_path = "rock-paper-scissors.ico"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        print("🎨 Icon set")
    
    # Create main window with error handling
    try:
        window = EnhancedMainWindow()
        print("✅ Enhanced window created successfully")
    except Exception as e:
        print(f"❌ Error creating enhanced window: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Show window
    print("👁️  Showing enhanced window...")
    window.show()
    
    # Center window
    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()
    window_geometry = window.frameGeometry()
    window_geometry.moveCenter(screen_geometry.center())
    window.move(window_geometry.topLeft())
    
    print("✅ Enhanced application should now be visible and fully functional!")
    print("💡 Features: Enhanced UI, animations, statistics tracking, improved login")
    
    # Run application
    return app.exec() if PYQT_VERSION == 6 else app.exec_()


if __name__ == "__main__":
    try:
        result = main()
        print(f"🏁 Enhanced application finished with code: {result}")
        sys.exit(result)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)