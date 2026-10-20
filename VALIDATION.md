# Validation record

Field-guide update reviewed on **20 October 2026**.

## Executed successfully

- Built 14 static HTML pages and generated the GitHub README and five topic guides plus the resource index from the shared catalog.
- Validated five tracks, 24 unique topics, and 51 referenced resources with required annotations.
- Checked all generated HTML file links and fragments, duplicate IDs, language declarations, one primary heading per page, and project-site-compatible relative paths.
- Checked local Markdown file links and generated-content consistency; the explicitly historical list is excluded from current link validation.
- Checked browser-script syntax with Node.js.
- Ran the GC teaching computation and matched its complete output to the committed reference fixture. Also checked ambiguous-only sequences, mixed ambiguity, empty records, duplicate identifiers, missing headers, and invalid DNA characters.
- Ran the protein-structure project with Python 3.9.6, Biopython 1.85, and NumPy 2.0.2. Downloaded 1CRN mmCIF; verified 46 residues in chain A, experimental X-ray metadata, and a reported 1.5-angstrom resolution. Outputs remain ignored local artifacts.
- Parsed the R analysis script successfully with the available R interpreter.
- Browser-checked the homepage in both light and dark mode, switching modes, persistence after reload and navigation, the resource-library link, text search, combined path/level filters, a zero-result state, and clearing filters.

## External resources

The automated checker completed an initial 50-resource pass with **45 HTTP successes, zero confirmed missing pages, and five review warnings**: Elzero returned a bot/access block; Nextflow documentation, Nextflow training, nf-core documentation, and nf-core/rnaseq timed out from the local HTTP client. Relevant official pages and search results were also reviewed through web access. The additional BindCraft resource was reviewed on its authors' repository. A moved MuData documentation URL was corrected.

A reachable URL is not evidence that a course or scientific method has been independently validated. Editorial review dates are not changed by the link checker.

## Limits

- The complete RNA-seq analysis was not run: airway, DESeq2, and ggplot2 are absent from the local R library. Package setup and expected outputs are documented; only syntax was checked locally.
- The Nextflow and Snakemake wrappers were not executed because those engines are not installed locally. Their underlying Python computation was executed and verified. No production-scale scientific workflow or GPU model was run.
- The browser's viewport override did not produce the requested phone-sized viewport. Responsive CSS and menu behavior were reviewed in source; a physical narrow-screen rendering and complete keyboard/screen-reader audit remain unverified.
- GitHub Pages was disabled at inspection time. The connected tools do not provide a Pages configuration mutation, and the available browser is signed out of GitHub. The deployment workflow is supplied; a successful public deployment is not claimed here.

## Repeat the checks

```sh
python3 scripts/build.py --check
python3 scripts/check.py
python3 scripts/check_links.py
node --check site/assets/theme.js
node --check site/assets/app.js
```

Project-specific setup and runtime requirements are in each project README.
