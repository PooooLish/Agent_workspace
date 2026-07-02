# Software Toolchain

## External Software Policy

External editing software is allowed when it improves quality or handoff, but follow these rules:

- Check whether the software is already installed before planning around it.
- Ask for approval before installing software, launching GUI apps, signing in, or using paid/cloud features.
- Keep original footage in the task's raw footage folder.
- Export renders, project files, logs, and scratch media into the task workspace.
- Maintain a scripted FFmpeg path when reproducibility matters.

## Recommended Roles

FFmpeg:
- Deterministic trims, concat previews, contact sheets, loudness checks, metadata checks, transcodes, and full-decode verification.
- Best when an agent must render repeatably without GUI interaction.

DaVinci Resolve:
- Best all-in-one route for manual polish: edit, color, Fusion motion graphics, Fairlight audio, and final deliver.
- Good when the montage needs cinematic color, audio shaping, refined keyframes, or a project file for human review.

Adobe Premiere / After Effects:
- Best when the user already works in Adobe or wants plugin-heavy edits, dynamic links, motion graphics, or handoff to a Premiere editor.
- Use Premiere for timeline assembly and After Effects for more complex compositing.

CapCut / Jianying:
- Best for fast short-form social versions, template-style captions, mobile-friendly effects, and vertical exports.
- Avoid overusing stock effects that obscure proof frames.

Bcut / Bijian:
- Useful for Bilibili-oriented packaging, quick captions, and creator-platform convenience.
- Keep a clean master outside the app before adding platform-specific overlays.

## Project Handoff

When using an NLE:

1. Keep a script-generated reference preview.
2. Create a project folder under `project_files/`.
3. Put rendered drafts in `outputs/previews/`.
4. Put final exports in `outputs/final/`.
5. Register exports in `manifests/export_registry.csv`.
6. Note non-scriptable manual decisions in `coordination/decision_log.md`.

## Baseline Render Settings

Master:
- 1920x1080, 60 fps, H.264 or ProRes/DNxHR intermediate when editing further.
- Preserve high bitrate for FPS motion; avoid heavy compression before final platform upload.

Audio:
- Keep game audio audible for hit confirmation.
- Duck BGM slightly around dense kill chains.
- Add SFX sparingly: impact hits, risers, downlifters, and whooshes should reinforce the edit, not replace gameplay.

Verification:
- Full FFmpeg decode.
- Contact sheet at regular intervals.
- Freeze sheet at final-kill confirmations.
- Manual visual check for banner/crosshair/caption overlap.
