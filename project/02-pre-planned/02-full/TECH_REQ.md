# Technical Requirements Document: Personal Technology Blog

**Created**: October 22, 2024
**Version**: 1.0
**Status**: Ready for Implementation
**Related Documents**: PRD.md

---

## Executive Summary

This document defines the technical approach for a high-performance personal technology blog using modern static site generation. The solution leverages Astro for optimal performance, AWS CDK for infrastructure-as-code deployment, and a git-based content workflow for developer-friendly publishing.

**Key Decisions**:
- Architecture: Static Site Generator (SSG) + JAMstack - Maximum performance and minimal operational overhead
- Cloud: AWS - Leveraging existing infrastructure with CDK deployment
- Framework: Astro - Zero-JS by default with excellent developer experience
- Estimated Monthly Cost: ~$3-8/month

---

## Architecture Decision

### Pattern Chosen: Static Site Generator (SSG) + JAMstack

**Rationale**:
The SSG approach perfectly aligns with the single-author blog requirements, delivering sub-second load times while maintaining minimal infrastructure costs. This architecture provides the "simple and straightforward" approach referenced in the PRD inspiration sites (anildash.com, hidekazu-konishi.com). For a personal blog with <10 concurrent users focused on sharing tech insights, static generation eliminates server management complexity while maximizing performance for readers discovering content through search engines.

**Key characteristics**:
- Pre-built static files served globally via CDN
- No server-side processing required for content delivery
- Git-based content workflow integrating with developer tools
- Automatic performance optimizations (image optimization, CSS bundling)

**System Components**:
```
Developer Workflow:
Developer → Write Markdown → Git Push → CDK Deploy → S3/CloudFront

User Experience:
User → Route53 (DNS) → CloudFront (CDN) → S3 (Static Files)

Content Pipeline:
Markdown Files → Astro Build → Optimized Static Assets → AWS S3
```

**Trade-offs Accepted**:
- ✅ Gaining: Sub-second page loads, minimal cost, zero server maintenance, excellent SEO
- ⚠️ Accepting: No real-time dynamic features (acceptable for blog content model)

---

## Technology Stack

### Static Site Generator: Astro

**Rationale**: Astro delivers exceptional performance with zero JavaScript by default while providing modern developer experience. Its component-agnostic approach allows future flexibility, and built-in optimizations align with performance goals.

**Alternatives Considered**:
- Hugo: Not chosen because Go templating is less familiar than JavaScript ecosystem
- Next.js: Not chosen because it's more complex than needed for a simple blog

**Key Features We'll Use**:
- Content Collections: Type-safe markdown processing with frontmatter validation
- Image Optimization: Automatic WebP conversion and responsive images
- Component Islands: Selective client-side interactivity when needed
- Built-in SEO: Automatic sitemap generation and meta tag management

### Styling: Tailwind CSS

**Rationale**: Utility-first approach enables rapid development of clean, professional designs. Perfect integration with Astro and supports the "simple and straightforward" design philosophy.

**Integration Approach**:
- Tailwind v4 with Vite plugin integration for modern build pipeline
- Primary usage: Utility classes directly in component markup
- Fallback: Plain CSS for complex or component-specific styling needs

**CSS Architecture Pattern**:
We'll employ a hybrid approach that prioritizes Tailwind utility classes while maintaining flexibility:

1. **Primary Pattern**: Use Tailwind utility classes directly in Astro components
2. **Global Styles**: Plain CSS in global.css for base styles and custom design tokens
3. **Component Styles**: Plain CSS for component-specific styles when utility classes become cumbersome

**Framework Compatibility Considerations**:
- Tailwind v4 introduces changes to @apply directive behavior in scoped contexts
- Modern CSS frameworks may have different behaviors in component-scoped vs. global styles
- Build-time CSS processing may affect how framework features compile
- Test CSS compilation early and across different contexts (global, scoped, production build)

**Testing Approach**:
- Verify Tailwind utilities work correctly in Astro component templates
- Test that global styles and component styles don't conflict
- Validate CSS compilation in both dev and production builds
- Check that styles render correctly after deployment (not just in development)

**Alternative Patterns if Compatibility Issues Arise**:
- Use plain CSS instead of framework-specific features like @apply
- Prefer utility classes in markup over CSS composition
- Extract common patterns to reusable components rather than CSS abstractions

### Content Management: Git-based Markdown

**Workflow**: Write blog posts locally in markdown with frontmatter metadata, commit to git repository, deploy via CDK script.

**Tools Needed**:
- Markdown editor: Any preferred editor (VS Code, Obsidian, etc.)
- Git client: For version control and publishing workflow
- AWS CDK CLI: For infrastructure deployment

---

## Infrastructure

### Cloud Platform: AWS

**Services to Use**:
- **Amazon S3**: Static file hosting with website configuration
- **Amazon CloudFront**: Global CDN for fast content delivery
- **Route53**: DNS management (when domain is configured)
- **AWS CDK**: Infrastructure as Code for repeatable deployments

**Architecture Diagram**:
```
Internet → Route53 (DNS) → CloudFront (CDN) → S3 Bucket (Static Files)
                                ↑
Developer → CDK Deploy → CloudFormation → AWS Resources
```

### Domain: Will decide later

Domain registration and configuration will be handled when ready. CDK stack will be configured to easily add custom domain via Route53 and SSL certificate through AWS Certificate Manager.

### Deployment Pipeline

**Approach**: CDK-based Greenfield Infrastructure Deployment

**⚠️ What CDK Will Create (Brand New Infrastructure):**

When you run `cdk deploy`, AWS CDK provisions entirely new infrastructure:

1. **S3 Bucket**: `tech-blog-{account}-{region}`
   - New bucket created specifically for your blog
   - Configured for static website hosting (index.html, 404.html)
   - Private bucket with no public access (CloudFront only)
   - Secure access via Origin Access Control

2. **CloudFront Distribution**: Global CDN
   - Unique CloudFront URL: `https://d{random}.cloudfront.net`
   - Global edge locations for fast content delivery
   - Caching optimized for static content
   - HTTPS enabled by default
   - Automatic cache invalidation on deployment

3. **Origin Access Control (OAC)**: Security Layer
   - Secure connection between CloudFront and S3
   - No public S3 bucket access required
   - AWS-recommended modern security pattern

4. **CloudFormation Stack**: Infrastructure as Code
   - All resources managed as single stack
   - Easy updates and rollbacks
   - Complete infrastructure visibility
   - Clean teardown via `cdk destroy`

**Deployment Process**:
```bash
# 1. Build Astro site locally
cd blog
npm run build

# 2. Deploy infrastructure and content
cd ../tech-blog-infrastructure
cdk deploy
# Creates: S3 bucket, CloudFront distribution, deploys files, invalidates cache

# 3. Access your blog at the CloudFront URL
# Output: https://d1234abcd.cloudfront.net
```

**Timing:**
- **Initial Deployment**: 3-5 minutes (creating all resources)
- **Subsequent Deployments**: 2-3 minutes (updating content + cache invalidation)
- **Cache Invalidation**: Automatic on each deployment

**Infrastructure Ownership:**
- All resources are in YOUR AWS account
- Full control over configuration
- No shared infrastructure with other users
- Complete isolation and security

---

## Blog-Specific Features

### Content Organization: Categories/Topics

**Implementation**: Astro Content Collections with taxonomy support
- Frontmatter-based topic classification
- Automatic topic index pages
- Related posts functionality

### Performance Optimization

**Image Handling**: Automatic optimization via Astro's built-in image service
- WebP conversion for modern browsers
- Responsive image generation
- Lazy loading by default

**SEO Approach**: Minimal initial setup
- Basic meta tags (title, description)
- Automatic sitemap generation
- No complex structured data initially

### Excluded Features (Initially)**:
- RSS feed generation: Not implemented initially
- Syntax highlighting: Plain text code blocks to maintain simplicity
- Analytics: No tracking initially
- Uptime monitoring: Rely on AWS reliability

---

## Performance & Scalability

### Performance Targets

Based on PRD requirements:
- **Page Load Time**: < 1 second (Lighthouse 90+ score)
- **Time to First Byte**: < 200ms (via CloudFront edge locations)
- **Core Web Vitals**: All metrics in "Good" range

### Scalability Plan

**Phase 1** (Launch - 1k monthly visitors):
Current S3 + CloudFront setup handles traffic easily

**Phase 2** (1k-10k monthly visitors):
No infrastructure changes needed, only content growth

**Phase 3** (10k+ monthly visitors):
Consider adding:
- Analytics for traffic insights
- RSS feed for subscriber growth
- Enhanced SEO optimization

**Cost Projection**:
- Phase 1: ~$5/month (S3 + CloudFront + Route53)
- Phase 2: ~$8/month (increased bandwidth)
- Phase 3: ~$12/month (additional features)

---

## Cost Estimation

### Monthly Infrastructure Costs

**Itemized Breakdown**:
- S3 Storage (1GB static files): ~$0.25
- CloudFront Data Transfer (10GB/month): ~$1.00
- Route53 Hosted Zone: $0.50
- S3 Requests (10k/month): ~$0.05
- **Total**: ~$2-5/month (scales with traffic)

**Cost Variables**:
- Traffic-dependent: CloudFront data transfer, S3 requests
- Fixed: Route53 hosted zone, minimal S3 storage

**Optimization Opportunities**:
- CloudFront caching reduces origin requests
- Image optimization reduces bandwidth costs
- Static nature eliminates compute costs

---

## Technology Decision Summary

| Decision Category | Chosen Technology | Rationale | Alternatives Considered |
|------------------|-------------------|-----------|------------------------|
| Architecture | SSG + JAMstack | Perfect for blog performance/cost | SSR, Serverless |
| Cloud Provider | AWS | Existing infrastructure, CDK support | GCP, Vercel |
| Framework | Astro | Zero-JS performance, modern DX | Hugo, Next.js |
| Styling | Tailwind CSS | Rapid development, clean designs | Custom CSS |
| Content Mgmt | Git-based Markdown | Developer-friendly, version controlled | Headless CMS |
| Deployment | Manual CDK | Control over timing, IaC benefits | GitHub Actions |
| Infrastructure | S3 + CloudFront | Industry standard, cost-effective | Amplify, Netlify |

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Set up AWS CDK project structure
- [ ] Initialize Astro blog project with Tailwind CSS
- [ ] Configure content collections for blog posts
- [ ] Create basic layout and styling
- [ ] Deploy hello-world version to AWS

### Phase 2: Content & Features (Week 2)
- [ ] Implement blog post listing page
- [ ] Create individual blog post template
- [ ] Add About Me page
- [ ] Configure topic/category system
- [ ] Set up image optimization pipeline

### Phase 3: Polish & Launch (Week 3)
- [ ] Performance optimization and testing
- [ ] SEO meta tags configuration
- [ ] Error pages (404, etc.)
- [ ] Final design refinements
- [ ] Production deployment and testing

---

## ⚠️ Critical: CloudFront Routing Architecture

### Static Site Routing Challenge

**Problem**:
CloudFront's `defaultRootObject` configuration only applies to the root path (`/`). When users navigate to `/blog` or `/about`, CloudFront does NOT automatically append `index.html` to the request. This causes S3 to return 403/404 errors because these paths don't exist as objects in the bucket.

**Impact**:
- Direct navigation to `/blog` returns "Access Denied"
- Links to `/about` from external sites fail
- Only root path `/` loads correctly
- Users see CloudFront error pages instead of blog content

### CloudFront Function Solution

**Purpose**: Normalize URLs and append index.html to directory requests

**Implementation**:
```javascript
// CloudFront Function attached to viewer-request event
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // Add trailing slash if missing and not a file
    if (uri !== '/' && !uri.includes('.') && !uri.endsWith('/')) {
        uri = uri + '/';
    }

    // Add index.html to directory requests
    if (uri.endsWith('/')) {
        uri = uri + 'index.html';
    }

    request.uri = uri;
    return request;
}
```

**Event Type**: Viewer Request (executes before CloudFront cache lookup)

**Performance**:
- Execution time: <1ms
- Cost: $0.10 per 1 million requests
- No cold start issues (unlike Lambda@Edge)

### Alternative Approaches Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| CloudFront Functions | Low latency, cheap, sufficient | Limited capabilities | ✅ **Chosen** |
| Lambda@Edge | Full programming capabilities | Higher latency & cost | ❌ Overkill for URL rewriting |
| S3 Website Hosting | Built-in routing | No HTTPS support, less CDN control | ❌ Not suitable |
| File-based output | No rewriting needed | Ugly URLs with .html | ❌ Poor UX |

### CDK Implementation

**In our stack** (`tech-blog-infrastructure-stack.ts`):

```typescript
// Create CloudFront Function for URL rewriting
const urlRewriteFunction = new cloudfront.Function(this, 'TechBlogUrlRewrite', {
  code: cloudfront.FunctionCode.fromInline(`
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // Add trailing slash if missing and not a file
    if (uri !== '/' && !uri.includes('.') && !uri.endsWith('/')) {
        uri = uri + '/';
    }

    // Add index.html to directory requests
    if (uri.endsWith('/')) {
        uri = uri + 'index.html';
    }

    request.uri = uri;
    return request;
}
  `),
});

// Attach function to CloudFront distribution
const distribution = new cloudfront.Distribution(this, 'TechBlogDistribution', {
  defaultBehavior: {
    // ... other config
    functionAssociations: [
      {
        function: urlRewriteFunction,
        eventType: cloudfront.FunctionEventType.VIEWER_REQUEST,
      },
    ],
  },
});
```

### URL Routing Tests

**Critical Tests** (must pass before deployment):
- [ ] Root path `/` serves homepage
- [ ] `/blog` serves blog listing page (not 403/404)
- [ ] `/blog/` (with trailing slash) also works
- [ ] `/about` serves about page
- [ ] Individual post URLs work (`/blog/first-post`)
- [ ] Static assets load correctly (CSS, JS, images)
- [ ] Invalid URLs return 404 error page
- [ ] Browser console shows no routing errors
- [ ] CloudFront Function executes without errors

### Troubleshooting Routing Issues

**If `/blog` or `/about` return 403/404**:

1. **Verify CloudFront Function is attached**:
   ```bash
   aws cloudfront get-distribution-config --id {DISTRIBUTION_ID} | grep FunctionAssociations
   ```

2. **Check function code in CDK stack** (should be in lines 25-63)

3. **Verify function event type is VIEWER_REQUEST**

4. **Redeploy CDK stack**:
   ```bash
   cd tech-blog-infrastructure
   cdk deploy
   ```

5. **Invalidate CloudFront cache**:
   ```bash
   aws cloudfront create-invalidation --distribution-id {ID} --paths "/*"
   ```

6. **Wait 2-3 minutes for propagation**

---

## ⚠️ Critical: Static File MIME Type Configuration

### Known CloudFront/S3 Issue

When serving static files through CloudFront from S3, files may be delivered with incorrect `Content-Type` headers, causing CSS and JavaScript to fail loading.

### Problem Details

**Symptoms:**
- Browser console error: "MIME type of 'text/plain' is not a supported stylesheet MIME type"
- CSS styles don't apply (unstyled HTML)
- JavaScript modules fail: "Expected a JavaScript module script but the server responded with a MIME type of 'text/plain'"
- Images may not display correctly

**Root Cause:**
1. Files uploaded to S3 without explicit Content-Type metadata
2. S3 auto-detection fails or defaults to `text/plain`
3. CloudFront caches the incorrect headers
4. Browsers refuse to apply resources with wrong MIME types

### Solution Implementation

**Our CDK Stack Handles This:**

The CDK stack (`tech-blog-infrastructure-stack.ts`) includes:

```typescript
new s3deploy.BucketDeployment(this, 'TechBlogDeployment', {
  sources: [s3deploy.Source.asset('../blog/dist')],
  destinationBucket: websiteBucket,
  distribution: distribution,
  distributionPaths: ['/*'], // ✅ Automatic cache invalidation
});
```

**How It Works:**
1. **Astro Build**: Generates files with proper extensions (.html, .css, .js)
2. **S3 Auto-Detection**: S3 infers MIME types from extensions
3. **Cache Invalidation**: CDK automatically invalidates CloudFront cache
4. **Correct Headers**: Files served with proper Content-Type

**Expected MIME Types:**
- `.html` → `text/html`
- `.css` → `text/css`
- `.js` → `application/javascript`
- `.json` → `application/json`
- `.svg` → `image/svg+xml`
- `.png` → `image/png`
- `.jpg` → `image/jpeg`
- `.woff2` → `font/woff2`

### Troubleshooting Steps

**If CSS/JS doesn't load after deployment:**

1. **Check Browser Console** (F12):
   ```
   Look for: "MIME type of 'text/plain' is not supported"
   This confirms the MIME type issue
   ```

2. **Inspect S3 Object Metadata**:
   ```bash
   # Check what Content-Type S3 has for your CSS
   aws s3api head-object \
     --bucket tech-blog-{account}-{region} \
     --key _astro/main.css

   # Look for: "ContentType": "text/css"
   # If you see "text/plain", that's the problem
   ```

3. **Fix S3 Metadata** (if incorrect):
   ```bash
   # Fix a specific CSS file
   aws s3 cp s3://tech-blog-{account}-{region}/_astro/main.css \
             s3://tech-blog-{account}-{region}/_astro/main.css \
     --content-type "text/css" \
     --metadata-directive REPLACE

   # Fix all CSS files (if multiple)
   aws s3 cp s3://tech-blog-{account}-{region}/_astro/ \
             s3://tech-blog-{account}-{region}/_astro/ \
     --recursive \
     --exclude "*" --include "*.css" \
     --content-type "text/css" \
     --metadata-directive REPLACE
   ```

4. **Invalidate CloudFront Cache**:
   ```bash
   # Get distribution ID from CDK output
   aws cloudfront create-invalidation \
     --distribution-id E1234ABCD5678 \
     --paths "/*"

   # Wait 2-3 minutes for propagation
   ```

5. **Clear Browser Cache**:
   - Chrome/Edge: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Firefox: Ctrl+Shift+F5 or Cmd+Shift+R
   - Or use Incognito/Private mode

6. **Verify Fix**:
   ```bash
   # Check headers CloudFront is serving
   curl -I https://d1234abcd.cloudfront.net/_astro/main.css

   # Should show: content-type: text/css
   ```

### Prevention

**Best Practices:**
- ✅ Always use CDK for deployments (includes automatic cache invalidation)
- ✅ Let Astro build handle file generation (proper extensions)
- ✅ Avoid manual S3 uploads (use `cdk deploy` instead)
- ✅ Test in browser DevTools Network tab after deployment
- ✅ Check S3 metadata if files don't render

**If manually uploading to S3:**
```bash
# Always specify content-type explicitly
aws s3 cp styles.css s3://bucket/ --content-type "text/css"
aws s3 cp script.js s3://bucket/ --content-type "application/javascript"
```

This issue is CRITICAL for blog functionality - unstyled HTML is unusable. Following these guidelines ensures it never occurs.

---

## ⚠️ Awareness: CSS Framework Integration Patterns

### Modern CSS Framework Considerations

**Context:**
Modern CSS frameworks (Tailwind v4, UnoCSS, etc.) offer powerful features like @apply directives, CSS-in-JS, and compile-time transformations. However, these features may behave differently depending on:
- Framework version
- Build tool integration
- CSS scope context (global vs. component-scoped)
- Static site generator architecture

**Common Integration Patterns:**

**Pattern 1: Utility-First in Markup (Recommended for Static Sites)**
```astro
<!-- Tailwind utilities directly in component -->
<header class="bg-white border-b border-gray-200 sticky top-0">
  <nav class="max-w-7xl mx-auto px-4">
    <!-- Content -->
  </nav>
</header>
```
**Pros**: Always works, no compilation issues, clear intent
**Cons**: More verbose HTML, harder to reuse patterns

**Pattern 2: CSS Composition with @apply**
```css
/* Component scoped style */
<style>
  .header {
    @apply bg-white border-b border-gray-200 sticky top-0;
  }
</style>
```
**Pros**: DRY, familiar CSS patterns
**Cons**: May not work in all contexts, especially component-scoped styles in some frameworks

**Pattern 3: Hybrid Approach**
```astro
<!-- Use utilities for simple cases -->
<div class="flex items-center space-x-4">

<!-- Use plain CSS for complex patterns -->
<style>
  .complex-component {
    /* Plain CSS properties */
    display: flex;
    align-items: center;
    gap: 1rem;
  }
</style>
```
**Pros**: Flexibility, works everywhere
**Cons**: Mixed patterns may reduce consistency

### Potential Compatibility Issues

**Issue: Framework Features in Scoped Styles**
Some CSS framework features (like @apply, @layer, custom directives) may not work in component-scoped `<style>` tags due to:
- CSS module isolation
- Build tool processing order
- Framework-specific compiler limitations

**Symptoms:**
- Build errors: "Cannot apply unknown utility class"
- Compilation warnings about missing CSS features
- Styles work in global.css but fail in component styles

**Prevention:**
1. Test your CSS approach early in both global and component contexts
2. Prefer utility classes in markup for maximum compatibility
3. Use plain CSS for component-scoped styles if framework features don't work
4. Check framework documentation for version-specific integration guidance

**Troubleshooting Steps:**

If you encounter CSS framework issues:

1. **Verify Framework Version**: Check if you're using the latest stable version
   ```bash
   npm list tailwindcss @tailwindcss/vite
   ```

2. **Test in Different Contexts**:
   - Does it work in global.css? → Framework is working
   - Does it fail in component `<style>` tags? → Scoping issue
   - Does it fail everywhere? → Integration issue

3. **Check Build Output**:
   ```bash
   npm run build
   # Look for CSS-related warnings or errors
   ```

4. **Review Framework Docs**: Check for version-specific integration patterns

5. **Try Alternative Patterns**:
   - Replace @apply with utility classes in markup
   - Use plain CSS in component styles
   - Move complex patterns to global styles

**Best Practices:**

✅ **Test CSS compilation early** - Don't wait until late in development
✅ **Prefer simple patterns** - Utility classes in markup are most reliable
✅ **Document your approach** - Be consistent across components
✅ **Validate after deployment** - Ensure styles work in production, not just dev

❌ **Don't assume features work everywhere** - Test in multiple contexts
❌ **Don't mix too many patterns** - Consistency aids maintainability
❌ **Don't skip build testing** - Dev mode may not catch all issues

### Framework-Specific Notes

**Tailwind CSS v4**:
- Major architectural changes from v3
- @apply behavior changed in some contexts
- Vite plugin integration is recommended path
- Component-scoped styles may have limitations

**When in Doubt**:
- Use utility classes directly in markup (most compatible)
- Use plain CSS for component-specific styling
- Reserve framework-specific features for global styles where well-supported

This is not a blocker for the project—it's an awareness item to help you make informed architectural decisions and troubleshoot quickly if issues arise.

---

## CDK Implementation Details

### Stack Structure
```typescript
// Primary stack components
- S3Bucket: Static website hosting
- CloudFrontDistribution: Global CDN
- OriginAccessControl: Secure S3 access
- BucketDeployment: Automated asset upload
- Optional: Certificate + Route53 for custom domain
```

### Deployment Commands
```bash
# Initial setup
npm install -g aws-cdk
cdk bootstrap

# Regular deployment
npm run build        # Build Astro site
cdk deploy          # Deploy infrastructure + content

# Development
npm run dev         # Local development server
```

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CDK Learning Curve | Medium | Low | Start with simple stack, expand gradually |
| AWS Cost Overrun | Low | Medium | Monitor billing, set up cost alerts |
| Content Loss | Low | High | Git version control, regular backups |

---

## Open Questions

- [ ] Custom domain preference (will be decided later)
- [ ] Future analytics preferences (not needed initially)
- [ ] RSS feed timeline (not initially required)

---

## Next Steps

1. **Review this document** - Confirm technical approach aligns with vision
2. **Set up development environment**:
   - Install Node.js, AWS CLI, and CDK
   - Initialize Astro project with Tailwind
3. **Begin Implementation**:
   - Option A: Follow roadmap directly
   - Option B: Use `/epcc-explore` to analyze Astro blog patterns first
4. **Deploy foundation** - Get basic version running on AWS

---

## Appendix: Useful Resources

### Documentation Links
- Astro: https://docs.astro.build/
- AWS CDK: https://docs.aws.amazon.com/cdk/
- Tailwind CSS: https://tailwindcss.com/docs

### Example Projects
- Astro blog starter: Demonstrates content collections and SEO
- CDK static site: Infrastructure as Code patterns for S3/CloudFront

### Community Resources
- Astro Discord: Active community for questions
- AWS CDK GitHub: Examples and patterns
- r/webdev: General web development discussions

---

**Technical Requirements Complete!** Ready to build your high-performance blog 🚀