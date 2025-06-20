Uzbekistan Fashion Market Backend
A Flask-based API for managing shops, users, and products, powered by MongoDB Atlas and deployed on Vercel.
Setup

Clone Repository:
git clone <repository-url>
cd uzbekistan-fashion-market-backend

Install Dependencies:
pip install -r requirements.txt

Set Environment Variables:Create a .env file for local testing:
MONGODB_URI=mongodb+srv://akb:123@cluster0.xs2d6gt.mongodb.net/uzbekistan_fashion_market?retryWrites=true&w=majority

For Vercel, add MONGODB_URI in Settings > Environment Variables.

Run Locally:
python api/index.py

Deploy to Vercel:
vercel --prod

API Endpoints

Users:

POST /api/users: Register a new user.curl -X POST https://ufm-gilt.vercel.app/api/users \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "securepass"}'

Response: {"\_id": "<uid>", "username": "testuser", "email": "test@example.com"} (201)
GET /api/users: Retrieve all users.curl https://ufm-gilt.vercel.app/api/users

Shops:

POST /api/shops: Create a new shop.curl -X POST https://ufm-gilt.vercel.app/api/shops \
-H "Content-Type: application/json" \
-d '{"name": "Test Shop", "owner": "<uid>", "description": "A test shop", "location": "Tashkent", "categories": ["Fashion"]}'

Response: {"\_id": "<shop_id>"} (201)
GET /api/shops: Retrieve all shops.curl https://ufm-gilt.vercel.app/api/shops

Products:

POST /api/products: Create a new product.curl -X POST https://ufm-gilt.vercel.app/api/products \
-H "Content-Type: application/json" \
-d '{"shopId": "<shop_id>", "name": "T-Shirt", "description": "Cotton T-Shirt", "price": 19.99, "stock": 100}'

Response: {"\_id": "<product_id>"} (201)
GET /api/products: Retrieve all products.curl https://ufm-gilt.vercel.app/api/products

MongoDB Schemas

users:
{
"\_id": "string",
"username": "string",
"email": "string",
"password": "string",
"role": "string",
"createdAt": "ISODate",
"updatedAt": "ISODate"
}

shops:
{
"\_id": "string",
"name": "string",
"owner": "string",
"description": "string",
"logo": "string",
"location": "string",
"categories": ["string"],
"isVerified": boolean,
"createdAt": "ISODate",
"updatedAt": "ISODate"
}

products:
{
"\_id": "string",
"shopId": "string",
"name": "string",
"description": "string",
"price": "number",
"stock": "number",
"categories": ["string"],
"createdAt": "ISODate",
"updatedAt": "ISODate"
}

Troubleshooting

MongoDB Connection:
Ensure IP is allowlisted in MongoDB Atlas.
Verify MONGODB_URI in Vercel settings.

Favicon Error:
Fixed by combining favicon routes in index.py.

Logs:vercel logs ufm-gilt.vercel.app
