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

---

## Ready to Generate Tech-Req!

Once you've answered these questions, run:
```bash
/tech-req --process TECH_REQ_QUESTIONS.md
```

This will generate your comprehensive `TECH_REQ.md` document with all technology decisions documented and explained.