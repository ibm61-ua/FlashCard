from flask import Flask, render_template, request, redirect, url_for, jsonify
import models
import random

app = Flask(__name__)

@app.route('/')
def index():
    syllabuses = models.get_all_syllabuses()
    return render_template('index.html', syllabuses=syllabuses)

@app.route('/add_syllabus', methods=['POST'])
def add_syllabus():
    name = request.form.get('name')
    if name:
        models.add_syllabus(name)
    return redirect(url_for('index'))

@app.route('/syllabus/<syllabus_id>')
def syllabus_view(syllabus_id):
    syllabus = models.get_syllabus(syllabus_id)
    if not syllabus:
        return "Syllabus not found", 404
    return render_template('syllabus.html', syllabus=syllabus)

@app.route('/syllabus/<syllabus_id>/add_flashcard', methods=['POST'])
def add_flashcard(syllabus_id):
    question = request.form.get('question')
    answer = request.form.get('answer')
    if question and answer:
        models.add_flashcard(syllabus_id, question, answer)
    return redirect(url_for('syllabus_view', syllabus_id=syllabus_id))

@app.route('/syllabus/<syllabus_id>/edit_flashcard/<flashcard_id>', methods=['GET', 'POST'])
def edit_flashcard(syllabus_id, flashcard_id):
    syllabus = models.get_syllabus(syllabus_id)
    if not syllabus:
        return "Syllabus not found", 404
        
    flashcard = next((f for f in syllabus['flashcards'] if f['id'] == flashcard_id), None)
    if not flashcard:
        return "Flashcard not found", 404
        
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        if question and answer:
            models.update_flashcard(syllabus_id, flashcard_id, question, answer)
        return redirect(url_for('syllabus_view', syllabus_id=syllabus_id))
        
    return render_template('edit_flashcard.html', syllabus=syllabus, flashcard=flashcard)

@app.route('/syllabus/<syllabus_id>/delete_flashcard/<flashcard_id>', methods=['POST'])
def delete_flashcard(syllabus_id, flashcard_id):
    models.delete_flashcard(syllabus_id, flashcard_id)
    return redirect(url_for('syllabus_view', syllabus_id=syllabus_id))

@app.route('/study/<syllabus_id>')
def study(syllabus_id):
    syllabus = models.get_syllabus(syllabus_id)
    if not syllabus:
        return "Syllabus not found", 404
    
    if not syllabus['flashcards']:
        return render_template('study.html', syllabus=syllabus, error="No hay flashcards en este temario aún.")
        
    # We pass the syllabus, and the frontend JS will pick random cards
    return render_template('study.html', syllabus=syllabus)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
