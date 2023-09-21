# Test assingment (Link Recorder)
Task: Implement a web application for simple tracking of visited links. 
- The application provides a JSON API over HTTP. 
- The application offers two HTTP resources. The first resource is used to send an array of links in a POST request. The time of their visit is considered the time of receipt by the service.
The second resource is used to retrieve a list of unique domains visited within a specified time interval using a GET request. 
- The field "status" of the response is used to convey any errors that occur during request processing.
- For data storage, the service should use the Redis database.
- The code should be covered by tests.
- Instructions for running the application should be located in the README file.

## Prerequisites
Before you begin, make sure you have the following:
- Docker installed on your system.
## Setup
1. Clone this repository using following comand:
```sh
https://github.com/Frostibums/funbox_test_task.git
```
2. Navigate to the project directory:
```sh
cd funbox_test_task
```
3. Change ***YOUR_APP_SECRET_KEY_HERE*** with your actual app secret key in **.env** file
4. Build the Docker image and run container:
```sh
docker-compose up --build
```
The Link Recorder API will be accessible at **http://localhost:8000** in your web browser.

## API endpoints
### POST /visited_links
This endpoint allows you to record visited links. The timestamp of each link's visit is automatically set to the time of the request.   

**Example Request**
```http
POST /visited_links
```
- Method: POST
- Body:
```json
{
    "links": [
        "https://ya.ru/",
        "https://ya.ru/?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/how-do-i-exit-vim"
    ]
}
```
  
**Example Response**
- Status Code: 200 OK
- Body:
```json
{
    "status": "ok"
}
```

<br>

### GET /visited_domains
This endpoint allows you to retrieve unique domains visited within a specified time interval.

**Example Request**
```http
GET /visited_domains?from=1545221231&to=1545217638
```
- from (optional): The timestamp in seconds from which to start the interval.
- to (optional): The timestamp in seconds until which to end the interval. Defaults to the current time if not provided.

**Example Response**
- Status Code: 200 OK
- Body:
```json
{
    "domains": [
        "ya.ru",
        "funbox.ru",
        "stackoverflow.com"
    ],
    "status": "ok"
}
```

## Testing
You can run tests for the application using Pytest. Run the following command:
```sh
docker exec -it link_recorder pytest
```
