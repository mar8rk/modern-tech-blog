# Technical Requirements Questionnaire

**Project**: Personal Technology Blog
**Date**: October 22, 2024
**Your Decisions So Far**:
- Architecture: Static Site Generator (SSG) + JAMstack
- Cloud Provider: AWS
- Framework: Astro

---

## Instructions

- Replace `[YOUR ANSWER]` with your response
- For multiple choice, select one option or write your own
- Feel free to add notes/context
- **Save this file and run**: `/tech-req --process TECH_REQ_QUESTIONS.md`

---

## Section 1: Styling Approach

Based on your Astro choice, here's what works well:

**Q1.1: CSS Framework**
- [ ] Tailwind CSS - Utility-first, rapid development, great for clean designs, integrates perfectly with Astro
- [ ] Custom CSS - Full control, more time-consuming, learning opportunity, simple approach
- [ ] [Other]: [Specify if you have a preference]

**Your Choice**: tailwind CSS

**Q1.2: Why this choice?**
[YOUR ANSWER - Optional]

**Q1.3: CSS Architecture Pattern Preference**

How do you prefer to write styles?

- [ ] **Utility classes in markup** - Use framework utilities directly in HTML/JSX (e.g., `<div class="flex items-center">`)
  - Most compatible, works everywhere
  - More verbose but explicit

- [ ] **CSS composition** - Compose utilities using @apply or similar (e.g., `.button { @apply bg-blue-500 px-4; }`)
  - DRY approach, familiar CSS patterns
  - May have compatibility considerations in some contexts

- [ ] **Hybrid approach** - Mix both patterns as appropriate
  - Flexibility to use best tool for each situation
  - Requires clear guidelines for consistency

- [ ] **No preference** - Will adapt based on what works best

**Your Choice**: [YOUR ANSWER]

**Q1.4: CSS Framework Compatibility Awareness**

Are you aware that some CSS framework features (like @apply directives, CSS modules, or custom functions) may behave differently in:
- Global stylesheets vs. component-scoped styles
- Development mode vs. production builds
- Different versions of the same framework

**Your Awareness**:
- [ ] Yes - I understand there may be compatibility considerations
- [ ] Somewhat - I'm aware issues can occur but not sure of specifics
- [ ] No - This is new information

**How comfortable are you adapting your CSS approach if compatibility issues arise?**
- [ ] Very comfortable - I can switch patterns easily
- [ ] Somewhat comfortable - Prefer to test early and adjust if needed
- [ ] Not comfortable - Need clear guidance on what will work

**Your Comfort Level**: [YOUR ANSWER]

**Q1.5: CSS Compilation Testing Approach**

How will you verify that your CSS approach works correctly?

**Testing priorities** (check all that apply):
- [ ] Test in development mode
- [ ] Test in production build mode
- [ ] Test in both global and component-scoped contexts
- [ ] Test after deployment to ensure styles render correctly
- [ ] Verify CSS compilation without errors or warnings

**Any specific CSS testing concerns?** [YOUR ANSWER or "None"]

---

## Section 2: Content Management

**Q2.1: How will you manage content?**

Based on single author blog:
- [ ] Git-based (Markdown files) - Version controlled, developer-friendly, works perfectly with Astro
- [ ] Headless CMS (Contentful, Strapi) - Web interface for writing, $0-50/month, adds complexity
- [ ] [Other]: [Specify]

**Your Choice**: Git based markdown

**Q2.2: Content workflow preference**
 locally in markdown and push

---

## Section 3: AWS Infrastructure Details

**Q3.1: AWS Services for Static Hosting**

For Astro SSG on AWS, recommend:
- [ ] S3 + CloudFront + Route53 - Simple, managed, ~$3-8/month, industry standard
- [ ] S3 + CloudFront + GitHub Actions - Same as above but with automated deployment
- [ ] AWS Amplify - Fully managed static hosting, ~$1-15/month, handles everything
- [ ] [Other]: [Specify if you have preferences]

**Your Choice**: S3 + Cloudfront

**Q3.2: Domain Setup**
- [ ] I have a domain: [YOUR DOMAIN NAME]
- [ ] Need to register a domain
- [ ] Will decide later

**Your Choice**: Will decide later

**Q3.3: Infrastructure Deployment Type**
- [x] Greenfield (Create brand new infrastructure from scratch)
- [ ] Brownfield (Use/modify existing infrastructure)
- [ ] Hybrid (Mix of new and existing)

**Your Choice**: Greenfield - CDK will create all new resources

**Q3.4: Infrastructure Understanding**

Please confirm your understanding of what CDK will create:
- [x] New S3 bucket: `tech-blog-{account}-{region}` for my blog only
- [x] New CloudFront distribution with unique URL (e.g., `https://d1234abcd.cloudfront.net`)
- [x] New Origin Access Control (OAC) for secure S3 access
- [x] New CloudFormation stack I own and control
- [x] Complete infrastructure isolation (not shared with anyone)
- [x] Clean teardown available via `cdk destroy`

**Your Understanding**: I understand this creates entirely new infrastructure dedicated to my blog. All resources are isolated in my AWS account and I receive a unique CloudFront URL.

---

## Section 4: CI/CD & Deployment

**Q4.1: Deployment Automation**
- [ ] Automated (GitHub Actions deploys on git push) - Recommended for blogs
- [ ] Manual (run deploy script when ready) - Simple, more control over timing
- [ ] [Other]: [Specify]

**Your Choice**: Manual

**Q4.2: Deployment frequency**
How often will you publish new blog posts?
- [ ] Multiple times per week
- [ ] Once per week
- [ ] Few times per month
- [ ] Once per month or less

**Your Choice**: Once per week
---

## Section 5: Blog-Specific Features

**Q5.1: Do you want RSS feed generation?**
- [ ] Yes - Automatic RSS feed for subscribers
- [ ] No - Not needed initially
- [ ] Undecided

**Your Choice**: not initially.

**Q5.2: Syntax highlighting for code blocks?**
- [ ] Yes - Essential for tech blog (Prism.js or Shiki)
- [ ] Basic - Simple highlighting only
- [ ] No - Plain text code blocks

**Your Choice**: plain text code block.

**Q5.3: Blog post categories/tags?**
- [ ] Yes - Organize posts by topics
- [ ] No - Keep it simple, no categorization
- [ ] Maybe later

**Your Choice**: yes, by topics.

---

## Section 6: Performance & SEO

**Q6.1: Image optimization**
- [ ] Automatic - Astro's built-in image optimization
- [ ] Manual - I'll optimize images myself before adding
- [ ] Not concerned - Basic approach

**Your Choice**: automatic.

**Q6.2: SEO requirements**
- [ ] Full SEO optimization - Meta tags, OpenGraph, sitemap, structured data
- [ ] Basic SEO - Just title and description tags
- [ ] Minimal - Don't worry about SEO initially

**Your Choice**: minimal
---

## Section 7: Analytics & Monitoring

**Q7.1: Do you need analytics?**
- [ ] Yes - Basic (Google Analytics or similar)
- [ ] Yes - Privacy-focused (Plausible, Fathom)
- [ ] No - Not needed initially
- [ ] Undecided

**Your Choice**: not initially.

If yes, any preferences?
[YOUR ANSWER]

**Q7.2: Uptime monitoring**
- [ ] Yes - Get notified if site goes down
- [ ] No - AWS is reliable enough
- [ ] Maybe later

**Your Choice**: maybe later

---

## Section 8: Additional Requirements

**Q8.1: Any specific design preferences?**
Examples: Dark mode toggle, specific color scheme, typography preferences, etc.

not now.

**Q8.2: Any other technical requirements or concerns?**
Examples: Accessibility requirements, specific integrations, newsletter signup, etc.

This should be deployed via CDK.

**Note on MIME Types**: I understand there's a known issue with CloudFront/S3 serving CSS/JS files with incorrect Content-Type headers. I'm aware that:
- CSS files may be served as `text/plain` instead of `text/css`
- This causes browsers to refuse rendering styles
- The CDK stack handles this automatically through proper configuration
- If I encounter this, I have troubleshooting steps available in TECH_REQ.md

---

## Section 9: Infrastructure & Deployment Awareness

**Q9.1: CloudFront/S3 MIME Type Issue Awareness**

Are you aware of the potential MIME type issue when serving static files from S3 through CloudFront?
- [x] Yes - I understand CSS/JS may be served with wrong Content-Type
- [ ] No - Please explain

**Your Understanding**: Yes, I understand that S3 may sometimes serve CSS files as `text/plain` instead of `text/css`, causing browsers to refuse loading styles. The CDK stack prevents this, but if it occurs, I know how to:

1. Verify S3 metadata: `aws s3api head-object --bucket tech-blog-{account}-{region} --key _astro/main.css`
2. Fix Content-Type if needed: `aws s3 cp` with `--content-type "text/css" --metadata-directive REPLACE`
3. Invalidate CloudFront cache: `aws cloudfront create-invalidation --distribution-id {ID} --paths "/*"`
4. Clear browser cache and reload (Cmd+Shift+R / Ctrl+Shift+F5)

**Q9.2: MIME Type Prevention**

How will the CDK stack prevent MIME type issues?
- [x] Astro builds files with correct extensions (.html, .css, .js)
- [x] S3 auto-detects MIME types from standard extensions
- [x] CDK triggers CloudFront cache invalidation on deployment
- [x] BucketDeployment handles file uploads correctly

**Your Understanding**: The infrastructure is designed to prevent this issue through proper build output, S3 auto-detection, and automatic cache invalidation.

**Q9.3: Infrastructure Isolation Model**

Do you understand the infrastructure isolation model?
- [x] Yes - All resources are in MY AWS account only
- [x] Yes - CloudFront URL is unique to my blog
- [x] Yes - No shared infrastructure with other users
- [x] Yes - I have complete control over all resources

**Your Understanding**: I understand that CDK creates dedicated infrastructure for my blog only. All resources (S3 bucket, CloudFront distribution, OAC) are isolated in my AWS account and not shared with anyone else.

---

## Section 10: Static Site Routing & URL Structure

**Q10.1: Static Site Output Structure Awareness**

Astro and other SSGs generate static files in different ways. Understanding this is critical for CDN configuration.

**Do you understand how Astro outputs files?**
- [ ] Yes - I know Astro generates `/blog/index.html` for clean URLs
- [ ] No - Please explain
- [ ] Unsure - Need more information

**Your Understanding**: [YOUR ANSWER]

**Background**: Astro generates directory-based output:
- `/blog` page → generates `/blog/index.html` file
- `/about` page → generates `/about/index.html` file
- Root page → generates `/index.html` file

This structure enables clean URLs but requires special CDN configuration.

---

**Q10.2: CloudFront Directory Routing Challenge**

Are you aware that CloudFront requires special configuration to serve directory-style URLs?

**The Issue:**
- CloudFront's `defaultRootObject` only applies to root path `/`
- Requests to `/blog` are NOT automatically mapped to `/blog/index.html`
- Without configuration, users get 403 "Access Denied" errors

**Are you aware of this limitation?**
- [ ] Yes - I understand CloudFront needs URL rewriting for clean URLs
- [ ] No - This is new information
- [ ] Partially - I knew there might be routing issues

**Your Understanding**: [YOUR ANSWER]

---

**Q10.3: URL Routing Solution Preference**

How should the infrastructure handle directory-style URLs?

**Options:**
- [ ] **CloudFront Function** - Lightweight URL rewriting (<1ms, $0.10/1M requests)
  - Rewrites `/blog` → `/blog/index.html` before S3 request
  - Best for simple URL normalization
  - Recommended for most static sites

- [ ] **Lambda@Edge** - Full programming capabilities (higher latency & cost)
  - More powerful but overkill for basic routing
  - Use only if complex logic needed

- [ ] **S3 Website Hosting** - Built-in routing rules
  - No HTTPS support (major limitation)
  - Less CDN control
  - NOT recommended for production

- [ ] **File-based URLs** - No rewriting needed
  - Users see `.html` in URLs (e.g., `/blog.html`)
  - Poor user experience
  - NOT recommended

**Your Choice**: [YOUR ANSWER]

**If CloudFront Function, confirm understanding:**
- [ ] Function executes on every request (viewer-request event)
- [ ] Adds index.html to directory requests automatically
- [ ] Handles trailing slash normalization
- [ ] No performance impact (<1ms execution time)
- [ ] Minimal cost ($0.10 per 1 million requests)

---

**Q10.4: URL Routing Test Requirements**

What URLs must work correctly after deployment? (Check all that apply)

**Critical URL Patterns:**
- [ ] Root path `/` serves homepage
- [ ] `/blog` (no trailing slash) serves blog listing
- [ ] `/blog/` (with trailing slash) also works
- [ ] `/about` serves about page
- [ ] Individual post URLs work (e.g., `/blog/first-post`)
- [ ] Static assets load (CSS, JS, images from `/_astro/` path)
- [ ] Invalid URLs return custom 404 page (not CloudFront error)

**Your Testing Checklist**: [Select all that apply above]

---

**Q10.5: CDN Routing Troubleshooting Awareness**

If after deployment `/blog` or `/about` return 403/404 errors, do you know how to troubleshoot?

**Troubleshooting Steps** (Check what you're comfortable doing):
- [ ] Verify CloudFront Function is attached to distribution
- [ ] Check function code includes URL rewriting logic
- [ ] Redeploy CDK stack to apply changes
- [ ] Invalidate CloudFront cache to clear stale content
- [ ] Test URLs after 2-3 minute propagation delay
- [ ] Check browser console for routing errors

**Your Comfort Level**: [YOUR ANSWER - e.g., "Need guidance", "Mostly comfortable", "Fully confident"]

---

**Q10.6: Alternative URL Structures Considered**

Have you considered alternatives to clean URLs?

**If facing routing complexity, alternatives include:**
- File-based URLs (`.html` extensions) - Eliminates routing issues but poor UX
- Hash-based routing (`/#/blog`) - Client-side only, bad for SEO
- Query parameters (`/?page=blog`) - Awkward for users

**Are you willing to use file-based URLs if routing proves difficult?**
- [ ] No - Clean URLs are essential for professional appearance
- [ ] Maybe - If it significantly simplifies deployment
- [ ] Yes - I don't mind `.html` in URLs

**Your Stance**: [YOUR ANSWER]

---

## Ready to Generate Tech-Req!

Once you've answered these questions, run:
```bash
/tech-req --process TECH_REQ_QUESTIONS.md
```

This will generate your comprehensive `TECH_REQ.md` document with all technology decisions documented and explained.