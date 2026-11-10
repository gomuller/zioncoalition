# Jesus-Greg image, animated GIF, and MP4 video publishing — ZERO MANUAL UPLOAD

**Canonical first reference for ALL Zion Coalition image, animated GIF, and MP4 video publishing.** Updated 2026-11-10. Companion prompt: [00-16-PROMPT-image-publishing.html](00-16-PROMPT-image-publishing.html).

> **MANDATORY FOR FUTURE ASSISTANTS:** Before claiming that image, GIF, or MP4 upload to GitHub is impossible, before asking Greg to upload anything manually, or before replacing an animated GIF with HTML, READ THIS FILE AND INSPECT THE ACTUAL WORKFLOWS. We already built, tested, and documented a fully automated ChatGPT → Google Drive → GitHub Actions → Zion Coalition pipeline for JPEG, PNG, WebP, GIF, and MP4 video. Do not confuse limitations of GitHub's text-only `create_file`/`update_file` APIs with limitations of the established publishing system. Greg should not have to re-teach this.

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

## Authoritative automated MP4 publishing (successfully tested 2026-11-10)

**This is the video counterpart to the image/GIF procedure above.** The binary bridge remains ChatGPT → Google Drive → GitHub Actions → the `gomuller/zioncoalition` repository, with **no manual upload**. Use the dedicated video workflow, not the image workflow. Always inspect the current files for changes before acting.

1. Prepare a real, browser-playable MP4 in the working container, ideally H.264 video and AAC audio for broad HTML5 support. Preserve the original. Confirm container path, byte size, codec information, and duration; when compressing for GitHub, target a manageable file size (the Brooklyn test was **20,075,282 bytes**, approximately 20.1 MB, lasting about **2:09**). Test decoding before publishing.
2. Upload the MP4 using the **same** `files__manage_library` mechanism and public Google Drive staging folder as for images:
   ```json
   {"operations":[{"operation":"upload","container_path":"/mnt/data/EXACT-VIDEO.mp4","destination_path":"/Google Drive/Jesus-Greg Public Images/EXACT-VIDEO.mp4"}]}
   ```
   If the exact source is an exported snapshot with a `file_id`, use `source_file_ref` where appropriate. Staging folder ID: `1-xgO3kkjuDJhe97WbCfZRzeHK2C5dM6G`. This is PUBLIC transfer staging; never send confidential footage here.
3. Extract the new Drive file ID from `external-gdrive:...:file:<ID>`. Check the Drive file's visibility if feasible. Form its share URL `https://drive.google.com/file/d/<ID>/view?usp=sharing`.
4. In GitHub repository `gomuller/zioncoalition` on `main`, edit or (if missing) create **`video-publish-request.json`** with the GitHub connector:
   ```json
   {"video_url":"https://drive.google.com/file/d/<ID>/view?usp=sharing","filename":"DESIRED-ROOT-FILENAME.mp4"}
   ```
   Use `fetch_file` + `update_file` and current blob SHA for existing files. An actual change to this request file triggers `.github/workflows/publish-video-from-drive.yml` on push. A workflow-source edit alone **does not** trigger it. If retrying after a fix, make a fresh request-file commit (a harmless `request_version` field is accepted by the tested workflow) or use an authorized rerun action. Avoid concurrent writers to the request file.
5. The video workflow `publish-video-from-drive.yml` checks out `main` with `actions/checkout@v5`, installs `ffmpeg` to provide `ffprobe` and Python `gdown`, downloads the public Drive link, validates a simple root-level `.mp4` filename, enforces **more than 1,000 and at most 50,000,000 bytes**, checks the MP4 `ftyp` header, and uses `ffprobe` to check video stream and **1–1,800 seconds** duration. It commits the original downloaded bytes to `main`, rebasing before pushing.
6. **Proven gotcha:** on the first MP4 publishing run, Drive downloaded the full 20.1 MB successfully, but the job **failed** because the hosted GitHub runner did not have the `ffprobe` executable. The diagnostic was `FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'`. We repaired the workflow by installing `ffmpeg` with `sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg >/dev/null`; we then changed `video-publish-request.json` to retrigger. **The second run succeeded.** Do not repeat the faulty assumption that `ffprobe` exists by default.
7. **Verify each stage separately:** Drive upload; request commit; GitHub Actions run `status=completed`, `conclusion=success`; presence of exact filename in `https://api.github.com/repos/gomuller/zioncoalition/git/trees/main`, including byte size and Git blob SHA; GitHub Pages **build and deploy** outcome; and the **live** `https://zioncoalition.org/<filename>.mp4` URL and its actual playback in a browser. An Actions success for video does not imply Pages deployment success, and a Git tree entry alone is not a live-web test. Do not call the feature fully ready until the Pages site and playback have been checked or explicitly report a limitation.
8. Embed the video in the HTML page using `<video controls playsinline preload="metadata" poster="DESIRED-POSTER.jpg" src="DESIRED-ROOT-FILENAME.mp4">...</video>`. GitHub's normal text API updates the HTML; binary bytes go by Drive-to-Actions. For a vertical film, use `width:100%;height:auto;aspect-ratio:9/16;max-height:82vh;object-fit:contain` as an example. Publish a separately extracted first-frame poster through the existing **image** pipeline to show a preview before play. Verify that poster is in the repo, too.
9. **GitHub Pages deployment gotcha encountered:** the page build for this MP4 succeeded, but the deployment job failed with `No artifacts named "github-pages" were found for this workflow run`. We called GitHub's `rerun_failed_workflow_run_jobs` for run `42826032870`; its retry was **still in progress at the last confirmed inspection**, so don't claim Pages success without a fresh check. Inspect jobs and logs; distinguish infrastructure/deployment artifact errors from missing MP4.
10. **Cleanup:** only after file, Pages, and live playback are verified, remove only the exact temporary Drive staging MP4 using the returned Drive file ID. If cleanup is not available, leave it and report so. Never delete the original source or published GitHub MP4.

### 2026-11-10 — MP4 proof and exact records

- Video: `brooklyn-sculptor-final.mp4`, **20,075,282 bytes**; originally a **33.9 MB**, approximately **2:09** vertical movie that was compressed before publishing.
- Public Drive staging file ID: `14tUpYymh4zfZgWq8ZWh7cZVELYDj4P8A`; staged under `/Google Drive/Jesus-Greg Public Images/brooklyn-sculptor-final.mp4`.
- Publisher workflow: [`.github/workflows/publish-video-from-drive.yml`](.github/workflows/publish-video-from-drive.yml), created in commit `6f97f31d180e71b6142ee333ba27a376e6a95ec7` and fixed in commit `e3bd04edb9fad072567c05660941d1f216e4fbb9`.
- Trigger file: [`video-publish-request.json`](video-publish-request.json), first request commit `0afec0cbdbeeb5eaccc177cb7288ccee6c447bca`, retry request commit `956e329bb4dbae8bac105e7cdaa81050c217cde9`.
- Initial failed workflow (missing `ffprobe`): https://github.com/gomuller/zioncoalition/actions/runs/42825684968
- **Successful video publisher:** https://github.com/gomuller/zioncoalition/actions/runs/42825880617
- GitHub `main` tree **confirmed** `brooklyn-sculptor-final.mp4` with exactly **20,075,282 bytes**, Git blob SHA `005fab32ec6e108699614f2cbf2f6dc89fac5174`.
- Also confirmed in Git tree: `brooklyn-sculptor-comments.gif` (**568,779 bytes**, SHA `f66c7926c5ce8cabd2ebc3bd88b526f4355d48b2`); `brooklyn-sculptor-poster.jpg` (**53,297 bytes**, SHA `94ef885fcb65933f373d250ac19286be9b47ef22`).
- HTML: `01-brooklyn-sculptor.html` contains enlarged vertical video and poster plus the verbatim-comment GIF. Target: https://zioncoalition.org/01-brooklyn-sculptor.html
- The successful **publisher** and a successful **Pages deployment** are separate facts. Pages run https://github.com/gomuller/zioncoalition/actions/runs/42826032870 failed first deployment due to a missing Pages artifact; failed-jobs rerun requested. Verify its latest status independently.

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
- Don't prematurely report success. Distinguish **Drive uploaded**, **request committed**, **Actions started**, **media publisher succeeded**, **Git tree verified**, **Pages deployment succeeded**, **live playback verified**, and **Drive staging cleaned**.
- Keep original text verbatim in text-driven artwork. Inspect readability and animation timing; a 30-slide × 12-second GIF takes six minutes.
- MP4 uses **a different workflow and request file** from images and GIFs. Check the current `.github/workflows/publish-video-from-drive.yml`, and include `ffmpeg`/`ffprobe` provisioning. Never repeat the first-run failure. 
- Public Drive staging must not be used for private material. Avoid overwriting existing destination filenames accidentally.
- Update **both this canonical Markdown document and its companion `00-16-PROMPT-image-publishing.html`** when the pipeline changes. The HTML prompt is a navigation and memory-recovery mirror, not a competing procedure.

### GitHub Pages deployment recovery — 2026-11-10

- Pages run `42827270287` built successfully but its initial deployment stayed in `syncing_files` until the 10-minute timeout. Rerunning its failed deploy job reused the cancelled deployment ID and failed immediately with `Deployment cancelled.`
- **Do not rerun this same cancelled deployment again.** Make a new, purposeful commit to `main` to generate a fresh Pages build/deploy run, then inspect its new deployment ID and outcome. A successfully committed MP4 and a successful Pages deployment are separate checkpoints.
- If a fresh deployment again stalls in `syncing_files`, investigate artifact size and the Pages service/configuration rather than continuing blind retries.
