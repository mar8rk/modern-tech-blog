# AWS Deployment Guide

Complete guide for deploying your Modern Tech Blog to AWS infrastructure using two approaches: **AWS Amplify** (easy) and **S3 + CloudFront** (advanced).

## 🏗️ Architecture Comparison

| Feature | AWS Amplify | S3 + CloudFront |
|---------|-------------|------------------|
| **Setup Time** | 5 minutes | 15-30 minutes |
| **Monthly Cost** | $1-5 | $0.50-2 |
| **Auto-deployment** | ✅ Built-in | ✅ GitHub Actions |
| **Custom domain** | ✅ Easy | ✅ Manual setup |
| **SSL/HTTPS** | ✅ Automatic | ✅ Free certificate |
| **Global CDN** | ✅ Built-in | ✅ CloudFront |
| **Control level** | Medium | Full control |
| **Scalability** | High | Unlimited |

---

## 🚀 Option 1: AWS Amplify (Recommended for Beginners)

### Prerequisites
- AWS Account
- GitHub repository (you already have this!)

### Step 1: Setup Amplify App

1. **Go to AWS Amplify Console:**
   - https://console.aws.amazon.com/amplify/

2. **Create New App:**
   - Click "New App" → "Host web app"
   - Choose "GitHub"
   - Select repository: `mar8rk/modern-tech-blog`
   - Select branch: `main`

3. **Configure Build:**
   - App name: `modern-tech-blog`
   - Build settings: Auto-detected from `amplify.yml` ✅
   - Environment variables: None needed

4. **Deploy:**
   - Click "Save and deploy"
   - Wait ~5 minutes for first deployment

### Expected Result
- **Live URL:** `https://main.d[random].amplifyapp.com`
- **Auto-deployment:** Every git push triggers new build
- **Cost:** ~$1-5/month for typical blog traffic

---

## ⚡ Option 2: S3 + CloudFront (Maximum Control)

### Prerequisites
- AWS Account with programmatic access
- AWS CLI installed: `pip install awscli`
- AWS CLI configured: `aws configure`

### Step 1: Deploy Infrastructure

```bash
# Deploy CloudFormation stack
aws cloudformation create-stack \
  --stack-name modern-tech-blog \
  --template-body file://cloudformation-blog.yml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=BucketName,ParameterValue=mar8rk-tech-blog

# Wait for stack creation (5-10 minutes)
aws cloudformation wait stack-create-complete --stack-name modern-tech-blog

# Get outputs
aws cloudformation describe-stacks \
  --stack-name modern-tech-blog \
  --query 'Stacks[0].Outputs'
```

### Step 2: Manual Deployment

```bash
# Make deployment script executable
chmod +x deploy-s3.sh

# Deploy your site
./deploy-s3.sh
```

### Step 3: Setup GitHub Actions (Optional)

1. **Get AWS credentials from CloudFormation outputs:**
   ```bash
   aws cloudformation describe-stacks \
     --stack-name modern-tech-blog \
     --query 'Stacks[0].Outputs[?OutputKey==`DeploymentUserAccessKeyId`].OutputValue' \
     --output text
   ```

2. **Add GitHub Secrets:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `AWS_ACCESS_KEY_ID`: From CloudFormation output
     - `AWS_SECRET_ACCESS_KEY`: From CloudFormation output
     - `CLOUDFRONT_DISTRIBUTION_ID`: From CloudFormation output

3. **Enable GitHub Actions:**
   - Push to main branch
   - Check Actions tab for automatic deployment

### Expected Result
- **S3 URL:** `http://mar8rk-tech-blog.s3-website-us-east-1.amazonaws.com`
- **CloudFront URL:** `https://d[random].cloudfront.net`
- **Auto-deployment:** GitHub Actions on every push
- **Cost:** ~$0.50-2/month for typical blog traffic

---

## 🛠️ Advanced Configuration

### Custom Domain (Both Options)

#### For Amplify:
1. Go to Amplify Console → Domain management
2. Add domain → Enter your domain
3. Configure DNS records as shown

#### For S3 + CloudFront:
1. **Update CloudFormation:**
   ```bash
   aws cloudformation update-stack \
     --stack-name modern-tech-blog \
     --template-body file://cloudformation-blog.yml \
     --capabilities CAPABILITY_IAM \
     --parameters ParameterKey=BucketName,ParameterValue=mar8rk-tech-blog \
                  ParameterKey=DomainName,ParameterValue=yourdomain.com
   ```

2. **Update DNS:**
   - Point your domain to Route53 nameservers (from CloudFormation output)

### Performance Optimization

Both setups include:
- ✅ **Global CDN** for fast worldwide access
- ✅ **Compression** for smaller file sizes
- ✅ **Cache optimization** (1 year for assets, 5 minutes for HTML)
- ✅ **HTTP/2** support
- ✅ **Security headers** for protection

### Monitoring & Analytics

#### CloudWatch Metrics (S3 + CloudFront):
- **CloudFront:** Request count, data transfer, error rates
- **S3:** Storage usage, request metrics
- **Cost:** Billing alerts for budget management

#### Amplify Metrics:
- Built-in analytics in Amplify Console
- Real-time deployment logs
- Performance insights

---

## 💰 Cost Breakdown

### AWS Amplify
```
Build minutes: $0.01 per minute
- ~3 minutes per build
- ~30 builds/month = $0.90

Hosting: $0.15 per GB served
- ~10 GB/month for blog = $1.50

Total: ~$2.40/month
```

### S3 + CloudFront
```
S3 Storage: $0.023 per GB/month
- ~0.5 GB = $0.01

S3 Requests: $0.0004 per 1,000 GET requests
- ~10,000 requests = $0.004

CloudFront: $0.085 per GB (first 10 TB)
- ~10 GB = $0.85

Total: ~$0.86/month
```

---

## 🔍 Troubleshooting

### Common Issues

**Amplify Build Fails:**
```bash
# Check build logs in Amplify Console
# Common fix: Verify amplify.yml syntax
```

**S3 Deployment Permission Denied:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify IAM permissions
aws iam get-user-policy --user-name mar8rk-tech-blog-deployment-user --policy-name S3DeploymentPolicy
```

**CloudFront Cache Issues:**
```bash
# Invalidate cache manually
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

### Performance Testing

```bash
# Test website speed
curl -o /dev/null -s -w "%{time_total}\n" https://your-site.com

# Test from multiple locations
# Use tools like GTmetrix, WebPageTest, or Pingdom
```

---

## 🎯 Recommendations

### Choose Amplify If:
- ✅ You want the easiest setup
- ✅ You're comfortable with ~$2-5/month cost
- ✅ You don't need fine-grained control
- ✅ You want built-in branch previews

### Choose S3 + CloudFront If:
- ✅ You want minimum cost (~$0.50-2/month)
- ✅ You need maximum performance control
- ✅ You want to learn AWS infrastructure
- ✅ You plan to scale significantly

### Migration Path
1. **Start with Amplify** for quick setup
2. **Learn S3 + CloudFront** when you need more control
3. **Easy migration:** Both use same Hugo build process

---

## 📚 Next Steps

After deployment:

1. **Test your site** thoroughly
2. **Set up monitoring** (CloudWatch alarms)
3. **Configure backups** (S3 versioning)
4. **Add custom domain** if desired
5. **Set up analytics** (Google Analytics)

Both approaches will give you a fast, reliable, and cost-effective blog hosting solution! 🚀