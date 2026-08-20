from flask import Flask, render_template, request, redirect # type: ignore
import sqlite3

app = Flask(__name__)
# intiallize the database if not exists

def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, name TEXT, quantity  INTEGER)")
    conn.commit()
    conn.close()

# dashboard route which shows all the inventory items 
@app.route("/")
def index():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    return render_template("index.html", items=items)


### to add item route so i can get shows form, POST saves the new item 
@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        c.execute("INSERT INTO inventory (name, quantity) VALUES (?,?)",(name,quantity))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_item.html", edit=False)

### to delete item route which is removing routes by id 
@app.route("/delete/<int:item_id>")
def delete_item(item_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect("/")

## to edit the item route 
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    if request.method == "POST":
        new_name = request.form["name"]
        new_quantity = request.form["quantity"]
        c.execute("UPDATE inventory SET name=?, quantity=? WHERE id=?", (new_name, new_quantity, item_id))
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        c.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
        item = c.fetchone()
        conn.close()
        return render_template("add_item.html", item=item, edit=True)

@app.route("/reports")
def reports():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    ###show items with less than 5 items 
    c.execute("SELECT * FROM inventory WHERE quantity < 5")
    low_stock = c.fetchall()
    conn.close()
    return render_template("reports.html", low_stock=low_stock )



if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)

