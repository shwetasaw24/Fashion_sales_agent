# MongoDB Cart Persistence

This document explains what was implemented for cart persistence using MongoDB, how to enable it, verify it, and extend it for production.

## Summary of Changes
- **New**: `db/mongo_client.py` — Mongo client wrapper (connects to `MONGO_URI` / `MONGO_DB`) and exposes `get_collection()`.
- **Updated**: `services/cart_service.py` — loads carts from Mongo and upserts on cart creation, add, remove, and clear operations. Logs added to indicate persistence.
- **Updated**: `requirements.txt` — added `pymongo` dependency.
- **Updated**: `frontend/src/components/ChatArea.jsx` — persists `customerId` in localStorage and fetches cart from backend on mount; updates cart from the backend response on add operations.
- **Updated**: `.env.example` and `QUICK_START.md` — instructions for enabling MongoDB locally.

## Prerequisites
- Docker Desktop or a running MongoDB server
- Python 3.10+ and a virtualenv (the repo includes a venv at `backend/.venv`) or your preferred environment manager
- Node.js and npm for running the frontend

## Local Setup (Development)

1. Start a local MongoDB container (example using `mongo:6.0`):

```powershell
docker run -d -p 27017:27017 --name fashion_mongo -v mongodb_data:/data/db mongo:6.0
```

2. Configure environment variables for backend (PowerShell):

```powershell
cd backend
set MONGO_URI=mongodb://localhost:27017
set MONGO_DB=fashion_agent_db
```

3. Install backend dependencies and run the backend:

```powershell
cd backend
pip install -r requirements.txt
set USE_FAKE_REDIS=true
uvicorn app:app --reload --port 8000 --log-level debug
```

4. Start the frontend (new terminal):

```powershell
cd frontend
npm install
npm run dev
```

5. Open the frontend at `http://localhost:5173` and use the chat to request recommendations and add a product to cart.

## Verifying Persistence

- The frontend keeps a `customer_id` in localStorage under `fs_customer_id` — this ID is used for add-to-cart requests.
- Check the backend logs (running `uvicorn`) for lines like:
  - `Persisted initial cart to Mongo for customer_XXXX (items=0)`
  - `Persisted new cart item to Mongo for customer_XXXX (items=1)`

- Inspect the Mongo collection directly with `mongosh` (from host or via Docker exec):

```powershell
docker exec -it fashion_mongo mongosh --eval "use fashion_agent_db; db.carts.find({customer_id:'customer_XXXX'}).pretty()"
```

Replace `customer_XXXX` with the value in your localStorage or copy it from network requests in the browser devtools.

## API Details
- POST `/api/cart/add` — Adds items to the cart. Payload:
  - `customer_id`: string
  - `sku`: product SKU
  - `quantity`: number (default 1)
  - `size`: size string (default `M`)
  - `color`: color string (optional)

- GET `/api/cart/{customer_id}` — Returns cart summary including `items` and `totals`.

## Notes
- The backend will gracefully fallback to an in-memory cart when `pymongo` is not installed or Mongo is unavailable. When `pymongo` is not installed you will see: `pymongo not installed; MongoDB features disabled` in server stderr.
- The `backend/db/mongo_client.py` wrapper returns `None` for `client` and `db` when `pymongo` isn't available. `cart_service` checks `MONGO_COLLECTION` before performing DB operations.

## Production Considerations

- Use a running MongoDB cluster or managed service (Atlas) and set `MONGO_URI` accordingly. Protect credentials: do not commit them to the repository.
- Consider adding indexes on `customer_id` in the `carts` collection for fast reads:
  ```js
  db.carts.createIndex({ customer_id: 1 })
  ```
- If you require higher performance use Redis for frequently updated cart data and periodically persist to Mongo, or use a Redis + Mongo combination.
- Secure your database with authentication, network policies, and backups.

## Troubleshooting

- If cart add fails in the frontend: check `Network` tab and verify the payload includes a valid `customer_id`.
- If backend logs show `MongoDB upsert failed` or connection errors, verify `MONGO_URI` and the container status:
  - `docker ps` to ensure container is running
  - `docker logs -f fashion_mongo`

## Suggested Tests

- Add an automated test in `backend/test_cart_mongo.py` that runs only when a Mongo test URI is available, which:
  - Creates a unique `customer_id`
  - Calls add/remove endpoints
  - Asserts that the `carts` collection has the correct document

## Files Updated
- backend/db/mongo_client.py (new)
- backend/services/cart_service.py (modified)
- backend/requirements.txt (modified)
- backend/.env.example (modified)
- backend/MONGO_PERSISTENCE.md (this file)
- frontend/src/components/ChatArea.jsx (modified)

If you'd like, I can also add a short test and example script to demonstrate the full flow (frontend → backend → Mongo) in CI-mode or locally. Would you like that?
