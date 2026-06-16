# Student Finance Tracker - Quick Reference

## Quick Start Commands

### Windows
```bash
setup.bat
python init_db.py
python run.py
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
python init_db.py
python run.py
```

## Key Features Quick Reference

| Feature | URL | Purpose |
|---------|-----|---------|
| Dashboard | `/dashboard` | View financial overview |
| Add Income | `/add-income` | Record income |
| Add Expense | `/add-expense` | Track spending |
| Expenses | `/expenses` | View all expenses |
| Wishlist | `/wishlist` | Manage purchase goals |
| Budgets | `/budgets` | Set budget limits |
| AI Chat | `/ai/chat` | Talk to financial advisor |
| Categories | `/add-category` | Create expense categories |

## Default Settings

- **Database**: `student_finance_tracker`
- **Port**: `5000`
- **Flask Environment**: `development`
- **Session Timeout**: `7 days`

## Environment Variables Reference

```env
# Required for all features
SECRET_KEY = Random string for session encryption
MYSQL_USER = Database username
MYSQL_PASSWORD = Database password
MYSQL_HOST = Database host (127.0.0.1)
MYSQL_PORT = Database port (3306)
MYSQL_DATABASE = Database name

# Required for AI features
OPENAI_API_KEY = Your OpenAI API key
OPENAI_MODEL = gpt-4o-mini (default)

# Optional - for email password reset
MAIL_SERVER = smtp.gmail.com (or other SMTP)
MAIL_PORT = 587
MAIL_USERNAME = Your email
MAIL_PASSWORD = Your app password
```

## Common Issues & Solutions

### MySQL Connection Failed
- Ensure MySQL server is running
- Verify credentials in `.env`
- Check database exists: `CREATE DATABASE student_finance_tracker;`

### OpenAI API Error
- Verify API key in `.env`
- Check API key is active on OpenAI dashboard
- Ensure account has credits

### Port 5000 Already in Use
- Change port in `run.py`: `app.run(port=5001)`
- Or kill process on 5000

### Templates Not Found
- Run from project root directory
- Ensure `app/templates/` exists
- Check folder structure matches

## Database Schema Quick Reference

```
Users (id, username, email, password_hash, date_created)
  ├── Income (id, user_id, income_amount, income_source, date)
  ├── Categories (id, user_id, category_name, is_default)
  │   └── Expenses (id, user_id, category_id, amount, description, expense_date)
  │   └── BudgetGoals (id, user_id, category_id, monthly_limit)
  ├── Wishlist (id, user_id, item_name, target_price, priority, description, status)
  ├── Notifications (id, user_id, title, message, created_at, is_read)
  └── AIChatHistory (id, user_id, question, response, timestamp)
```

## Security Notes

✅ Passwords hashed with PBKDF2-SHA256
✅ CSRF protection on all forms
✅ Password reset tokens expire in 30 minutes
✅ Session protection enabled
✅ Secure HTTP-only cookies
✅ SQL injection prevention via SQLAlchemy ORM

## Performance Tips

- Use pagination for large datasets
- Index frequently queried fields in MySQL
- Cache dashboard data (future enhancement)
- Monitor database connection pool
- Use CDN for static files in production

## Useful MySQL Commands

```sql
-- Check database
SHOW DATABASES;

-- Check tables
USE student_finance_tracker;
SHOW TABLES;

-- View user data
SELECT * FROM users;

-- Check expenses for a user
SELECT * FROM expenses WHERE user_id = 1;

-- Clear test data
DELETE FROM expenses WHERE user_id = 1;
DELETE FROM income WHERE user_id = 1;

-- Check AI chat history
SELECT * FROM ai_chat_history;
```

## Debugging Mode

To enable Flask debug mode for detailed error messages:
```python
# In run.py
app.run(debug=True)
```

Or in `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=true
```

## Testing the AI Feature

Example prompts to try:
- "I have $500/month. How should I budget?"
- "Tips for saving for a gaming laptop?"
- "Should I cut my food budget?"
- "How to track my freelance income?"
- "Best emergency fund size?"

## File Structure Overview

```
project/
├── app/                          # Main application package
│   ├── models.py                 # Database models
│   ├── routes.py                 # Main routes (dashboard, expenses, etc)
│   ├── auth.py                   # Authentication routes
│   ├── ai.py                     # AI chat routes
│   ├── forms.py                  # WTForms for all pages
│   ├── utils.py                  # Helper functions
│   ├── email_service.py          # Email utilities
│   ├── __init__.py               # App factory
│   └── templates/                # HTML templates
├── config.py                     # Flask configuration
├── run.py                        # Application entry point
├── init_db.py                    # Database initialization
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── setup.bat                     # Windows setup script
├── setup.sh                      # macOS/Linux setup script
├── README.md                     # Full documentation
└── QUICKSTART.md                 # This file
```

## Support & Documentation

- Full docs: See `README.md`
- API endpoints: Check `routes.py`, `auth.py`, `ai.py`
- Database schema: See `models.py`
- Forms: See `forms.py` for all input validation

---

Last Updated: 2026-06-16
