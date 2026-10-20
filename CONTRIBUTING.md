# Help improve the field guide

Thank you for sharing resources, corrections, and practical examples. A small, well-explained contribution is useful.

## Suggest a resource

Open an issue or pull request with:

- The topic and intended learner.
- An author, maintainer, or publisher link.
- Prerequisites, format, language, and access or compute requirements.
- One or two sentences explaining what the learner can do afterward.
- Any important version assumptions or limitations.

Prefer a few complementary resources to many overlapping links. Arabic resources and accessible specialist introductions are welcome. Link to books at their author or publisher rather than uploading additional copies. Respect the source's attribution and reuse terms.

## Update the shared content

`content/catalog.json` is the source for the five learning paths, annotated resources, and project overviews. Every topic contains prerequisites, concepts, an outcome, a practice activity, interpretation guidance, and resource IDs.

1. Edit the catalog, or the relevant project code and instructions.
2. Run `python3 scripts/build.py` from the repository root.
3. Run `python3 scripts/check.py` and inspect the local website.
4. For changed URLs, run `python3 scripts/check_links.py` and manually review warnings.
5. Commit the regenerated `README.md` and `guides/*.md` with the source change.

Do not edit generated topic pages directly: their first line identifies the generator. `guides/start-here.md` and project READMEs are maintained manually; update their corresponding website copy in `scripts/build.py` if changing the introductory wording or setup presentation. Project overview fields shared with the website belong in the catalog.

The collection review date describes a deliberate editorial review of the collection. Do not advance it automatically when checking links or modifying one item. State any scientific examples you could not execute in `VALIDATION.md`.

## Website changes

The site uses Python's standard library to generate static HTML, plus plain CSS and JavaScript. It has no analytics, backend, external fonts, or account requirement. Keep local links relative so GitHub project-site paths work. Read [site/README.md](site/README.md) for preview and publishing.

Verify light and dark themes, keyboard navigation, mobile navigation, search/filter combinations, no-result feedback, and a representative topic page. Honor reduced-motion preferences. Do not add inaccessible contrast or large decorative assets that slow down basic reading.

## Scientific examples

Use small public or synthetic datasets. State the question, data provenance, experimental units, software requirements, expected outputs, and limitations. Record environment versions and make verification possible. A plausible plot or a successful model run is not by itself scientific validation.
