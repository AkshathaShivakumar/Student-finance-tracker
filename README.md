# Student Finance Tracker

A comprehensive web application designed for college students to manage their finances, track expenses, set budgets, plan savings, and get AI-powered financial advice.

## Features

### 🎯 Core Functionality
- **User Authentication**: Secure registration, login, and password reset functionality
- **Income Tracking**: Record income from various sources (part-time jobs, freelance work, allowance, etc.)
- **Expense Management**: Track spending by category with detailed descriptions
- **Smart Budgeting**: Set monthly budget limits for expense categories
- **Wishlist**: Plan future purchases with target prices and priority levels
- **AI Financial Advisor**: Chat with OpenAI-powered assistant for personalized financial advice
- **Analytics Dashboard**: Visualize spending patterns with Chart.js

### 📊 Dashboard Analytics
- Total Income, Expenses, and Savings overview
- Spending breakdown by category (Pie Chart)
- Monthly spending trends (Line Chart)
- Recent transaction history
- Wishlist progress tracking

### 🤖 AI Assistant
- Interactive chat interface powered by OpenAI GPT-4 mini
- Persistent chat history with timestamps
- Conversational financial advice and budgeting tips
- Context-aware responses for student-specific financial challenges

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python Flask
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login, Flask-WTF
- **Email**: Flask-Mail (password reset)
- **Charts**: Chart.js
- **AI**: OpenAI API
- **Password Security**: Werkzeug (PBKDF2-SHA256 hashing)
- **Token Generation**: itsdangerous (for secure email tokens)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- OpenAI API Key (for AI features)

### Step 1: Clone or Download the Project
```bash
cd c:\Users\Administrator\Downloads\project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:
```env
# Database
MYSQL_USER=studentfinance
MYSQL_PASSWORD=your_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=student_finance_tracker

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Flask
SECRET_KEY=your_secret_key_here
```

### Step 5: Set Up MySQL Database
1. Open MySQL command line:
```sql
CREATE DATABASE student_finance_tracker;
CREATE USER 'studentfinance'@'localhost' IDENTIFIED BY 'StudentFinance@123';
GRANT ALL PRIVILEGES ON student_finance_tracker.* TO 'studentfinance'@'localhost';
FLUSH PRIVILEGES;
```

### Step 6: Initialize Database Tables
```bash
python init_db.py
```

### Step 7: Run the Application
```bash
python run.py
```

The application will be available at: **http://localhost:5000**

## Usage Guide

### 1. Create Account
- Visit the home page and click "Get Started"
- Fill in username, email, and password
- Account created with automatic welcome email

### 2. Add Income
- Navigate to "Add Income" in sidebar
- Enter income source (job name, freelance gig, etc.)
- Record the amount and date
- View total income on dashboard

### 3. Add Expenses
- Click "Add Expense" in sidebar
- First time: Create a category (Food, Transport, etc.)
- Enter amount, category, and date
- Optional: Add description for reference
- View all expenses with pagination

### 4. Set Budget Goals
- Go to "Budgets" section
- Set monthly spending limits per category
- Monitor actual vs. budgeted spending
- Visual progress bars show budget utilization

### 5. Manage Wishlist
- Add items you want to purchase
- Set target price and priority level
- Track status: Pending → In Progress → Completed
- Monitor overall wishlist progress percentage

### 6. AI Financial Advisor
- Open "AI Assistant" from sidebar
- Ask any financial question in natural language
- Get personalized advice from AI
- Chat history automatically saved
- Examples:
  - "How should I budget $500 monthly?"
  - "Tips for saving for a laptop?"
  - "Should I increase my food budget?"

### 7. View Analytics
- Dashboard shows key metrics at a glance
- Spending by Category pie chart
- Monthly Trend line chart
- Recent transactions list
- All data updates in real-time

## Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: PBKDF2-SHA256 hashed password
- `date_created`: Account creation timestamp

### Income
- `id`: Primary key
- `user_id`: Foreign key to Users
- `income_amount`: Amount received (Numeric)
- `income_source`: Source description
- `date`: Income date

### Expenses
- `id`: Primary key
- `user_id`: Foreign key to Users
- `category_id`: Foreign key to Categories
- `amount`: Expense amount (Numeric)
- `description`: Optional note
- `expense_date`: Expense date

### Categories
- `id`: Primary key
- `user_id`: Foreign key to Users
- `category_name`: Category name (Food, Transport, etc.)
- `is_default`: Boolean flag for default categories

### Wishlist
- `id`: Primary key
- `user_id`: Foreign key to Users
- `item_name`: Name of desired item
- `target_price`: Target purchase price
- `priority`: High/Medium/Low
- `description`: Optional details
- `status`: Pending/In Progress/Completed

### BudgetGoals
- `id`: Primary key
- `user_id`: Foreign key to Users
- `category_id`: Foreign key to Categories
- `monthly_limit`: Monthly spending limit (Numeric)

### Notifications
- `id`: Primary key
- `user_id`: Foreign key to Users
- `title`: Notification title
- `message`: Notification message
- `created_at`: Creation timestamp
- `is_read`: Read status boolean

### AIChatHistory
- `id`: Primary key
- `user_id`: Foreign key to Users
- `question`: User's question
- `response`: AI's response
- `timestamp`: Chat timestamp

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password/<token>` - Reset password with token

### Dashboard
- `GET /dashboard` - Main dashboard view

### Income
- `GET /add-income` - Income form page
- `POST /add-income` - Submit new income

### Expenses
- `GET /expenses` - View all expenses (paginated)
- `GET /add-expense` - Expense form page
- `POST /add-expense` - Submit new expense
- `POST /delete-expense/<id>` - Delete expense

### Wishlist
- `GET /wishlist` - View wishlist
- `GET /add-wishlist` - Wishlist form page
- `POST /add-wishlist` - Add wishlist item
- `POST /delete-wishlist/<id>` - Remove wishlist item
- `POST /update-wishlist-status/<id>/<status>` - Update item status

### Budgets
- `GET /budgets` - View budget goals
- `GET /add-budget` - Budget form page
- `POST /add-budget` - Create budget goal
- `POST /delete-budget/<id>` - Delete budget goal

### Categories
- `GET /add-category` - Category form page
- `POST /add-category` - Create category

### AI Chat
- `GET /ai/chat` - Chat interface
- `POST /api/chat` - Send chat message
- `GET /api/chat-history` - Get chat history
- `DELETE /api/delete-chat/<id>` - Delete chat entry

## Security Features

✅ **Password Security**
- PBKDF2-SHA256 hashing with Werkzeug
- Minimum 8 character password requirement
- Password confirmation validation

✅ **Session Management**
- Flask-Login with strong session protection
- Secure cookie settings (HttpOnly, SameSite)
- Auto-logout on browser close (optional 7-day remember-me)

✅ **CSRF Protection**
- Flask-WTF CSRF token validation on all forms
- Token validation on state-changing operations

✅ **Email Security**
- Secure password reset tokens with 30-minute expiration
- Itsdangerous library for token generation
- One-time use reset links

✅ **Database Security**
- Parameterized queries via SQLAlchemy ORM
- Connection pooling with pre-ping verification
- Foreign key constraints and cascading deletes

## Configuration

### Email Setup (for Password Reset)
To enable password reset emails:

1. Enable 2FA on Gmail account
2. Generate "App Password" in Google Account settings
3. Update `.env`:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### OpenAI API Configuration
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

## Troubleshooting

### Database Connection Error
```
Error: Access denied for user 'studentfinance'
```
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists: `SHOW DATABASES;`

### OpenAI API Error
```
Error: Invalid OpenAI API key
```
- Verify API key is correct
- Check API key is active on OpenAI dashboard
- Ensure billing is enabled

### Port Already in Use
```
ERROR: Address already in use
```
- Kill process on port 5000: `lsof -ti:5000 | xargs kill -9`
- Or change port in `run.py`

### Templates Not Loading
- Ensure `app/templates/` directory exists
- Check template file paths match route names
- Verify Jinja2 syntax in template files

## Deployment

### Production Checklist
- [ ] Change `SECRET_KEY` in `.env` to random string
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=false`
- [ ] Use production WSGI server (Gunicorn, Waitress)
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure proper database backups
- [ ] Set up monitoring and logging
- [ ] Configure CDN for static files

### Deployment with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Project Structure
```
student-finance-tracker/
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── forgot_password.html
│   │   │   └── reset_password.html
│   │   ├── ai/
│   │   │   └── chat.html
│   │   ├── add_*.html (feature templates)
│   │   └── (other templates)
│   ├── __init__.py (app factory)
│   ├── models.py (SQLAlchemy models)
│   ├── routes.py (main routes)
│   ├── auth.py (authentication routes)
│   ├── ai.py (AI chat routes)
│   ├── forms.py (WTForms)
│   ├── utils.py (utility functions)
│   └── email_service.py (email functions)
├── config.py (Flask configuration)
├── run.py (application entry point)
├── init_db.py (database initialization)
├── requirements.txt (Python dependencies)
├── .env.example (environment template)
├── .gitignore (Git ignore rules)
└── README.md (this file)
```

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Export reports (PDF, Excel)
- [ ] Social sharing features
- [ ] Monthly email summaries
- [ ] Advanced analytics and forecasting
- [ ] Multi-user household budgets
- [ ] Payment integration (Stripe)
- [ ] Goal-based savings automation
- [ ] Investment tracking
- [ ] Dark mode theme

## Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a detailed issue report
3. Include error messages and steps to reproduce

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- Bootstrap 5 for UI framework
- Chart.js for data visualization
- OpenAI for AI capabilities
- Flask community for excellent documentation

---

**Built with ❤️ for college students managing their finances**

Version: 1.0.0  
Last Updated: 2026-06-16
