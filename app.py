from flask import Flask, render_template, request, redirect, url_for
import os
import PyPDF2  # To handle PDF extraction
import cohere

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pre_meeting_content = ""  # To store content from the pre-meeting document
discussion_points = []  # Store the discussion points
discussed_points = []  # Store the points marked as discussed

# Initialize Cohere
co = cohere.Client('qzxcsxL1fhLcgRFcKXjqCnNWVwI3nr9dO3JPt8Zg')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html', discussion_points=discussion_points)

# Route for document upload
@app.route('/upload', methods=['POST'])
def upload():
    global pre_meeting_content
    if 'file' not in request.files:
        return 'No file uploaded!', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract content from the pre-meeting document (PDF)
    pre_meeting_content = extract_text_from_pdf(file_path)
    return redirect(url_for('home'))

# Route for adding discussion points
@app.route('/add_point', methods=['POST'])
def add_point():
    point = request.form['discussion_point'].strip()
    if point and point not in discussion_points:
        discussion_points.append(point)
    return redirect(url_for('home'))

# Route for marking points as discussed
@app.route('/mark_discussed', methods=['POST'])
def mark_discussed():
    points = request.form.getlist('discussion_point')
    for point in points:
        if point not in discussed_points:
            discussed_points.append(point)
    return redirect(url_for('home'))

# Route to generate summary
@app.route('/generate_summary', methods=['GET'])
def generate_summary():
    global pre_meeting_content

    # Check if both pre-meeting document and discussion points are empty
    if not pre_meeting_content and not discussion_points:
        return "Please upload a pre-meeting document or add discussion points first."

    # Generate different summaries based on the available input
    if pre_meeting_content and not discussion_points:
        # Only pre-meeting document is provided
        part1 = generate_agendas_summary(pre_meeting_content)
        return f"<h2>Meeting Summary</h2><p>{part1}</p>"

    if discussion_points and not pre_meeting_content:
        # Only discussion points are provided
        part2 = generate_discussed_agendas(discussion_points)
        return f"<h2>Meeting Summary</h2><p>{part2}</p>"

    if pre_meeting_content and discussion_points:
        # Both pre-meeting document and discussion points are available
        part1 = generate_agendas_summary(pre_meeting_content, discussion_points)
        part2 = generate_discussed_agendas(discussed_points)
        part3 = generate_undiscussed_agendas(discussion_points, discussed_points)

        # Combine all parts into a single summary with bullet points
        full_summary = (
            f"<h2>Three-Part Summary</h2>"
            f"<h3>Part 1: Agendas</h3><ul>{part1}</ul>"
            f"<h3>Part 2: Discussed Agendas</h3><ul>{part2}</ul>"
            f"<h3>Part 3: Undiscussed Agendas</h3><ul>{part3}</ul>"
        )
        return f"<div>{full_summary}</div>"

# Function to generate agenda summary (Part 1)
def generate_agendas_summary(pre_meeting_content, discussion_points=None):
    if discussion_points:
        prompt = f"Generate a bullet-point summary of the meeting agendas based on the following pre-meeting document and discussion points:\n\nPre-Meeting Document:\n{pre_meeting_content}\n\nDiscussion Points:\n{discussion_points}"
    else:
        prompt = f"Generate a bullet-point summary of the meeting agenda based solely on the pre-meeting document:\n\n{pre_meeting_content}"
    
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )
    # Format the response as bullet points
    summary = response.generations[0].text.strip().replace("\n", "</li><li>")
    return f"<li>{summary}</li>"

# Function to generate discussed agendas (Part 2)
def generate_discussed_agendas(discussed_points):
    prompt = f"Generate a bullet-point summary of the discussed points in the meeting:\n\n{discussed_points}"
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    # Format the response as bullet points
    summary = response.generations[0].text.strip().replace("\n", "</li><li>")
    return f"<li>{summary}</li>"

# Function to generate undiscussed agendas (Part 3)
def generate_undiscussed_agendas(discussion_points, discussed_points):
    undiscussed = [point for point in discussion_points if point not in discussed_points]
    prompt = f"Generate a bullet-point summary of the undiscussed points that should be addressed in the next meeting:\n\n{undiscussed}"
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    # Format the response as bullet points
    summary = response.generations[0].text.strip().replace("\n", "</li><li>")
    return f"<li>{summary}</li>"

# Run the Flask app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
