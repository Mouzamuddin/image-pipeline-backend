# image-pipeline-backend
This backend, built with FastAPI, allows users to upload images (original and mask) and store metadata in MongoDB. It also serves images statically.

Features
Image Upload: Upload an original and mask image with an optional description.
Metadata Storage: Stores metadata in MongoDB.
Static Hosting: Serves uploaded images.
CORS Support: Allows requests from a React frontend hosted at https://imagepipelinemask.netlify.app.
Requirements
Python 3.7+
MongoDB
Python dependencies listed in requirements.txt

Install dependencies:
run
pip install -r requirements.txt

Configure environment variables: Create a .env file with:

Run the app:
uvicorn main:app --reload

Access the API at http://localhost:8000.

API Endpoints
GET /
Returns a welcome message.

POST /upload/
Upload images and store metadata.

Form Data: original_image, mask_image, description
Response: URLs for uploaded images and metadata.
GET /images/{image_id}
Fetch image metadata by ID

Error Handling
Returns a 500 status code with an error message if something goes wrong.
