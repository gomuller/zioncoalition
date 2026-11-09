# Jesus-Greg image publishing

## Working route (verified 2026-11-09)

1. Save the generated image and upload it to Google Drive.
2. Set **General access → Anyone with the link → Viewer**.
3. Provide the Google Drive share link and desired destination filename.
4. ChatGPT updates `image-publish-request.json` in this repository.
5. A GitHub Actions `push` trigger runs `.github/workflows/publish-image-from-url.yml`, downloads and validates the image, and commits it to the root of `main`.
6. Published URL: `https://zioncoalition.org/<filename>`.

The workflow also supports manual `workflow_dispatch` with `image_url` and `filename`.

### Verified tests

- `01-jesus-greg-full-resolution.jpg` — Google Drive to GitHub via manual workflow, 174,690 bytes.
- `01-jesus-greg-automatic-publish-test.jpg` — Google Drive to GitHub via automatic request-file trigger, 174,690 bytes.

### Important limitation

ChatGPT-generated local images are not automatically transferred to Google Drive by the connected Google Drive upload tool. That tool requires a compatible connector file reference, not a local `/mnt/data` path. Until that bridge is available, a person must upload newly generated images to Drive once.

### Safety and file rules

- JPEG, PNG, or WebP, up to 10 MB and 60 million pixels.
- Destination is a simple root-level filename; no directories.
- The image must be publicly retrievable; do not publish private files.
- The workflow may replace an existing file with the same filename; choose distinct filenames for new art.
