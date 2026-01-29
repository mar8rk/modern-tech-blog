# Exploration: Blog Frameworks for Static Site Generation

**Date**: January 29, 2026 | **Scope**: Medium | **Status**: ✅ Complete

## 1. Foundation (What exists)

**Tech landscape**: Static Site Generator ecosystem with mature options spanning multiple languages and approaches
**Architecture**: File-based content → Build process → Static HTML/CSS/JS → CDN hosting
**Structure**: Markdown/MDX content files, template systems, build toolchains, deployment pipelines
**CLAUDE.md instructions**: None found - greenfield project

## 2. Patterns (How it's built)

### Framework Categories by Architecture:

**React-based Static Generation**:
- **Next.js**: Full-stack framework with static export capabilities (137K+ GitHub stars)
  - Pattern: App Router + Static Generation + Markdown processing
  - When to use: Need React ecosystem, dynamic features, or complex interactivity
  - Setup time: ~15-30 minutes (framework complexity)

- **Astro**: Islands architecture with multi-framework support (53K+ stars)
  - Pattern: Component islands + Markdown/MDX + Minimal JS shipping
  - When to use: Want modern DX with optimal performance
  - Setup time: ~10 minutes (`npm create astro@latest`)

**Go-based Generators**:
- **Hugo**: Speed-focused with extensive theme ecosystem (86K+ stars)
  - Pattern: Go templates + Fast builds (<1s for large sites) + Git submodule themes
  - When to use: Large sites, need speed, established workflow
  - Setup time: ~5 minutes (`hugo new site` + theme)

**Ruby-based Traditional**:
- **Jekyll**: Blog-aware with GitHub Pages native support (51K+ stars)
  - Pattern: Liquid templates + Plugin ecosystem + GitHub Pages integration
  - When to use: GitHub-centric workflow, established Jekyll ecosystem
  - Setup time: ~15 minutes (Ruby dependencies + GitHub setup)

**Specialized Documentation**:
- **Docusaurus**: Facebook-backed for technical content (63K+ stars)
  - Pattern: React + Markdown + Versioning + Built-in search
  - When to use: Documentation-heavy tech blogs, need built-in features
  - Setup time: ~10 minutes

### Content Management Patterns:

**File-based Workflow** (Universal):
- Markdown files in `content/` or `posts/` directories
- Front matter for metadata (YAML/TOML)
- Git-based version control and publishing

**Syntax Highlighting Patterns**:
- **Prism.js**: Client-side highlighting (Jekyll, Gatsby)
- **Highlight.js**: Universal support across platforms
- **Shiki**: VS Code-powered highlighting (Astro, modern tooling)
- Built-in solutions: Hugo (Chroma), Docusaurus (integrated)

## 3. Constraints (What limits decisions)

### Technical Constraints:
- **Hugo**: Requires Go installation, theme as Git submodule
- **Jekyll**: Ruby dependencies, potential version conflicts
- **Next.js**: Node.js ecosystem, more complex build process
- **Astro**: Node.js required, relatively newer ecosystem

### Performance Characteristics:
- **Build Speed**: Hugo (fastest, <1s) > Astro ≈ Next.js > Jekyll (slowest, Ruby overhead)
- **Runtime Performance**: Astro (minimal JS) > Hugo (static) > Next.js (React hydration) > Jekyll (jQuery themes)
- **Bundle Size**: Hugo/Jekyll (minimal) > Astro (islands) > Next.js (full React)

### Deployment Constraints:
**GitHub Pages**: Native Jekyll support, others require build workflows
**Netlify/Vercel**: Universal support with auto-detection
**Free Tier Limits**: Build time limits (varies by platform)

### Quick Setup Requirements (ASAP timeline):
- Must have 1-command project creation
- Pre-built themes available
- Documentation must be clear and complete
- Community support for troubleshooting

## 4. Reusability (What to leverage)

### Theme Ecosystems:
**Hugo**: Largest theme ecosystem (500+ themes), academic/tech focus
- Example themes: PaperMod, Terminal, Academic
- Installation: `git submodule add [theme-url] themes/[name]`

**Jekyll**: Mature ecosystem, GitHub Pages compatible
- Example themes: Minima, Chirpy, Beautiful Jekyll
- Installation: Gem-based or fork-based

**Astro**: Growing ecosystem with modern designs
- Example themes: Blog template, Portfolio themes
- Installation: `npm create astro@latest -- --template [template]`

### Code Highlighting Solutions:
**Universal**: Prism.js, Highlight.js work across all platforms
**Platform-specific**: Hugo Chroma (fast), Astro Shiki (VS Code accuracy)
**Theme integration**: Most themes include pre-configured highlighting

### Modern Design Patterns:
- **Dark/Light mode**: Standard in modern themes
- **Mobile-first responsive**: Expected baseline
- **Typography focus**: Inter, Source Sans Pro, system fonts
- **Minimal aesthetics**: Clean, distraction-free reading

## 5. Handoff (What's next)

### For PLAN Phase:
**Recommended choice based on constraints**:
- **Primary**: **Hugo** - Fastest setup (5 min), excellent performance, mature ecosystem
- **Alternative**: **Astro** - Modern DX, optimal performance, growing ecosystem

**Key constraints to follow**:
- Must achieve <30 min from start to first post published
- Must support Markdown with code highlighting
- Must have clean, modern theme available
- Must support free deployment (Netlify/Vercel/GitHub Pages)

**Decision factors**:
1. **Setup speed**: Hugo > Astro > Jekyll > Next.js
2. **Learning curve**: Hugo ≈ Jekyll < Astro < Next.js
3. **Performance**: Astro ≈ Hugo > Jekyll > Next.js
4. **Theme quality**: Hugo > Jekyll > Astro > Next.js (for tech blogs)

### For CODE Phase:
**Tools and commands for chosen framework**:
- **Hugo**: `hugo new site`, `hugo server`, `hugo new posts/[name].md`
- **Astro**: `npm create astro@latest`, `npm run dev`, file creation in `src/content/`

**Deployment pipeline**:
- Git repository with automatic deploy on push
- Build command detection by platform
- CDN distribution for performance

### For COMMIT Phase:
**Quality gates**:
- Site builds without errors
- Pages load under 3 seconds
- Mobile responsive test passes
- Syntax highlighting works for major languages (JavaScript, Python, Go, etc.)

### Success Criteria Met:
✅ Identified frameworks meeting "ASAP" timeline requirement
✅ Found multiple options with excellent Markdown support
✅ Documented code highlighting solutions
✅ Confirmed free deployment options available
✅ Located modern, clean theme options

### Gaps Requiring Clarification:
- None - sufficient information gathered for implementation decision

**Recommended next step**: `/epcc-plan` with Hugo or Astro as primary options