---
name: yozhkinroll
description: Specialized skills for Yozhkin Roll website design, Tilda integration, and SEO optimization.
---

# Yozhkin Roll: Rich Aesthetic & Tilda Integration (V4+)

This skill defines the technical standards, design language, and deployment protocols for the "Yozhkin Roll" project.

## 🎨 1. Design Language: "Rich Dark" & "Nova V26"
- **Color Palette:** 
    - EZ-Orange: `#ff7a00`
    - Background: Deep Dark `#111` for loyalty/footer, Soft White `#f8f8f8` for content.
- **Visual Effects:** 
    - **Glassmorphism**: `backdrop-filter: blur(10px)`, transclucent backgrounds, and thin borders (`rgba(255,255,255,0.1)`).
    - **Glow & Depth**: Strategic use of radial gradients for ambient lighting.
- **Typography:** 
    - **Outfit**: Premium headlines (font-weight 700-800, uppercase).
    - **Inter**: High-readability body text.

## 🧱 2. Master Component Architecture
- **Consolidated Styles**: All global CSS lived in `PRODUCTION/ui/master_styles.css`. No local overrides in individual blocks if possible.
- **SEO & Head Enrichment**: All `<head>` metadata, Schema.org JSON-LD, and OG tags are managed in `PRODUCTION/ui/seo_head.html`.
- **Component isolation**: Classes prefixed with `.nova-` or `.magic-` to avoid Tilda system collisions.

## 📈 3. SEO & Conversion Standards
- **Schema.org**: Extensive `Restaurant` & `OfferCatalog` markup in `seo_head.html`.
- **Typography SEO**: Strict use of `H1` (Main Hero), `H2` (Section Titles), and `H3` (Component Subtitles) with local target keywords (Сочи, Адлер, Сириус).
- **Hanging Conjunctions**: Never leave single-letter conjunctions (и, с, в, на) at the end of a line. Use `&nbsp;`.

## 📱 4. Mobile UX Best Practices
- **2-Column Grid**: Active on mobile for product cards using `.uc-nova-card`.
- **Padding Reset**: Reduced vertical spacing (`40px`) on mobile to avoid gaps.
- **Typography Scaling**: Fluid font sizes using `clamp()`.

## 🛠️ 5. Deployment Workflow (Tilda)
1.  **CSS**: Paste `PRODUCTION/ui/master_styles.css` into Site Settings -> Custom CSS.
2.  **HEAD**: Paste `PRODUCTION/ui/seo_head.html` into Site Settings -> HEAD.
3.  **Blocks**: Copy individual template files into T123 blocks sequentially as mapped in `master_home.html`.
