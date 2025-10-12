## 📘 Posts & Comments API

### 🔹 Endpoints

#### Posts
- `GET /api/posts/` — List posts (searchable by title/content)
- `POST /api/posts/` — Create post (auth required)
- `PUT /api/posts/{id}/` — Update post (owner only)
- `DELETE /api/posts/{id}/` — Delete post (owner only)

#### Comments
- `GET /api/comments/` — List comments
- `POST /api/comments/` — Create comment (auth required)
- `PUT /api/comments/{id}/` — Update comment (owner only)
- `DELETE /api/comments/{id}/` — Delete comment (owner only)

### 🔹 Sample Request (Create Post)
```http
POST /api/posts/
Authorization: Token <your_token>
Content-Type: application/json

{
  "title": "My First Post",
  "content": "Hello world!"
}