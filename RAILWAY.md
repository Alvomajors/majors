# Railway deployment configuration for Majors API

## Deploy on Railway

1. Push this repository to GitHub.
2. Go to https://railway.app and create a new project.
3. Choose "Deploy from GitHub repo".
4. Select this repository.
5. Set the service to use the root folder.
6. Add these environment variables in the Railway dashboard:

```env
APP_NAME=Majors API
APP_VERSION=1.0.0
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/majors?retryWrites=true&w=majority
DATABASE_NAME=majors
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/<your-project-id>
```

## Optional: use your local Dockerfile
Railway supports Docker-based deployments automatically if a Dockerfile is present.

## Dockerfile already included
This repo already contains a Dockerfile that runs the FastAPI app with Uvicorn.

## Important notes
- Use MongoDB Atlas for production database.
- Use Infura or Alchemy for Ethereum RPC instead of a local Geth node.
- Keep all secrets in Railway environment variables, never in code.
- Do not commit private keys or production wallet keys.

## Health check
Railway can use this endpoint for health checks:

```text
/health
```

## Start command
Railway will use the Dockerfile automatically. If needed, set start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
