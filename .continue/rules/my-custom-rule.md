---
description: This file defines how AI coding agents should read, generate, and modify code in this repository. All automated code generation must follow these rules.
---

- Output Format Rules

AI behavior rules:

- Follow existing project structure and patterns.
- Do not introduce new libraries or frameworks unless explicitly requested.
- Prefer minimal, safe, and incremental changes.
- Maintain backward compatibility.
- Avoid modifying unrelated files.

Output format rules:

- Use clear explanations with simple language.
- Prefer bullet points and short paragraphs.
- Use code blocks only when necessary.
- Include a short summary at the end when helpful.
- When relevant, explicitly mention:
  - Inputs
  - Outputs
  - Side effects
  - Dependencies

Teaching rules:

- Assume the reader is a beginner to intermediate developer.
- Never assume prior knowledge of frameworks or libraries.
- Explain non-obvious logic clearly.
- If something is missing or unclear, explicitly point it out.

Safety rules:

- Do NOT modify code unless explicitly asked.
- Do NOT refactor code unless explicitly requested.
- Do NOT change configuration files unless asked.
- Ask clarifying questions only if the goal is ambiguous.

Project coding standards:

- Write clean, readable, and maintainable code.
- Follow existing linting and formatting rules.
- Avoid duplicate logic.
- Keep functions small and focused.
- Prefer composition over inheritance.
- Add comments only when logic is not obvious.

Preferred patterns and conventions:

- Keep UI, business logic, and services separated.
- Avoid large monolithic files.
- Reuse existing utilities and shared components.
- Centralize API calls in service layers.
- Avoid API calls directly inside UI components.

File naming conventions:

- Components use PascalCase.
- Hooks use the "useSomething" naming pattern.
- Utilities use camelCase.
- Constants use UPPER_SNAKE_CASE.
- Test files use *.test.* or *.spec.* naming.

Error handling approach:

- Never silently ignore errors.
- Always provide meaningful error messages.
- Fail gracefully when errors occur.
- Avoid exposing raw backend errors to the UI.
- Log errors when appropriate.

Testing requirements:

- Add tests for new logic when feasible.
- Do not break existing tests.
- Update tests when behavior changes.
- Mock external services in tests.
- Avoid network calls in tests.

When analyzing files:

- Always mention the file name and language.
- Explain how the file fits into the overall system.
- Describe the responsibilities of the file.
- Mention key dependencies and side effects.

Final rule:

- When unsure, follow existing project patterns instead of introducing new ones.



