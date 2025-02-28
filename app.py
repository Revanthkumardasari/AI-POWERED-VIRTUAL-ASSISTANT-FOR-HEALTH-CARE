from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

os.environ['GOOGLE_API_KEY'] = "AIzaSyD5LzD14to-tQWALMfya2E_I5OvT08qiaU"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def send_text_request(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def image_analysis_request(image_path):
    model = genai.GenerativeModel('gemini-pro-vision')
    image = Image.open(image_path)
    response = model.generate_content(["Analyze the image", image])
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_input = data['message']
    if ' show image' in user_input.lower():
        image_path = input("Enter the path of the image file: ") # You may need to handle file upload in frontend
        output = image_analysis_request(image_path)
    else:
        output = send_text_request('''Act as a ai based personal healthcare assistant for
         the following message direct give answer if any other querry is there please say 
         am a healthcare chatboat cant assist you with that  
         no intro needed and all answer in plain paragraph of max 30 words or less are also
         accepted for following querry-: ''' + user_input)
    return jsonify({'message': output})

if __name__ == '__main__':
    app.run(debug=True)
