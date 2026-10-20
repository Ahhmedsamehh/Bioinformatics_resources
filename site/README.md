# Website development and GitHub Pages

The website is a static field guide with searchable resources, five learning paths, and three starter projects. Its warm paper-and-botanical design has accessible light and dark palettes, mobile navigation, and reduced-motion support.

## Build and preview

Python 3.9+ is sufficient; no Python or JavaScript packages are needed to build the site.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. Stop the server with Control-C. The `_site/` directory is generated and ignored by Git. Project tutorials have their own runtime requirements; those are independent of the website build.

`content/catalog.json` drives the scientific tracks, resource annotations, and project overviews in both the website and GitHub Markdown. Templates live in `scripts/build.py`; styling and browser behavior live in `site/assets/`. Handwritten entry-point and setup documentation is identified in `CONTRIBUTING.md`.

## Theme behavior

- On the first visit, the theme follows `prefers-color-scheme`.
- A visible button changes between light and dark mode and stores the choice in browser-local storage.
- The choice persists across pages and reloads. Until a choice is made, device-theme changes are followed.
- If storage is unavailable, switching still works for the current page.
- No preference is transmitted to a server. Without JavaScript, content remains readable in the default light palette; interactive search and the theme control require JavaScript.

## Publish on GitHub Pages

The intended URL is `https://ahhmedsamehh.github.io/Bioinformatics_resources/`.

1. Merge the field-guide update into `main`.
2. In the repository's **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
3. Run **Build and publish field guide** from the Actions tab, or push a content change to `main`.
4. Confirm that the deployment succeeds before sharing the URL.

The workflow checks generated Markdown, builds the site, validates links and fixtures, and deploys the static artifact. Pull requests build and check without publishing. GitHub Pages must be enabled by an account with the necessary repository settings permission; the default workflow token does not enable an unconfigured Pages site.

The publishing job uses the `github-pages` environment. Keep its deployment rules aligned with the default branch. No site content should depend on a secret or backend service.

## Resource maintenance

The weekly link-review workflow checks the current catalog. It flags confirmed missing pages and reports bot blocks or timeouts for manual review, without changing editorial review dates. It does not send messages or create issues. A reachable URL does not establish scientific quality.

See [VALIDATION.md](../VALIDATION.md) for verification performed during the update and any runtime limits.
