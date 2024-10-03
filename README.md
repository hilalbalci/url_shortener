# URL Shortener

This project provides a RESTful API to shorten long URLs and redirect users to the original URL when the shortened version is accessed. It includes features such as account management, rate limiting (daily URL shortening limit), Redis caching, and analytics tracking.

## Purpose

The primary goal of this project is to create a URL shortening service where users can:
- Create accounts
- Shorten URLs with a daily limit
- Retrieve and use shortened URLs via API
- Get analytics on the shortened URLs

Each account comes with an `API_KEY` that is required for authenticated requests.

## Key Features

- **Account System**: Each account has a unique `API_KEY` for authentication.
- **Daily Limit**: Accounts have a daily limit on how many URLs they can shorten.
- **URL Shortening**: Convert long URLs into shorter, unique identifiers.
- **URL Redirection**: Redirect users to the original URL when the shortened URL is visited.
- **Redis Caching**: Cached shortened URLs for faster access.
- **Analytics**: Tracks clicks on shortened URLs and provides usage statistics.

## API Endpoints

### 1. Create Account

- **URL**: `/account`
- **Method**: `POST`
- **Description**: Creates a new account with a unique API key and a daily URL shortening limit.
  
#### Request Body:
```json
{
  "name": "Account Name",
  "daily_limit": 50
}
```
#### Returns:
```json
{
  "id": 1,
  "api_key": "your-api-key-here",
  "daily_limit": 50,
  "name":  "Account Name"
}
```


You can use this api-key in the header to provide authentication for the shortening url.


### 2. Update Account
- **URL**: `/account/<string:account_id>`
- **Method**: `PUT`
- **Description**: Updates the Account Name and Daily Limit.
#### Request Body:
```json
{
  "name": "Account Name",
  "daily_limit": 10
}
```
#### Returns:
```json
{
  "id": 1,
  "api_key": "your-api-key-here",
  "daily_limit": 10,
  "name":  "Account Name"
}
```

### 3. Get Account
- **URL**: `/account/<string:account_id>`
- **Method**: `GET`
- **Description**: Returns the corresponding account information.
#### Returns:
```json
{
  "id": 1,
  "api_key": "your-api-key-here",
  "daily_limit": 10,
  "name":  "Account Name"
}
```

### 4. Shorten Url
- **URL**: `/shorten_url`
- **Method**: `POST`
- **Description**: Creates a new shortened url or returns the existing shortened url for the given account and url.
#### Request Body:
```json
{
  "url": "https://www.google.com",
}
```
- **Headers**: {"api_key":"your-api-key-here"}

#### Returns:
```json
{
  "short_url": "short_url" 
}
```
### 5. Redirect

- **URL**: `/<short_url>`
- **Method**: `GET`
- **Description**: Redirects to the corresponding url.
- **Headers**: {"api_key":"your-api-key-here"}
#### Returns: Redirects to the original url

### 6. Analytics

- **URL**: `/analytics`
- **Method**: `GET`
- **Description**: Returns the analytics for the given account
- **Headers**: {"api_key":"your-api-key-here"}

#### Returns:
```json

[
    {
        "click_count": 3,
        "created_at": "2024-10-03T18:21:47.053852",
        "original_url": "https://www.google.com",
        "short_url": "SoZ2m5DJE9"
    },
    {
        "click_count": 1,
        "created_at": "2024-10-03T18:22:20.347076",
        "original_url": "https://www.google.com/dasdasdas",
        "short_url": "z3JzSKqwy0"
    },
    {
        "click_count": 2,
        "created_at": "2024-10-03T18:22:48.410892",
        "original_url": "https://www.facebook.com",
        "short_url": "UfmkzrOKW3"
    }
]
```
   
