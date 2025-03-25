# Pitch Deck Editor

A web application for creating and managing presentation slides with customizable templates and themes.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or higher
- Node.js 14 or higher
- npm (comes with Node.js)
- Git

## Clone the Repository

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd new_folder
```

## Backend Setup

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask development server:
```bash
# Make sure you're in the project root directory
python backend/app.py
```

The API server will be available at `http://localhost:5000`
and Swagger UI will be available at `http://localhost:5000/api`

## Frontend Setup

1. Navigate to the frontend directory and install dependencies:
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

2. Create a `.env` file in the frontend directory if it doesn't exist:
```bash
# Create .env file
echo VITE_API_URL=http://localhost:5000 > .env
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Development

- The backend API runs on `http://localhost:5000`
- The frontend development server runs on `http://localhost:3000`
- The frontend is configured to proxy API requests to the backend

## Project Structure

```
├── backend/            # Flask backend
│   ├── apis/           # API endpoints
│   ├── models/         # Database models
│   ├── app.py          # Main application file
│   └── requirements.txt #Python dependencies
├── frontend/           # React frontend
│   ├── src/            # Source files
│   ├── public/         # Static files
│   └── index.html      # HTML template
└──   # 
```

## Features

- Slide creation and management
- Customizable templates
- Theme support
- Image upload capability
- User authentication
- Real-time editing
