![banner](https://res.cloudinary.com/dloadb2bx/image/upload/v1706370132/apilibrary_jm3cox.png)
# API Digital Library

## Technologies
![enter image description here](https://camo.githubusercontent.com/0562f16a4ae7e35dae6087bf8b7805fb7e664a9e7e20ae6d163d94e56b94f32d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3336373041303f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666664643534) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![enter image description here](https://camo.githubusercontent.com/63d721e5f8294c62d26a43f71778ffcccf4b23b83234050aa6ead289c3f0e987/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6d7973716c2d2532333030303030662e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d6d7973716c266c6f676f436f6c6f723d7768697465) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Overview

The API Digital Library is a Python-based web application that leverages technologies such as Python 3, SQL Alchemy, Flask, and MySQL to provide a platform for users to manage their book collections. This project serves as a practical exercise in developing a robust API, focusing on fundamental principles and best practices.

## Features

-   **User Authentication:** Users can create accounts, log in, and manage their bookshelves.
-   **Book Management:** Users can add, view, and remove books from their personal bookshelves.
-   **Admin Privileges:** Only users with admin access have the authority to create, update, and delete authors and books.
-   **Database Integration:** The application utilizes SQL Alchemy to interact with a relational database, enhancing data storage and retrieval capabilities.
-   **Dockerization:** The project is containerized using Docker, facilitating easy deployment and scalability.

## Main Objectives

The primary objectives of the API Digital Library project are:

1.  **Skill Development:** Gain practical experience in developing APIs using Python and related technologies.
2.  **Database Interaction:** Learn how to work with a relational database (MySQL) and utilize SQL Alchemy for efficient data management.
3.  **User Authentication:** Implement user authentication mechanisms to secure account creation and access to specific features.
4.  **Testing Practices:** Achieve comprehensive test coverage using the Coverage library and Pytest, ensuring the reliability of the application.

## Usage

### Setup

1.  Clone the repository to your local machine:
    
    bashCopy code
    
    `git clone https://github.com/your-username/api-digital-library.git` 
    
2.  Navigate to the project directory:
    
    bashCopy code
    
    `cd api-digital-library` 
    
3.  Install the required dependencies:
    
    bashCopy code
    
    `pip install -r requirements.txt` 
    

### Running the Application

1.  Build and run the Docker container:
    
    bashCopy code
    
    `docker-compose up -d` 
    
2.  Access the application at http://localhost:5000.
    

### Testing

1.  Run the test suite:
    
    bashCopy code
    
    `coverage run -m pytest` 
    
2.  View the test coverage report:
    
    bashCopy code
    
    `coverage report` 
    

## Notes

-   Ensure that you have Docker and Python 3 installed on your machine before running the application.
-   For admin privileges, customize the user roles and access controls in the application code.
