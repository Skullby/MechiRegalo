from flask import Flask, render_template, request
from datetime import datetime
from collections import Counter
import re


app = Flask(__name__)

# Load the chat history from the text file (assumes chat_history.txt is in the same directory as app.py)
def load_chat_history():
    with open('chat_history.txt', 'r', encoding='utf-8') as file:
        chat_lines = file.readlines()
    return chat_lines

# Function to count occurrences of "Te amo" by sender, allowing for variations like "te amoooo"
def count_te_amo(chat_lines):
    te_amo_nico = 0
    te_amo_mechi = 0
    # Regular expression to match "te amo" with any number of trailing "o"s
    te_amo_pattern = re.compile(r'\bte amo+o*\b', re.IGNORECASE)
    
    for line in chat_lines:
        # Convert the line to lowercase and check if it matches the "te amo" pattern
        if te_amo_pattern.search(line):
            if "nicolas yunes" in line.lower():
                te_amo_nico += 1
            elif "mecho aguirre" in line.lower():
                te_amo_mechi += 1
    return te_amo_nico, te_amo_mechi


def count_messages_by_hour(chat_lines):
    hourly_counter = [0] * 24  # 24-hour array for message count per hour
    for line in chat_lines:
        if line.startswith('['):  # Assuming each message line starts with a timestamp like [15/11/2019, 1:58:08 PM]
            try:
                # Extract the time part (HH:MM:SS AM/PM), handle any non-breaking spaces or extra characters
                timestamp = line.split(']')[0][1:]  # Extracts the timestamp [15/11/2019, 1:58:08 PM]
                time_part = timestamp.split(',')[1].strip()  # Get the time part (1:58:08 PM)
                
                # Replace any non-breaking spaces (Unicode \u202F) with normal spaces
                time_part = time_part.replace('\u202F', ' ')
                
                # Extract the HH:MM:SS part and the AM/PM part
                time_str = time_part.split(' ')[0]  # Get time string HH:MM:SS
                am_pm = time_part.split(' ')[-1]  # Get AM/PM
                
                # Split time into hour, minute, and second
                hour, minute, second = time_str.split(':')
                hour = int(hour)

                # Convert 12-hour format to 24-hour format
                if am_pm == "PM" and hour != 12:
                    hour += 12
                elif am_pm == "AM" and hour == 12:
                    hour = 0  # Midnight case

                # Increment message count for the corresponding hour
                hourly_counter[hour] += 1

            except (ValueError, IndexError):
                continue

    return hourly_counter





# Function to count occurrences of "mlem" by sender, case-insensitive
def count_mlem(chat_lines):
    mlem_nico = 0
    mlem_mechi = 0
    # Case-insensitive "mlem" matching
    for line in chat_lines:
        if "mlem" in line.lower():
            if "nicolas yunes" in line.lower():
                mlem_nico += 1
            elif "mecho aguirre" in line.lower():
                mlem_mechi += 1
    return mlem_nico, mlem_mechi



def filter_by_date(chat_lines, start_date, end_date):
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_lines = []
        for line in chat_lines:
            # Assuming chat history lines contain a date at the start in format like [01/01/2024]
            if line.startswith('['):
                try:
                    line_date = datetime.strptime(line[1:11], '%d/%m/%Y')
                    if start_date <= line_date <= end_date:
                        filtered_lines.append(line)
                except ValueError:
                    continue
        return filtered_lines
    return chat_lines

# Function to filter messages by sender
def filter_by_sender(chat_lines, sender):
    if sender == 'nico':
        return [line for line in chat_lines if "Nicolas Yunes" in line]
    elif sender == 'mechi':
        return [line for line in chat_lines if "Mecho Aguirre" in line]
    return chat_lines

# Route for the homepage and search functionality
@app.route('/', methods=['GET', 'POST'])
def home():
    query = None
    results = None
    start_date = None
    end_date = None
    sender_filter = None
    
    # Initialize the variables with default values
    te_amo_nico = 0
    te_amo_mechi = 0
    hourly_messages = [0] * 24  # 24-hour array with default values of 0
    mlem_nico = 0
    mlem_mechi = 0

    # Load chat history
    chat_history = load_chat_history()

    # Run the counting functions (if chat history is available)
    if chat_history:
        te_amo_nico, te_amo_mechi = count_te_amo(chat_history)
        hourly_messages = count_messages_by_hour(chat_history)
        mlem_nico, mlem_mechi = count_mlem(chat_history)

    if request.method == 'POST':
        query = request.form.get('query')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        sender_filter = request.form.get('sender')

        # Apply query filter
        if query:
            chat_history = [line for line in chat_history if query.lower() in line.lower()]
        
        # Apply date filter
        chat_history = filter_by_date(chat_history, start_date, end_date)
        
        # Apply sender filter
        if sender_filter:
            chat_history = filter_by_sender(chat_history, sender_filter)
        
        results = chat_history

    return render_template(
        'index.html',
        query=query, results=results, start_date=start_date, end_date=end_date, sender_filter=sender_filter,
        te_amo_nico=te_amo_nico, te_amo_mechi=te_amo_mechi,
        hourly_messages=hourly_messages,
        mlem_nico=mlem_nico, mlem_mechi=mlem_mechi
    )

if __name__ == '__main__':
    app.run(debug=True)

