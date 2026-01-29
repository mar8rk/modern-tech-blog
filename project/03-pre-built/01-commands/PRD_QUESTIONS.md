# Product Requirements Questionnaire

**Project**: Personal Technology Blog
**Date**: October 22, 2024

**Foundation (from interactive session)**:
- **Vision**: Personal technology blog to share professional thoughts with tech audience, with full content ownership and control
- **Problem**: Need to own and control content while sharing tech insights online (vs. depending on third-party platforms)
- **Target Users**: Mixed professional tech audience (colleagues, developers, industry peers, potential employers) who want valuable tech insights
- **Inspiration**: Simple and straightforward approach like anildash.com and hidekazu-konishi.com
- **Success Vision**: Regular visitors who find content valuable enough to link to it

---

## Instructions

- Replace `[YOUR ANSWER]` with your response
- Be as detailed or brief as needed
- Skip optional sections marked (Optional) if not applicable
- Feel free to add notes/context anywhere
- **Save this file and run**: `/prd --process PRD_QUESTIONS.md`

---

## Section 1: Core Features

⚠️ **STAY NON-TECHNICAL**: Focus on WHAT users need to do, NOT HOW it will be implemented.

### 1.1 The ONE Must-Have Feature

**What's the ONE thing users absolutely must be able to do?**

render our blog page

**Why is this essential?**

the goal is a blog that people can read

---

### 1.2 User Journey

**Walk me through a typical user's journey from start to finish:**

Example format:
1. User arrives at...
2. User does...
3. System responds with...
4. User achieves...

the user arrives at our page and reads an article.

---

### 1.3 All Features List

**List all features/capabilities you envision (we'll prioritize in next questions):**

1. basic blog page
2. individual blog posts
3. about me page.

---

### 1.4 Feature Prioritization

**From your list above, which are MUST HAVE (P0) - can't launch without these:**

All are P0

**Which are SHOULD HAVE (P1) - important but can wait:**

N/A

**Which are NICE TO HAVE (P2) - future enhancements:**

N/A

---

### 1.5 Content & Navigation (if applicable)

**What types of content will users see?** (e.g., blog posts, pages, images, videos)

blog posts, main blog page, images.

**How should users navigate through the content?** (e.g., categories, search, chronological, filters)

categories and chronological

**What actions can users take?** (e.g., read, create, comment, share, subscribe, purchase)

just reading.

**What URL structure do you expect for your content?** (Select all that apply)
- [ ] Clean URLs without file extensions (e.g., `/blog`, `/about`)
- [ ] File-based URLs with extensions (e.g., `/blog.html`, `/about.html`)
- [ ] Directory-style URLs with trailing slashes (e.g., `/blog/`, `/about/`)
- [ ] No preference - whatever is easiest to implement

**Your Choice**: [YOUR ANSWER]

**How do you expect users to access pages?**

Example scenarios:
1. User types `/blog` directly in browser → Should this work? [Yes/No]
2. External link to `/about` (no trailing slash) → Should this work? [Yes/No]
3. User bookmarks `/blog/` (with trailing slash) → Should this work? [Yes/No]

**Your Expectations**: [YOUR ANSWER]

**If a user navigates to an invalid URL (e.g., `/nonexistent`), what should happen?**
- [ ] Show custom 404 error page
- [ ] Redirect to homepage
- [ ] Show CloudFront/server error page
- [ ] Other: [Specify]

**Your Choice**: [YOUR ANSWER]

---

### 1.6 Styling Architecture & CSS Framework Considerations (Optional)

**Do you have preferences or requirements for how styles are managed?**

Example considerations:
- Utility-first CSS frameworks (like Tailwind)
- Component-scoped styling
- Traditional global CSS
- CSS-in-JS approaches

**Your Preference**: [YOUR ANSWER or "No preference"]

**Are you aware of any compatibility considerations between CSS frameworks and your planned tech stack?**

Context: Some CSS frameworks have specific integration requirements or features that behave differently in various environments (e.g., scoped styles, build-time compilation, module systems).

**Your Awareness**: [YOUR ANSWER or "Not aware of specific issues"]

**How important is it that CSS framework features work identically in both global and component-scoped contexts?**

- [ ] Very important - Need consistency everywhere
- [ ] Somewhat important - Willing to adapt approach if needed
- [ ] Not important - Can use different patterns in different contexts

**Your Priority**: [YOUR ANSWER]

---

## Section 2: Technical Constraints

⚠️ **NOTE**: This captures constraints, NOT specific technology choices. Technology decisions happen in `/tech-req` command.

### 2.1 Deployment

**Where should this run?**
- [ ] Cloud (AWS/Azure/GCP)
- [ ] Local/On-premises
- [ ] Hybrid
- [ ] Other: [Specify]

**Your Choice**: AWS

**If Cloud, any provider preference?**
- [ ] AWS
- [ ] Azure
- [ ] GCP
- [ ] No preference

**Your Choice**: AWS

**Why this deployment approach?**

we already use AWS

**Infrastructure Approach:**

**Do you understand that CDK will create entirely new AWS infrastructure?**
- [x] Yes - I understand CDK provisions new S3 bucket, CloudFront distribution, and OAC
- [ ] No - Please explain

**Your Understanding**: Yes, CDK creates brand new infrastructure dedicated to this blog. I'll receive a unique CloudFront URL and all resources will be isolated in my AWS account.

**Are you comfortable with building from scratch (greenfield deployment)?**
- [x] Yes - I want dedicated infrastructure for my blog
- [ ] No - I prefer to use existing infrastructure
- [ ] Unsure - Need more information

**Your Choice**: Yes, I want complete control and isolation.

---

### 2.2 Scale & Performance

**How many people would use this at once?**
- [ ] Just me
- [ ] Small team (<10)
- [ ] Department (10-100)
- [ ] Organization (100-1000)
- [ ] Public internet (1000+)

**Your Choice**: small team

**Any performance requirements?** (e.g., page load time < 2s, response time < 500ms)

basic standards for load time.

---

### 2.3 Data & Integration

**Does this need to connect to any existing systems?** (APIs, databases, third-party services)

No

**If yes, what systems and why?**

[YOUR ANSWER]

**Do you need to store data?** (beyond simple static content)

No.

**If yes, what kind and how much?** (e.g., user profiles - 100 users, transaction logs - 10K/month)

[YOUR ANSWER]

**Do you need user authentication?**
- [ ] No authentication needed
- [ ] Single user only (just me)
- [ ] Multiple users (team/organization)
- [ ] Public users (anyone can sign up)
- [ ] Third-party login needed (Google, GitHub, etc.)

**Your Choice**: No auth

---

### 2.4 Team & Technology

**What's your team's technical comfort level?**
- [ ] Beginner - Prefer simple, managed solutions
- [ ] Intermediate - Comfortable with most tools
- [ ] Advanced - Can handle complex setups

**Your Choice**: intermediate.

**Any existing technologies you MUST use?** (company standards, existing stack, licensing)

no requirements

**Any technologies you MUST avoid?** (licensing issues, past problems, company policy)

no contraints

---

## Section 3: Constraints & Scope

### 3.1 Timeline

**When would you like this working?**

Today

**Any key milestones or deadlines?**

No

---

### 3.2 Budget

**Any budget constraints for infrastructure/hosting costs?**

No specific budget

**How much time can you invest in development?**

20 hours

---

### 3.3 Security & Compliance

**Any security or compliance requirements?** (HIPAA, SOC2, GDPR, data residency, etc.)

No

**If yes, explain:**

[YOUR ANSWER]

---

### 3.4 Maintenance

**What are you comfortable maintaining long-term?**

Yes, I can manage this.

---

### 3.5 Out of Scope

**What is explicitly OUT of scope for the first version?**

1. [YOUR ANSWER]
2. [YOUR ANSWER]
... (add as many as needed)

**If you had to cut features, what's the absolute minimum viable version?**

[YOUR ANSWER]

---

## Section 4: Success Metrics

### 4.1 User Success Metrics

**How will you know this is working well for users?**

We have a page loaded and working.

**What metrics would you track?** (e.g., daily active users, time on site, task completion rate)

1. daily users
2. time on site

---

### 4.2 Technical Success Metrics

**What technical metrics matter?** (e.g., uptime, response time, error rate)

uptime, response time.

**Any specific targets?** (e.g., 99% uptime, page load < 2s)

no specific targets

---

### 4.3 Acceptance Criteria

**What specific things must work for you to consider this "done"?**

- [ ] A deployed blog

---

## Section 5: User Journeys (Optional but Recommended)

### 5.1 Primary User Journey

**Describe the main user flow in detail:**

**Journey Name**: [e.g., "Professional discovers and reads tech article"]

1. User starts at: [Entry point]
2. User does: [Action]
3. System responds with: [Response]
4. User does next: [Next action]
5. User achieves: [Outcome/goal]

Professional discovers and reads tech article

---

### 5.2 Secondary User Journey (Optional)

**If applicable, describe a secondary important flow:**

**Journey Name**: [e.g., "Author publishes new article"]

N/A

---

## Section 6: Open Questions & Risks (Optional)

### 6.1 Open Questions

**Anything you're still unsure about?**

- [ ] [YOUR QUESTION]
- [ ] [YOUR QUESTION]
... (add as many as needed)

---

### 6.2 Risks & Concerns

**What could go wrong? What are you worried about?**

[YOUR ANSWER or "No major concerns"]

---

## Next Steps

**When you're done**:
1. Save this file
2. Run: `/prd --process PRD_QUESTIONS.md`
3. I'll generate your comprehensive PRD.md!