# Buytrack
## WhatsApp agent to create tables and handle tabular data (initial test is for tracking expenses)
Buytrack LLM Instructions

1. Define task
2. Suggest and share data columns based on task and also be prepare to add any column the user asks for.
3. Receive data and start recording.

Possible tasks and templates:
  - Expenses tracking for projects
  - Personal expenses
  - Group trip expenses
  - Clients database
  - Tasks and to do

1. Welcome prompt and questions.
    - At each step there the agent always sends a message before, to ask for the required information, and a message after, to confirm the information received.
1. User describes the categories for his expenses (business, personal, project_name_1, project_name_2, etc.). If none are given the category "personal" will be the default.
2. User can describe subcategories for each project, if none are given, the agent will suggest some once messages start to be received.
    - User can always ask to add, modify or delete a category and subcategories at any moment and the agent must reclassify the expenses at another category or subcategory given by the user or create a new one if none are given.
3. User sends images, images with text, or just text messages.
    - If a registry has no data the agent asks for clarification.
    - If data is missed the agent can make a suggestion on the category and subcategory.
    - The agent will ask for confirmation about the data to register.
4. The agent stores the data in a tabe format (excel, sheets, etc.).
    - The data stored includes at least Owner, date, category, subcategory, amount spent, payment_method (cash, credit, debit, spei) and can ideally add project, company_name, description, invoice number, and deductibility (for accounting).
5. The agent provides how to total expenses for that subcategory with the latest added information so the user can keep track.

The agent provides a summary of the week expenses, end of month expenses, and year expenses.
The agent provides data analysis suggesting savings.
The user can also ask to add regular payments to the table and the agent will handle them accordingly (netflix monthly subscription)
The user can also ask to keep track of payments that are debt (owning a friend X amount) so the agent can include in the table and give recordatories to the user.
IMPORTANT: Once an expense is confirmed the agent proceeds to add it to the database and cannot delete it or replace it, it can only highlight it by adding an additional column for manual reviewing. Manual modification by the user is required. This is to avoid deleting data by mistake.


Pending tasks:
1. tests
2. explore langchain and other LLMs to save costs.
