from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# CSV file to store participants
CSV_FILE = 'participants.csv'

# Priority order: VIP > Regular > Guest
PRIORITY_ORDER = {'VIP': 1, 'Regular': 2, 'Guest': 3}


def init_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'email', 'category', 'timestamp'])


def read_participants():
    """Read all participants from CSV file"""
    participants = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            participants = list(reader)
    return participants


def write_participant(name, email, category):
    """Write a new participant to CSV file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, email, category, timestamp])


@app.route('/register', methods=['POST'])
def register():
    """Handle event registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data or 'email' not in data or 'category' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip()
        category = data['category'].strip()
        
        # Validate category
        if category not in PRIORITY_ORDER:
            return jsonify({'error': 'Invalid category. Must be VIP, Regular, or Guest'}), 400
        
        # Save participant
        write_participant(name, email, category)
        
        return jsonify({
            'message': 'Registration successful',
            'name': name,
            'email': email,
            'category': category
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/participants', methods=['GET'])
def get_participants():
    """Get all participants sorted by priority"""
    try:
        participants = read_participants()
        
        # Sort by priority (VIP → Regular → Guest)
        participants.sort(key=lambda x: PRIORITY_ORDER.get(x['category'], 999))
        
        return jsonify(participants), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


@app.route('/')
def index():
    """Serve the frontend HTML file"""
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    # Initialize CSV file on startup
    init_csv()
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

