# Microblogging-Social-Network-API
A minimal Microblogging Social Network API written in (Python/Django).

## Getting Started

1. Prerequisites:
    * Docker and docker-compose installed.
2. Cloning the Repository:
    * Clone this repository to your local machine: ```git clone https://github.com/0xOrigin/Microblogging-Social-Network-API.git```
3. Setting up Environment Variables:
    * Create a .env and .env.backend.dev files in the project's root directory.
    * Use the .env-templates to fill in the required values.
4. Building the Containers:
    * In your terminal, navigate to the project's root directory and run: ```sudo docker-compose up -d --build && sudo docker-compose -f docker-compose-nginx.yml up -d --build```
5. Running the Application:
    * To start the application, run: ```sudo docker-compose up -d && sudo docker-compose -f docker-compose-nginx.yml up -d```

## Accessing the Application

- The application should now be accessible through your web browser at the specified URL (often http://localhost:8080/ or similar).

## Additional Information
  * API Reference: [Postman Collection]()
  * Project Assumptions & Notes: [Project Assumptions]()
  * .env file example: [.env file]()
  * .env.backend.dev file example: [.env.backend.dev file]()
