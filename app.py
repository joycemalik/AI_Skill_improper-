from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient
import time

app = Flask(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
client = InferenceClient(api_key=api_key)

students_db = {}

# Generate unique student file name
def get_next_student_id():
    existing_files = [f for f in os.listdir() if f.startswith('P') and f.endswith('.txt')]
    if not existing_files:
        return 'P101'
    numbers = [int(f[1:-4]) for f in existing_files]
    return f'P{max(numbers) + 1}'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    student_id = get_next_student_id()
    students_db[student_id] = {
        'name': data['name'],
        'course': data['course'],
        'interests': data['interests'].split(',')
    }
    
    with open(f"{student_id}.txt", "w") as file:
        file.write(f"Name: {data['name']}\n")
        file.write(f"Course: {data['course']}\n")
        file.write(f"Interests: {data['interests']}\n")
    
    return redirect(url_for('loading', student_id=student_id))

@app.route('/loading/<student_id>')
def loading(student_id):
    time.sleep(5)
    generate_roadmap(student_id)
    return redirect(url_for('roadmap', student_id=student_id))

@app.route('/roadmap/<student_id>')
def roadmap(student_id):
    roadmap_data = students_db.get(student_id, {}).get('roadmap', 'No roadmap available')
    return render_template('roadmap.html', roadmap=roadmap_data.replace('\n', '<br>'))

# Generate AI-powered career roadmap
def generate_roadmap(student_id):
    file_path = f"{student_id}.txt"
    if not os.path.exists(file_path):
        students_db[student_id]['roadmap'] = "No personality file found."
        return
    
    with open(file_path, "r") as file:
        personality_info = file.read()
    
    student_data = students_db[student_id]
    prompt = f"""
    Student Info:
    {personality_info}

    Generate a structured dynamic roadmap focusing on skills for the next week, month, and year. Return the result in plain text format, 
    also provide the reason how it is going to help the student. also keep in mind the industry demands and career growth.
    Give a very persoanllized answer, backed with high research and authoritive tone. all under 750 words.
    
    
    """

    messages = [{"role": "user", "content": prompt}]
    
    stream = client.chat.completions.create(
        model="mistralai/Mistral-Nemo-Instruct-2407",
        messages=messages,
        max_tokens=750,
        stream=True
    )

    roadmap = "".join([chunk.choices[0].delta.content for chunk in stream])
    students_db[student_id]['roadmap'] = roadmap

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
