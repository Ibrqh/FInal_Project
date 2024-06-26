from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import TransactionForm, EditTransactionForm, RegistrationForm, LoginForm, BudgetForm
from models import db, Transaction, User, Budget
from auth import auth as auth_blueprint
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'

db.init_app(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

app.register_blueprint(auth_blueprint)

@app.route('/')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            date=form.date.data,
            description=form.description.data,
            amount=form.amount.data,
            category=form.category.data,
            user_id=current_user.id
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added successfully!')
        return redirect(url_for('index'))
    return render_template('add_transaction.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to edit this transaction.')
        return redirect(url_for('index'))
    form = EditTransactionForm(obj=transaction)
    if form.validate_on_submit():
        transaction.date = form.date.data
        transaction.description = form.description.data
        transaction.amount = form.amount.data
        transaction.category = form.category.data
        db.session.commit()
        flash('Transaction updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_transaction.html', form=form, transaction=transaction)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.')
        return redirect(url_for('index'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!')
    return redirect(url_for('index'))

@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    form = BudgetForm()
    if form.validate_on_submit():
        new_budget = Budget(
            category=form.category.data,
            amount=form.amount.data,
            user_id=current_user.id
        )
        db.session.add(new_budget)
        db.session.commit()
        flash('Budget set successfully!')
        return redirect(url_for('budget'))
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return render_template('budget.html', form=form, budgets=budgets)

@app.route('/report')
@login_required
def report():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    income = sum(t.amount for t in transactions if t.category == 'income')
    expense = sum(t.amount for t in transactions if t.category == 'expense')

    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    budget_dict = {b.category: b.amount for b in budgets}

    budget_income = budget_dict.get('income', 0)
    budget_expense = budget_dict.get('expense', 0)

    return render_template('report.html', transactions=transactions, income=income, expense=expense,
                           budget_income=budget_income, budget_expense=budget_expense)

if __name__ == '__main__':
    app.run(debug=True)
