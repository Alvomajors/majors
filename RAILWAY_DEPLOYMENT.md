# Railway Deployment Guide for Majors API

## Quick Start

This guide walks you through deploying the Majors API to Railway with MongoDB Atlas and Infura/Alchemy.

## Prerequisites

- GitHub account with this repo pushed
- Railway account (https://railway.app)
- MongoDB Atlas account (https://www.mongodb.com/cloud/atlas)
- Infura or Alchemy account for Ethereum RPC

## Step 1: Set up MongoDB Atlas

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a new cluster
3. Choose your region (closest to your users)
4. Create a database user:
   - Username: `majors_user`
   - Password: generate a strong password
5. Add IP access: allow 0.0.0.0/0 for now (or restrict to Railway IP later)
6. Copy the connection string:
   ```
   mongodb+srv://majors_user:<password>@<cluster>.mongodb.net/majors?retryWrites=true&w=majority
   ```
7. Replace `<password>` with your actual password

## Step 2: Set up Ethereum RPC

### Option A: Infura
1. Go to https://infura.io
2. Create a new project
3. Choose Ethereum mainnet (or testnet if needed)
4. Copy your RPC URL:
   ```
   https://mainnet.infura.io/v3/<your-project-id>
   ```

### Option B: Alchemy
1. Go to https://www.alchemy.com
2. Create a new app
3. Choose Ethereum mainnet
4. Copy your RPC URL:
   ```
   https://eth-mainnet.g.alchemy.com/v2/<your-api-key>
   ```

## Step 3: Generate a Strong JWT Secret

Generate a strong random secret (at least 32 characters):

```bash
openssl rand -hex 32
```

Save this value for later.

## Step 4: Deploy on Railway

1. Go to https://railway.app and log in
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select this repository
5. Railway will auto-detect the Dockerfile and deploy

## Step 5: Add Environment Variables

In the Railway dashboard:

1. Go to your project
2. Click the service (majors-api or similar)
3. Click "Variables"
4. Add these environment variables:

```env
APP_NAME=Majors API
APP_VERSION=1.0.0
MONGODB_URL=mongodb+srv://majors_user:<password>@<cluster>.mongodb.net/majors?retryWrites=true&w=majority
DATABASE_NAME=majors
SECRET_KEY=<your-generated-secret-from-step-3>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/<your-project-id>
```

Replace:
- `<password>` with your MongoDB password
- `<cluster>` with your MongoDB cluster name
- `<your-generated-secret-from-step-3>` with your JWT secret
- `<your-project-id>` with your Infura or Alchemy RPC ID

## Step 6: Test the Deployment

Once Railway deploys (usually 2-5 minutes):

1. Get your Railway domain from the "Deployments" tab
2. Test the health check:
   ```bash
   curl https://<your-railway-url>/health
   ```
   Expected response:
   ```json
   {"status": "healthy"}
   ```

3. Test registration:
   ```bash
   curl -X POST https://<your-railway-url>/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

4. Test blockchain network:
   ```bash
   curl https://<your-railway-url>/blockchain/network
   ```
   Expected response:
   ```json
   {"connected": true, "chain_id": 1, "latest_block": 18750000}
   ```

## Step 7: Set up Health Checks (Optional)

In Railway:

1. Go to your service settings
2. Enable health checks
3. Set endpoint to `/health`
4. Set interval to 30 seconds

Railway will monitor this endpoint and restart the service if it fails.

## Step 8: Enable Custom Domain (Optional)

1. In Railway dashboard, go to your service
2. Click "Settings"
3. Add a custom domain
4. Point your DNS records to Railway's endpoint

## Monitoring and Logs

In Railway dashboard:
- Logs: Click "Logs" tab to see real-time API logs
- Metrics: View CPU, memory, and network usage
- Deployments: See deployment history

## Database Indexes (Important for Production)

For better performance, create indexes in MongoDB Atlas:

1. Go to MongoDB Atlas
2. Click "Collections"
3. Create indexes on:
   - `users.username` (unique)
   - `items.created_at`
   - `items.name`

## Security Checklist

- [ ] MongoDB password is strong (20+ characters, mixed case, numbers, symbols)
- [ ] JWT secret is strong (32+ characters)
- [ ] MongoDB network access is restricted or monitored
- [ ] Infura/Alchemy API key is secure
- [ ] Never commit `.env` file
- [ ] Use HTTPS only (Railway provides this by default)
- [ ] Enable rate limiting on API endpoints (future enhancement)
- [ ] Rotate secrets regularly

## Troubleshooting

### "Ethereum node is not reachable"
Check your `ETHEREUM_RPC_URL` is correct and active.

### "MongoDB connection failed"
Check your `MONGODB_URL` is correct and MongoDB Atlas allows your Railway IP.

### "401 Unauthorized"
Ensure your `SECRET_KEY` is set and matches on Railway.

### Service keeps restarting
Check Railway logs for errors. Common issues:
- MongoDB connection timeout
- Missing environment variables
- Ethereum RPC unreachable

## Next Steps

1. Deploy to production
2. Test all endpoints
3. Monitor logs and metrics
4. Set up CI/CD to auto-deploy on GitHub push
5. Consider adding rate limiting and authentication for blockchain endpoints

## Production Architecture

```
┌─────────────┐
│   GitHub    │
│  Repository │
└──────┬──────┘
       │ push
       ▼
┌─────────────────┐
│   Railway API   │──────────┐
│ (FastAPI)       │          │
└─────────────────┘          │
       │                     │
       │ connect             │
       ▼                     ▼
┌──────────────────┐  ┌─────────────────┐
│ MongoDB Atlas    │  │ Infura/Alchemy  │
│ (Database)       │  │ (Ethereum RPC)  │
└──────────────────┘  └─────────────────┘
```

## Support

- Railway docs: https://docs.railway.app
- MongoDB Atlas docs: https://docs.atlas.mongodb.com
- Infura docs: https://docs.infura.io
- FastAPI docs: https://fastapi.tiangolo.com
