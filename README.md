# GlowGain 🌿

> Daily skincare & weight-gain routine tracker with a **100% local AI coach** — runs entirely on your phone, no server, no API key, no cloud.

[![Deploy to GitHub Pages](https://github.com/xeno2426/glowgain/actions/workflows/deploy.yml/badge.svg)](https://github.com/xeno2426/glowgain/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 📋 **Daily Checklist** | Task blocks by time (Morning / Afternoon / Evening / Night) with per-day filtering (workout only Mon/Wed/Fri) |
| 🧠 **Local AI Coach** | Powered by [Transformers.js](https://github.com/huggingface/transformers.js) — runs SmolLM2 or TinyLlama **in your browser**, no internet after download |
| ⚖️ **Weight Tracker** | Daily logging, 7-day SVG trend chart, weekly gain feedback vs. +0.3–0.5 kg/week target |
| 🔥 **Streak System** | Overall, skincare, and diet streaks; 14-day heatmap; 8 unlockable badges |
| 📖 **Routine Guide** | Full reference for every step with tips and rationale |
| 📱 **PWA** | Install to home screen, works fully offline after first load |
| 🎉 **Confetti** | Fires on 100% day completion |

---

## 🤖 AI Coach System Prompt

The AI coach uses a **two-tier prompt system** tuned for small local models:

### Compact Prompt (SmolLM2 135M / 360M)
Short, structured, explicit — small models need brevity and clear directives:
```
You are GlowGain AI, a health coach. Be warm, short, specific.
ROUTINE: [full routine]
TODAY: Done: [...] | Pending: [...] | Completion: X% | Weight: Y kg | Streak: Z days
Rules: 2-4 sentences only. Reference their actual tasks. End with 1 question.
```

### Full Prompt (TinyLlama 1.1B+)
Rich context, nuanced coaching instructions, explicit rules — for models that can follow them:
- Persona definition with coaching style
- Full routine breakdown (morning → night)
- Live stats table (done tasks, pending, weight, streak)
- 8 explicit coaching rules (always acknowledge done tasks, never guilt-trip, etc.)
- A FORBIDDEN section (no generic advice, no multi-suggestions)

**Key design decisions:**
- System prompt is **rebuilt fresh on every message** with live data from localStorage
- Last 8 messages are included for conversation context
- `repetition_penalty: 1.15` reduces repetitive filler in small model replies
- Token leakage (leftover template tokens) is stripped via regex post-processing

---

## 📁 Repository Structure

```
glowgain/
├── index.html              # Full single-file PWA app
├── manifest.json           # PWA manifest (installable)
├── sw.js                   # Service worker (offline caching)
├── README.md
├── LICENSE                 # MIT
├── .gitignore
└── .github/
    └── workflows/
        └── deploy.yml      # Auto-deploy to GitHub Pages on push to main
```

---

## 🚀 Getting Started

### Option A — GitHub Pages (live, no setup)
1. Fork this repo
2. Go to **Settings → Pages → Source: GitHub Actions**
3. Push any change to `main` — deploys automatically
4. App lives at `https://xeno2426.github.io/glowgain`

### Option B — Termux on Android (fully offline)
```bash
# Install dependencies
pkg install python git

# Clone the repo
git clone https://github.com/xeno2426/glowgain.git
cd glowgain

# Serve locally
python -m http.server 3000
```
Open `http://localhost:3000` in Chrome → tap **⋮ → Add to Home Screen**.

### Option C — Any static host
Drop `index.html`, `manifest.json`, and `sw.js` into any static hosting (Netlify, Vercel, Cloudflare Pages).

---

## 🧠 AI Models

| Model | Size | Best for | Prompt type |
|-------|------|----------|-------------|
| **SmolLM2 135M** ⭐ | ~270 MB | Redmi 9i (2 GB RAM) — fastest | Compact |
| SmolLM2 360M | ~720 MB | Better replies, still fast | Compact |
| TinyLlama 1.1B | ~637 MB | Best quality, follows instructions best | Full |

All models use **4-bit quantization (q4)** via Transformers.js to fit in phone RAM.  
Downloaded once → **cached in browser cache** → works fully offline forever after.

---

## 📋 Routine Overview

| Time | Tasks |
|------|-------|
| **Morning** | Cetaphil wash → Pond's Gel moisturizer → UVROZ SPF50 → 2 chapatis + 2 eggs |
| **Afternoon** | Rice + dal + veg lunch; reapply sunscreen if outdoors |
| **Evening** | Milk + bananas (300+ cal); Workout on Mon/Wed/Fri |
| **Night** | Chapatis + sabzi/dal dinner → Cetaphil wash → Pond's Gel night |
| **Wed & Sat** | Sugar face scrub |
| **Sunday** | Chicken or fish |

**Goal:** +0.3–0.5 kg/week lean bulk + clear, glowing skin.

---

## 🔒 Privacy

- **All data stored locally** in `localStorage` — never sent anywhere
- **AI runs entirely in your browser** via WebAssembly — no API calls after model download
- No analytics, no tracking, no accounts

---

## 🛠️ Tech Stack

- **Vanilla JS + HTML + CSS** — zero build step, zero dependencies
- **[Transformers.js](https://github.com/huggingface/transformers.js) v3.5** — local LLM inference in browser
- **Service Worker** — offline PWA support
- **localStorage** — all persistence

---

## 📄 License

MIT © [xeno2426](https://github.com/xeno2426)
