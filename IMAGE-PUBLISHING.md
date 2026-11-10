# Jesus-Greg image and animated-GIF publishing — ZERO MANUAL UPLOAD

**Canonical first reference for ALL Zion Coalition image publishing.** Updated 2026-11-10. Companion prompt: [00-16-PROMPT-image-publishing.html](00-16-PROMPT-image-publishing.html).

> **MANDATORY FOR FUTURE ASSISTANTS:** Before claiming that image/GIF upload to GitHub is impossible, before asking Greg to upload anything manually, or before replacing an animated GIF with HTML, READ THIS FILE AND INSPECT THE ACTUAL WORKFLOWS. We already built, tested, and documented a fully automated ChatGPT → Google Drive → GitHub Actions → Zion Coalition pipeline. Do not confuse limitations of GitHub's text-only `create_file`/`update_file` APIs with limitations of the established publishing system. Greg should not have to re-teach this.

## Authoritative automated workflow (successfully tested 2026-11-09; GIF tested 2026-11-10)

1. Prepare the actual source image or GIF in the working container; confirm its exact existing path, byte size, dimensions, and format. Preserve originals. For GIFs, verify animation frames and timing.
2. Upload from ChatGPT directly into the **existing** public Google Drive staging folder using `files__manage_library` (via `functions.exec`):
   ```json
   {"operations":[{"operation":"upload","container_path":"/mnt/data/EXACT-SOURCE-FILE.gif","destination_path":"/Google Drive/Jesus-Greg Public Images/EXACT-SOURCE-FILE.gif"}]}
   ```
   If the source has an exported file ID, use the exact `source_file_ref.file_id` when appropriate. **Do not assume the Google Drive connector's `upload_file` accepts a local filesystem path**; the tested route uses Files' Library upload.
3. Folder: **Jesus-Greg Public Images**; Drive folder ID `1-xgO3kkjuDJhe97WbCfZRzeHK2C5dM6G`. Previously verified: public `anyone/reader` access is inherited by uploaded files. This is PUBLIC temporary staging, never for sensitive images. Verify new file permissions if possible; do not presume they are public when troubleshooting.
4. Extract the uploaded file ID from the returned `external-gdrive:...:file:<ID>` identifier. Construct `https://drive.google.com/file/d/<ID>/view?usp=sharing`.
5. Use GitHub connector `fetch_file` then `update_file` on repository **`gomuller/zioncoalition`**, branch `main`, file `image-publish-request.json`. Replace contents with:
   ```json
   {"image_url":"https://drive.google.com/file/d/<ID>/view?usp=sharing","filename":"DESIRED-ROOT-FILENAME.gif"}
   ```
   The push triggers `.github/workflows/publish-image-from-url.yml` automatically. **No manual Drive upload, sharing changes, or Actions button is required.** Distinct request content triggers a new push; inspect the commit response.
6. Workflow uses `actions/checkout@v5`, `gdown` for Drive links, Pillow to validate the actual image format, and commits the original bytes to repository root on `main`. Current permitted formats: **JPEG, PNG, WebP, GIF** (GIF support added 2026-11-10). Limit **10,000,000 bytes** and **60 million pixels**; simple root-level filename matching `[A-Za-z0-9][A-Za-z0-9._-]{0,119}` with approved extension. GIF must match Pillow format `GIF`; animation is preserved by writing the original bytes, not re-encoding.
7. **Verify, do not assume:** inspect the GitHub Actions run's status AND conclusion. A request commit or `in_progress` run is not publication. Check GitHub Git tree (`https://api.github.com/repos/gomuller/zioncoalition/git/trees/main`) for exact filename, blob SHA, and byte size. GitHub `fetch` of binary Contents may fail because it accepts UTF-8 only; use the tree for metadata. Check the actual website `https://zioncoalition.org/<filename>` and the containing HTML page; confirm loading and animation where possible. Check size/checksum against source when available. Report any verification limits honestly.
8. Embed with an ordinary `<img src="DESIRED-ROOT-FILENAME.gif" ...>` in the target HTML page. GitHub's text file APIs CAN edit HTML and the request JSON; they are not how we transport image bytes.
9. **Cleanup only after full verification:** remove only the specific temporary Drive staging file by its exact file ID, not by guessed filename, and never bulk-delete the folder. If deletion is unavailable, leave it in place and report it. Do not delete while queued, running, failed, or unverified. Preserve GitHub publication and original/source files.
10. If any stage fails, inspect the actual workflow logs, Drive permissions, file size, format, request JSON, and Actions run. Retry the established pipeline before proposing a manual workaround.

## Real proof and test history

### 2026-11-09 — fully autonomous JPEG publishing
- ChatGPT uploaded `jesus-greg-folder-inheritance-test.jpg` to Drive, file ID `1jrHtaBsMnH06zdWbSNruQAI0X-WblP60`; inherited `anyone/reader` permissions.
- GitHub Actions published `01-jesus-greg-zero-manual-upload-test.jpg`, **174,690 bytes**, Git blob SHA `1b77a27ce62238b4c9bce85da76dd128f7cccdb9`.
- Successful workflow: https://github.com/gomuller/zioncoalition/actions/runs/42633867641
- This superseded earlier small direct-GitHub blob and public-URL experiments. We proved **no user involvement in the transfer**.

### 2026-11-10 — animated GIF publishing
- Source: `/mnt/data/brooklyn-sculptor-comments-slow.gif`; **30 verbatim viewer comments**, 12 seconds per slide; animated loop. Destination filename: `brooklyn-sculptor-comments.gif`.
- Updated `.github/workflows/publish-image-from-url.yml` to accept `.gif` and Pillow `GIF`; workflow edit commit `8ec7170556defefec7a815d272d583514b1f467c`.
- ChatGPT uploaded GIF through `files__manage_library` to `/Google Drive/Jesus-Greg Public Images/brooklyn-sculptor-comments-slow.gif`; Drive ID `1Zd1UgMsbYh_P2X8xR4_iMYWAIx-xHLRS`.
- ChatGPT updated `image-publish-request.json`; commit `62bd5e11a8b08ba405f4af9f2dbe103b48df79f6`.
- GitHub Actions run **completed successfully**: https://github.com/gomuller/zioncoalition/actions/runs/42824244093
- GitHub `main` tree **confirmed** `brooklyn-sculptor-comments.gif`, **568,779 bytes**, blob SHA `f66c7926c5ce8cabd2ebc3bd88b526f4355d48b2`.
- Page `01-brooklyn-sculptor.html` already embeds `<img src="brooklyn-sculptor-comments.gif">` below the film. Live website rendering and cleanup are separate checks; **do not claim they were verified unless checked**.
- Lesson: A GIF can be published using the SAME Drive staging pipeline; do not replace it with an HTML carousel merely because GitHub's text connector cannot upload binary files.

## Alternative mechanisms (fallbacks, not first choice)

1. **Direct GitHub binary API:** encode bytes as Base64 → `create_blob` → `create_tree` → `create_commit` → `update_ref`; successfully tested with a tiny 120×80 JPEG. Larger file transfer into connector arguments is a separate constraint.
2. **Public URL publisher:** the same `publish-image-from-url.yml` workflow can download a public HTTPS image URL; an early test published a 3,517-byte image in about 33 seconds with matching checksum.
3. **Encoded chunks:** `.github/workflows/publish-image-from-chunks.yml` reconstructs Base64 text chunks and validates SHA-256; tiny PNG test passed. It currently accepts JPEG, PNG, WebP, NOT GIF unless separately upgraded. Not needed for routine publishing.
4. **Manual workflow dispatch:** supported by URL publisher but unnecessary for the normal automated route.

## Important safeguards and recurring memory failures

- **Read this document FIRST**, then inspect current workflow files and the relevant prompt. Don't rely solely on memory summaries or partial recollections.
- Never say `I cannot upload binary files to GitHub` as though that defeats the established Drive-to-Actions bridge.
- Don't prematurely report success. Distinguish **Drive uploaded**, **request committed**, **Actions started**, **Actions succeeded**, **Git tree verified**, **website verified**, and **Drive staging cleaned**.
- Keep original text verbatim in text-driven artwork. Inspect readability and animation timing; a 30-slide × 12-second GIF takes six minutes.
- Public Drive staging must not be used for private material. Avoid overwriting existing destination filenames accidentally.
- Update **both this canonical Markdown document and its companion `00-16-PROMPT-image-publishing.html`** when the pipeline changes. The HTML prompt is a navigation and memory-recovery mirror, not a competing procedure.
