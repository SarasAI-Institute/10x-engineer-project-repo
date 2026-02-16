# PromptLab

PromptLab is an internal tool designed for AI engineers to store, organize, and manage their prompts. Built on the FastAPI framework, it provides an efficient and scalable way to handle prompt data.

## Features

- Store and manage AI prompts
- Organize prompts by categories
- API endpoints for prompt CRUD operations
- Intuitive user interface for easy prompt management

## Prerequisites and Installation

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- FastAPI
- Uvicorn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PromptLab.git
   ```
2. Change into the project directory:
   ```bash
   cd PromptLab
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start Guide

1. Run the FastAPI application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Access the application at `http://127.0.0.1:8000`.

## API Endpoint Summary

- **GET /prompts/**: Retrieve a list of all prompts.

  **Example Request:**
  ```bash
  curl -X GET http://yourapi.com/prompts/
  ```

- **POST /prompts/**: Create a new prompt.

  **Example Request:**
  ```bash
  curl -X POST http://yourapi.com/prompts/ -d '{"title": "New Prompt", "content": "Prompt content"}' -H 'Content-Type: application/json'
  ```

- **GET /prompts/{id}**: Retrieve a prompt by its ID.

  **Example Request:**
  ```bash
  curl -X GET http://yourapi.com/prompts/1
  ```

- **PUT /prompts/{id}**: Update a prompt by its ID.

  **Example Request:**
  ```bash
  curl -X PUT http://yourapi.com/prompts/1 -d '{"title": "Updated Title", "content": "Updated content"}' -H 'Content-Type: application/json'
  ```

- **DELETE /prompts/{id}**: Delete a prompt by its ID.

  **Example Request:**
  ```bash
  curl -X DELETE http://yourapi.com/prompts/1
  ```


### Example

Here is a sample curl request to fetch all prompts:

```bash
curl -X GET "http://127.0.0.1:8000/prompts/" -H "accept: application/json"
```

## Development Setup

To contribute to this project, follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

# Contributing to PromptLab

Thank you for considering contributing to this project! We welcome improvements and fixes from the community. Please read through the following guidelines to effectively contribute to the project.

## How to Contribute

1. **Fork the Repository**: Start by forking the repository to your GitHub account.

2. **Clone the Repository**: Clone the forked repository to your local machine.

   ```bash
   git clone https://github.com/your-username/project-name.git
   ```

3. **Create a Branch**: For new features or bug fixes, create a new branch from the `main` branch.

   ```bash
   git checkout -b feature/new-feature
   ```

4. **Make Changes**: Implement your changes. Ensure your code follows the project's style and includes necessary documentation and tests.

5. **Commit Changes**: Commit your changes with a descriptive commit message.

   ```bash
   git commit -m "Description of changes"
   ```

6. **Push Changes**: Push your changes to your forked repository.

   ```bash
   git push origin feature/new-feature
   ```

7. **Create a Pull Request**: Navigate to the original repository and open a pull request from your forked repository's branch.

8. **Review Process**: Your pull request will be reviewed by the maintainers. Please be responsive to any requested changes.

## Coding Standards

- Use clear, concise, and descriptive commit messages.
- Follow the project's coding style and guidelines.
- Write unit tests for new features or bug fixes.

## Reporting Issues

If you encounter any issues or would like to request a new feature, please open an issue in the GitHub issues tab with a detailed description.

Thank you for your contributions and support!
```

Now, update the `README.md` file with a brief introduction to the contributing guidelines:

```markdown README.md
