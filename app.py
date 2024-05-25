from flask import Flask, render_template, request, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Sorular listesi
questions = []

# E-posta gönderim fonksiyonu
def send_email(student_name, student_email, answers):
    sender = 'your-email@gmail.com'
    password = 'your-app-password'
    receiver = 'teacher-email@example.com'
    subject = f"{student_name} isimli öğrencinin test sonuçları"
    body = f"Öğrenci: {student_name}\nE-posta: {student_email}\nCevaplar:\n"
    for i, answer in enumerate(answers):
        body += f"Soru {i+1}: {answer}\n"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderilirken bir hata oluştu: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form['question']
        options = [request.form['option1'], request.form['option2'], request.form['option3'], request.form['option4']]
        answer = request.form['answer']
        questions.append({
            'question': question_text,
            'options': options,
            'answer': answer
        })
        return redirect(url_for('add_question'))
    return render_template('add_question.html')

@app.route('/student')
def student():
    return render_template('student.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['name']
    student_email = request.form['email']
    answers = []
    for i in range(len(questions)):
        answers.append(request.form.get(f'question_{i}'))
    
    send_email(student_name, student_email, answers)
    return redirect(url_for('student'))

if __name__ == '__main__':
    app.run(debug=True)
  
