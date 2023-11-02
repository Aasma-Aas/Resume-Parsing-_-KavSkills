import os
import docx2txt
import nltk
import re
from tabulate import tabulate
from pdfminer.high_level import extract_text
from PyPDF2 import PdfFileReader
from flask import Flask, redirect, url_for, render_template, request

class ResumeParser:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        nltk.download('stopwords')

    @staticmethod
    def extract_text_from_docx(docx_path):
        txt = docx2txt.process(docx_path)
        if txt:
            return txt.replace('\t', ' ')
        return None

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        return extract_text(pdf_path)

    @staticmethod
    def extract_names(txt):
        person_names = []
        for sent in nltk.sent_tokenize(txt):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    person_names.append(
                        ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                    )
        return person_names[0] if person_names else ""

    @staticmethod
    def extract_phone_number(resume_text):
        PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        phone = re.findall(PHONE_REG, resume_text)
        if phone:
            number = ''.join(phone[0])
            if resume_text.find(number) >= 0 and len(number) < 16:
                return number
        return ""

    @staticmethod
    def extract_emails(resume_text):
        EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
        return re.findall(EMAIL_REG, resume_text)

    @staticmethod
    def extract_skills(input_text):
        SKILLS_DB = [
            'android developer',
            'app developer',
            'JavaScript',
            'Java',
            'machine learning',
            'data science',
            'python',
            'CSS',
            'doctor',
            'teacher',
            'web development',
            'communication',
            'team work',
        ]
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(input_text)

        filtered_tokens = [w for w in word_tokens if w not in stop_words]
        filtered_tokens = [w for w in filtered_tokens if w.isalpha()]

        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

        found_skills = set()

        for token in filtered_tokens:
            if token.lower() in SKILLS_DB:
                found_skills.add(token)

        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)

        return found_skills

    @staticmethod
    def extract_education(input_text):
        RESERVED_WORDS = [
            'school',
            'college',
            'university',
            'academy',
            'faculty',
            'degree',
            'institute',
        ]
        organizations = []

        for sent in nltk.sent_tokenize(input_text):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                    organizations.append(' '.join(c[0] for c in chunk.leaves()))

        education = set()
        for org in organizations:
            for word in RESERVED_WORDS:
                if org.lower().find(word) >= 0:
                    education.add(org)

        return education

    @staticmethod
    def parse_resume(resume_text, output_file_path):
        name = ResumeParser.extract_names(resume_text)
        email = ResumeParser.extract_emails(resume_text)
        phone = ResumeParser.extract_phone_number(resume_text)
        skills = ResumeParser.extract_skills(resume_text)
        education = ResumeParser.extract_education(resume_text)

        info = {
            "Name": name,
            "Email": ", ".join(email),
            "Phone": phone,
            "Skills": ", ".join(skills),
            "Education": ", ".join(education),
        }

        with open(output_file_path, 'a') as f:
            f.write(tabulate(info.items(), headers=["Field", "Value"]))
            f.write("\n\n")