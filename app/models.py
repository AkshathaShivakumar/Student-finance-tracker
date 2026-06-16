from datetime import datetime
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    incomes = db.relationship("Income", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    expenses = db.relationship("Expense", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    categories = db.relationship("Category", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    wishlist_items = db.relationship("Wishlist", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    budget_goals = db.relationship("BudgetGoal", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    chat_history = db.relationship("AIChatHistory", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    income_amount = db.Column(db.Numeric(12, 2), nullable=False)
    income_source = db.Column(db.String(128), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Income {self.income_source} {self.income_amount}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_name = db.Column(db.String(80), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)

    expenses = db.relationship("Expense", backref="category", lazy="dynamic", cascade="all, delete-orphan")
    budget_goals = db.relationship("BudgetGoal", backref="category", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.category_name}>"


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    expense_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Expense {self.amount} {self.expense_date}>"


class Wishlist(db.Model):
    __tablename__ = "wishlist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_name = db.Column(db.String(140), nullable=False)
    target_price = db.Column(db.Numeric(12, 2), nullable=False)
    priority = db.Column(db.String(32), nullable=False, default="Medium")
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(32), nullable=False, default="Pending")

    def __repr__(self):
        return f"<Wishlist {self.item_name} {self.status}>"


class BudgetGoal(db.Model):
    __tablename__ = "budget_goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    monthly_limit = db.Column(db.Numeric(12, 2), nullable=False)

    def __repr__(self):
        return f"<BudgetGoal category_id={self.category_id} limit={self.monthly_limit}>"


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Notification {self.title}>"


class AIChatHistory(db.Model):
    __tablename__ = "ai_chat_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AIChatHistory user_id={self.user_id} timestamp={self.timestamp}>"
