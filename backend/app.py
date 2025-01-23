from flask import Flask, render_template,request
import mysql.connector
app = Flask(__name__,template_folder='../templates',static_folder='../static')

@app.route('/')
def home():
    try:
        # MySQL Configuration
        db_config = {
            'host': 'localhost',
            'user': 'root',  # Your MySQL username
            'password': 'Hemanth@0925',  # Your MySQL password
            'database': 'theater_db'
        }
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Fetch show details
        cursor.execute("SELECT * FROM shows;")
        shows = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()
        return render_template("shows.html", shows=shows)
    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route('/shows')
def shows():
    theater_shows = [
        {"id": 1, "name": "Movie A", "date": "2025-01-25", "capacity": 10, "price": 15},
        {"id": 2, "name": "Movie B", "date": "2025-01-26", "capacity": 8, "price": 12},
        {"id": 3, "name": "Movie C", "date": "2025-01-27", "capacity": 2, "price": 20}
    ]
    return render_template("shows.html", shows = theater_shows)


@app.route("/book", methods=["POST"])
def book():
    show_id = request.form.get("show_id")
    db_config = {
        'host': 'localhost',
        'user': 'root',  # Your MySQL username
        'password': 'Hemanth@0925',  # Your MySQL password
        'database': 'theater_db'
    }
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Check available seats
        query = "SELECT * FROM shows WHERE id = %s"
        cursor.execute(query, (show_id,))
        show = cursor.fetchone()
        print(show)

        if show and show['CAPACITY'] > 0:
            # Reduce seats by 1
            update_query = "UPDATE shows SET capacity = capacity - 1 WHERE id = %s"
            cursor.execute(update_query, (show_id,))
            connection.commit()
            message = f"Successfully booked {show['SCREEN_NAME']}!"
        else:
            message = "Sorry, no seats available for this show."

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        message = f"Error: {err}"

    return render_template("booking_result.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
