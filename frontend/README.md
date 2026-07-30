# Dinero frontend

Dinero is the React client for the bank application. It includes secure registration and login, protected routes, checking and savings account creation, deposits, withdrawals, live balances, transaction history, and a responsive dashboard.

## Backend requirement

Run this frontend with the repository's `agent/rest-api-jwt-auth` backend. The unauthenticated API on `main` does not provide the `/auth/*` endpoints used by this client.

## Run locally

1. Start MongoDB/Atlas through the backend environment configuration.
2. Start the JWT API from the repository root:

   ```bash
   git switch agent/rest-api-jwt-auth
   source .venv/bin/activate
   uvicorn BankAPI:app --reload
   ```

3. In another terminal, start the frontend branch:

   ```bash
   cd frontend
   cp .env.example .env.local
   npm ci
   npm run dev
   ```

4. Open `http://localhost:5173`, register a new profile, open an account, and test deposits and withdrawals. Each action should appear immediately in the dashboard and in MongoDB Atlas.

The default API address is `http://127.0.0.1:8000`. Change `VITE_API_URL` in `.env.local` only if the API runs elsewhere.

## Verification

```bash
npm run lint
npm run build
```
