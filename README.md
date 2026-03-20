**PromptLab**

AI Prompt Engineering Platform for managing reusable prompts and collections via a REST API.


**Project Overview and Purpose**

PromptLab is an AI prompt management platform built for engineers who need a structured way to create, store, and reuse prompts.

Instead of scattered prompt definitions across codebases or documents, PromptLab provides a centralized system to manage prompts and group them into collections. This improves consistency, reusability, and collaboration across teams working on AI-driven applications.

The platform is implemented using FastAPI and Python, making it lightweight, performant, and easy to extend with features like persistent storage, authentication, and UI integration.

**Features List**

PromptLab currently supports:

Full CRUD operations for prompts

Grouping prompts into collections

Search functionality (title and description)

Filtering prompts by collection

Automatic timestamp management

RESTful API built with FastAPI

In-memory storage for rapid prototyping

Interactive API documentation via Swagger UI

Future Improvements

Persistent database integration

Authentication and role-based access control

Prompt version management

Tagging and categorization

Web-based frontend interface

Tech Stack

The platform is built using:

Python 3.10+ – Core language

FastAPI – API framework for high performance

Pydantic – Data validation and schema management

Pytest – Testing framework

GitHub – Source control and collaboration

**Prerequisites and Installation**

Ensure the following are installed:

Python 3.10 or higher

Git

pip (Python package manager)

Clone the repository:

git clone <your-repo-url>
cd promptlab

Install backend dependencies:

cd backend
pip install -r requirements.txt

#Quick Start Guide

Start the backend server:

cd backend
python main.py

The API will be available at:

http://localhost:8000

FastAPI provides built-in interactive documentation.

Access it at:

http://localhost:8000/docs

You can use this interface to explore and test all endpoints.

#API Endpoint Summary with Examples
Health Endpoint
Method	Endpoint	Description
GET	/health	Returns API health status

Example:

curl -X GET http://localhost:8000/health

Example Response:

{
  "status": "healthy",
  "version": "1.0.0"
}
**Prompt Endpoints**

Method	Endpoint	Description
GET	/prompts	Fetch all prompts
GET	/prompts/{prompt_id}	Fetch a specific prompt
POST	/prompts	Create a new prompt
PUT	/prompts/{prompt_id}	Update an existing prompt
DELETE	/prompts/{prompt_id}	Delete a prompt

Example: Create Prompt

POST /prompts
{
  "title": "Summarize Text",
  "content": "Summarize the following: {{input}}",
  "description": "Summarizes input text"
}
Collection Endpoints
Method	Endpoint	Description
GET	/collections	Fetch all collections
GET	/collections/{collection_id}	Fetch a specific collection
POST	/collections	Create a new collection
DELETE	/collections/{collection_id}	Delete a collection

Example:

curl -X GET http://localhost:8000/collections
Development Setup

Set up the development environment:

cd backend
pip install -r requirements.txt
python main.py

Run tests:

cd backend
pytest tests/ -v

#Run tests with coverage:

pytest tests/ --cov=app
Project Structure
promptlab/
├── README.md
├── PROJECT_BRIEF.md
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── models.py
│   │   ├── storage.py
│   │   └── utils.py
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
│
├── docs/
│   └── API_REFERENCE.md
│
├── frontend/
│   └── (future frontend application)
│
├── specs/
│   ├── prompt-versions.md
│   └── tagging-system.md
│
└── .github/
    └── copilot-instructions.md
Documentation

Additional resources:

API Reference: docs/API_REFERENCE.md

Feature Specifications:

specs/prompt-versions.md

specs/tagging-system.md

These documents provide deeper details on API behavior and planned enhancements.

**Contributing Guidelines**

To contribute:

Fork the repository

Create a feature or fix branch

Implement your changes

Run tests locally

Push and open a Pull Request

Example:

git checkout -b feature/update-readme
git add .
git commit -m "Improve README documentation"
git push origin feature/update-readme

Ensure code quality, test coverage, and proper documentation in all contributions.

**Summary**

PromptLab offers a clean and extensible backend for managing AI prompts with a focus on structure and reuse.

It provides core capabilities for prompt and collection management while remaining simple enough to extend with production-grade features like persistence, authentication, and UI integration.