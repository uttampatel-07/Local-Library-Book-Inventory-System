# Local Library Book Inventory System (LLIS)

A comprehensive web-based book inventory management system built with Python Flask. This system allows you to manage your library's book collection with features for adding, editing, searching, and tracking book availability.

## Features

- 📚 **Book Management**: Add, edit, view, and delete books
- 🔍 **Search Functionality**: Search books by title, author, ISBN, or category
- 📊 **Dashboard Statistics**: View total books, copies, available, and borrowed counts
- 📖 **Borrow/Return System**: Track book availability with borrow and return functionality
- 🎨 **Modern UI**: Beautiful, responsive interface built with Bootstrap 5
- 💾 **SQLite Database**: Lightweight database for easy setup and portability

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Easy Method (Recommended)

**Windows Users:**
- Double-click `run_server.bat` to start the server
- Or right-click `run_server.ps1` and select "Run with PowerShell"

**All Platforms:**
- Double-click `run.py` (if Python is associated with .py files)
- Or run: `python run.py`

### Manual Method

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Adding a Book
1. Click on "Add Book" in the navigation menu
2. Fill in the book details:
   - **Title** (required)
   - **Author** (required)
   - **ISBN** (required, must be unique)
   - **Publisher** (optional)
   - **Publication Year** (optional)
   - **Category** (optional)
   - **Total Copies** (required)
   - **Description** (optional)
3. Click "Add Book" to save

### Viewing Books
- The home page displays all books in a table format
- Click the eye icon to view detailed information about a book

### Editing a Book
1. Click the pencil icon next to any book
2. Modify the book details
3. Click "Add Book" to save changes

### Deleting a Book
1. Click the trash icon next to any book
2. Confirm the deletion

### Searching Books
1. Click "Search" in the navigation menu
2. Enter a search term (title, author, ISBN, or category)
3. Click "Search" to view results

### Borrowing a Book
- Click the green arrow down icon to borrow a copy
- The available copies count will decrease

### Returning a Book
- Click the blue arrow up icon to return a copy
- The available copies count will increase

## Database

The application uses SQLite database (`library.db`) which is automatically created when you first run the application. The database file will be created in the same directory as `app.py`.

## Project Structure

```
CSE Project Uttam/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── run_server.bat        # Windows batch file to run server
├── run_server.ps1        # PowerShell script to run server
├── run.py                # Python script to run server
├── library.db            # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── add_book.html     # Add book form
│   ├── edit_book.html    # Edit book form
│   ├── view_book.html    # Book details page
│   └── search.html       # Search page
└── static/               # Static files (CSS, JS, images)
    ├── css/
    │   └── style.css     # Custom stylesheet
    └── js/
        └── main.js       # Custom JavaScript
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **WTForms**: Form handling and validation
- **Bootstrap 5**: Frontend framework
- **SQLite**: Database

## Security Note

⚠️ **Important**: Change the `SECRET_KEY` in `app.py` before deploying to production. The current key is for development only.

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or refer to Flask documentation.

