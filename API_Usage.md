## Base URL
http://localhost:8000/api/books/



## Endpoints

### 1. Submit Recommendation
- **Endpoint:** `/recommendations/`
- **Method:** `POST`
- **Description:** Submit a new book recommendation.
- **Request Body:**
  
  {
    "title": "string",
    "authors": "string",
    "categories": "string",
    "rating": "float",
    "publication_date": "string (YYYY-MM-DD)"
  }



Response (200 OK):

{
  "status": "ok",
  "data": {
    "id": "integer",
    "title": "string",
    "authors": "string",
    "categories": "string",
    "rating": "float",
    "publication_date": "string (YYYY-MM-DD)"
  }
}


Response (400 Bad Request):

{
  "status": "error",
  "error_code": 400,
  "error_message": "string"
}




### 2. List Recommendations
Endpoint: /recommendations/list/
Method: GET
Description: List book recommendations with filters.
Query Parameters:
title (optional)
authors (optional)
categories (optional)
min_rating (optional)
max_rating (optional)
start_date (optional)
end_date (optional)
Response (200 OK):

{
  "status": "ok",
  "data": [
    {
      "id": "integer",
      "title": "string",
      "authors": "string",
      "categories": "string",
      "rating": "float",
      "publication_date": "string (YYYY-MM-DD)"
    }
  ]
}

Response (400 Bad Request):

{
  "status": "error",
  "error_code": 400,
  "error_message": "string"
}





### 3. Manage User Interactions
Endpoint: /user-interactions/
Method: POST
Description: Create/update user interactions with book recommendations.
Request Body:

{
  "book": "integer",
  "liked": "boolean",
  "comment": "string"
}
Response (200 OK):

{
  "status": "ok",
  "data": {
    "message": "Interaction recorded successfully."
  }
}
Response (400 Bad Request):

{
  "status": "error",
  "error_code": 400,
  "error_message": "string"
}
Response (404 Not Found):

{
  "status": "error",
  "error_code": 404,
  "error_message": "string"
}




4. Search Books
Endpoint: /search/
Method: GET
Description: Search for books using keywords, authors, or categories from Google Books API
Query Parameters:
q (optional)
authors (optional)
category (optional)
Response (200 OK):

{
  "status": "ok",
  "data": [
    {
      "id": "string",
      "title": "string",
      "authors": "string",
      "description": "string",
      "cover_image": "string (URL)",
      "averageRating": "float",
      "ratingsCount": "integer",
      "categories": "string"
    }
  ]
}
Response (400 Bad Request):

{
  "status": "error",
  "error_code": 400,
  "error_message": "At least one search parameter ('q', 'authors', 'category') is required."
}
Response (500 Internal Server Error):

{
  "status": "error",
  "error_code": 500,
  "error_message": "string"
}




## Notes
- Use tools like Swagger or Postman for interactive testing.
- Ensure all requests are formatted correctly and include required parameters.







