# Event Registration Priority Handling System

A simple event registration system with priority-based participant management.

## Features

- Register participants with name, email, and category (VIP/Regular/Guest)
- Automatic priority sorting (VIP → Regular → Guest)
- Real-time participant list display
- CSV-based data storage (no database required)

## Project Structure

```
.
├── app.py              # Flask backend
├── index.html          # Frontend HTML page
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## Setup & Run

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Flask backend:**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

3. **Open frontend:**
   - Open `index.html` in your browser
   - Or use a simple HTTP server:
     ```bash
     python -m http.server 8000
     ```
   - Then open `http://localhost:8000/index.html`

4. **Update API URL (if needed):**
   - If your backend is on a different URL, edit `index.html` and change the `API_URL` constant in the JavaScript section

### Docker Deployment

1. **Build Docker image:**
   ```bash
   docker build -t event-registration .
   ```

2. **Run container:**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/data:/app/data event-registration
   ```

### Deploy on Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the Dockerfile for deployment
4. Render will automatically build and deploy

**Note:** For production, update the `API_URL` in `index.html` to point to your Render backend URL.

## API Endpoints

- `POST /register` - Register a new participant
  - Body: `{ "name": "John Doe", "email": "john@example.com", "category": "VIP" }`
  
- `GET /participants` - Get all participants sorted by priority
  - Returns: Array of participants with name, email, category, and timestamp

- `GET /health` - Health check endpoint

## Data Storage

Participants are stored in `participants.csv` with the following format:
```
name,email,category,timestamp
John Doe,john@example.com,VIP,2024-01-15 10:30:00
```

## Notes

- No authentication required (as per requirements)
- Data persists in CSV file
- Frontend auto-refreshes every 5 seconds
- CORS enabled for cross-origin requests

