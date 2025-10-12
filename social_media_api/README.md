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

## 👥 Follow System

### 🔹 Endpoints

#### Follow a User
- `POST /api/accounts/follow/<user_id>/`
- Requires authentication
- Follows the user with the given ID

#### Unfollow a User
- `POST /api/accounts/unfollow/<user_id>/`
- Requires authentication
- Unfollows the user with the given ID

### 🔹 Feed
- `GET /api/feed/`
- Requires authentication
- Returns posts from users the current user follows, ordered by most recent

### 🔹 Sample Response (Feed)
```json
[
  {
    "id": 5,
    "author": "jane_doe",
    "title": "Weekend Vibes",
    "content": "Loving the beach today!",
    "created_at": "2025-10-12T18:00:00Z",
    "updated_at": "2025-10-12T18:00:00Z"
  },
  ...
]