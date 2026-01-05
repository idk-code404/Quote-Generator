import random
import datetime
import time
import sys
import os

# Collection of inspirational quotes
QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"quote": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle"},
    {"quote": "Whoever is happy will make others happy too.", "author": "Anne Frank"},
    {"quote": "You only live once, but if you do it right, once is enough.", "author": "Mae West"},
    {"quote": "The purpose of our lives is to be happy.", "author": "Dalai Lama"},
    {"quote": "Get busy living or get busy dying.", "author": "Stephen King"},
    {"quote": "You have within you right now, everything you need to deal with whatever the world can throw at you.", "author": "Brian Tracy"},
    {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"quote": "The best way to predict the future is to create it.", "author": "Peter Drucker"},
    {"quote": "The only limit to our realization of tomorrow will be our doubts of today.", "author": "Franklin D. Roosevelt"},
    {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
    {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
    {"quote": "Keep your face always toward the sunshine - and shadows will fall behind you.", "author": "Walt Whitman"},
    {"quote": "Life is either a daring adventure or nothing at all.", "author": "Helen Keller"},
    {"quote": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu"},
    {"quote": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson"},
    {"quote": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky"},
    {"quote": "I have not failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison"}
]

def display_header():
    """Display a header with the current date"""
    today = datetime.date.today()
    print("=" * 60)
    print(" " * 20 + "DAILY QUOTE GENERATOR")
    print("=" * 60)
    print(f"Date: {today.strftime('%A, %B %d, %Y')}")
    print("-" * 60)

def get_daily_quote(seed=None):
    """
    Get a quote for today. If seed is provided, use it for deterministic
    daily selection. Otherwise, pick a random quote.
    """
    if seed is None:
        # Use today's date as a seed for daily consistency
        today = datetime.date.today()
        seed = today.toordinal()  # Convert date to integer
    
    # Set the seed for reproducibility
    random.seed(seed)
    
    # Select and return a quote
    return random.choice(QUOTES)

def display_quote(quote_data):
    """Display the quote in a nice format"""
    quote = quote_data["quote"]
    author = quote_data["author"]
    
    print("\n✨ TODAY'S QUOTE ✨")
    print("-" * 40)
    
    # Format long quotes with word wrapping
    words = quote.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= 50:  # Limit line width
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    # Print the formatted quote
    for line in lines:
        print(f"  {line}")
    
    print("-" * 40)
    print(f"  — {author}")
    print()

def save_quote_to_file(quote_data):
    """Save today's quote to a file"""
    today = datetime.date.today()
    filename = "daily_quotes.txt"
    
    try:
        # Check if file exists
        file_exists = os.path.exists(filename)
        
        with open(filename, "a", encoding="utf-8") as file:
            if not file_exists:
                file.write("DAILY QUOTE JOURNAL\n")
                file.write("=" * 50 + "\n\n")
            
            file.write(f"📅 {today.strftime('%A, %B %d, %Y')}\n")
            file.write(f"\"{quote_data['quote']}\"\n")
            file.write(f"— {quote_data['author']}\n")
            file.write("-" * 40 + "\n\n")
        
        return True
    except Exception as e:
        print(f"Could not save quote to file: {e}")
        return False

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 60)
    print("MENU:")
    print("  1. Get today's daily quote")
    print("  2. Get a random quote")
    print("  3. View quote history")
    print("  4. Exit")
    print("=" * 60)
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            if choice in ["1", "2", "3", "4"]:
                return int(choice)
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def view_quote_history():
    """Display saved quotes from file"""
    filename = "daily_quotes.txt"
    
    if not os.path.exists(filename):
        print("\nNo quote history found.")
        print("Generate some quotes first and they will be saved automatically.")
        return
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            print("\n" + "=" * 60)
            print("QUOTE HISTORY")
            print("=" * 60)
            print(content)
    except Exception as e:
        print(f"Error reading quote history: {e}")

def animate_text(text, delay=0.03):
    """Animate text typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def main():
    """Main program function"""
    # Clear screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Display welcome message with animation
    print("\n" + "=" * 60)
    animate_text("Welcome to the Daily Quote Generator!", 0.05)
    print("=" * 60)
    time.sleep(0.5)
    
    while True:
        display_header()
        choice = display_menu()
        
        if choice == 1:
            # Get today's quote
            quote = get_daily_quote()
            display_quote(quote)
            
            # Ask if user wants to save it
            save_option = input("Save this quote to your journal? (y/n): ").strip().lower()
            if save_option == 'y':
                if save_quote_to_file(quote):
                    print("Quote saved successfully!")
            
            input("\nPress Enter to continue...")
        
        elif choice == 2:
            # Get a random quote (not based on date)
            random.seed()  # Reset seed to current time
            quote = random.choice(QUOTES)
            display_quote(quote)
            
            # Ask if user wants to save it
            save_option = input("Save this quote to your journal? (y/n): ").strip().lower()
            if save_option == 'y':
                if save_quote_to_file(quote):
                    print("Quote saved successfully!")
            
            input("\nPress Enter to continue...")
        
        elif choice == 3:
            # View quote history
            view_quote_history()
            input("\nPress Enter to continue...")
        
        elif choice == 4:
            # Exit program
            print("\nThank you for using the Daily Quote Generator!")
            print("May your day be filled with inspiration! ✨")
            time.sleep(1)
            break
        
        # Clear screen for next iteration
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
