from flask import Flask, jsonify, render_template, request, redirect, url_for, Blueprint

import time, os, PyPDF2
from app.authentication.login import login
from app.authentication.profiles import Profiles
# from app.authentication.extr import ResumeParser
from werkzeug.utils import secure_filename



# from app.authentication.resumeApp import parse_resume

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")


app_blueprint = Blueprint('app_blueprint', __name__, static_folder='app/static', template_folder='app/templates')

@app_blueprint.route('/')
def base():
    return render_template('/layouts/base.html')

@app_blueprint.route('/index')
def index():
    return render_template('/home/index.html')

@app_blueprint.route("/login", methods=["POST", "GET"]) 
def login_page():
    return login()

@app_blueprint.route('/index', methods=['POST'])
def select():
    username = 'ashleykhanaasmara61@gmail.com'
    password = 'aasmara@61'
    choice = request.form.get('choice_select')
    target = request.form.get('target')
    location = request.form.get('location')
    options = None
    scraper = Profiles(username, password, choice, target, location, options)
    scraper.login()
    scraper.collect_links()
    # Example: Return a JSON response with a message
    response_data = {'message': 'Scraping completed successfully'}
    return jsonify(response_data)

# @app_blueprint.route('/index', methods=['POST'])
# def upload_resume():
#     # Check if the POST request has the file part
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file part'})

#     resume_file = request.files['resume']

#     # If the user does not select a file, the browser submits an empty file without a filename
#     if resume_file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     if resume_file:
#         try:
#             # You might want to define a directory for uploading and secure the filename
#             # For example, let's use the 'uploads' folder
#             upload_folder = 'E:/FlaskWebAPP1/app/authentication'
#             os.makedirs(upload_folder, exist_ok=True)
#             resume_filename = os.path.join(upload_folder, secure_filename(resume_file.filename))

#             # Save the uploaded file
#             resume_file.save(resume_filename)

#             # Parse the resume and get the results
#             output_file_path = "resume_output.txt"  # Change this path to where you want to save the results
#             resume_parser = ResumeParser()
#             resume_text = resume_parser.extract_text_from_pdf(resume_filename)
#             resume_parser.parse_resume(resume_text, output_file_path)

#             # Read and return the parsed results
#             with open(output_file_path, 'r') as f:
#                 parsed_data = f.read()
#             return jsonify({'parsed_data': parsed_data})
#         except Exception as e:
#             return jsonify({'error': str(e)})
# def select():
#     username = 'Shezak276@gmail.com'
#     password = 'Sheza03214471676'
#     choice = request.form.get('choice_select')
#     target = request.form.get('target')
#     location = request.form.get('location')
#     options = None

#     try:
#         scraper = Profiles(username, password, choice, target, location, options)
#         scraper.login()
#         scraper.collect_links()

#         # Successful scraping
#         response_data = {'message': 'Scraping completed successfully'}
#     except Exception as e:
#         # Error occurred during scraping
#         response_data = {'message': f'Resume not found. Error: {str(e)}'}

#     if 'application/json' in request.headers.get('Accept', ''):
#         return jsonify(response_data)
#     else:
#         response_data = {'message': f'Resume not found. Error: {str(e)}'}




#     return jsonify(response_data)
# @app_blueprint.route('/index', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return "No file part"
#         file = request.files['file']
#         if file.filename == '':
#             return "No selected file"

        # if file:
        #     # Save the uploaded file to a temporary location
        #     file.save('uploads/' + file.filename)

        #     # Get the path to the saved file
        #     pdf_path = 'uploads/' + file.filename

        #     # Create an instance of the ResumeParser class
        #     resume_parser = ResumeParser()


        #     resume_text = resume_parser.extract_text_from_pdf(pdf_path)
        #     name = resume_parser.extract_names(resume_text)
        #     email = resume_parser.extract_emails(resume_text)

        #     # Print or process the extracted information
        #     print("Name:", name)
        #     print("Email:", email)

    #         return "Processing the uploaded resume"
    # else:
    #     return "Invalid request method"

# @app_blueprint.route('/upload', methods=['GET', 'POST'])
# def upload_resume():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         text_pdf = []
#         pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             text_pdf.append(page.extract_text())
#         parsed_data = parse_resume(text_pdf[0])
#         return render_template('upload.html',parsed_data = parsed_data)

app.register_blueprint(app_blueprint)
if __name__ == '__main__':
    app.run(debug=True)
