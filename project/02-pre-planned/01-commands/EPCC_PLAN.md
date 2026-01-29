# Implementation Plan: Personal Technology Blog

**Created**: October 22, 2024
**Status**: Ready for Implementation
**Related Documents**: PRD.md, TECH_REQ.md
**Timeline**: 20 hours total development time
**Target Launch**: Today (immediate deployment)

---

## 📋 Project Overview

### What We're Building
A high-performance personal technology blog using static site generation (Astro) deployed on AWS infrastructure. The blog will serve as a platform for sharing professional tech insights with full content ownership and control.

### Why It's Needed
- Establish content ownership and control vs. third-party platforms
- Create professional platform for sharing tech insights
- Build discoverable presence for career and thought leadership
- Maintain simple, straightforward design philosophy

### Success Criteria
- [ ] **Functional**: Blog loads and displays content correctly
- [ ] **Performance**: Page load times < 1 second (Lighthouse 90+)
- [ ] **Accessibility**: Site accessible via CloudFront URL
- [ ] **Content**: All three core pages (blog, posts, about) functional
- [ ] **SEO**: Basic meta tags and sitemap generation working
- [ ] **Deployment**: Successful CDK deployment to AWS

### Non-Goals (Out of Scope)
- RSS feed generation (Phase 2)
- Syntax highlighting for code blocks (maintaining simplicity)
- Analytics tracking (not initially required)
- User authentication or comments system
- Complex SEO optimization beyond basics

---

## 🏗️ Technical Approach

### Architecture Decision: Static Site Generator + JAMstack

**Chosen Stack**:
- **Framework**: Astro (zero-JS by default, excellent performance)
- **Styling**: Tailwind CSS (utility-first, rapid development)
- **Content**: Git-based Markdown with frontmatter
- **Deployment**: AWS CDK (Infrastructure as Code)
- **Hosting**: S3 + CloudFront + Route53

**System Architecture**:
```
Developer Workflow:
Developer → Write Markdown → Git Commit → CDK Deploy → S3/CloudFront

User Experience:
User → Route53 (DNS) → CloudFront (CDN) → S3 (Static Files)

Content Pipeline:
Markdown Files → Astro Build → Optimized Static Assets → AWS S3
```

**Key Benefits**:
- Sub-second page load times via CDN
- Minimal operational overhead (~$3-8/month)
- Developer-friendly git-based workflow
- Automatic performance optimizations
- Zero server maintenance required

### ⚠️ Infrastructure Deployment Approach

**IMPORTANT: This Creates Brand New AWS Infrastructure**

When you run `cdk deploy`, AWS CDK will provision **entirely new infrastructure** dedicated to your blog:

✅ **New S3 Bucket**: `tech-blog-{account}-{region}` created fresh for your static files
✅ **New CloudFront Distribution**: Unique CloudFront URL (e.g., `https://d1234abcd.cloudfront.net`)
✅ **New Origin Access Control (OAC)**: Secure connection between CloudFront and S3
✅ **New CloudFormation Stack**: Infrastructure as code you own and control

**What This Means:**
- You're NOT reusing existing infrastructure - everything is built from scratch
- All AWS resources are dedicated to YOUR blog (isolated and independent)
- You receive a unique CloudFront URL where your blog will be accessible
- Infrastructure is defined as code in `tech-blog-infrastructure/` directory
- Complete teardown available via `cdk destroy` when finished

This greenfield approach ensures complete control, repeatability, and isolation.

---

## 📝 Detailed Task Breakdown

### Phase 1: Foundation & Infrastructure (8 hours)

#### Task 1.1: Development Environment Setup (1 hour)
- **Description**: Install and configure required tools
- **Deliverables**:
  - Node.js, AWS CLI, CDK CLI installed
  - AWS credentials configured
  - Project directory structure created
- **Dependencies**: None
- **Priority**: Critical
- **Estimate**: 1 hour

#### Task 1.2: AWS CDK Project Initialization (3 hours)
- **Description**: Set up CDK project with S3, CloudFront, Route53 configuration and URL routing
- **Deliverables**:
  - CDK project structure with TypeScript
  - S3 bucket with static website hosting
  - CloudFront distribution with caching rules
  - **CloudFront Function for directory-style URL handling**
  - **Function association with viewer-request event**
  - Origin Access Control for secure S3 access
- **Dependencies**: Task 1.1
- **Priority**: Critical
- **Estimate**: 3 hours (added 1 hour for URL routing configuration)

#### ⚠️ Known Issue: Static File MIME Types

**Critical Configuration Requirement**

There's a common issue when serving static files (CSS, JavaScript, images) through CloudFront from S3: files may be served with incorrect `Content-Type` headers (e.g., `text/plain` instead of `text/css`), causing browsers to refuse rendering.

**Symptoms:**
- CSS styles don't apply (page appears unstyled)
- JavaScript modules fail to load with MIME type errors
- Browser console shows: "MIME type of 'text/plain' is not a supported stylesheet MIME type"

**Root Causes:**
1. S3 may incorrectly infer MIME types during upload
2. CloudFront caches these incorrect headers
3. CDK BucketDeployment needs proper configuration

**Prevention (Built into CDK Stack):**

Our CDK stack handles this automatically by:
1. **Proper Build Output**: Astro generates files with correct extensions
2. **S3 Auto-Detection**: S3 infers MIME types from standard extensions (.html, .css, .js)
3. **Cache Invalidation**: CDK triggers CloudFront invalidation on deployment

**If You Encounter This Issue:**

If CSS/JS files aren't rendering after deployment:

**Step 1: Verify S3 Metadata**
```bash
# Check Content-Type in S3
aws s3api head-object --bucket tech-blog-{account}-{region} --key _astro/main.css
# Should show: ContentType: 'text/css'
# If it shows 'text/plain', that's the problem
```

**Step 2: Fix S3 Metadata (if needed)**
```bash
# Fix CSS files
aws s3 cp s3://tech-blog-{account}-{region}/_astro/main.css s3://tech-blog-{account}-{region}/_astro/main.css \
  --content-type "text/css" \
  --metadata-directive REPLACE

# Fix JS files
aws s3 cp s3://tech-blog-{account}-{region}/_astro/main.js s3://tech-blog-{account}-{region}/_astro/main.js \
  --content-type "application/javascript" \
  --metadata-directive REPLACE
```

**Step 3: Invalidate CloudFront Cache**
```bash
# Get your distribution ID from CDK output
aws cloudfront create-invalidation \
  --distribution-id {YOUR_DISTRIBUTION_ID} \
  --paths "/*"
```

**Step 4: Verify Fix**
- Wait 2-3 minutes for invalidation to complete
- Clear browser cache (Cmd+Shift+R / Ctrl+Shift+F5)
- Reload your blog - styles should now render correctly

**Prevention for Future Deployments:**

The CDK stack automatically triggers cache invalidation on each deployment. If you manually upload files to S3, ensure you set Content-Type explicitly.

**Debugging Tips:**
- Check browser console for MIME type errors
- Use browser DevTools Network tab to inspect Content-Type headers
- Verify S3 object metadata in AWS Console: S3 → Object → Properties → Metadata

#### ⚠️ Critical Issue: CloudFront Directory URL Routing

**Common Deployment Problem**

A critical issue occurs when serving static sites through CloudFront: directory-style URLs like `/blog` or `/about` return 403 "Access Denied" errors, even though the content exists.

**Symptoms:**
- Homepage (`/`) loads correctly
- `/blog` returns 403 Forbidden or 404 Not Found
- `/about` returns 403 Forbidden or 404 Not Found
- Direct navigation to `/blog/index.html` works

**Root Cause:**
1. Astro generates directory-based output: `/blog/index.html`, `/about/index.html`
2. CloudFront's `defaultRootObject` only applies to root path `/`
3. Requests to `/blog` are forwarded to S3 as-is (looking for an object named "blog")
4. S3 returns 403 because `/blog` doesn't exist as an object
5. CloudFront serves the error to users

**Solution (Implemented in CDK Stack):**

Our CDK stack includes a CloudFront Function for URL rewriting:

```typescript
// CloudFront Function transforms URLs before S3 request
// /blog → /blog/ → /blog/index.html
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
```

**Prevention (Built into CDK Stack):**
- CloudFront Function attached to viewer-request event
- URL rewriting happens before CloudFront cache lookup
- Performance impact: <1ms per request
- Cost: $0.10 per 1 million requests

**If You Encounter This Issue:**

1. **Verify CloudFront Function is attached:**
   ```bash
   aws cloudfront get-distribution-config --id {DISTRIBUTION_ID} | grep FunctionAssociations
   ```

2. **Check CDK stack includes function association:**
   Look for `functionAssociations` in the CloudFront distribution configuration

3. **Redeploy if needed:**
   ```bash
   cd tech-blog-infrastructure
   cdk deploy
   ```

4. **Invalidate CloudFront cache:**
   ```bash
   aws cloudfront create-invalidation --distribution-id {ID} --paths "/*"
   ```

#### Task 1.3: Astro Blog Project Setup (2 hours)
- **Description**: Initialize Astro project with Tailwind CSS integration
- **Deliverables**:
  - Astro project with blog template
  - Tailwind CSS configured and integrated
  - Content collections set up for blog posts
  - Basic project structure organized
- **Dependencies**: Task 1.1
- **Priority**: Critical
- **Estimate**: 2 hours

**CSS Framework Integration Considerations**:
- Test CSS compilation during development to catch framework-specific issues early
- Be aware that CSS frameworks may have version-specific behaviors, especially around features like @apply directives, CSS modules, or scoped styles
- Consider how your chosen framework interacts with component-level styling (scoped vs. global)
- Verify that framework features compile correctly in your build environment before extensive use

**Integration Testing Checklist**:
- [ ] CSS builds without errors in development mode
- [ ] CSS builds correctly for production
- [ ] Framework utilities work in both global and component-scoped contexts
- [ ] No compilation warnings related to CSS processing

#### Task 1.4: Hello World Deployment (1.5 hours)
- **Description**: Deploy basic Astro site to AWS to validate infrastructure and URL routing
- **Deliverables**:
  - Working CloudFront URL serving Astro site
  - **Verified directory URL routing (/blog, /about)**
  - **Confirmed CloudFront Function behavior**
  - CDK deployment pipeline functioning
  - Basic connectivity confirmed
- **Dependencies**: Tasks 1.2, 1.3
- **Priority**: Critical
- **Estimate**: 1.5 hours (added 0.5 hours for comprehensive routing validation)

**Critical Testing Checklist**:
- [ ] Root path `/` loads homepage correctly
- [ ] `/blog` loads blog listing page (not 403/404)
- [ ] `/blog/` (with trailing slash) also works
- [ ] `/about` loads about page (not 403/404)
- [ ] Individual post URLs work (e.g., `/blog/first-post`)
- [ ] Static assets load correctly (CSS, JS, images)
- [ ] Custom 404 page displays for invalid URLs
- [ ] Browser console shows no routing errors
- [ ] CloudFront Function executes without errors (check CloudFront monitoring)

#### Task 1.5: Basic Layout & Styling Foundation (2 hours)
- **Description**: Create responsive layout foundation with Tailwind
- **Deliverables**:
  - Header with navigation
  - Footer with basic info
  - Responsive grid system
  - Typography scale established
  - Color scheme defined (minimal, clean)
- **Dependencies**: Tasks 1.3, 1.4
- **Priority**: High
- **Estimate**: 2 hours

**CSS Architecture Pattern Considerations**:
- Decide early whether to use utility classes directly in markup vs. CSS composition patterns
- Test your CSS approach in both global stylesheets and component-scoped styles
- Be aware that some CSS framework features may behave differently in scoped contexts
- Consider establishing a consistent styling pattern across components for maintainability

**Styling Verification Checklist**:
- [ ] Typography renders consistently across pages
- [ ] Responsive breakpoints work as expected
- [ ] Component styles don't conflict with global styles
- [ ] CSS framework utilities compile correctly in all contexts

### Phase 2: Core Features Implementation (8 hours)

#### Task 2.1: Blog Post Listing Page (2 hours)
- **Description**: Main blog page displaying list of published posts
- **Deliverables**:
  - Post listing with title, date, excerpt
  - Responsive card-based layout
  - Pagination (if needed for future)
  - Topic/category filtering capability
- **Dependencies**: Task 1.5
- **Priority**: Critical
- **Estimate**: 2 hours

#### Task 2.2: Individual Blog Post Template (2 hours)
- **Description**: Dynamic pages for individual blog posts
- **Deliverables**:
  - Post template with proper typography
  - Markdown rendering with proper styling
  - Post metadata display (date, topics)
  - Basic navigation (previous/next posts)
- **Dependencies**: Task 2.1
- **Priority**: Critical
- **Estimate**: 2 hours

#### Task 2.3: About Me Page (1 hour)
- **Description**: Static page with author information and background
- **Deliverables**:
  - Professional author bio
  - Contact information
  - Professional background/expertise
  - Consistent with site design
- **Dependencies**: Task 1.5
- **Priority**: Critical
- **Estimate**: 1 hour

#### Task 2.4: Content Collections & Topic System (2 hours)
- **Description**: Configure Astro content collections with taxonomy
- **Deliverables**:
  - Content collection schema with validation
  - Topic/category system in frontmatter
  - Automatic topic index pages
  - Related posts functionality
- **Dependencies**: Tasks 2.1, 2.2
- **Priority**: High
- **Estimate**: 2 hours

#### Task 2.5: Image Optimization Pipeline (1 hour)
- **Description**: Set up Astro's built-in image optimization
- **Deliverables**:
  - Automatic WebP conversion
  - Responsive image generation
  - Lazy loading configuration
  - Image compression settings
- **Dependencies**: Task 2.2
- **Priority**: Medium
- **Estimate**: 1 hour

### Phase 3: Polish & Production (4 hours)

#### Task 3.1: SEO & Meta Tags Configuration (1 hour)
- **Description**: Basic SEO setup for better discoverability
- **Deliverables**:
  - Dynamic meta tags for each page
  - Automatic sitemap generation
  - Basic OpenGraph tags
  - Proper title structure
- **Dependencies**: Tasks 2.1, 2.2, 2.3
- **Priority**: High
- **Estimate**: 1 hour

#### Task 3.2: Error Pages & Edge Cases (1 hour)
- **Description**: Create 404 and error handling pages
- **Deliverables**:
  - Custom 404 page with site navigation
  - Proper error handling for missing posts
  - Graceful degradation for edge cases
- **Dependencies**: Task 1.5
- **Priority**: Medium
- **Estimate**: 1 hour

#### Task 3.3: Performance Optimization & Testing (1 hour)
- **Description**: Optimize site performance and run lighthouse tests
- **Deliverables**:
  - Lighthouse score 90+ achieved
  - Core Web Vitals in "Good" range
  - CloudFront caching optimized
  - Asset optimization verified
- **Dependencies**: All previous tasks
- **Priority**: High
- **Estimate**: 1 hour

#### Task 3.4: Final Deployment & Validation (1 hour)
- **Description**: Production deployment with comprehensive testing
- **Deliverables**:
  - Production site fully deployed
  - All functionality verified
  - Performance metrics confirmed
  - CDN cache configuration validated
- **Dependencies**: All previous tasks
- **Priority**: Critical
- **Estimate**: 1 hour

---

## 🔒 Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| CDK deployment fails | Medium | High | Start with minimal stack, test incrementally, have rollback plan |
| AWS cost overrun | Low | Medium | Set up billing alerts, monitor usage, use cost calculator |
| Performance targets not met | Low | Medium | Use Lighthouse CI, optimize images, leverage CDN caching |
| Content workflow too complex | Low | Low | Test markdown workflow early, create documentation |
| Domain/DNS issues | Low | Medium | Start with CloudFront URL, add domain later |
| Timeline overrun (>20 hours) | Medium | Medium | Prioritize P0 features, defer nice-to-haves, track time closely |

### Mitigation Strategies

**Technical Risks**:
- Create CDK stack deployment checklist
- Test each component independently before integration
- Keep rollback scripts ready for each deployment

**Timeline Risks**:
- Focus on MVP features first (blog listing, individual posts, about page)
- Defer optimization tasks if timeline is tight
- Use existing Astro templates as starting point

**Performance Risks**:
- Set up Lighthouse CI early in development
- Use CDN-friendly caching headers
- Optimize images during development, not after

---

## 🧪 Testing Strategy

### Development Testing (Ongoing)
- **Local Development**: `npm run dev` for real-time testing
- **Build Validation**: `npm run build` before each deployment
- **Link Checking**: Verify all internal links work correctly
- **Mobile Responsiveness**: Test on various screen sizes

### CSS Compilation Testing
- **Framework Integration**: Verify CSS framework features compile correctly in development and production builds
- **Component Styling**: Test CSS in both global and component-scoped contexts
- **Build Validation**: Check for CSS-related warnings or errors during build process
- **Style Verification**: Ensure styles render correctly after deployment (not just in development)

### Performance Testing
- **Lighthouse Audits**: Target 90+ score on all metrics
- **Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1
- **Load Time Testing**: Verify <1 second page load target
- **CDN Performance**: Test from multiple geographic locations

### Content Testing
- **Markdown Rendering**: Verify all markdown syntax renders correctly
- **Image Loading**: Test image optimization and lazy loading
- **Topic System**: Verify categorization and filtering works
- **Navigation**: Test all internal links and page transitions

### Infrastructure Testing
- **CDK Deployment**: Verify infrastructure deploys without errors
- **S3 Access**: Confirm proper bucket permissions and access
- **CloudFront**: Verify CDN caching and distribution works
- **Error Handling**: Test 404 pages and error scenarios

### Acceptance Testing Checklist
- [ ] All three core pages load correctly
- [ ] Blog posts display with proper formatting
- [ ] About page displays author information
- [ ] Site loads in <1 second
- [ ] Mobile responsive on all screen sizes
- [ ] SEO meta tags present on all pages
- [ ] Images load and are optimized
- [ ] Navigation works correctly
- [ ] 404 page displays for invalid URLs

---

## 📈 Success Metrics & Monitoring

### Performance Metrics
- **Page Load Time**: < 1 second (Target: 0.5-0.8 seconds)
- **Time to First Byte**: < 200ms
- **Lighthouse Performance Score**: 90+
- **Core Web Vitals**: All metrics in "Good" range

### User Experience Metrics
- **Navigation Success**: All internal links work
- **Content Readability**: Proper typography and spacing
- **Mobile Experience**: Responsive on all devices
- **Error Handling**: Graceful 404 and error pages

### Technical Metrics
- **Deployment Success**: CDK deploys without errors
- **Uptime**: 99.9% (leveraging AWS reliability)
- **Cost Efficiency**: Monthly costs within $3-8 range
- **Build Performance**: Site builds in <2 minutes

---

## 🔗 Dependencies & Prerequisites

### External Dependencies
- **AWS Account**: With appropriate permissions for S3, CloudFront, Route53
- **Node.js**: Version 18+ for Astro and CDK
- **AWS CLI**: Configured with valid credentials
- **CDK CLI**: Global installation required

### Internal Dependencies
- **Content**: Initial blog posts in markdown format
- **Assets**: Any images or media files for the site
- **Domain** (Optional): Custom domain can be added later

### Blockers & Risks
- **AWS Permissions**: Ensure account has necessary IAM permissions
- **Regional Availability**: Confirm all AWS services available in target region
- **Content Preparation**: Have at least 1-2 sample blog posts ready

---

## 📅 Implementation Timeline

### Week 1: Foundation (Day 1)
- **Morning (4 hours)**: Tasks 1.1-1.3 (Environment setup, CDK init, Astro setup)
- **Afternoon (4 hours)**: Tasks 1.4-1.5 (Hello world deployment, basic layout)
- **Deliverable**: Working hello-world site deployed to AWS

### Week 1: Core Features (Day 2-3)
- **Day 2 (4 hours)**: Tasks 2.1-2.2 (Blog listing, individual posts)
- **Day 3 (4 hours)**: Tasks 2.3-2.5 (About page, content system, images)
- **Deliverable**: Fully functional blog with all core features

### Week 1: Polish (Day 3-4)
- **Day 3-4 (4 hours)**: Tasks 3.1-3.4 (SEO, error pages, optimization, final deployment)
- **Deliverable**: Production-ready blog meeting all success criteria

### Buffer Time
- **Built-in buffer**: Each task estimate includes small buffer
- **Contingency**: Can defer Task 2.5 (images) and Task 3.2 (error pages) if needed
- **MVP Scope**: Tasks 1.1-1.5, 2.1-2.3, 3.4 represent absolute minimum

---

## 📚 Documentation Plan

### Code Documentation
- **README.md**: Setup, development, and deployment instructions
- **Inline Comments**: Key CDK and Astro configuration explained
- **Deployment Guide**: Step-by-step CDK deployment process

### Content Documentation
- **Writing Guide**: Markdown format and frontmatter schema
- **Publishing Workflow**: Git commit to deployment process
- **Asset Guidelines**: Image optimization and file organization

### Operations Documentation
- **Monitoring**: How to check site performance and uptime
- **Troubleshooting**: Common issues and solutions
- **Cost Management**: AWS billing and optimization tips

---

## 🚀 Rollout Plan

### Phase 1: Soft Launch
- Deploy to CloudFront URL
- Test all functionality end-to-end
- Verify performance metrics
- Share with small group for feedback

### Phase 2: Content Population
- Add 2-3 initial blog posts
- Populate About page with complete information
- Verify content displays correctly

### Phase 3: Production Launch
- (Optional) Configure custom domain
- Announce availability
- Monitor performance and costs
- Plan content creation schedule

### Rollback Procedure
- **Infrastructure**: Use CDK destroy and redeploy previous version
- **Content**: Git revert to previous working commit
- **DNS** (if custom domain): Update DNS records to previous configuration

---

## 📋 Pre-Implementation Checklist

Before starting the CODE phase, verify:

- [ ] **Requirements Clear**: PRD and TECH_REQ documents reviewed and understood
- [ ] **Environment Ready**: Development machine set up with required tools
- [ ] **AWS Access**: Account configured with appropriate permissions
- [ ] **Timeline Confirmed**: 20-hour budget confirmed and schedule planned
- [ ] **Success Criteria Agreed**: All stakeholders understand what "done" looks like
- [ ] **Risk Mitigation**: Aware of potential issues and have mitigation plans
- [ ] **Content Ready**: At least 1-2 sample blog posts prepared for testing

---

## 🎯 Next Steps

1. **Review This Plan**: Confirm approach aligns with vision and requirements
2. **Environment Setup**: Install Node.js, AWS CLI, CDK CLI
3. **AWS Configuration**: Set up credentials and verify permissions
4. **Begin Implementation**: Start with Task 1.1 (Development Environment Setup)
5. **Track Progress**: Use TodoWrite to monitor task completion

### Recommended Flow
```bash
# Review and approve this plan
# Then proceed to implementation phase:
/epcc-code "Set up development environment and AWS CDK project"
```

---

**Implementation Plan Complete!** 🎉

This plan provides a clear roadmap from requirements to deployed blog. The approach balances simplicity with modern best practices, ensuring a high-performance result within the 20-hour budget.

Ready to move to the CODE phase when you are!