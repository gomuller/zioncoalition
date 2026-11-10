# Lean GitHub Pages deployment experiment (not live)

**Status: isolated design and read-only audit.** Branch: `experiment/lean-pages-deployment`. Nothing on this branch is deployed to `zioncoalition.org`; no artwork, links, or media have been changed.

## Problem and evidence
- Main repository has 525 files, 706,218,847 bytes of tracked file contents. The Pages build uploaded a 687,363,659-byte artifact; the deploy stage stalled at `syncing_files` and timed out.
- PNG: 239 files, 522,919,539 bytes. GIF: 12 files, 118,349,752 bytes. MP4: 2 files, 42,511,471 bytes.
- Five-PNG read-only audit (GitHub run 42835342950) measured: original 16,992,336 bytes; optimized PNG 16,049,401 (5.5% smaller); lossless WebP 11,574,836 (31.9% smaller); WebP quality 85 2,455,816 (85.5% smaller). Lossy quality 85 is **not** visually validated.
- Estimated lossless WebP saving across all PNGs ~167 MB **only if the sample is representative**. Simply adding WebPs without excluding PNGs would make the deployment larger.

## Safety-first plan
1. Run `python3 tools/audit_lean_pages.py` in a checked-out repository to inventory media sizes and approximate literal references. This audit is intentionally conservative and cannot prove a file is unused. Preserve the report.
2. Identify the source of the Pages build and whether it deploys repository root, Jekyll output, or a custom artifact. A 687 MB deployment may also encounter service issues unrelated to size.
3. Create a **staging-only** site builder that copies the site to a temporary directory; do not edit or delete originals in `main`. Convert a representative PNG subset to **lossless** WebP, preserving alpha and dimensions. Rewrite every known reference in the temporary copy only, including HTML, CSS, JS, relative paths, URL-encoded paths, and linked gallery pages. Avoid filename collisions.
4. Fail closed if a rewritten reference cannot resolve; also check browser rendering, image transparency, mobile layout, animation, and direct deep links. Literal scans are insufficient for dynamic JavaScript references. Do not exclude original PNGs from staging until all references are confirmed migrated.
5. Measure the resulting *deploy artifact* size, not just the working-tree size. Compare to 687 MB baseline. Confirm that the smaller artifact can deploy successfully on a test/preview branch or separate preview site before any production cutover.
6. Preserve exact public image URLs if they are linked externally. Changing `.png` URLs to `.webp` can break existing direct links even if HTML is rewritten; consider keeping compatibility files or an external media host with URL redirects before removing old PNGs from Pages.
7. Alternative architecture: publish media to a dedicated static object store/CDN, with versioned URL mapping and redirects; GitHub Pages then deploys mainly HTML/CSS/JS. This may be safer for large video/GIF collections than rewriting hundreds of image links.
8. Only after visual, link, byte-size, and preview-deployment verification, propose a reversible production change. Keep original media in GitHub and a rollback path. No mass deletion without explicit approval.

## Current decision
**Do not run bulk WebP conversion or change production Pages settings yet.** First collect reference dependencies and test a staging build. The user wants all artwork preserved, and the primary objective is a reliable deployment rather than a speculative compression target.

## Reference audit results — November 10, 2026
- Experimental run [42836562898](https://github.com/gomuller/zioncoalition/actions/runs/42836562898) succeeded.
- 81 media files, **143,939,599 bytes (~143.9 MB)**, had no literal filename mention in the scanned text files; 549,661,233 media bytes had at least one literal mention. These categories do **not** establish actual reachability or safe deletion.
- Largest unmentioned candidates: `coins (1).gif` 12,186,201 bytes; `bird (1).gif` 9,963,302; `jcarrot (1).gif` 8,453,912; `j-eyes (1).gif` 4,760,842; `follow (1).png` 3,874,475.
- **Do not remove or exclude any of these from production.** Next: inspect exact external links and dynamic usage, then stage a reversible deployment with URL compatibility before any cutover.

## Staging ZIP simulation — November 10, 2026
- [Successful GitHub Actions run 42836901692](https://github.com/gomuller/zioncoalition/actions/runs/42836901692).
- Full checkout ZIP: **684,767,737 bytes**. Candidate ZIP: **583,763,802 bytes**. Measured ZIP reduction **101,003,935 bytes (~14.75%)**.
- Candidate temporarily omitted **76** media files totaling **104,700,867 raw bytes**. Earlier reference audit reported 81 files / 143,939,599 bytes; difference arises because the simulator also scans newer text including audit/plan content, so its naive reference heuristic changes when files mention media names. This proves the current text-scan method is **not stable enough to determine safe exclusions**.
- Both ZIPs were removed at end of run. This was **not** a GitHub Pages deployment, so no deployment success is implied. No originals were changed.
- **Next:** freeze a deterministic, explicit allowlist of actual page dependencies, and test lossless WebP conversion in staging. Keep old direct asset URLs reachable before any production switch.
