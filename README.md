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



System:
You are an assistant that extracts structured information from the text received to match a specific format (store it as tables)
You must always respond with valid JSON only.



### Agent logic
0. The user texts something to start the chat.
1. Welcome prompt and questions. User receives an explanation of how to work, a template message to easily copy/paste and an example of how to fill it (using this format decreases greatly the errors).
  - The user can modify the template message to what best fits their needs. Ex. asking to add a column for company_name, description, invoice number, and deductibility (for accounting).
2. The agent asks for categories (business, personal, project_name_1, project_name_2, etc.) and wait for the user to respond. The agent will explain that the user can decide to skip this part but all expenses will be given the category "personal" by default until the user decides to change it or start recording at a new category.
3. The agent asks for subcategories of each project(category) and provides an example for personal (rent, services, supermarket, eating out, fun, extras, health, savings). If savings is selected the agent suggests to open a separate account (bank/investment) that allows him to transfer money so it remains separated anc can be easily tracked. The agent also explains that this step can be optional at the moment but it will ask where to place expenses as soon the registry starts.
    NOTE: User can always ask to add or modify category and subcategories names at any moment. The agent must proceed to reclassify the expenses at the new category defined by the user making sure. The agent must always ask for confirmation before applying the changes and in case there is a category or subcategory already named that way, the agent must ask for clarification.
3. After setup the user can start sending images, images with text, or just text messages making sure to include category and subcategory.
4. The service  and extract data
    - The agent proceeds to extract information from the image, image with prompt or text received (the ocr does this) and the information extracted is provided to the agent.
5. The agent then receives the text extracted and analyzes it to adapt fill the template message and send back to the user for confirmation.
    - If no data was extracted, the agent asks the user for clarification.
    - If no subcategories is specified the agent can make a suggestion on the subcategory based on the information provided and also previous records.
    - If there are minor typos in the text the agent asks for clarification.
4. The agent will ask for confirmation about the data to register everytime.
5. After user confirmation, the agent stores the data in a table format (excel, sheets or other database that the user provides permission in the cloud) and then provides the accumulated expenses for that subcategory monthly with the latest added information so the user can keep track.
    - The data stored must include at least the data from the data from the template message (Owner, date, category, subcategory, amount spent, payment_method (cash, credit, debit, spei)).
    IMPORTANT: Once an expense is confirmed the agent proceeds to add it to the database and cannot delete it or replace it, it can only highlight it by adding an additional column for manual reviewing. Manual modification by the user is required. This is to avoid deleting data by mistake.
6. The user can ask for expenses summary and analysis for a specific period of time.


Other additional interactions:
- The user can also ask to add regular payments to the table and the agent will handle them accordingly (netflix monthly subscription).

Future updates:
- The user can also ask to keep track of payments that are debt (owning a friend X amount) so the agent can include in the table and give recordatories.
- The agent provides a summary of the week expenses, end of month expenses, and year expenses.
- The agent provides data analysis suggesting savings.
- Only the group admin in whatsapp can ask to modify entries from the users, otherwise each user can only ask to modify entries they have made.
