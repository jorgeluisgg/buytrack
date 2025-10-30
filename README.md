# Buytrack
## WhatsApp agent to track expenses

Instructions
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

The data stored includes at least Owner, date, category, subcategory, amount spent, payment type (cash, credit, debit, spei) and can ideally add description, invoice number, and deductibility (for accounting).
The agent provides a summary of the week expenses, end of month expenses, and year expenses.
The agent provides data analysis suggesting savings.
