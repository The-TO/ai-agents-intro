# Topic HTTP status codes

### Simple Explanation

HTTP status codes are a way for a server to communicate with a client (usually a web browser) about the outcome of a request. When you send a request to a server, the server responds with a status code that indicates whether the request was successful or not. HTTP status codes are three-digit numbers that are divided into five categories: informational, successful, redirect, client error, and server error.

HTTP status codes are used to provide feedback to the client about the outcome of the request. For example, if you request a webpage that doesn't exist, the server might respond with a 404 status code to indicate that the page was not found. On the other hand, if the request is successful, the server might respond with a 200 status code to indicate that the request was received and understood.

Understanding HTTP status codes is important for any web developer or programmer, as it allows you to write more robust and error-free code. By checking the status code of a response, you can determine whether the request was successful or not, and take the appropriate action accordingly.

### Key Concepts

* **HTTP Status Code**: a three-digit number that indicates the outcome of a request.
* **HTTP Method**: the action being requested, such as GET, POST, PUT, DELETE, etc.
* **Response Status Code**: the code returned by the server in response to a request.
* **Server Error**: a status code indicating that the server encountered an error while processing the request.
* **Client Error**: a status code indicating that the client (e.g. web browser) encountered an error while making the request.

### Example

```bash
GET / HTTP/1.1
Host: example.com
Accept: text/html

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 1234
```

This code example shows a GET request to the root URL of the `example.com` website, and a response with a 200 status code indicating that the request was successful.
