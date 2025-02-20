from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from database import create_database_from_csv, init_database
from gemini_service import process_question
import traceback
import os

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Global variable to store the current DataFrame
current_data = None

# Initialize database when app starts
init_database()

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "Server is running",
        "app": "DataChat AI"
    }), 200

@app.route('/upload/<file_type>', methods=['POST', 'OPTIONS'])
def upload_file(file_type):
    # Handle preflight request
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    print(f"Received {file_type} file upload request")
    
    if 'file' not in request.files:
        print("No file in request")
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    print(f"Received file: {file.filename}")
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        if file_type == 'csv':
            # Handle CSV file
            df = pd.read_csv(file)
            
            if df.empty:
                return jsonify({'error': 'The uploaded file is empty'}), 400
            
            global current_data
            current_data = df
            
            # Create SQLite database from CSV
            create_database_from_csv(df)
            
            return jsonify({
                'message': 'File uploaded successfully',
                'columns': list(df.columns),
                'rows': len(df),
                'preview': df.head(5).to_dict('records')
            })
            
        elif file_type == 'pdf':
            # TODO: Implement PDF handling
            return jsonify({'error': 'PDF support coming soon'}), 501
        
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
            
    except Exception as e:
        print(f"Error processing file: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def process_query():
    print("Received query request")
    
    if current_data is None:
        return jsonify({'error': 'Please upload a data file first'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        question = data.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
            
        print(f"Processing question: {question}")
        result = process_question(question, current_data)
        print(f"Query result: {result}")
        
        return jsonify(result)
    except Exception as e:
        print(f"Error processing query: {traceback.format_exc()}")
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    # Explicitly bind to all interfaces
    app.run(host='127.0.0.1', port=5000, debug=True) 