#!/bin/bash
# deploy-s3.sh - Deploy Modern Tech Blog to AWS S3 + CloudFront
set -e

# Configuration
BUCKET_NAME="mar8rk-tech-blog"
DISTRIBUTION_ID=""  # Set this after creating CloudFront distribution
REGION="us-east-1"
HUGO_SITE_DIR="project/modern-tech-blog"

echo "🚀 Deploying Modern Tech Blog to AWS S3 + CloudFront..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Run: aws configure"
    exit 1
fi

# Navigate to Hugo site directory
cd "$HUGO_SITE_DIR"

# Check if Hugo is installed
if ! command -v hugo &> /dev/null; then
    echo "❌ Hugo not found. Please install Hugo first:"
    echo "   https://gohugo.io/installation/"
    exit 1
fi

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf public/

# Build the site
echo "🔨 Building site with Hugo..."
hugo --minify

# Check build output
if [ ! -d "public" ]; then
    echo "❌ Build failed - public directory not found"
    exit 1
fi

echo "✅ Build successful!"
echo "📊 Build statistics:"
find public -type f | wc -l | xargs echo "   Files:"
du -sh public | awk '{print "   Size: " $1}'

# Check if S3 bucket exists
if aws s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
    echo "📦 Creating S3 bucket: $BUCKET_NAME"

    if [ "$REGION" = "us-east-1" ]; then
        aws s3 mb "s3://$BUCKET_NAME"
    else
        aws s3 mb "s3://$BUCKET_NAME" --region "$REGION"
    fi

    # Configure bucket for static website hosting
    aws s3 website "s3://$BUCKET_NAME" \
        --index-document index.html \
        --error-document 404.html

    echo "✅ S3 bucket created and configured for static hosting"
else
    echo "📦 Using existing S3 bucket: $BUCKET_NAME"
fi

# Deploy to S3
echo "📤 Syncing files to S3..."
aws s3 sync public/ "s3://$BUCKET_NAME" \
    --delete \
    --cache-control "public, max-age=31536000, immutable" \
    --exclude "*.html" \
    --exclude "*.xml" \
    --exclude "*.json"

# Upload HTML files with shorter cache
aws s3 sync public/ "s3://$BUCKET_NAME" \
    --delete \
    --cache-control "public, max-age=300" \
    --exclude "*" \
    --include "*.html" \
    --include "*.xml" \
    --include "*.json"

echo "✅ Files synced to S3!"

# Invalidate CloudFront cache if distribution ID is set
if [ -n "$DISTRIBUTION_ID" ]; then
    echo "🔄 Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id "$DISTRIBUTION_ID" \
        --paths "/*" \
        --output table

    echo "✅ CloudFront invalidation created!"
else
    echo "⚠️  Set DISTRIBUTION_ID in this script to enable cache invalidation"
fi

# Get S3 website URL
S3_URL="http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo ""
echo "🎉 Deployment complete!"
echo "📁 S3 Bucket: s3://$BUCKET_NAME"
echo "🌐 S3 Website URL: $S3_URL"

if [ -n "$DISTRIBUTION_ID" ]; then
    echo "⚡ CloudFront URL: Check AWS Console for your distribution URL"
else
    echo "💡 Next: Set up CloudFront distribution for global CDN and HTTPS"
fi

echo ""
echo "📊 Deployment stats:"
aws s3 ls "s3://$BUCKET_NAME" --recursive --human-readable --summarize | tail -2