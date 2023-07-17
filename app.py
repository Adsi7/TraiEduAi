# save this as app.py
import sqlite3
import random
from flask import Flask, render_template, redirect , url_for, g, session, request

app = Flask(__name__)





def getdb_tools():
    # Establish a connection to the "tooldb.db" database
    connection = sqlite3.connect("tooldb.db")
    # Set the row factory to sqlite3.Row
    # This allows fetching rows as dictionary-like objects
    connection.row_factory = sqlite3.Row
    return connection


def getdb_paper():
    # Establish a connection to the "paperdb.db" database
    connection2 = sqlite3.connect("paperdb.db")
    # Set the row factory to sqlite3.Row
    # This allows fetching rows as dictionary-like objects
    connection2.row_factory = sqlite3.Row
    return connection2

    
# Flask route for the root URL ("/")
@app.route("/")
def index():
    return render_template('index.html')


# Flask route for the root URL ("/imprint")
@app.route("/imprint")
def imprint():
    return render_template('imprint.html')


# Flask route for the root URL ("/TransferableSkills")
@app.route("/TransferableSkills")
def TransferableSkills():
    return render_template('TransferableSkills.html')


# Flask route for the root URL ("/about")
@app.route("/about")
def about():
    return render_template('about.html')


# Flask route for the "/tools" URL with the HTTP method "POST"
@app.route("/tools", methods=['POST'])
def tools():
    # Establish connection database and create cursor object to execute
    connection = getdb_tools()
    cursor = connection.cursor()
    # Retrieve value from POST request's form data
    datastring = request.form['skill']
    # Execute the SQL query and fetch all the results 
    datenabfrage = "SELECT * FROM Plain_tools_cd WHERE TransferableSkill='{}'".format(datastring)
    cursor.execute(datenabfrage)
    results = cursor.fetchall()
    # Render template, passing data to the template
    return render_template('tool.html', data=results)


# Flask route for the "/paper" URL with the HTTP method "POST"
@app.route("/paper",  methods=['POST'])
def paper():
    # Establish connection database and create cursor object to execute
    connection2= getdb_paper()
    cursor= connection2.cursor()
    # Retrieve value from POST request's form data
    datastring= request.form['skill']
    # Execute the SQL query and fetch all the results 
    datenabfrage= "SELECT * FROM Plain_paper_cd WHERE TransferableSkill='{}'".format(datastring)
    cursor.execute(datenabfrage)
    results= cursor.fetchall()
    # Render template, passing data to the template
    return render_template('paper.html', data=results) 


@app.route("/searchTool", methods=['POST'])
#function for searching tools
def searchTool():
    # Establish connection database and create cursor object to execute
    connection= getdb_tools()
    cursor= connection.cursor()
    # Retrieve value from POST request's form data
    dataSearch=request.form['skill'] 
    # Execute the SQL query and fetch all the results 
    datenabfrage= "SELECT * FROM Plain_tools_cd WHERE Name Like'{}'".format(dataSearch)
    cursor.execute(datenabfrage)
    results= cursor.fetchall()
    # Render template, passing data to the template
    return render_template('tool.html', data=results, type="search" , variable=dataSearch)


@app.route("/searchPaper", methods=['POST'])
#function for searching paper
def searchPaper():
    # Establish connection database and create cursor object to execute
    connection= getdb_paper()
    cursor= connection.cursor()
    # Retrieve value from POST request's form data
    dataSearch=request.form['skill'] 
    # Execute the SQL query and fetch all the results 
    datenabfrage= "SELECT * FROM Plain_paper_cd WHERE NameTool Like'{}'".format(dataSearch)
    cursor.execute(datenabfrage)
    results= cursor.fetchall()
    # Render template, passing data to the template
    return render_template('paper.html', data=results, type="search" , variable=dataSearch)


@app.route("/allTools", methods=['POST'])
#function for display all tools
def allTools():
    # Establish connection database and create cursor object to execute
    connection= getdb_tools()
    cursor= connection.cursor()
    # Execute the SQL query and fetch all the results 
    datenabfrage= "SELECT * FROM Plain_tools_cd"
    cursor.execute(datenabfrage)
    results= cursor.fetchall()
    # Render template, passing data to the template
    return render_template('tool.html', data=results,  variable="All Tools")


@app.route("/allPaper", methods=['POST'])
#function for displaying all papers
def allPaper():
    # Establish connection database and create cursor object to execute
    connection= getdb_paper()
    cursor= connection.cursor()
    # Execute the SQL query and fetch all the results 
    datenabfrage= "SELECT * FROM Plain_paper_cd"
    cursor.execute(datenabfrage)
    results= cursor.fetchall()
    # Render template, passing data to the template
    return render_template('paper.html', data=results,  variable="All Papers")




@app.route("/filterPaper", methods=['POST'])
#function for filtering paper
def filterPaper():
    # Establish connection database and create cursor object to execute
    connection = getdb_paper()
    cursor = connection.cursor()

    # Retrieve the list of selected subskills from the form request
    subskills_group = request.form.getlist('group')
    subskills_sub = request.form.getlist('sub')
    subskills = subskills_group + subskills_sub

    # Construct the placeholders for the SQL query
    placeholders_group = ' OR '.join(['FocusGroup LIKE ?'] * len(subskills_group))
    placeholders_sub = ' OR '.join(['SubSkill LIKE ?'] * len(subskills_sub))
    query = "SELECT * FROM Plain_paper_cd"

    # Append the WHERE conditions only if the lists are not empty
    if subskills_group and subskills_sub:
        query += f" WHERE ({placeholders_group}) AND ({placeholders_sub})"
    elif subskills_group:
        query += f" WHERE ({placeholders_group})"
    elif subskills_sub:
        query += f" WHERE ({placeholders_sub})"

    # Check if no subskills or focusgroupg options are selected
    if not subskills_group and not subskills_sub:
        return render_template('paper.html', data=[])

    parameters = tuple(f"%{subskill}%" for subskill in subskills)

     # Execute the SQL query and fetch all the results 
    cursor.execute(query, parameters)
    results = cursor.fetchall()

    # Render template, passing data to the template
    return render_template('paper.html', data=results ,variable="Filtered Papers")




@app.route("/filterTools", methods=['POST'])
#function for filtering tools
def filterTools():
    # Establish connection database and create cursor object to execute
    connection = getdb_tools()
    cursor = connection.cursor()

    # Retrieve the list of selected subskills from the form request
    subskills_group = request.form.getlist('group')
    subskills_sub = request.form.getlist('sub')
    subskills_price = request.form.getlist('price')
    subskills = subskills_group + subskills_sub

    # Construct the placeholders for the SQL query
    placeholders_group = ' OR '.join(['FocusGroup LIKE ?'] * len(subskills_group))
    placeholders_sub = ' OR '.join(['SubSkill LIKE ?'] * len(subskills_sub))
    placeholders_price = ' OR '.join(['Pricing LIKE ?'] * len(subskills_price))
    query = "SELECT * FROM Plain_tools_cd"

    # Append the WHERE conditions only if the lists are not empty
    if subskills_group and subskills_sub:
        query += f" WHERE ({placeholders_group}) AND ({placeholders_sub})"
    elif subskills_group:
        query += f" WHERE ({placeholders_group})"
    elif subskills_sub:
        query += f" WHERE ({placeholders_sub})"

    # Handle scenario where pricing is selected
    if subskills_price:
        if subskills_group or subskills_sub:
            query += f" AND ({placeholders_price})"
        else:
            query += f" WHERE ({placeholders_price})"
        parameters = tuple(f"%{subskill}%" for subskill in subskills) + tuple(subskills_price)
    else:
        parameters = tuple(f"%{subskill}%" for subskill in subskills)

    # Check if no subskills or pricing options are selected
    if not subskills_group and not subskills_sub and not subskills_price:
        return render_template('tool.html', data=[])

    # Execute the SQL query and fetch all the results 
    cursor.execute(query, parameters)
    results = cursor.fetchall()

    # Render template, passing data to the template
    return render_template('tool.html', data=results ,  variable="Filtered Tools")


if __name__ == "_app_":
    app.run(debug=True)

