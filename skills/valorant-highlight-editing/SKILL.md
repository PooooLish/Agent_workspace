---
name: valorant-highlight-editing
description: Plan, review, and produce Valorant / Wu Wei Qi Yue / tactical FPS kill-highlight montages from local gameplay footage. Use when Codex is asked to select clips, verify 4k/5k or ace evidence, build FFmpeg previews, prepare DaVinci Resolve / Premiere / CapCut workflows, choose BGM, design beat-synced effects, make vertical or horizontal exports for Bilibili, YouTube, Douyin/TikTok, or turn platform montage conventions into reusable editing rules.
---

# Valorant Highlight Editing

## Core Rule

Preserve competitive evidence first, then add style. A kill segment is valid only after the kill icon, ace/four-kill banner, round win, or other agreed confirmation is visible. Do not place transitions, flashes, zooms, or heavy motion blur over the confirmation frame.

## Quick Workflow

1. Inspect the task folder, local rules, current handoff, manifests, and preview outputs.
2. Classify source clips by evidence strength:
   - `explicit_4k5k`: readable personal four/five-kill or ace-style banner.
   - `team_wipe_candidate`: team result visible but personal count unconfirmed.
   - `high_count_candidate`: dense kill chain but exact count unconfirmed.
   - `excluded`: corrupt, weak, three-kill filler, or unclear.
3. Build the cut from strongest sources first. Do not pad runtime with uncertain clips.
4. Keep the meaningful kill chain from any selected source through final confirmation unless the user asks for isolated moments.
5. Sync edits to music only after gameplay evidence is safe.
6. Verify the render with full decode plus contact sheets around freeze/transition moments.

## Style Process

For platform-inspired editing patterns, read `references/platform_style_patterns.md`.
For source links and refresh prompts, read `references/research_sources.md` only when updating the skill or checking current tool/platform assumptions.

Use this order:

1. **Hook:** open with the cleanest final-kill, ace, flick, operator shot, or clutch confirmation.
2. **Build:** let aiming, crosshair correction, utility reveal, and recoil control remain readable.
3. **Impact:** on confirmed kill frames, use short punch-ins, exposure flashes, hit markers, whoosh/hit SFX, or sub-8-frame shake.
4. **Release:** after the final confirmation, add a cloned-frame hold, flash card, hard cut, dip-to-black, or beat-synced transition.
5. **Reset:** give the next clip a readable first frame so viewers know map, angle, weapon, and threat.

## Toolchain Choice

For software selection and handoff patterns, read `references/software_toolchain.md`.

Default guidance:

- Use FFmpeg for deterministic scripted previews, contact sheets, verification, and batch exports.
- Use DaVinci Resolve when color, sound, Fusion effects, or a professional NLE project is needed.
- Use Adobe Premiere when the user already works in Adobe or needs After Effects / plugin workflows.
- Use CapCut/Jianying or Bcut/Bijian for fast short-form versions, captions, templates, and mobile/social publishing.
- Do not install or launch external GUI software without user approval.

## Export Standards

Use these defaults unless the user requests otherwise:

- Master preview: 1920x1080, 60 fps, H.264 high bitrate, AAC 192k+.
- YouTube/Bilibili horizontal: 1920x1080 or 2560x1440, 60 fps.
- Douyin/TikTok vertical: 1080x1920, 60 fps, reframed with crosshair/action safe.
- Keep a clean master without platform captions or watermarks.

## Quality Gates

Before reporting completion:

- Full-decode the output with FFmpeg.
- Generate timed sheets or freeze sheets at transitions and final-kill confirmations.
- Confirm transitions start after confirmation frames.
- Confirm BGM licensing/attribution if publishing.
- Update task coordination notes, selection notes, and export registries.
