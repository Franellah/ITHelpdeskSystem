from flask import Flask, render_template, request, redirect
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def home():

    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")

    tickets = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        tickets=tickets
    )
@app.route('/delete/<int:id>')
def delete_ticket(id):

    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tickets WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_ticket(id):

    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        ticket_no = request.form['ticket_no']
        store = request.form['store']
        asset_name = request.form['asset_name']
        issue_category = request.form['issue_category']
        priority = request.form['priority']
        issue_description = request.form['issue_description']
        status = request.form['status']
        assigned_to = request.form['assigned_to']

        cursor.execute("""
            UPDATE tickets
            SET ticket_no=?,
                store=?,
                asset_name=?,
                issue_category=?,
                priority=?,
                issue_description=?,
                status=?,
                assigned_to=?
            WHERE id=?
        """,
        (
            ticket_no,
            store,
            asset_name,
            issue_category,
            priority,
            issue_description,
            status,
            assigned_to,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM tickets WHERE id=?",
        (id,)
    )

    ticket = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_ticket.html',
        ticket=ticket
    )

@app.route('/add', methods=['GET', 'POST'])
def add_ticket():

    try:
        assets_data = requests.get(
            "http://127.0.0.1:5000/api/assets"
        ).json()

        assets = []

        for asset in assets_data:
            assets.append(asset["asset_name"])

    except:
        assets = []

    stores = [
        "1470091 Head Office",
        "1470001 Exhibition",
        "1470002 Sar",
        "1470003 Bab Al Bahrain",
        "1470005 Riffa",
        "1470006 Muharraq",
        "1470007 Seef 2",
        "1470008 Tubli",
        "1470010 Sakhir",
        "1470011 Juffair",
        "1470014 City Center",
        "1470015 King Fahad Causeway",
        "1470017 Ramli Mall",
        "1470018 Bahrain Defense Force",
        "1470019 Arad",
        "1470020 Isa Town",
        "1470021 Janabiya",
        "1470022 Oasis Mall",
        "1470023 Adliya",
        "1470024 Avenues",
        "1470025 Hidd Plaza",
        "1470026 Alsayah",
        "1470027 New Airport",
        "1470028 Askar",
        "1470029 Amwaj",
        "1470030 Juffair 2",
        "1470031 Diyar",
        "1470032 Seef Drive",
        "1470033 Bu Quwah",
        "1470034 Madinat Hamad",
        "1470035 Sitra Drive",
        "1470036 District Drive",
        "1470037 Riffa Views"
    ]

    issue_categories = [
        "Hardware",
        "Software",
        "Network",
        "POS",
        "Printer",
        "Kiosk",
        "Server",
        "CCTV",
        "Email",
        "Other"
    ]

    priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    technicians = [
        "Fadhel Ahmed",
        "Wilson John",
        "Muhammad Jaffer",
        "Ranjith",
        "Wulfran"
    ]

    if request.method == "POST":

        store = request.form["store"]
        asset_name = request.form["asset_name"]
        issue_category = request.form["issue_category"]
        priority = request.form["priority"]
        issue_description = request.form["issue_description"]
        status = request.form["status"]
        assigned_to = request.form["assigned_to"]

        conn = sqlite3.connect("helpdesk.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tickets")
        count = cursor.fetchone()[0] + 1

        ticket_no = f"TKT-{count:05d}"

        date_opened = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO tickets (
                ticket_no,
                store,
                asset_name,
                issue_category,
                priority,
                issue_description,
                status,
                date_opened,
                assigned_to
            )
            VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            ticket_no,
            store,
            asset_name,
            issue_category,
            priority,
            issue_description,
            status,
            date_opened,
            assigned_to
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template(
        'add_ticket.html',
        stores=stores,
        assets=assets,
        issue_categories=issue_categories,
        priorities=priorities,
        technicians=technicians
)
   
if __name__ == '__main__':
    app.run(debug=True, port=5001)