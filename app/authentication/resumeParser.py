# resume_parser.py

# import pdfplumber

# def parse_resume(pdf_file):
#     parsed_data = {"email": "", "phone": "", "name": ""}
#     with pdfplumber.open(pdf_file) as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#         # Implement your logic to extract email, phone, and name here
#         # Example:
#         if "Email:" in text:
#             parsed_data["email"] = text.split("Email:")[1].split()[0]
#         if "Phone:" in text:
#             parsed_data["phone"] = text.split("Phone:")[1].split()[0]
#     return parsed_data


# import pickle, re, os
# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer(stop_words='english')
# with open('tfidf.pkl', 'wb') as tfidf_file:
#     pickle.dump(tfidf, tfidf_file)
# def parse_resume(pdf_file):
    


#     with open('clf.pkl', 'wb') as clf_file:
#         pickle.dump(clf, clf_file)
#     clf = pickle.load(open('clf.pkl', 'rb'))

#     def cleanResume(txt):
#         cleanText = re.sub('http\S+\s', ' ', txt)
#         cleanText = re.sub('RT|cc', ' ', cleanText)
#         cleanText = re.sub('#\S+\s', ' ', cleanText)
#         cleanText = re.sub('@\S+', '  ', cleanText)  
#         cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
#         cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
#         cleanText = re.sub('\s+', ' ', cleanText)
#         return cleanText

#     # Clean the input resume
#     cleaned_resume = cleanResume(pdf_file)

#     # Transform the cleaned resume using the trained TfidfVectorizer
#     input_features = tfidfd.transform([cleaned_resume])

#     # Make the prediction using the loaded classifier
#     prediction_id = clf.predict(input_features)[0]

#     # Map category ID to category name
#     category_mapping = {
#         15: "Java Developer",
#         23: "Testing",
#         8: "DevOps Engineer",
#         20: "Python Developer",
#         24: "Web Designing",
#         12: "HR",
#         13: "Hadoop",
#         3: "Blockchain",
#         10: "ETL Developer",
#         18: "Operations Manager",
#         6: "Data Science",
#         22: "Sales",
#         16: "Mechanical Engineer",
#         1: "Arts",
#         7: "Database",
#         11: "Electrical Engineering",
#         14: "Health and fitness",
#         19: "PMO",
#         4: "Business Analyst",
#         9: "DotNet Developer",
#         2: "Automation Testing",
#         17: "Network Security Engineer",
#         21: "SAP Developer",
#         5: "Civil Engineer",
#         0: "Advocate",
#     }

#     category_name = category_mapping.get(prediction_id, "Unknown")
#     return category_name

    # print("Predicted Category:", category_name)
    # print(prediction_id)
    
import pickle, re, os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Import the appropriate classifier if you're using SVC

# Create and save the TfidfVectorizer outside the function
tfidf = TfidfVectorizer(stop_words='english')
with open('tfidf.pkl', 'wb') as tfidf_file:
    pickle.dump(tfidf, tfidf_file)

# Load the trained classifier
try: 
    with open('clf.pkl', 'rb') as clf_file:
        clf = pickle.load(clf_file)
except EOFError:
    'File size!= 0'

def parse_resume(text_pdf):
    # print('def text_pdf', dtype(text_pdf))

    
    # def pdfextract(pdf_file):
    #    text = []
    #    with open(pdf_file, 'rb') as file:
    #         pdf_reader = PyPDF2.PdfFileReader(file)
    #         for page_num in range(pdf_reader.numPages):
    #             page = pdf_reader.getPage(page_num)
    #             text.append(page.extract_text())
    #             print('textttttttttttttttttttt:', text)
    #         return text

    # pdf_text = pdfextract(pdf_file)
    # pdf_text = " ".join(pdf_text)

    def cleanResume(txt):
        cleanText = re.sub('http\S+\s', ' ', txt)
        cleanText = re.sub('RT|cc', ' ', cleanText)
        cleanText = re.sub('#\S+\s', ' ', cleanText)
        cleanText = re.sub('@\S+', '  ', cleanText)  
        cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
        cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
        cleanText = re.sub('\s+', ' ', cleanText)
        return cleanText

# Clean the input resume
    cleaned_resume = cleanResume(text_pdf)
    print('cleaned_resume=========', cleaned_resume)

    # Transform the cleaned resume using the trained TfidfVectorizer
    input_features = tfidf.transform([cleaned_resume])

    # Make the prediction using the loaded classifier
    prediction_id = clf.predict(input_features)[0]

    # Map category ID to category name
    category_mapping = {
        15: "Java Developer",
        23: "Testing",
        8: "DevOps Engineer",
        20: "Python Developer",
        24: "Web Designing",
        12: "HR",
        13: "Hadoop",
        3: "Blockchain",
        10: "ETL Developer",
        18: "Operations Manager",
        6: "Data Science",
        22: "Sales",
        16: "Mechanical Engineer",
        1: "Arts",
        7: "Database",
        11: "Electrical Engineering",
        14: "Health and fitness",
        19: "PMO",
        4: "Business Analyst",
        9: "DotNet Developer",
        2: "Automation Testing",
        17: "Network Security Engineer",
        21: "SAP Developer",
        5: "Civil Engineer",
        0: "Advocate",
    }

    category_name = category_mapping.get(prediction_id, "Unknown")
    return category_name

# Example usage:
# category = parse_resume('sample_resume.pdf')
# print("Predicted Category:", category)


