from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, EmailField, TelField
from wtforms.validators import DataRequired, NumberRange, Optional, Email
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Set database path to avoid instance folder issues
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "library.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    category = db.Column(db.String(50))
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    description = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to borrowings
    borrowings = db.relationship('Borrowing', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    borrower_email = db.Column(db.String(100))
    borrower_phone = db.Column(db.String(20))
    borrower_id = db.Column(db.String(50))  # Library card ID, student ID, etc.
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='borrowed')  # 'borrowed' or 'returned'
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Borrowing {self.borrower_name} - {self.book.title if self.book else "Unknown"}>'

# Forms
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[Optional()])
    publication_year = IntegerField('Publication Year', validators=[Optional(), NumberRange(min=1000, max=9999)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Biography', 'Biography'),
        ('Technology', 'Technology'),
        ('Literature', 'Literature'),
        ('Education', 'Education'),
        ('Other', 'Other')
    ], validators=[Optional()])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Add Book')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Optional()])
    submit = SubmitField('Search')

class BorrowForm(FlaskForm):
    borrower_name = StringField('Borrower Name', validators=[DataRequired()])
    borrower_email = EmailField('Email', validators=[Optional(), Email()])
    borrower_phone = TelField('Phone Number', validators=[Optional()])
    borrower_id = StringField('ID Number (Library Card/Student ID)', validators=[Optional()])
    due_date = StringField('Due Date (YYYY-MM-DD)', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Issue Book')

class ReturnForm(FlaskForm):
    borrower_name = StringField('Borrower Name', validators=[Optional()])
    notes = TextAreaField('Return Notes', validators=[Optional()])
    submit = SubmitField('Return Book')

# Routes
@app.route('/')
def index():
    books = Book.query.all()
    total_books = len(books)
    total_copies = sum(book.total_copies for book in books)
    available_copies = sum(book.available_copies for book in books)
    borrowed_copies = total_copies - available_copies
    
    stats = {
        'total_books': total_books,
        'total_copies': total_copies,
        'available_copies': available_copies,
        'borrowed_copies': borrowed_copies
    }
    
    return render_template('index.html', books=books, stats=stats)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Check if ISBN already exists
        existing_book = Book.query.filter_by(isbn=form.isbn.data).first()
        if existing_book:
            flash('A book with this ISBN already exists!', 'danger')
            return render_template('add_book.html', form=form)
        
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            publisher=form.publisher.data or None,
            publication_year=form.publication_year.data or None,
            category=form.category.data or None,
            total_copies=form.total_copies.data,
            available_copies=form.total_copies.data,
            description=form.description.data or None
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html', form=form)

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        # Check if ISBN is being changed and if new ISBN already exists
        if form.isbn.data != book.isbn:
            existing_book = Book.query.filter_by(isbn=form.isbn.data).first()
            if existing_book:
                flash('A book with this ISBN already exists!', 'danger')
                return render_template('edit_book.html', form=form, book=book)
        
        # Calculate available copies based on total copies change
        copies_diff = form.total_copies.data - book.total_copies
        new_available = book.available_copies + copies_diff
        
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.publisher = form.publisher.data or None
        book.publication_year = form.publication_year.data or None
        book.category = form.category.data or None
        book.total_copies = form.total_copies.data
        book.available_copies = max(0, new_available)  # Ensure non-negative
        book.description = form.description.data or None
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_book.html', form=form, book=book)

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/view_book/<int:id>')
def view_book(id):
    book = Book.query.get_or_404(id)
    active_borrowings = Borrowing.query.filter_by(book_id=id, status='borrowed').order_by(Borrowing.borrow_date.desc()).all()
    return render_template('view_book.html', book=book, active_borrowings=active_borrowings)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    books = []
    
    if form.validate_on_submit() and form.search.data:
        search_term = f"%{form.search.data}%"
        books = Book.query.filter(
            db.or_(
                Book.title.like(search_term),
                Book.author.like(search_term),
                Book.isbn.like(search_term),
                Book.category.like(search_term)
            )
        ).all()
    
    return render_template('search.html', form=form, books=books)

@app.route('/borrow/<int:id>', methods=['GET', 'POST'])
def borrow_book(id):
    book = Book.query.get_or_404(id)
    form = BorrowForm()
    
    if form.validate_on_submit():
        if book.available_copies > 0:
            # Parse due date if provided
            due_date = None
            if form.due_date.data:
                try:
                    due_date = datetime.strptime(form.due_date.data, '%Y-%m-%d')
                except ValueError:
                    flash('Invalid date format. Please use YYYY-MM-DD', 'danger')
                    return render_template('borrow_book.html', form=form, book=book)
            
            # Create borrowing record
            borrowing = Borrowing(
                book_id=book.id,
                borrower_name=form.borrower_name.data,
                borrower_email=form.borrower_email.data or None,
                borrower_phone=form.borrower_phone.data or None,
                borrower_id=form.borrower_id.data or None,
                due_date=due_date,
                notes=form.notes.data or None,
                status='borrowed'
            )
            
            # Update book availability
            book.available_copies -= 1
            
            db.session.add(borrowing)
            db.session.commit()
            flash(f'Book "{book.title}" issued to {form.borrower_name.data} successfully!', 'success')
            return redirect(url_for('view_book', id=book.id))
        else:
            flash(f'No copies available for "{book.title}"!', 'danger')
            return redirect(url_for('index'))
    
    return render_template('borrow_book.html', form=form, book=book)

@app.route('/return/<int:id>', methods=['GET', 'POST'])
def return_book(id):
    book = Book.query.get_or_404(id)
    active_borrowings = Borrowing.query.filter_by(book_id=id, status='borrowed').all()
    form = ReturnForm()
    
    if form.validate_on_submit():
        if book.available_copies < book.total_copies:
            # If borrower name is provided, try to find specific borrowing
            borrowing = None
            if form.borrower_name.data:
                borrowing = Borrowing.query.filter_by(
                    book_id=id, 
                    status='borrowed',
                    borrower_name=form.borrower_name.data
                ).first()
            
            # If not found or no name provided, get the oldest borrowing
            if not borrowing and active_borrowings:
                borrowing = active_borrowings[0]
            
            if borrowing:
                borrowing.return_date = datetime.utcnow()
                borrowing.status = 'returned'
                if form.notes.data:
                    borrowing.notes = (borrowing.notes or '') + f'\nReturn: {form.notes.data}'
            
            # Update book availability
            book.available_copies += 1
            db.session.commit()
            flash(f'Book "{book.title}" returned successfully!', 'success')
            return redirect(url_for('view_book', id=book.id))
        else:
            flash(f'All copies of "{book.title}" are already available!', 'warning')
            return redirect(url_for('index'))
    
    return render_template('return_book.html', form=form, book=book, active_borrowings=active_borrowings)

@app.route('/borrowings')
def borrowings():
    """View all borrowings history"""
    from datetime import date
    all_borrowings = Borrowing.query.order_by(Borrowing.borrow_date.desc()).all()
    active_borrowings = Borrowing.query.filter_by(status='borrowed').order_by(Borrowing.borrow_date.desc()).all()
    
    # Calculate days for each borrowing
    today = date.today()
    for borrowing in active_borrowings:
        borrowing.days_borrowed = (today - borrowing.borrow_date.date()).days
        if borrowing.due_date:
            borrowing.days_overdue = max(0, (today - borrowing.due_date.date()).days)
        else:
            borrowing.days_overdue = 0
    
    return render_template('borrowings.html', all_borrowings=all_borrowings, active_borrowings=active_borrowings, today=today)

# Initialize database
def init_db():
    """Initialize the database and create tables if they don't exist"""
    with app.app_context():
        try:
            db.create_all()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            # Try to remove corrupted database and recreate
            db_path = os.path.join(basedir, "library.db")
            if os.path.exists(db_path):
                try:
                    os.remove(db_path)
                    print("Removed corrupted database file. Recreating...")
                    db.create_all()
                    print("Database recreated successfully!")
                except Exception as e2:
                    print(f"Error recreating database: {e2}")

# Initialize on import
init_db()

if __name__ == '__main__':
    app.run(debug=True)

