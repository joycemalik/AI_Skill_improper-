from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient
# import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
client = InferenceClient(api_key=api_key)

# Mock database for student information
students_db = {}

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Submit route
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    student_id = data['student_id']
    students_db[student_id] = {
        'name': data['name'],
        'course': data['course'],
        'interests': data['interests']
    }
    
    response = generate_roadmap(student_id)
    return jsonify(response)

# Results route
@app.route('/roadmap/<student_id>')
def roadmap(student_id):
    roadmap_data = students_db.get(student_id, {}).get('roadmap', 'No roadmap available')
    return render_template('roadmap.html', roadmap=roadmap_data)

# Generate AI-powered career roadmap
def generate_roadmap(student_id):
    with open(f"{student_id}.txt", "r") as file:
        personality_info = file.read()
    
    student_data = students_db[student_id]
    prompt = f"""
    Student Information:
    Name: {student_data['name']}
    Course: {student_data['course']}
    Interests: {', '.join(student_data['interests'])}
    
    Personality Info:
    {personality_info}
    
    Generate a structured, dynamic learning roadmap for this student. Suggest skills to learn in the next year, upcoming months, and weeks. Include reasons for each suggestion, along with evidence of demand and industry trends.
    """

    messages = [
        {"role": "user", "content": prompt}
    ]
    
    stream = client.chat.completions.create(
        model="mistralai/Mistral-Nemo-Instruct-2407", 
        messages=messages, 
        max_tokens=500,
        stream=True
    )

    roadmap = ""
    for chunk in stream:
        roadmap += chunk.choices[0].delta.content
    
    students_db[student_id]['roadmap'] = roadmap
    return {
        'student_id': student_id,
        'roadmap': roadmap
    }

if __name__ == "__main__":
    app.run(debug=True)
