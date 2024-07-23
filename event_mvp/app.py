from flask import Flask, render_template, request, redirect, url_for
import openai
import os
from datetime import datetime

app = Flask(__name__)
openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/')
def index():
    return render_template('create_event.html')

@app.route('/create_event', methods=['POST'])
def create_event():
    event_name = request.form['event_name']
    event_date = request.form['event_date']
    event_time = request.form['event_time']
    event_location = request.form['event_location']
    event_category = request.form['event_category']
    event_capacity = request.form['event_capacity']
    event_description = request.form['event_description']

    # Generate event description using OpenAI API
    description_prompt = f"Create a brief 3-line description for a {event_category} named {event_name} happening at {event_location} on {event_date} at {event_time}."
    description_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=description_prompt,
        max_tokens=50
    )
    generated_description = description_response.choices[0].text.strip()

    # Generate event banner image using DALL-E API (hypothetical)
    image_prompt = f"{event_category}, {event_name}, {event_location}"
    image_response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="1024x1024"
    )
    image_url = image_response['data'][0]['url']

    # Save image locally
    image_path = os.path.join('static/images', f"{event_name.replace(' ', '_')}.png")
    img_data = requests.get(image_url).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)

    event_data = {
        'name': event_name,
        'date': event_date,
        'time': event_time,
        'location': event_location,
        'category': event_category,
        'capacity': event_capacity,
        'description': generated_description,
        'image_path': image_path
    }

    return render_template('event_page.html', event=event_data)

if __name__ == '__main__':
    app.run(debug=True)
