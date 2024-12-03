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
│   ├── app.py                 
│   ├── db.py                 
│   ├── meetings.db           
│   ├── requirements.txt      
│   ├── static/               
│   ├── templates/            
│   ├── uploads/              
│   ├── venv/                 
│   └── test.py               
│
├── Post_meet/
│   ├── post_app.py           
│   ├── templates/            
│   └── uploads/                 
│                 
└── README.md                 

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
