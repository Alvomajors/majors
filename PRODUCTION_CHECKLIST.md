# Production Checklist for Majors API

## Before Deployment

- [ ] Generate a strong JWT SECRET_KEY
- [ ] Create MongoDB Atlas cluster
- [ ] Create database user in MongoDB
- [ ] Get MongoDB connection string
- [ ] Create Infura or Alchemy account
- [ ] Get Ethereum RPC URL
- [ ] Push repo to GitHub
- [ ] Create Railway account

## Deployment Steps

- [ ] Connect GitHub repo to Railway
- [ ] Add all environment variables on Railway
- [ ] Deploy the service
- [ ] Wait for build to complete (2-5 minutes)
- [ ] Get Railway domain URL

## Post-Deployment Testing

- [ ] Test `/health` endpoint
- [ ] Test `/auth/register` endpoint
- [ ] Test `/auth/login` endpoint
- [ ] Test `/blockchain/network` endpoint
- [ ] Test `/items/` endpoint
- [ ] Verify logs show no errors

## Security Hardening

- [ ] Enable MongoDB network access restrictions
- [ ] Use strong passwords (20+ characters)
- [ ] Rotate JWT secret every 90 days
- [ ] Monitor Railway logs regularly
- [ ] Set up alerts for service crashes
- [ ] Review MongoDB access logs weekly

## Production Optimization

- [ ] Create database indexes
- [ ] Enable MongoDB backup
- [ ] Set up health check endpoint
- [ ] Configure Railway autoscaling
- [ ] Add rate limiting (future feature)
- [ ] Enable request logging

## Monitoring

- [ ] Check Railway metrics daily
- [ ] Monitor MongoDB storage usage
- [ ] Review API error logs weekly
- [ ] Track API response times
- [ ] Monitor Ethereum RPC rate limits

## Documentation

- [ ] Update README with deployment instructions
- [ ] Document API endpoints
- [ ] Create runbook for common issues
- [ ] Document backup procedures
- [ ] Update team on deployment
