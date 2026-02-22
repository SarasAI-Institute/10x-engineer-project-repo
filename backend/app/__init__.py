"""PromptLab - AI Prompt Engineering Platform.

PromptLab is a tool for AI engineers to store, organize, and manage their prompts.
Think of it as "Postman for Prompts" - a professional workspace for prompt templates.

Features:
    - Store prompt templates with variables ({{input}}, {{context}})
    - Organize prompts into collections
    - Tag and search prompts
    - Track version history via timestamps
    - Test prompts with sample inputs

Architecture:
    - api.py: FastAPI routes and endpoints
    - models.py: Pydantic data models
    - storage.py: In-memory data storage
    - utils.py: Helper functions
"""

__version__ = "0.1.0"
