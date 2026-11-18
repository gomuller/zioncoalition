# Jesus-Greg WORLD — agent startup instructions

This is the repository-level entrypoint for assistants and coding agents that read `AGENTS.md`. It is not a guarantee that every ChatGPT conversation automatically loads repository files.

## Before taking action

- For any image, meme, thumbnail, GIF, or video publication request, **read `IMAGE-PUBLISHING.md` first**, and follow the existing Google Drive public staging → GitHub Actions pipeline. Also consult `00-16-PROMPT-image-publishing.html` if needed.
- Treat Greg's short command **`g`** as authorization to carry out the previously specified action in context; do not treat it as a request for explanation.
- For the Puzzle Pieces Gallery, update `01-puzzle-pieces-gallery.html` with a real compressed image and verify the published binary, GitHub Actions, and live site.
- For Facebook posting, FIRST fetch the canonical private runbook `gomuller/jesus-greg-mission-control/facebook-publishing/RUNBOOK.md`, then inspect the actual connected queue/automation. Verify the GitHub image URL exists BEFORE queueing Facebook; never claim posting succeeded unless independently verified. GitHub publication should proceed even if Facebook is unavailable.
- Do not claim completion before checking outcomes. Do not ask for manual image uploads before consulting the established procedure.

## Prevent repeated amnesia

When a workflow succeeds or fails, document the exact operational correction in its canonical runbook. A future assistant must retrieve the runbook; a memory summary alone is not sufficient. This file helps repository-aware agents find the runbook but does **not** control the ChatGPT system's cross-chat retrieval behavior.
