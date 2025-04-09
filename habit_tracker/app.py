from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os
app = Flask(__name__)

# Absolute path to the database
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'habit_tracker.db')

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Habit model
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['POST'])
def add_habit():
    habit_name = request.form.get('habit')
    if habit_name:
        new_habit = Habit(name=habit_name)
        db.session.add(new_habit)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_habit(id):
    habit_to_delete = Habit.query.get(id)
    if habit_to_delete:
        db.session.delete(habit_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/analyze')
def analyze_habits():
    habits = Habit.query.all()
    df = pd.DataFrame([(habit.name, habit.date) for habit in habits], columns=['habit', 'date'])

    # Data analysis: Count occurrences per habit
    habit_count = df['habit'].value_counts()

    # Plotting the data
    fig, ax = plt.subplots(figsize=(10, 6))
    habit_count.plot(kind='bar', ax=ax)
    ax.set_title('Habit Occurrences')

    # Save plot to a BytesIO object and encode it as base64 for rendering in HTML
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return render_template('result.html', plot_url=plot_url, habit_count=habit_count)

if __name__ == '__main__':
    app.run(debug=True)
