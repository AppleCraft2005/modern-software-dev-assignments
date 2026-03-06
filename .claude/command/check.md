<prompt_info>
Intent: Run linter, formatter, and automated tests on the backend application.
Description: This command is used to format the code (black), check coding standards (ruff), and ensure no code is broken via testing (pytest).
</prompt_info>

# Execution Instructions
When this command is called, perform the following steps sequentially:

1. Run python `-m black week4/backend/` to format the code.
2. Run python `-m ruff check week4/backend/` to check for linting issues.
3. Run python `-m pytest week4/backend/tests/` to execute all tests.

# Expected Output
- If all the commands above succeed without errors, provide a brief summary stating "Code is properly formatted and all tests passed!".
- If there are errors or failed tests, summarize which parts failed and provide 1-2 specific suggestions for fixing them so the application can run normally again.