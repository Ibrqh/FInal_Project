from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class TransactionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    submit = SubmitField('Add Transaction')

class EditTransactionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    submit = SubmitField('Update Transaction')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BudgetForm(FlaskForm):
    category = SelectField('Category', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Set Budget')
