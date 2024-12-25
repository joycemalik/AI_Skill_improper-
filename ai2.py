from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
client = InferenceClient(api_key=api_key)

# Mock database for student information
students_db = {}

# Read student data and generate roadmap
def submit(student_id, name, course, interests):
    students_db[student_id] = {
        'name': name,
        'course': course,
        'interests': interests
    }
    
    response = generate_roadmap(student_id)
    return response

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
    
    Generate a structured, dynamic learning roadmap for this student. Suggest skills to learn in the next year, upcoming months, and weeks. Focus on industry demands, skill gaps, and career growth.
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
    
    return {
        'student_id': student_id,
        'roadmap': roadmap
    }

# Example usage
if __name__ == "__main__":
    response = submit("P101", "John Doe", "Computer Science", ["AI", "Machine Learning"])
    print(response)
