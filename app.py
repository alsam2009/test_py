from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YouTube Video Embed</title>
        </head>
        <body>
            <h1>Watch YouTube Video</h1>
            <form id="videoForm" action="/embed" method="post">
                <label for="videoUrl">Enter YouTube Video URL:</label>
                <input type="text" id="videoUrl" name="videoUrl" required>
                <button type="submit">Submit</button>
            </form>
            <div id="videoContainer"></div>
        </body>
        </html>
    ''')

@app.route('/embed', methods=['POST'])
def embed():
    video_url = request.form['videoUrl']
    video_id = get_video_id(video_url)
    embed_url = f'https://www.youtube.com/embed/{video_id}'
    response = requests.get(embed_url)
    return response.content

def get_video_id(url):
    import re
    video_id = ''
    match = re.match(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
    if match and match.group(1):
        video_id = match.group(1)
    return video_id

if __name__ == '__main__':
    app.run(debug=True)
