"""
Informatica Environment Quick Launcher
One-click access to all Informatica environments through Okta SSO
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import webbrowser
import os
import subprocess
import platform
import html
import random
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageTk
import requests


class InformaticaLauncher:
    """Main launcher application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Informatica Quick Launcher")
        self.root.geometry("520x700")
        self.root.resizable(False, False)
        
        # Quiz state
        self.current_quiz = None
        self.quiz_answered = False
        self.selected_answer = None
        self.answer_buttons = []
        
        # Load button icons
        self.button_icon = None
        self.app_icons = {}
        icon_path = Path(__file__).parent / "informatica_logo.png"
        if icon_path.exists():
            try:
                # Set window icon
                icon_img = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, icon_img)
                
                # Load smaller icon for buttons
                img = Image.open(icon_path)
                img = img.resize((24, 24), Image.LANCZOS)
                self.button_icon = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Could not load icons: {e}")
        
        # Load configuration
        self.config = self.load_config()
        
        # Set window icon and style
        self.setup_styles()
        
        # Load daily quiz
        self.load_daily_quiz()
        
        # Create UI
        self.create_header()
        self.create_environment_buttons()
        self.create_footer()
        
        # Center window
        self.center_window()
    
    def load_config(self):
        """Load environment configuration from JSON file"""
        config_path = Path(__file__).parent / "config.json"
        
        if not config_path.exists():
            messagebox.showerror(
                "Configuration Error",
                f"Config file not found: {config_path}\n\nPlease create config.json"
            )
            self.root.quit()
            return {}
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showerror(
                "Configuration Error",
                f"Invalid JSON in config.json:\n{e}"
            )
            self.root.quit()
            return {}
    
    def setup_styles(self):
        """Configure UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom button styles
        style.configure('Dev.TButton', 
                       background='#4CAF50', 
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=15)
        
        style.configure('QA.TButton',
                       background='#2196F3',
                       foreground='white', 
                       font=('Arial', 12, 'bold'),
                       padding=15)
        
        style.configure('UAT.TButton',
                       background='#FF9800',
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=15)
        
        style.configure('Prod.TButton',
                       background='#F44336',
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=15)
        
        # Hover effects
        style.map('Dev.TButton', background=[('active', '#45a049')])
        style.map('QA.TButton', background=[('active', '#1976D2')])
        style.map('UAT.TButton', background=[('active', '#F57C00')])
        style.map('Prod.TButton', background=[('active', '#D32F2F')])
    
    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.root, bg='#E6F3FF', height=120)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Try to load and display logo
        logo_path = Path(__file__).parent / "informatica_logo.png"
        if logo_path.exists():
            try:
                # Load and resize logo
                img = Image.open(logo_path)
                img = img.resize((50, 50), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Store reference to prevent garbage collection
                self.logo_image = photo
                
                logo_label = tk.Label(
                    header_frame,
                    image=photo,
                    bg='#E6F3FF'
                )
                logo_label.pack(pady=(10, 5))
            except Exception as e:
                print(f"Could not load logo: {e}")
        
        title_label = tk.Label(
            header_frame,
            text="Informatica Quick Launcher",
            font=('Arial', 13, 'bold'),
            bg='#E6F3FF',
            fg='#0055aa',
            wraplength=500
        )
        title_label.pack(pady=(2, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Click environment to launch via Okta SSO",
            font=('Arial', 8),
            bg='#E6F3FF',
            fg='#555'
        )
        subtitle_label.pack(pady=(0, 5))
    
    def create_environment_buttons(self):
        """Create tabbed interface for categories"""
        # Create tab container
        tab_container = tk.Frame(self.root, bg='white')
        tab_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create tab buttons frame
        tab_frame = tk.Frame(tab_container, bg='#D6E8FF', height=45)
        tab_frame.pack(fill=tk.X, padx=0, pady=0)
        tab_frame.pack_propagate(False)
        
        # Create content frame
        self.content_frame = tk.Frame(tab_container, bg='white')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Get categories
        categories = self.config.get('categories', {})
        
        if not categories:
            # Fallback to old format
            environments = self.config.get('environments', [])
            categories = {'Informatica': environments}
        
        # Create tab buttons
        self.tab_buttons = {}
        self.tab_contents = {}
        
        for idx, (category_name, items) in enumerate(categories.items()):
            # Create tab button
            tab_btn = tk.Button(
                tab_frame,
                text=category_name,
                font=('Arial', 11, 'bold'),
                bg='#D6E8FF',
                fg='#0055aa',
                activebackground='#B8D8F5',
                activeforeground='#0055aa',
                relief=tk.FLAT,
                borderwidth=0,
                cursor='hand2',
                padx=20,
                pady=10,
                command=lambda cat=category_name: self.switch_tab(cat)
            )
            tab_btn.pack(side=tk.LEFT, padx=2)
            self.tab_buttons[category_name] = tab_btn
            self.tab_contents[category_name] = items
        
        # Add Quiz tab
        quiz_tab_btn = tk.Button(
            tab_frame,
            text="Quiz",
            font=('Arial', 11, 'bold'),
            bg='#D6E8FF',
            fg='#0055aa',
            activebackground='#B8D8F5',
            activeforeground='#0055aa',
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            padx=20,
            pady=10,
            command=lambda: self.switch_tab("Quiz")
        )
        quiz_tab_btn.pack(side=tk.LEFT, padx=2)
        self.tab_buttons["Quiz"] = quiz_tab_btn
        
        # Show first tab by default
        first_category = list(categories.keys())[0] if categories else None
        if first_category:
            self.switch_tab(first_category)
    
    def switch_tab(self, category_name):
        """Switch to selected tab"""
        # Update tab button styles
        for cat, btn in self.tab_buttons.items():
            if cat == category_name:
                btn.config(bg='white', relief=tk.RAISED, borderwidth=1)
            else:
                btn.config(bg='#D6E8FF', relief=tk.FLAT, borderwidth=0)
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Check if this is the Quiz tab
        if category_name == "Quiz":
            self.show_quiz_tab()
            return
        
        # Get items for this category
        items = self.tab_contents.get(category_name, [])
        
        if not items:
            no_env_label = tk.Label(
                self.content_frame,
                text=f"No items in {category_name}",
                font=('Arial', 12),
                fg='#888',
                bg='white'
            )
            no_env_label.pack(pady=50)
            return
        
        # Add logout button at the top
        logout_btn = tk.Button(
            self.content_frame,
            text="Logout from Okta",
            font=('Arial', 10),
            bg='#FFB6C1',
            fg='#1a1a1a',
            activebackground='#FFA0B0',
            activeforeground='#1a1a1a',
            relief=tk.RAISED,
            borderwidth=1,
            cursor='hand2',
            command=self.logout_okta
        )
        logout_btn.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Add separator
        separator = tk.Frame(self.content_frame, height=2, bg='#e0e0e0')
        separator.pack(fill=tk.X, pady=5)
        
        # Add environment/app buttons
        for idx, item in enumerate(items):
            self.create_environment_button(self.content_frame, item, idx)
    
    def create_environment_button(self, parent, env, index):
        """Create a single environment button"""
        name = env.get('name', 'Unknown')
        short_name = env.get('shortName', name)
        url = env.get('url', '')
        custom_icon = env.get('icon', None)
        
        # Load custom icon if specified
        btn_icon = self.button_icon  # Default to Informatica icon
        if custom_icon:
            icon_path = Path(__file__).parent / custom_icon
            if icon_path.exists() and custom_icon not in self.app_icons:
                try:
                    img = Image.open(icon_path)
                    img = img.resize((24, 24), Image.LANCZOS)
                    self.app_icons[custom_icon] = ImageTk.PhotoImage(img)
                    btn_icon = self.app_icons[custom_icon]
                except Exception as e:
                    print(f"Could not load icon {custom_icon}: {e}")
            elif custom_icon in self.app_icons:
                btn_icon = self.app_icons[custom_icon]
        
        # Create button - all light blue with icon
        btn = tk.Button(
            parent,
            text=f"  {short_name}",
            font=('Arial', 12, 'bold'),
            bg='#87CEEB',
            fg='#1a1a1a',
            activebackground='#6FB8DC',
            activeforeground='#1a1a1a',
            relief=tk.RAISED,
            borderwidth=1,
            cursor='hand2',
            command=lambda u=url, n=name: self.launch_environment(u, n),
            compound=tk.LEFT,
            image=btn_icon if btn_icon else None
        )
        btn.pack(fill=tk.X, pady=6, ipady=10)
        
        # Bind hover effects
        btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#6FB8DC'))
        btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#87CEEB'))
    
    
    def launch_environment(self, url, name):
        """Launch environment in browser"""
        if not url:
            messagebox.showerror("Error", f"No URL configured for {name}")
            return
        
        try:
            webbrowser.open(url)
            self.log_access(name)
            
            # Show confirmation
            status_text = f"✓ Launched {name}"
            self.update_status(status_text)
            
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to open {name}:\n{e}"
            )
    
    def logout_okta(self):
        """Logout from Okta SSO"""
        logout_url = self.config.get('okta_logout_url')
        
        if not logout_url:
            # Fallback to default Okta logout pattern
            okta_domain = self.config.get('okta_domain', '')
            if okta_domain:
                logout_url = f"{okta_domain.rstrip('/')}/login/signout"
            else:
                messagebox.showwarning(
                    "Logout URL Missing",
                    "No Okta logout URL configured in config.json"
                )
                return
        
        try:
            webbrowser.open(logout_url)
            self.update_status("✓ Opened Okta logout page")
            
            # Log the logout
            log_file = Path(__file__).parent / "access_log.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(log_file, 'a') as f:
                    f.write(f"{timestamp} - Logged out from Okta\n")
            except Exception:
                pass
                
        except Exception as e:
            messagebox.showerror(
                "Logout Error",
                f"Failed to open logout page:\n{e}"
            )
    
    def log_access(self, env_name):
        """Log environment access for tracking"""
        log_file = Path(__file__).parent / "access_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_file, 'a') as f:
                f.write(f"{timestamp} - Accessed: {env_name}\n")
        except Exception:
            pass  # Silent fail for logging
    
    def show_quiz_tab(self):
        """Show quiz in its own tab"""
        if not self.current_quiz:
            no_quiz_label = tk.Label(
                self.content_frame,
                text="No quiz available today",
                font=('Arial', 12),
                fg='#888',
                bg='white'
            )
            no_quiz_label.pack(pady=50)
            return
        
        # Header with date
        today = datetime.now().strftime("%B %d, %Y")
        header_frame = tk.Frame(self.content_frame, bg='#FFE5B4')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = tk.Label(
            header_frame,
            text=f"📚 Daily Quiz - {today}",
            font=('Arial', 14, 'bold'),
            bg='#FFE5B4',
            fg='#8B4513'
        )
        header_label.pack(pady=15)
        
        # Question text
        question_frame = tk.Frame(self.content_frame, bg='white')
        question_frame.pack(fill=tk.X, padx=30, pady=(10, 20))
        
        question_label = tk.Label(
            question_frame,
            text=self.current_quiz['question'],
            font=('Arial', 12),
            bg='white',
            fg='#333',
            wraplength=450,
            justify=tk.LEFT
        )
        question_label.pack(anchor=tk.W)
        
        # Answer buttons frame
        answers_frame = tk.Frame(self.content_frame, bg='white')
        answers_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Prepare all answers and shuffle
        all_answers = [self.current_quiz['correct_answer']] + self.current_quiz['incorrect_answers']
        random.shuffle(all_answers)
        
        # Reset answer buttons
        self.answer_buttons = []
        
        # Create answer buttons - stacked vertically for better readability
        for idx, answer in enumerate(all_answers):
            btn = tk.Button(
                answers_frame,
                text=f"{chr(65+idx)}) {answer}",  # A), B), C), D)
                font=('Arial', 11),
                bg='#87CEEB',
                fg='#1a1a1a',
                activebackground='#6FB8DC',
                relief=tk.RAISED,
                borderwidth=1,
                cursor='hand2',
                wraplength=400,
                justify=tk.LEFT,
                anchor='w',
                padx=20,
                pady=15,
                command=lambda a=answer: self.check_answer(a)
            )
            btn.pack(fill=tk.X, pady=8)
            self.answer_buttons.append((btn, answer))
        
        # Control buttons
        control_frame = tk.Frame(self.content_frame, bg='white')
        control_frame.pack(fill=tk.X, padx=30, pady=(20, 10))
        
        self.show_answer_btn = tk.Button(
            control_frame,
            text="Show Answer",
            font=('Arial', 10),
            bg='#FFD700',
            fg='#1a1a1a',
            activebackground='#FFC700',
            relief=tk.RAISED,
            borderwidth=1,
            cursor='hand2',
            command=self.show_answer,
            padx=15,
            pady=8
        )
        self.show_answer_btn.pack(side=tk.LEFT, padx=5)
        
        self.result_label = tk.Label(
            control_frame,
            text="",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        )
        self.result_label.pack(side=tk.LEFT, padx=15)
    
    def create_footer(self):
        """Create footer with status bar"""
        footer_frame = tk.Frame(self.root, bg='#f5f5f5', height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            footer_frame,
            text="Ready • Tip: Click Logout before switching environments",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666',
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Add refresh button
        refresh_btn = tk.Button(
            footer_frame,
            text="⟳ Reload",
            font=('Arial', 8),
            bg='#e0e0e0',
            fg='#333',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.reload_config
        )
        refresh_btn.pack(side=tk.RIGHT, padx=15, pady=5)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))
    
    def reload_config(self):
        """Reload configuration and rebuild UI"""
        # Reload icons
        self.app_icons = {}
        
        # Reset quiz state
        self.quiz_answered = False
        self.selected_answer = None
        self.answer_buttons = []
        
        self.config = self.load_config()
        self.load_daily_quiz()
        
        # Clear and rebuild UI
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_header()
        self.create_environment_buttons()
        self.create_footer()
        
        self.update_status("Configuration reloaded")
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_daily_quiz(self):
        """Load or fetch daily quiz question"""
        cache_file = Path(__file__).parent / "quiz_cache.json"
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Try to load from cache
        cache_data = {'history': []}
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                # If we have today's question, use it
                if cache_data.get('current_date') == today and cache_data.get('current_question'):
                    self.current_quiz = cache_data['current_question']
                    return
            except Exception as e:
                print(f"Error loading quiz cache: {e}")
                cache_data = {'history': []}
        
        # Fetch new question
        self.current_quiz = self.fetch_quiz_question()
        
        # Add to history
        if 'history' not in cache_data:
            cache_data['history'] = []
        
        # Keep last 30 days of history
        cache_data['history'] = cache_data['history'][-29:] if len(cache_data['history']) > 29 else cache_data['history']
        cache_data['history'].append({
            'date': today,
            'question': self.current_quiz['question']
        })
        
        # Save to cache
        self.save_quiz_cache(today, cache_data['history'])
    
    def fetch_quiz_question(self):
        """Fetch a quiz question from Open Trivia Database API"""
        fallback_questions = [
            {
                "question": "What is the capital of Australia?",
                "correct_answer": "Canberra",
                "incorrect_answers": ["Sydney", "Melbourne", "Brisbane"]
            },
            {
                "question": "What is the largest planet in our solar system?",
                "correct_answer": "Jupiter",
                "incorrect_answers": ["Saturn", "Neptune", "Uranus"]
            },
            {
                "question": "In what year did World War II end?",
                "correct_answer": "1945",
                "incorrect_answers": ["1944", "1946", "1943"]
            },
            {
                "question": "What is the smallest prime number?",
                "correct_answer": "2",
                "incorrect_answers": ["1", "3", "5"]
            },
            {
                "question": "Which element has the chemical symbol 'Au'?",
                "correct_answer": "Gold",
                "incorrect_answers": ["Silver", "Aluminum", "Argon"]
            },
            {
                "question": "What is the speed of light in vacuum (approximately)?",
                "correct_answer": "299,792 km/s",
                "incorrect_answers": ["150,000 km/s", "500,000 km/s", "250,000 km/s"]
            },
            {
                "question": "Which country has the longest coastline in the world?",
                "correct_answer": "Canada",
                "incorrect_answers": ["Russia", "Indonesia", "Norway"]
            },
            {
                "question": "What is the most abundant gas in Earth's atmosphere?",
                "correct_answer": "Nitrogen",
                "incorrect_answers": ["Oxygen", "Carbon Dioxide", "Argon"]
            }
        ]
        
        # Analytical/Educational categories only:
        # 17=Science & Nature, 22=Geography, 23=History, 9=General Knowledge
        categories = [17, 22, 23, 9]
        selected_category = random.choice(categories)
        
        try:
            # Try to fetch from API with specific analytical categories
            response = requests.get(
                f"https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple&category={selected_category}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('response_code') == 0 and data.get('results'):
                    result = data['results'][0]
                    # Decode HTML entities
                    return {
                        'question': html.unescape(result['question']),
                        'correct_answer': html.unescape(result['correct_answer']),
                        'incorrect_answers': [html.unescape(ans) for ans in result['incorrect_answers']]
                    }
        except Exception as e:
            print(f"Error fetching quiz from API: {e}")
        
        # Fallback to built-in questions
        return random.choice(fallback_questions)
    
    def save_quiz_cache(self, date, history=None):
        """Save current quiz to cache file"""
        cache_file = Path(__file__).parent / "quiz_cache.json"
        
        try:
            cache = {
                'current_date': date,
                'current_question': self.current_quiz,
                'history': history if history is not None else []
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving quiz cache: {e}")
    
    def check_answer(self, selected_answer):
        """Check if selected answer is correct and provide visual feedback"""
        if self.quiz_answered:
            return  # Already answered
        
        self.quiz_answered = True
        self.selected_answer = selected_answer
        correct_answer = self.current_quiz['correct_answer']
        
        # Update button colors
        for btn, answer in self.answer_buttons:
            if answer == correct_answer:
                # Highlight correct answer in green
                btn.config(bg='#90EE90', fg='#006400', relief=tk.SUNKEN)
            elif answer == selected_answer and answer != correct_answer:
                # Highlight wrong selection in red
                btn.config(bg='#FFB6C1', fg='#8B0000', relief=tk.SUNKEN)
            else:
                # Dim other answers
                btn.config(bg='#E0E0E0', state=tk.DISABLED)
            
            # Disable all buttons
            btn.config(state=tk.DISABLED)
        
        # Show result message
        if selected_answer == correct_answer:
            self.result_label.config(text="✓ Correct!", fg='#006400')
        else:
            self.result_label.config(text="✗ Incorrect", fg='#8B0000')
        
        # Disable show answer button since answer is now visible
        self.show_answer_btn.config(state=tk.DISABLED)
    
    def show_answer(self):
        """Reveal the correct answer without selecting"""
        if self.quiz_answered:
            return
        
        self.quiz_answered = True
        correct_answer = self.current_quiz['correct_answer']
        
        # Highlight correct answer
        for btn, answer in self.answer_buttons:
            if answer == correct_answer:
                btn.config(bg='#90EE90', fg='#006400', relief=tk.SUNKEN)
            else:
                btn.config(bg='#E0E0E0')
            btn.config(state=tk.DISABLED)
        
        self.result_label.config(text=f"Answer: {correct_answer}", fg='#0055aa')
        self.show_answer_btn.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = InformaticaLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
