from flask import Flask, request, jsonify, render_template, send_file
import os
import yt_dlp as youtube_dl

# Initialize Flask app
app = Flask(__name__)

# Folder to store downloaded files
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the download request
@app.route('/download', methods=['POST'])
def download():
    # Get the YouTube link from the request
    youtube_link = request.json.get('link')
    if not youtube_link:
        return jsonify({'success': False, 'message': 'No link provided'})

    try:
        # Options for downloading audio
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best quality audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                'preferredcodec': 'mp3',      # Convert to MP3
                'preferredquality': '192',    # Set audio quality
            }],
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Output file template
            'ffmpeg_location': 'C:\\Users\\pandi\\OneDrive\\Desktop\\youtube-downloader\\ffmpeg-7.1.1-essentials_build\\bin'  # Path to FFmpeg
        }

        # Download the audio
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_link, download=True)  # Extract video info
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')  # Fix filename

        # Return success and the file path
        return jsonify({'success': True, 'fileUrl': filename})
    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({'success': False, 'message': str(e)})

# Route to serve the downloaded file
@app.route('/download-file/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)