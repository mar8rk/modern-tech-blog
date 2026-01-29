#!/bin/bash
# deploy.sh - Modern Tech Blog Deployment Script
set -e

echo "🚀 Deploying Modern Tech Blog..."

# Check if Hugo is installed
if ! command -v hugo &> /dev/null; then
    echo "❌ Hugo not found. Please install Hugo first:"
    echo "   https://gohugo.io/installation/"
    exit 1
fi

# Check Hugo version
HUGO_VERSION=$(hugo version | grep -o 'v[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
echo "📦 Using Hugo $HUGO_VERSION"

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf public/

# Build the site
echo "🔨 Building site..."
hugo --minify --verbose

# Check build output
if [ ! -d "public" ]; then
    echo "❌ Build failed - public directory not found"
    exit 1
fi

echo "✅ Build successful!"
echo "📊 Build statistics:"
find public -type f | wc -l | xargs echo "   Files:"
du -sh public | awk '{print "   Size: " $1}'

# If GitHub Pages deployment
if [ "$1" = "github-pages" ]; then
    echo "📤 Deploying to GitHub Pages..."

    # Check if gh-pages branch exists
    git checkout gh-pages 2>/dev/null || git checkout -b gh-pages

    # Copy files
    cp -r public/* .

    # Commit and push
    git add .
    git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M:%S')"
    git push origin gh-pages

    echo "✅ Deployed to GitHub Pages!"
    git checkout main
fi

echo "🎉 Deployment complete!"
echo "📁 Static files ready in: public/"

if [ "$1" != "github-pages" ]; then
    echo "💡 Next steps:"
    echo "   1. Create GitHub repository: https://github.com/new"
    echo "   2. Connect to Netlify: https://app.netlify.com/start"
    echo "   3. Or serve locally: hugo server"
fi