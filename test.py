from app import app
from app import discussion_points
import cohere # type: ignore



# Initialize the Cohere client with your API key
co = cohere.Client('qzxcsxL1fhLcgRFcKXjqCnNWVwI3nr9dO3JPt8Zg')

def generate_summary_with_cohere(discussion_points):
    # Join all discussion points into a single string
    text_input = "\n".join(discussion_points)

    # Create a prompt for Cohere summarization
    prompt = f"Summarize the following discussion points:\n{text_input}\nPlease include key decisions, unresolved issues, and action items."

    # Call Cohere's Generate API
    response = co.generate(
        model='command-xlarge-nightly',  # Cohere's large model for generation
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
    )

    # Extract and return the generated summary
    summary = response.generations[0].text.strip()
    return summary


@app.route('/generate_summary', methods=['GET'])
def summarize_meeting():
    if not discussion_points:
        return "No discussion points available for summarization", 400

    # Call the Cohere summarization function
    summary = generate_summary_with_cohere(discussion_points)

    return f"<h1>Meeting Summary</h1><p>{summary}</p>"

