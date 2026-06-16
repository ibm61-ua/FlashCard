import json
import os
import uuid

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_all_syllabuses():
    return load_data()

def get_syllabus(syllabus_id):
    data = load_data()
    for syllabus in data:
        if syllabus['id'] == syllabus_id:
            return syllabus
    return None

def add_syllabus(name):
    data = load_data()
    new_syllabus = {
        'id': str(uuid.uuid4()),
        'name': name,
        'flashcards': []
    }
    data.append(new_syllabus)
    save_data(data)
    return new_syllabus

def add_flashcard(syllabus_id, question, answer):
    data = load_data()
    for syllabus in data:
        if syllabus['id'] == syllabus_id:
            new_flashcard = {
                'id': str(uuid.uuid4()),
                'question': question,
                'answer': answer
            }
            syllabus['flashcards'].append(new_flashcard)
            save_data(data)
            return new_flashcard
    return None

def update_flashcard(syllabus_id, flashcard_id, question, answer):
    data = load_data()
    for syllabus in data:
        if syllabus['id'] == syllabus_id:
            for flashcard in syllabus['flashcards']:
                if flashcard['id'] == flashcard_id:
                    flashcard['question'] = question
                    flashcard['answer'] = answer
                    save_data(data)
                    return flashcard
    return None
