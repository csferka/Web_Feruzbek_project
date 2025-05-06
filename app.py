import os
import psycopg2
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
# More explicit CORS configuration
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Database connection function
def db_connect():
    conn = psycopg2.connect(
        host="feruzbek-db-final.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com",
        database="Finalproject",
        user="postgres",
        password="your_password_here",  # Replace with your actual password
        port="5432"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"status": "API is working"}), 200

@app.route('/api/movies', methods=['GET'])
def get_movies():
    try:
        conn = db_connect()
        cur = conn.cursor()

        # First check if id column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'tbl_feruzbek_movie_data' 
            AND column_name = 'id';
        """)

        id_column_exists = cur.fetchone() is not None

        if id_column_exists:
            cur.execute("SELECT * FROM tbl_feruzbek_movie_data")
        else:
            # If no ID column, use title as a unique identifier
            cur.execute("SELECT title, distributor, release_date, budget_millions, opening_weekend, " +
                       "north_america, other_territories, worldwide FROM tbl_feruzbek_movie_data")

        rows = cur.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cur.description]

        # Convert to list of dictionaries
        movies = []
        for row in rows:
            movie = {}
            for i, col in enumerate(column_names):
                movie[col] = row[i]

            # If no ID column exists, use title as ID
            if not id_column_exists and 'title' in movie:
                movie['id'] = movie['title']  # Use title as the ID

            movies.append(movie)

        cur.close()
        conn.close()

        return jsonify({"movies": movies}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/movies', methods=['POST'])
def add_movie():
    try:
        data = request.get_json()

        # Extract movie data
        title = data.get('title')
        distributor = data.get('distributor')
        release_date = data.get('release_date')
        budget_millions = data.get('budget_millions')
        opening_weekend = data.get('opening_weekend')
        north_america = data.get('north_america')
        other_territories = data.get('other_territories')
        worldwide = data.get('worldwide')

        # Connect to the database
        conn = db_connect()
        cur = conn.cursor()

        # Insert new movie
        cur.execute("""
            INSERT INTO tbl_feruzbek_movie_data 
            (title, distributor, release_date, budget_millions, opening_weekend, north_america, other_territories, worldwide)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, distributor, release_date, budget_millions, opening_weekend, north_america, other_territories, worldwide))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Movie added successfully"}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to add movie"}), 500

@app.route('/api/movies/<path:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        # Connect to the database
        conn = db_connect()
        cur = conn.cursor()

        print(f"Attempting to delete movie with identifier: {movie_id}")

        # First check if id column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'tbl_feruzbek_movie_data' 
            AND column_name = 'id';
        """)

        id_column_exists = cur.fetchone() is not None

        if id_column_exists and movie_id.isdigit():
            # Try to delete by numeric ID
            print(f"Deleting by ID: {movie_id}")
            cur.execute("DELETE FROM tbl_feruzbek_movie_data WHERE id = %s", (int(movie_id),))
        else:
            # Delete by title
            print(f"Deleting by title: {movie_id}")
            cur.execute("DELETE FROM tbl_feruzbek_movie_data WHERE title = %s", (movie_id,))

        # Check if any row was affected
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            print(f"No movie found with identifier: {movie_id}")
            return jsonify({"error": "Movie not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        print(f"Successfully deleted movie with identifier: {movie_id}")
        return jsonify({"message": "Movie deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting movie: {str(e)}")
        return jsonify({"error": f"Failed to delete movie: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
