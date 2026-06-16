from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=64, message="Username must be between 3 and 64 characters.")
        ]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Invalid email address.")]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered. Please use a different email or log in.")


class LoginForm(FlaskForm):
    email_or_username = StringField(
        "Email or Username",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    submit = SubmitField("Login")


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Invalid email address.")]
    )
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("No account found with this email address.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Reset Password")


class AddIncomeForm(FlaskForm):
    income_source = StringField(
        "Income Source",
        validators=[DataRequired(), Length(min=1, max=128)]
    )
    income_amount = FloatField(
        "Amount",
        validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0.")]
    )
    date = DateField(
        "Date",
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Income")


class AddExpenseForm(FlaskForm):
    category = SelectField(
        "Category",
        validators=[DataRequired()],
        coerce=int
    )
    amount = FloatField(
        "Amount",
        validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0.")]
    )
    description = TextAreaField(
        "Description",
        validators=[Length(max=500)]
    )
    expense_date = DateField(
        "Date",
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Expense")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = []


class AddWishlistForm(FlaskForm):
    item_name = StringField(
        "Item Name",
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    target_price = FloatField(
        "Target Price",
        validators=[DataRequired(), NumberRange(min=0.01, message="Price must be greater than 0.")]
    )
    priority = SelectField(
        "Priority",
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
        validators=[DataRequired()]
    )
    description = TextAreaField(
        "Description",
        validators=[Length(max=500)]
    )
    submit = SubmitField("Add to Wishlist")


class AddBudgetGoalForm(FlaskForm):
    category = SelectField(
        "Category",
        validators=[DataRequired()],
        coerce=int
    )
    monthly_limit = FloatField(
        "Monthly Limit",
        validators=[DataRequired(), NumberRange(min=0.01, message="Limit must be greater than 0.")]
    )
    submit = SubmitField("Set Budget Goal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = []


class AddCategoryForm(FlaskForm):
    category_name = StringField(
        "Category Name",
        validators=[DataRequired(), Length(min=1, max=80)]
    )
    submit = SubmitField("Create Category")


class AIQueryForm(FlaskForm):
    question = TextAreaField(
        "Ask me anything about your finances",
        validators=[DataRequired(), Length(min=1, max=2000)]
    )
    submit = SubmitField("Get Advice")
