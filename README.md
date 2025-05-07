# Smart Voting & Polling Platform

This project is a secure, role-based web application for managing and participating in polls and elections. It is built with Streamlit (Python) and MySQL.

## Features

- User registration and login (student and admin roles)
- Role-based access: admins can create, edit, and delete polls and options; students can vote in active polls
- One vote per user per poll, enforced by the database
- Live poll results with graphical charts
- Cascading deletes for poll integrity
- Passwords are securely hashed

## Project Structure

voting_polling_system/
  .streamlit/
    config.toml
    secrets.toml
  assets/
    fonts/
  main.py
  db.py
  pages/
    1_Home.py
    2_Poll_Detail.py
    3_Admin_Dashboard.py
    4_Results.py
  requirements.txt
  README.md

## Setup Instructions

1. Clone the repository and enter the folder:
   git clone 
   cd voting_polling_system

2. Install dependencies:
   pip install -r requirements.txt

3. Configure the database:
   - Create a MySQL database (for example, voting_polling_system).
   - Run the provided SQL scripts to create the required tables.

4. Configure Streamlit secrets:
   - Edit .streamlit/secrets.toml with your MySQL credentials:
     [mysql]
     host = "localhost"
     port = 3306
     database = "voting_polling_system"
     user = "your_mysql_user"
     password = "your_mysql_password"

5. Run the application:
   streamlit run main.py
   Access the app at http://localhost:8501

## Usage

Register as a student or admin. Admins can manage polls through the Admin Dashboard. Students can vote in active polls. Results are available as bar charts.

## Technologies

Python 3  
Streamlit  
MySQL  
pandas

