# Meeting-master-LLM

## Overview:
This project is a tool designed to efficiently manage meetings by organizing discussion points, recording meetings, tracking unresolved issues, and generating post-meeting summaries. It utilizes Large Language Models (LLMs) to generate accurate summaries, including key decisions and unresolved points. The project is divided into two parts:

Pre-Meeting Management Tool (Dhiwise_meet):

Allows users to upload pre-meeting documents, organize discussion points, and generate meeting agendas.
Tracks meeting progress, flagging unresolved points.
Post-Meeting Management Tool (Dhiwise_postmeet):

Handles meeting recordings, generates summaries, and organizes key decisions and action items.

## Project Structure:


├── Pre_meet/
│   ├── app.py                # Main application file for pre-meeting tool
│   ├── db.py                 # Database management (SQLite)
│   ├── meetings.db           # Database file
│   ├── requirements.txt      # List of dependencies
│   ├── static/               # Static files (CSS, JavaScript)
│   ├── templates/            # HTML templates
│   ├── uploads/              # Folder for uploaded files
│   ├── venv/                 # Virtual environment (if created locally)
│   └── test.py               # Test script for the pre-meeting tool
│
├── Post_meet/
│   ├── post_app.py           # Main application file for post-meeting tool
│   ├── templates/            # HTML templates for the post-meeting tool
│   └── uploads/              # Folder for video uploads
│
└── README.md                 # Project documentation

Setup Instructions:

Prerequisites:
Python 3.8+
Virtual environment for dependency management is recommended.
Installation Steps
Create a virtual environment in the project directory:
python3 -m venv venv
For Windows: `venv\Scripts\activate` # for macOS : source venv/bin/activate

Install the required dependencies: Navigate to the Dhiwise_meet directory and install the packages:
pip install -r requirements.txt

Run the pre-meeting tool: Inside the Dhiwise_meet directory, run:
python app.py
This will start the pre-meeting tool on localhost:5000.

Run the post-meeting tool: Navigate to the Dhiwise_postmeet directory and run:
python post_app.py
This will start the post-meeting tool, accessible via localhost.

Usage:
Pre-Meeting Tool: The tool will launch at localhost:5000, allowing users to upload documents and add discussion points.
Post-Meeting Tool: Submit meeting recordings, and the tool will generate summaries and track unresolved points.
