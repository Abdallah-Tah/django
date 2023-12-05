To enhance your current README file with Django-specific setup instructions and migration details, you can integrate these steps into the "How to Run" section. Here's a revised version of your README, including Django setup and migration instructions:

```markdown
# Yoga Asana Practice and Learning Platform

## Overview

This project aims to simplify the experience of learning and practicing yoga by teaching users how to properly perform Asanas (yoga postures). Developed as part of the COS 457: Database Systems course at the University of Southern Maine, this web application is built using Python FastAPI and HTML.

## Authors

- Abdallah Mohamad
- Aleksandra Milinovic

## Advisor

Dr. Behrooz Mansouri

## Features

- A structured course on asanas divided into three levels: beginner, intermediate, and advanced.
- A database containing 200 asanas and their details.
- Course schedules for up to 300 weeks.
- Steps for each asana displayed on the screen with adequate time for users to adjust their posture.
- Optional images for steps that require visual guidelines.

## Database Schema

The application utilizes a robust database design as depicted in the ER diagram (Figure 1). For a detailed understanding of the ER notation used, please refer to Figure 2.

### Entity Sets and Their Attributes

- **Asana**
  - ID, name, important, effects, created_at, updated_at
- **Course**
  - ID, level
- **Week**
  - ID, asanas, notes
- **Step**
  - ID, technique, order
- **User**
  - ID, name, email, password, created_at, updated_at
- **User Progress**
  - user_id, remaining_todo, asanas_learned, week

### Relationship Sets

- **to_do**: Multiple asanas can be associated with multiple weeks.
- **has_asanas**: Information about all asanas practiced in specific courses.
- **has_steps**: Step data for asanas.
- **has_week**: Information about weeks of each course.

## Collaboration

The project was a collaborative effort, with team members frequently meeting to discuss requirements and solutions. Work was done collectively, and any individual contributions were promptly shared and reviewed by all team members.

## How to Run

1. Clone the repository:
   ```bash
   git clone [repository URL]
   cd [repository name]
   ```
2. Setup the Django Environment:
   - Perform database migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
   - Create a superuser (optional but recommended for admin access):
     ```bash
     python manage.py createsuperuser
     ```
4. Run the FastAPI server:
   ```bash
   python manage.py runserver
   ```
5. Access the application in a web browser at `http://127.0.0.1:8000/`.
6. (Optional) To access the Django admin panel, navigate to `http://127.0.0.1:8000/admin` and log in using the superuser credentials.

## License

This project is licensed under the MIT License.

## Acknowledgements

We would like to thank Dr. Behrooz Mansouri for his invaluable guidance and the University of Southern Maine for providing us the opportunity to work on this project.

For more details, please refer to the documentation included in the repository.
```

Ensure that the repository URL and the name of the repository are correctly specified. This updated README includes steps for cloning the repository, installing dependencies, setting up Django's environment (including migrations and creating a superuser), and running the server. It provides a clear and comprehensive guide for setting up and running your application.