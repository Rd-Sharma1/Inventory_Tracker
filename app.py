import sqlite3
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session

app = Flask(__name__)

app.config["SESSIO_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    conn = sqlite3.connect("project.db", check_same_thread=False)
    db1 = conn.cursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")


        db1.execute("SELECT name FROM users WHERE name = ?", (username,))
        name = db1.fetchone()

        if not name:
            return "Invalid name"
        
        db1.execute("SELECT password FROM users WHERE name = ?", (username,))
        stored_password = db1.fetchone()

        if password != stored_password[0]:
            return "Invalid password"
        
        session["user"] = username
        inventory = db1.execute("SELECT * FROM inventory").fetchall()
        return render_template("main.html", inventory=inventory)
    else:
        inventory = db1.execute("SELECT * FROM inventory").fetchall()
        return render_template("main.html", inventory=inventory)

@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method == "POST":
        connection = sqlite3.connect("project.db", check_same_thread=False)
        db2 = connection.cursor()
        name = request.form.get("username")
        passw = request.form.get("password")
        db2.execute("INSERT INTO users (name, password) VALUES (? , ?)", (name, passw,))

        connection.commit()
        connection.close()
        return render_template("login.html")
    else:
        return render_template("signin.html")


@app.route("/lend", methods=["GET", "POST"])
def lend():
    conn = sqlite3.connect("project.db", check_same_thread=False)
    db = conn.cursor()
    if request.method =="POST":

        item_name = request.json.get("item")
        quantity = int(request.json.get("qty"))

        if item_name and quantity:
            db.execute("INSERT INTO inventory (item, qty, owner) VALUES (?, ?, ?)", (item_name, quantity, session["user"]))
            conn.commit()
            return jsonify({"qty": quantity, "name": item_name}),200

        return jsonify({"error": "INVALID INPUT"}), 400
    else:

        items = db.execute("SELECT item, qty FROM inventory WHERE owner = ?", (session["user"],)).fetchall()
        requests = db.execute("SELECT notify.id, inventory.item, notify.quantity, reason, duration, message FROM notify JOIN inventory ON notify.item_id = inventory.id WHERE owner = ?", (session["user"],)).fetchall()
        return render_template("lend.html", items = items, requests = requests)

    
@app.route("/borrow", methods=["GET", "POST"])
def borrow():
    conn = sqlite3.connect("project.db", check_same_thread=False)
    db = conn.cursor()
    if request.method == "GET":
        b_items = db.execute("""
            SELECT item, qty, owner 
            FROM inventory 
            WHERE id NOT IN (
                SELECT item_id 
                FROM borrowed_items 
                WHERE returned_at IS NULL
                UNION
                SELECT item_id 
                FROM notify
            ) AND owner != ?
        """, (session["user"],)).fetchall()
        return render_template("borrow.html", b_items=b_items)
    elif request.method == "POST":

        item = request.json.get("item") 
        qty = request.json.get("qty")
        owner = request.json.get("owner")
        message = request.json.get("message")
        duration = request.json.get("duration")
        reason = request.json.get("reason")

        if item and qty and owner and duration and reason:
            if session["user"] == owner:  
                return jsonify({"error": "You cannot borrow your own item"}), 400
            else:
                item_id_row = db.execute("SELECT id FROM inventory WHERE item = ?", (item,)).fetchone()
                if item_id_row:
                    item_id = item_id_row[0]

                #print(item_id, session["user"], qty, reason, duration, message)
                borrower_id_row = db.execute("SELECT id FROM users WHERE name = ?", (session["user"],)).fetchone()
                if borrower_id_row:
                    borrower_id = borrower_id_row[0]

                lender_id_row = db.execute("SELECT id FROM users WHERE name = ?", (owner,)).fetchone()
                if lender_id_row:
                    lender_id = lender_id_row[0]

                db.execute("INSERT INTO notify (item_id, borrower_id, lender_id, quantity, reason, duration, message) VALUES (?, ?, ?, ?, ?, ?, ?)", (item_id, borrower_id, lender_id, qty, reason, duration, message))
                conn.commit()
                return jsonify({"qty": qty, "item": item, "owner": owner }),200
        return jsonify({"error": "INVALID INPUT"}), 400
    

@app.route("/approve-request", methods=["POST"])
def approve_request():
    data = request.get_json()
    request_id = data.get("id")
    if not request_id:
        return jsonify({"error": "Invalid request ID."}), 400


    conn = sqlite3.connect("project.db", check_same_thread=False)
    db = conn.cursor()

    # The following code was implemented with guidance from ChatGPT. 
    try:
        # Explicitly start a transaction
        conn.execute("BEGIN")

        # Fetch request details
        request_details = db.execute(
            "SELECT item_id, borrower_id, lender_id, quantity FROM notify WHERE id = ?", (request_id,)
        ).fetchone()

        if not request_details:
            print(f"REQUEST ID {request_id} not found in 'notify.")
            return jsonify({"error": "Request not found."}), 404
        
        print(f"Processing request: {request_details}")
        
        # Delete request from notify_table
        db.execute("DELETE FROM notify WHERE id = ?", (request_id,))
        print(f"Deleted from notify")

        # Insert into borrowed_items
        db.execute(
            """
            INSERT INTO borrowed_items 
            (item_id, borrower_id, lender_id, quantity) 
            VALUES (?, ?, ?, ?)
            """,
            (
                request_details[0],  # item_id
                request_details[1],  # borrower_id
                request_details[2],  # lender_id
                request_details[3],  # quantity
            ),
        )
        print(f"Inserted into 'borrowed_items'.")

        # Update inventory quantity (optional)
        db.execute(
            """
            DELETE FROM inventory
            WHERE id = ?
            """,
            (
                request_details[0],  # item_id
            ),
        )
        print(f"Deleted from 'inventory'.")

        # Commit the transaction
        conn.commit()
        return jsonify({"message": "Request approved successfully!"}), 200

    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print("Error approving request ID {request_id}: {e}")
        return jsonify({"error": "Failed to approve request. Reason: {str(e)}"}), 500

    finally:
        # Close the database connection
        conn.close()
        print("Database connection closed.")


