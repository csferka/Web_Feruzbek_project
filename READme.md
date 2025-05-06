# 🎬 Movie Data API with Flask & PostgreSQL

A RESTful API built using Flask and PostgreSQL to manage movie data. It allows clients to fetch, add, and delete movie entries. CORS is enabled for smooth frontend integration.

---

## 🚀 Features

- ✅ Fetch all movies
- ➕ Add a new movie
- ❌ Delete a movie by ID or title
- 🔁 CORS support for `/api/*` endpoints
- 🔍 Test route to check API status

---

## 📁 Project Structure



---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie-data-api.git
cd movie-data-api

Set Up Virtual Environment & Install Dependencies
python3 -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate


Configure Database
Edit the db_connect() function in app.py:

conn = psycopg2.connect(
    host="your-db-host",
    database="Finalproject",
    user="postgres",
    password="your_password_here",
    port="5432"
)

Ensure your PostgreSQL DB contains the following table:

CREATE TABLE tbl_feruzbek_movie_data (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    distributor VARCHAR(255),
    release_date DATE,
    budget_millions NUMERIC,
    opening_weekend NUMERIC,
    north_america NUMERIC,
    other_territories NUMERIC,
    worldwide NUMERIC
);


🌐 Frontend Deployment on Amazon S3

🔹 Steps to Deploy index.html on S3:
Go to S3 Console
Create a new bucket (disable “Block all public access”).
Upload index.html to the bucket.
Go to Properties → Static website hosting and enable it.
Set:
Index document: index.html
Copy the Static Website URL provided.
Make sure your Flask API (app.py) CORS policy allows requests from this S3 domain.


🖥️ Backend Deployment on AWS EC2

🔹 Launch EC2 Instance:
Launch an EC2 instance (Ubuntu is recommended).
SSH into the instance:
ssh -i your-key.pem ubuntu@your-ec2-public-ip
🔹 Install Python and Dependencies:
sudo apt update
sudo apt install python3-pip python3-venv
git clone https://github.com/your-username/movie-data-api.git
cd movie-data-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🔹 Run Flask App:
python app.py
Optional: Use gunicorn or tmux/screen to keep the app running in background.

🔐 Security & Networking

In EC2 Security Groups, allow inbound traffic for:
Port 5000 (Flask)
Or configure Nginx/Apache and allow HTTP (port 80)
Make sure PostgreSQL security group allows inbound from the EC2 IP or VPC
