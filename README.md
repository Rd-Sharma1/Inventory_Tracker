# **LEND & BORROW - A Hostel Inventory Tracker**

## **Overview**
Lend & Borrow- Hostel Inventory Tracker is a web-based inventory system designed to facilitate lending and borrowing among users. The application allows users to list items they are willing to lend, borrow available items, and request to borrow them. The goal is to promote resource sharing within a community while maintaining a simple and intuitive interface.

## **Features**
### **Core Functionality**
- **Lending Items**: Users can add items they are willing to lend, specifying details such as name, and quantity.
- **Borrowing Items**: Users can browse the communal inventory and request to borrow available items, providing reason, and a message to lender.
- **Viewing Inventory**: A centralized inventory displays all available items in the system.

## **Technologies Used**
- **Flask** (Backend Framework)
- **SQLite** (Database)
- **Jinja** (Templating Engine)
- **HTML, CSS, Bootstrap** (Frontend Design)
- **JavaScript** (Minimal interactivity via inline scripts in HTML)

## **File Structure**
- **app.py**: The main Flask application, handling routing, database interactions, and business logic.
- **templates/**: Contains all HTML files rendered using Jinja.
  - `main.html` – Landing page displaying the communal inventory.
  - `lend.html` – Page for users to add items for lending.
  - `borrow.html` – Page for users to request borrowed items.
  - `login.html` / `signin.html` – User authentication pages.
- **static/**: Contains CSS files
  - `login.css` – Login styling.
  - `signin.css` – Sign-in styling.
  - `main.css` – Index page styling.
  - `lend.css` – Lend page styling.
  - `borrow.css` – Borrow page styling.
- **project.db**: SQLite database storing user and inventory data.
- **README.md**: This documentation.

## **Design Choices**
### **Chosen Approaches**
1. **SQLite for simplicity** – A lightweight database that is easy to manage for small-scale applications.
2. **Bootstrap for UI** – Ensured a responsive and modern design with minimal custom CSS.
3. **Minimal JavaScript** – Kept the frontend lightweight by using JavaScript only where necessary.

### **Debated Design Choices**
- **Handling Multiple Borrow Requests**: Initially, we considered allowing multiple users to request the same item and letting the lender choose the borrower. However, this was excluded to maintain simplicity and avoid conflicts. A system involving **cash transactions or a point-based system** could have made this fairer, but it would have **complicated the core functionality** of direct lending and borrowing.

## **Challenges Faced**
- Implementing an intuitive lending/borrowing workflow while maintaining a simple UI.
- Deciding on a fair borrowing system without introducing unnecessary complexity.
- Ensuring database integrity and preventing duplicate requests.

## **How to Run the Project**
1. **Clone the Repository**:
   ```bash
   git clone <https://github.com/Rd-Sharma1/Inventory_Tracker>
   cd CS50_FP
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   flask run
   ```
5. **Access in Browser**:
   Once the Flask server is running, open your web browser and navigate to http://localhost:5000/ to access the application.

## **Credits**
- AI Assistance: ChatGPT
- Additional Contributions: Piyush Varshney, Prajjwal Arya


## **Future Improvements**
- **Notifications for Lend Requests**
- **Automated Return Reminders**
- **User Ratings & Reviews**
- **Item Categories & Search Filters**

---
