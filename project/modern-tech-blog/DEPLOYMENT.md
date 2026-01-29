# Deployment Guide

This guide covers deploying the Modern Tech Blog to various platforms.

## 🚀 Quick Deploy (Recommended: Netlify)

### Option 1: Netlify (Automated)

1. **Create GitHub Repository**
   ```bash
   # If you have GitHub CLI authenticated
   gh repo create modern-tech-blog --public --description "A modern tech blog built with Hugo and PaperMod"

   # Or manually at https://github.com/new
   # Repository name: modern-tech-blog
   # Description: A modern tech blog built with Hugo and PaperMod
   # Public repository
   ```

2. **Push Code to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/modern-tech-blog.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy to Netlify**
   - Visit [app.netlify.com](https://app.netlify.com)
   - Click "New site from Git"
   - Choose GitHub and select your repository
   - Build settings are auto-detected from `netlify.toml`:
     - Build command: `hugo --minify`
     - Publish directory: `public`
     - Hugo version: 0.146.0
   - Click "Deploy site"

### Option 2: Netlify CLI (Local)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy directly
netlify deploy --prod --dir=public

# Or deploy with build
netlify build && netlify deploy --prod
```

## 🔧 Alternative Deployment Options

### GitHub Pages

```bash
# Build and deploy to gh-pages branch
./deploy.sh github-pages

# Or manually:
hugo --minify
git checkout -b gh-pages
cp -r public/* .
git add .
git commit -m "Deploy"
git push origin gh-pages
```

### Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Configure build settings:
   - Build Command: `hugo --minify`
   - Output Directory: `public`

### AWS S3 + CloudFront

```bash
# Build site
hugo --minify

# Sync to S3 (requires AWS CLI)
aws s3 sync public/ s3://your-bucket-name --delete

# Invalidate CloudFront (optional)
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

## 📊 Build Performance

- **Build Time**: ~50ms (17 pages)
- **Output Size**: 312K (23 files)
- **Hugo Version**: 0.146.0 extended
- **Theme**: PaperMod (optimized)

## 🔍 Verification Checklist

After deployment, verify:

- [ ] Homepage loads correctly
- [ ] All blog posts are accessible
- [ ] About page displays properly
- [ ] Navigation menu works
- [ ] Code syntax highlighting functions
- [ ] Mobile responsiveness
- [ ] Fast loading times (<3 seconds)
- [ ] Dark/light theme toggle works

## 🚨 Troubleshooting

### Build Failures

**Hugo version mismatch:**
```bash
# Check version
hugo version

# Expected: v0.146.0 extended
# Install correct version from https://gohugo.io/installation/
```

**Theme not found:**
```bash
# Ensure submodule is initialized
git submodule update --init --recursive

# Or re-add theme
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

**Build command fails:**
```bash
# Use explicit Hugo path
/usr/local/bin/hugo --minify

# Or check PATH
which hugo
```

### Deployment Issues

**Netlify build fails:**
- Check Hugo version in `netlify.toml`
- Verify build command: `hugo --minify`
- Ensure theme submodule is accessible

**GitHub Pages 404:**
- Check repository is public
- Verify gh-pages branch exists
- Ensure files are in root directory (not subfolder)

**Performance issues:**
- Run `hugo --minify` for production builds
- Check image sizes and formats
- Verify CDN configuration

## 📝 Environment Variables

For advanced deployments, set these in your platform:

```
HUGO_VERSION=0.146.0
HUGO_ENV=production
NODE_VERSION=18
NPM_VERSION=9
```

## 🔄 Continuous Deployment

The repository is configured for automatic deployment on push to main branch:

1. **GitHub Actions** (optional - add `.github/workflows/deploy.yml`)
2. **Netlify** (recommended - configured in `netlify.toml`)
3. **Vercel** (auto-detects Hugo projects)

---

**Need help?** Check the [Hugo documentation](https://gohugo.io/documentation/) or [PaperMod theme guide](https://github.com/adityatelange/hugo-PaperMod).