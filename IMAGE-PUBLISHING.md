# Jesus-Greg image publishing — zero manual upload verified

## Fully automatic route (verified 2026-11-09)

1. ChatGPT generates or prepares an image file in its working container.
2. ChatGPT calls `files__manage_library` with an upload operation:
   - `container_path`: the exact local image path
   - `destination_path`: `/Google Drive/Jesus-Greg Public Images/<filename>`
3. The existing Google Drive folder **Jesus-Greg Public Images** inherits public Viewer access to newly uploaded files. Folder ID: `1-xgO3kkjuDJhe97WbCfZRzeHK2C5dM6G`.
4. Extract the new Google Drive file ID from the upload result (the suffix of the `external-gdrive:...:file:<ID>` identifier). Verify its metadata and public `anyone/reader` permission using the Google Drive connector.
5. ChatGPT updates `image-publish-request.json` in this repository using GitHub connector `fetch_file` then `update_file`:
   ```json
   {"image_url":"https://drive.google.com/file/d/<ID>/view?usp=sharing","filename":"01-descriptive-image.jpg"}
   ```
6. The push automatically triggers `.github/workflows/publish-image-from-url.yml`. The workflow downloads, validates, and commits the original image to `main`.
7. Check the GitHub Actions run status and the repository Git tree to verify the published file, its byte count, and Git blob checksum.
8. Final public URL: `https://zioncoalition.org/<filename>`.

**No manual Drive upload, sharing change, or GitHub Actions button is required.**

### End-to-end verified test

- Drive upload: `jesus-greg-folder-inheritance-test.jpg`, file ID `1jrHtaBsMnH06zdWbSNruQAI0X-WblP60`, 174,690 bytes; inherited `anyone/reader`.
- Published: `01-jesus-greg-zero-manual-upload-test.jpg`, 174,690 bytes, Git blob SHA `1b77a27ce62238b4c9bce85da76dd128f7cccdb9`.
- Successful Actions run: https://github.com/gomuller/zioncoalition/actions/runs/42633867641

### Alternatives and safeguards

- Manual URL dispatch remains supported in `.github/workflows/publish-image-from-url.yml`.
- Encoded chunk reconstruction is separately supported in `.github/workflows/publish-image-from-chunks.yml`; its tiny PNG test passed but it is no longer needed for routine publishing.
- JPEG, PNG, WebP; maximum 10 MB and 60 million pixels; simple root-level filename only.
- Files placed in the public folder are **publicly readable**. Do not place private or sensitive images there.
- Existing destination filenames may be overwritten; use distinctive names for new artwork.
- Verify success rather than assuming a workflow request was published.
