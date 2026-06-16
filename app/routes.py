from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db
from app.models import Income, Expense, Category, Wishlist, BudgetGoal
from app.forms import (
    AddIncomeForm, AddExpenseForm, AddWishlistForm, AddBudgetGoalForm, AddCategoryForm
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("home.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    today = datetime.today().date()
    thirty_days_ago = today - timedelta(days=30)
    
    total_income = db.session.query(func.sum(Income.income_amount)).filter(
        Income.user_id == current_user.id
    ).scalar() or 0
    
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id
    ).scalar() or 0
    
    current_savings = float(total_income) - float(total_expenses)
    
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(
        Expense.expense_date.desc()
    ).limit(5).all()
    
    monthly_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.expense_date >= thirty_days_ago
    ).scalar() or 0
    
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    wishlist_progress = 0
    if wishlist_items:
        wishlist_progress = len([w for w in wishlist_items if w.status == "Completed"]) / len(wishlist_items) * 100
    
    highest_category_expense = db.session.query(
        Category.category_name,
        func.sum(Expense.amount).label("total")
    ).join(Expense).filter(
        Expense.user_id == current_user.id
    ).group_by(Category.id).order_by(func.sum(Expense.amount).desc()).first()
    
    category_expenses = db.session.query(
        Category.category_name,
        func.sum(Expense.amount).label("total")
    ).join(Expense).filter(
        Expense.user_id == current_user.id
    ).group_by(Category.id).all()
    
    return render_template(
        "dashboard.html",
        total_income=float(total_income),
        total_expenses=float(total_expenses),
        current_savings=current_savings,
        monthly_expenses=float(monthly_expenses),
        recent_expenses=recent_expenses,
        wishlist_progress=wishlist_progress,
        highest_category=highest_category_expense,
        category_expenses=category_expenses
    )


@main_bp.route("/add-income", methods=["GET", "POST"])
@login_required
def add_income():
    form = AddIncomeForm()
    if form.validate_on_submit():
        try:
            income = Income(
                user_id=current_user.id,
                income_source=form.income_source.data,
                income_amount=form.income_amount.data,
                date=form.date.data
            )
            db.session.add(income)
            db.session.commit()
            flash("Income added successfully!", "success")
            return redirect(url_for("main.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding income. Please try again.", "danger")
            print(f"Error: {e}")
    
    return render_template("add_income.html", form=form)


@main_bp.route("/add-expense", methods=["GET", "POST"])
@login_required
def add_expense():
    form = AddExpenseForm()
    
    user_categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category.choices = [(c.id, c.category_name) for c in user_categories]
    
    if not user_categories:
        flash("Please create a category first.", "warning")
        return redirect(url_for("main.add_category"))
    
    if form.validate_on_submit():
        try:
            expense = Expense(
                user_id=current_user.id,
                category_id=form.category.data,
                amount=form.amount.data,
                description=form.description.data,
                expense_date=form.expense_date.data
            )
            db.session.add(expense)
            db.session.commit()
            flash("Expense added successfully!", "success")
            return redirect(url_for("main.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding expense. Please try again.", "danger")
            print(f"Error: {e}")
    
    return render_template("add_expense.html", form=form)


@main_bp.route("/expenses")
@login_required
def expenses():
    page = request.args.get("page", 1, type=int)
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(
        Expense.expense_date.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template("expenses.html", expenses=expenses)


@main_bp.route("/delete-expense/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.expenses"))
    
    try:
        db.session.delete(expense)
        db.session.commit()
        flash("Expense deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting expense.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for("main.expenses"))


@main_bp.route("/wishlist")
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).order_by(
        Wishlist.priority.desc()
    ).all()
    
    return render_template("wishlist.html", wishlist_items=wishlist_items)


@main_bp.route("/add-wishlist", methods=["GET", "POST"])
@login_required
def add_wishlist():
    form = AddWishlistForm()
    if form.validate_on_submit():
        try:
            item = Wishlist(
                user_id=current_user.id,
                item_name=form.item_name.data,
                target_price=form.target_price.data,
                priority=form.priority.data,
                description=form.description.data,
                status="Pending"
            )
            db.session.add(item)
            db.session.commit()
            flash("Item added to wishlist!", "success")
            return redirect(url_for("main.wishlist"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding to wishlist.", "danger")
            print(f"Error: {e}")
    
    return render_template("add_wishlist.html", form=form)


@main_bp.route("/delete-wishlist/<int:wishlist_id>", methods=["POST"])
@login_required
def delete_wishlist(wishlist_id):
    item = Wishlist.query.get_or_404(wishlist_id)
    if item.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.wishlist"))
    
    try:
        db.session.delete(item)
        db.session.commit()
        flash("Item removed from wishlist!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error removing item.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for("main.wishlist"))


@main_bp.route("/update-wishlist-status/<int:wishlist_id>/<status>", methods=["POST"])
@login_required
def update_wishlist_status(wishlist_id, status):
    item = Wishlist.query.get_or_404(wishlist_id)
    if item.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.wishlist"))
    
    if status not in ["Pending", "In Progress", "Completed"]:
        flash("Invalid status.", "danger")
        return redirect(url_for("main.wishlist"))
    
    try:
        item.status = status
        db.session.commit()
        flash(f"Wishlist item status updated to {status}!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error updating status.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for("main.wishlist"))


@main_bp.route("/budgets")
@login_required
def budgets():
    budget_goals = BudgetGoal.query.filter_by(user_id=current_user.id).all()
    
    budget_data = []
    for budget in budget_goals:
        month_start = datetime.today().replace(day=1).date()
        month_expenses = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            Expense.category_id == budget.category_id,
            Expense.expense_date >= month_start
        ).scalar() or 0
        
        budget_data.append({
            "budget": budget,
            "spent": float(month_expenses),
            "remaining": float(budget.monthly_limit) - float(month_expenses),
            "percentage": (float(month_expenses) / float(budget.monthly_limit)) * 100 if float(budget.monthly_limit) > 0 else 0
        })
    
    return render_template("budgets.html", budget_data=budget_data)


@main_bp.route("/add-budget", methods=["GET", "POST"])
@login_required
def add_budget():
    form = AddBudgetGoalForm()
    
    user_categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category.choices = [(c.id, c.category_name) for c in user_categories]
    
    if not user_categories:
        flash("Please create a category first.", "warning")
        return redirect(url_for("main.add_category"))
    
    if form.validate_on_submit():
        try:
            existing_budget = BudgetGoal.query.filter_by(
                user_id=current_user.id,
                category_id=form.category.data
            ).first()
            
            if existing_budget:
                existing_budget.monthly_limit = form.monthly_limit.data
                db.session.commit()
                flash("Budget goal updated successfully!", "success")
            else:
                budget = BudgetGoal(
                    user_id=current_user.id,
                    category_id=form.category.data,
                    monthly_limit=form.monthly_limit.data
                )
                db.session.add(budget)
                db.session.commit()
                flash("Budget goal added successfully!", "success")
            
            return redirect(url_for("main.budgets"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding budget goal.", "danger")
            print(f"Error: {e}")
    
    return render_template("add_budget.html", form=form)


@main_bp.route("/delete-budget/<int:budget_id>", methods=["POST"])
@login_required
def delete_budget(budget_id):
    budget = BudgetGoal.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.budgets"))
    
    try:
        db.session.delete(budget)
        db.session.commit()
        flash("Budget goal deleted!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting budget.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for("main.budgets"))


@main_bp.route("/add-category", methods=["GET", "POST"])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        try:
            category = Category(
                user_id=current_user.id,
                category_name=form.category_name.data,
                is_default=False
            )
            db.session.add(category)
            db.session.commit()
            flash("Category created successfully!", "success")
            return redirect(request.referrer or url_for("main.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash("Error creating category.", "danger")
            print(f"Error: {e}")
    
    return render_template("add_category.html", form=form)

