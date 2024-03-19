import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
from werkzeug.exceptions import BadRequest

load_dotenv()

app = Flask(__name__)

try:
    print("Before loading model")
    model = WhisperModel(
        os.environ['MODEL_SIZE'],
        device=os.environ['DEVICE'],
        compute_type=os.environ['COMPUTER_TYPE']
    )
    print("After loading model")
except Exception as e:
    app.logger.error(f"Error initializing the model: {e}")
    raise RuntimeError("Failed to initialize the Whisper model.") from e


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio file to text using Whisper model.
    
    This endpoint expects a POST request with an audio file part. It returns
    the transcription result and processing time if the transcription is successful.
    
    Raises:
        BadRequest: If no file part is found in the request or the file part is empty.
    
    Returns:
        json: Transcription result and processing time.
    """
    if 'file' not in request.files:
        raise BadRequest(description="No file part in the request.")

    file = request.files['file']
    if file.filename == '':
        raise BadRequest(description="No selected file.")

    start_time = datetime.now()
    try:
        segments, info = model.transcribe(file, language='es')
    except Exception as e:
        app.logger.error(f"Transcription error: {e}")
        return jsonify({"error": f"Transcription error: {e}"}), 500
    end_time = datetime.now()

    processing_time = end_time - start_time
    transcription = ' '.join([segment.text for segment in segments])

    response = {
        "transcription": transcription,
        "processing_time": f"{processing_time.total_seconds():.2f} S."
    }

    return jsonify(response)


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    """
    Handle BadRequest errors by returning a JSON response with the error description.
    
    Args:
        error (BadRequest): The BadRequest exception raised by Flask/Werkzeug.
    
    Returns:
        json: Error message describing the bad request.
    """
    return jsonify({"error": error.description}), 400


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """
    Handle unexpected errors by logging the error and returning a generic error message.
    
    This generic handler catches all exceptions not explicitly handled by other error handlers.
    
    Args:
        error (Exception): The caught exception.
    
    Returns:
        json: A generic error message indicating an unexpected error occurred.
    """
    app.logger.error(f"Unexpected error: {error}")
    return jsonify({"error": "An unexpected error occurred."}), 500


if __name__ == '__main__':
    app.run(host=os.environ['HOST'], port=int(os.environ['PORT']), debug=True)
