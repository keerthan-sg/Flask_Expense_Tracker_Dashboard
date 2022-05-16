import json

from application import app
from flask import render_template, url_for, redirect,flash, get_flashed_messages
from application.form import UserDataForm
from application.models import IncomeExpenses
from application import db
#import json

@app.route('/')
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.asc()).all()
    return render_template('index.html',entries=entries)

@app.route('/add',methods=['POST','GET'])
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data,
                               category = form.category.data,
                               amount = form.amount.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"{form.type.data} is added to {form.type.data}","success")
        return redirect(url_for('index'))
    return render_template('add.html',title="Add Expenses",form=form)



@app.route('/delete_post/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash('Entry Deleted','success')
    return redirect(url_for('index'))



@app.route('/dashboard')
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()
    income_expense = []
    for total_amount_on_type, _ in income_vs_expense:
        income_expense.append(total_amount_on_type)

    income_vs_expense_on_cat = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()
    income_expense_on_cat = []
    for total_amount_on_cat, _ in income_vs_expense_on_cat:
        income_expense_on_cat.append((total_amount_on_cat))


    amount_vs_dates = db.session.query(db.func.sum(IncomeExpenses.amount),IncomeExpenses.date).group_by(
        IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    amount_label = []
    dates_label = []

    for amount,date in amount_vs_dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        amount_label.append(amount)



    return render_template('dashboard.html',
                            income_expense=json.dumps(income_expense),
                           income_expense_on_cat=json.dumps(income_expense_on_cat),
                           amount_label=json.dumps(amount_label),
                           dates_label=json.dumps(dates_label))

