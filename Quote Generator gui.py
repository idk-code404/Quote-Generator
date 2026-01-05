import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import datetime
import json
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO

class DailyQuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Quote Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # Set application icon (using a placeholder)
        self.root.iconbitmap(default=self.create_default_icon())
        
        # Current quote
        self.current_quote = None
        self.favorite_quotes = []
        
        # Initialize quote collections
        self.quotes = self.load_quotes()
        
        # Set up the GUI
        self.setup_styles()
        self.create_widgets()
        self.load_favorites()
        
        # Load today's quote automatically
        self.get_todays_quote()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'accent': '#2c3e50',
            'secondary': '#3498db',
            'highlight': '#e74c3c',
            'success': '#27ae60',
            'quote_bg': '#ffffff',
            'button_bg': '#3498db',
            'button_fg': '#ffffff'
        }
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Helvetica', 24, 'bold'),
                       foreground=self.colors['accent'])
        
        style.configure('Quote.TLabel',
                       font=('Georgia', 14),
                       foreground=self.colors['fg'],
                       background=self.colors['quote_bg'])
        
        style.configure('Author.TLabel',
                       font=('Helvetica', 12, 'italic'),
                       foreground=self.colors['secondary'])
        
        style.configure('Accent.TButton',
                       font=('Helvetica', 10, 'bold'),
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       padding=10)
        
        style.map('Accent.TButton',
                 background=[('active', self.colors['secondary']),
                           ('pressed', self.colors['accent'])])
    
    def create_default_icon(self):
        """Create a default icon for the app"""
        # This is a workaround for missing icon file
        # In production, use an actual .ico file
        return None
    
    def load_quotes(self):
        """Load quotes from JSON file or use default"""
        quotes_file = "quotes.json"
        default_quotes = [
            {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "Inspiration"},
            {"quote": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon", "category": "Life"},
            {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "Dreams"},
            {"quote": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle", "category": "Perseverance"},
            {"quote": "Whoever is happy will make others happy too.", "author": "Anne Frank", "category": "Happiness"},
            {"quote": "You only live once, but if you do it right, once is enough.", "author": "Mae West", "category": "Life"},
            {"quote": "The purpose of our lives is to be happy.", "author": "Dalai Lama", "category": "Happiness"},
            {"quote": "Get busy living or get busy dying.", "author": "Stephen King", "category": "Motivation"},
            {"quote": "You have within you right now, everything you need to deal with whatever the world can throw at you.", "author": "Brian Tracy", "category": "Self-belief"},
            {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "Confidence"},
            {"quote": "The best way to predict the future is to create it.", "author": "Peter Drucker", "category": "Future"},
            {"quote": "The only limit to our realization of tomorrow will be our doubts of today.", "author": "Franklin D. Roosevelt", "category": "Doubt"},
            {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "Perseverance"},
            {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "category": "Perseverance"},
            {"quote": "Keep your face always toward the sunshine - and shadows will fall behind you.", "author": "Walt Whitman", "category": "Positivity"},
            {"quote": "Life is either a daring adventure or nothing at all.", "author": "Helen Keller", "category": "Adventure"},
            {"quote": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu", "category": "Journey"},
            {"quote": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson", "category": "Self-discovery"},
            {"quote": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky", "category": "Opportunity"},
            {"quote": "I have not failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison", "category": "Perseverance"}
        ]
        
        try:
            if os.path.exists(quotes_file):
                with open(quotes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create the file with default quotes
                with open(quotes_file, 'w', encoding='utf-8') as f:
                    json.dump(default_quotes, f, indent=2)
                return default_quotes
        except Exception:
            return default_quotes
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.colors['accent'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="✨ Daily Quote Generator ✨",
                              font=('Helvetica', 24, 'bold'),
                              fg='white',
                              bg=self.colors['accent'])
        title_label.pack(expand=True, pady=20)
        
        # Date display
        date_frame = tk.Frame(self.root, bg=self.colors['bg'])
        date_frame.pack(fill=tk.X, pady=(10, 0))
        
        today = datetime.date.today()
        self.date_label = tk.Label(date_frame,
                                  text=today.strftime('%A, %B %d, %Y'),
                                  font=('Helvetica', 12),
                                  fg=self.colors['secondary'],
                                  bg=self.colors['bg'])
        self.date_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Quote display area
        quote_container = tk.Frame(content_frame, 
                                  bg=self.colors['quote_bg'],
                                  relief=tk.RAISED,
                                  borderwidth=2)
        quote_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Quote text with scrollbar
        quote_frame = tk.Frame(quote_container, bg=self.colors['quote_bg'])
        quote_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        self.quote_text = tk.Text(quote_frame,
                                 wrap=tk.WORD,
                                 font=('Georgia', 16),
                                 bg=self.colors['quote_bg'],
                                 fg=self.colors['fg'],
                                 height=8,
                                 relief=tk.FLAT,
                                 padx=10,
                                 pady=10)
        self.quote_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar for long quotes
        quote_scrollbar = tk.Scrollbar(quote_frame, command=self.quote_text.yview)
        quote_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.quote_text.config(yscrollcommand=quote_scrollbar.set)
        
        # Author display
        self.author_label = tk.Label(quote_container,
                                    text="",
                                    font=('Helvetica', 14, 'italic'),
                                    fg=self.colors['secondary'],
                                    bg=self.colors['quote_bg'])
        self.author_label.pack(pady=(0, 20))
        
        # Category display
        self.category_label = tk.Label(quote_container,
                                      text="",
                                      font=('Helvetica', 10),
                                      fg=self.colors['accent'],
                                      bg=self.colors['quote_bg'])
        self.category_label.pack(pady=(0, 10))
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Top row of buttons
        top_button_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        top_button_frame.pack(pady=(0, 10))
        
        ttk.Button(top_button_frame, 
                  text="Today's Quote",
                  style='Accent.TButton',
                  command=self.get_todays_quote).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_button_frame,
                  text="Random Quote",
                  style='Accent.TButton',
                  command=self.get_random_quote).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_button_frame,
                  text="Next Quote",
                  style='Accent.TButton',
                  command=self.get_next_quote).pack(side=tk.LEFT, padx=5)
        
        # Bottom row of buttons
        bottom_button_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        bottom_button_frame.pack()
        
        self.favorite_button = ttk.Button(bottom_button_frame,
                                         text="⭐ Add to Favorites",
                                         style='Accent.TButton',
                                         command=self.toggle_favorite)
        self.favorite_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bottom_button_frame,
                  text="Save to File",
                  style='Accent.TButton',
                  command=self.save_quote).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bottom_button_frame,
                  text="View Favorites",
                  style='Accent.TButton',
                  command=self.view_favorites).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bottom_button_frame,
                  text="Copy Quote",
                  style='Accent.TButton',
                  command=self.copy_quote).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=self.colors['accent'], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                    text="Ready",
                                    font=('Helvetica', 9),
                                    fg='white',
                                    bg=self.colors['accent'])
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Quote counter
        self.counter_label = tk.Label(status_frame,
                                     text="",
                                     font=('Helvetica', 9),
                                     fg='white',
                                     bg=self.colors['accent'])
        self.counter_label.pack(side=tk.RIGHT, padx=10)
        
        # Update counter
        self.update_counter()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))
    
    def update_counter(self):
        """Update quote counter in status bar"""
        total = len(self.quotes)
        fav_count = len(self.favorite_quotes)
        self.counter_label.config(text=f"Quotes: {total} | Favorites: {fav_count}")
    
    def get_todays_quote(self):
        """Get quote based on today's date"""
        today = datetime.date.today()
        seed = today.toordinal()
        random.seed(seed)
        
        self.current_quote = random.choice(self.quotes)
        self.display_quote(self.current_quote)
        self.update_status("Today's quote loaded")
    
    def get_random_quote(self):
        """Get a completely random quote"""
        random.seed()
        self.current_quote = random.choice(self.quotes)
        self.display_quote(self.current_quote)
        self.update_status("Random quote loaded")
    
    def get_next_quote(self):
        """Get the next quote in sequence"""
        if not self.current_quote:
            self.get_random_quote()
            return
        
        current_index = self.quotes.index(self.current_quote)
        next_index = (current_index + 1) % len(self.quotes)
        self.current_quote = self.quotes[next_index]
        self.display_quote(self.current_quote)
        self.update_status("Next quote loaded")
    
    def display_quote(self, quote_data):
        """Display the quote in the text widget"""
        # Clear the text widget
        self.quote_text.delete(1.0, tk.END)
        
        # Insert the quote with formatting
        self.quote_text.insert(1.0, quote_data["quote"])
        
        # Configure tag for quote styling
        self.quote_text.tag_configure("center", justify='center')
        self.quote_text.tag_add("center", 1.0, tk.END)
        
        # Update author and category labels
        self.author_label.config(text=f"— {quote_data['author']}")
        
        category = quote_data.get('category', 'Uncategorized')
        self.category_label.config(text=f"Category: {category}")
        
        # Update favorite button
        self.update_favorite_button()
        
        # Disable editing
        self.quote_text.config(state=tk.DISABLED)
    
    def update_favorite_button(self):
        """Update the favorite button text based on current quote status"""
        if not self.current_quote:
            return
        
        if self.current_quote in self.favorite_quotes:
            self.favorite_button.config(text="★ Remove from Favorites")
        else:
            self.favorite_button.config(text="⭐ Add to Favorites")
    
    def toggle_favorite(self):
        """Add or remove current quote from favorites"""
        if not self.current_quote:
            messagebox.showwarning("No Quote", "No quote to add to favorites!")
            return
        
        if self.current_quote in self.favorite_quotes:
            self.favorite_quotes.remove(self.current_quote)
            self.update_status("Removed from favorites")
        else:
            self.favorite_quotes.append(self.current_quote)
            self.update_status("Added to favorites")
        
        self.save_favorites()
        self.update_favorite_button()
        self.update_counter()
    
    def save_favorites(self):
        """Save favorites to a file"""
        try:
            with open('favorites.json', 'w', encoding='utf-8') as f:
                json.dump(self.favorite_quotes, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save favorites: {e}")
    
    def load_favorites(self):
        """Load favorites from a file"""
        try:
            if os.path.exists('favorites.json'):
                with open('favorites.json', 'r', encoding='utf-8') as f:
                    self.favorite_quotes = json.load(f)
        except Exception:
            self.favorite_quotes = []
    
    def save_quote(self):
        """Save current quote to a text file"""
        if not self.current_quote:
            messagebox.showwarning("No Quote", "No quote to save!")
            return
        
        try:
            today = datetime.date.today()
            filename = f"quote_{today.strftime('%Y%m%d')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Daily Quote - {today.strftime('%B %d, %Y')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f'"{self.current_quote["quote"]}"\n')
                f.write(f"— {self.current_quote['author']}\n")  # FIXED: Use single quotes for dict key
                if 'category' in self.current_quote:
                    f.write(f"Category: {self.current_quote['category']}\n")
            
            self.update_status(f"Quote saved to {filename}")
            messagebox.showinfo("Success", f"Quote saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save quote: {e}")
    
    def view_favorites(self):
        """Open a new window to view favorite quotes"""
        if not self.favorite_quotes:
            messagebox.showinfo("No Favorites", "You haven't added any quotes to favorites yet!")
            return
        
        favorites_window = tk.Toplevel(self.root)
        favorites_window.title("Favorite Quotes")
        favorites_window.geometry("700x500")
        favorites_window.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Label(favorites_window,
                         text="⭐ Your Favorite Quotes",
                         font=('Helvetica', 18, 'bold'),
                         fg=self.colors['accent'],
                         bg=self.colors['bg'])
        header.pack(pady=10)
        
        # Create a scrolled text widget
        text_area = scrolledtext.ScrolledText(favorites_window,
                                             wrap=tk.WORD,
                                             font=('Georgia', 12),
                                             width=80,
                                             height=20)
        text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Insert all favorite quotes
        for i, quote in enumerate(self.favorite_quotes, 1):
            text_area.insert(tk.END, f"{i}. \"{quote['quote']}\"\n")
            text_area.insert(tk.END, f"   — {quote['author']}\n")
            if 'category' in quote:
                text_area.insert(tk.END, f"   Category: {quote['category']}\n")
            text_area.insert(tk.END, "-" * 60 + "\n\n")
        
        text_area.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(favorites_window,
                              text="Close",
                              style='Accent.TButton',
                              command=favorites_window.destroy)
        close_btn.pack(pady=10)
    
    def copy_quote(self):
        """Copy current quote to clipboard"""
        if not self.current_quote:
            messagebox.showwarning("No Quote", "No quote to copy!")
            return
        
        quote_text = f'"{self.current_quote["quote"]}"\n— {self.current_quote["author"]}'
        
        self.root.clipboard_clear()
        self.root.clipboard_append(quote_text)
        self.update_status("Quote copied to clipboard")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Daily Quote Generator",
            "Daily Quote Generator v2.0\n\n"
            "A simple application that provides inspirational quotes.\n"
            "Features:\n"
            "• Get today's quote\n"
            "• Random quotes\n"
            "• Save favorites\n"
            "• Copy to clipboard\n\n"
            "© 2023 Daily Quote Generator"
        )

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = DailyQuoteGenerator(root)
    
    # Add menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Current Quote", command=app.save_quote)
    file_menu.add_command(label="View Favorites", command=app.view_favorites)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Quotes menu
    quote_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Quotes", menu=quote_menu)
    quote_menu.add_command(label="Today's Quote", command=app.get_todays_quote)
    quote_menu.add_command(label="Random Quote", command=app.get_random_quote)
    quote_menu.add_command(label="Next Quote", command=app.get_next_quote)
    
    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=app.show_about)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
