#!/usr/bin/env python3
"""Build the static field guide and its GitHub Markdown from one catalog.

Python standard library only. Run from any directory with Python 3.9+.
"""
import argparse
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/catalog.json').read_text())
RESOURCES = {r['id']: r for r in DATA['resources']}
TRACKS = {t['id']: t for t in DATA['tracks']}
REPO = DATA['repository']
SITE = 'https://ahhmedsamehh.github.io/Bioinformatics_resources/'
E = html.escape

ICONS = {
    'home': '<path d="m3 11 9-8 9 8M5 10v11h5v-7h4v7h5V10"/>',
    'start': '<path d="M5 21V3m0 1h14l-3 5 3 5H5"/>',
    'foundations': '<path d="M4 4h6c2 0 2 2 2 2s0-2 2-2h6v15h-6c-2 0-2 2-2 2s0-2-2-2H4zM12 6v15"/>',
    'structural': '<path d="m6 5 12 3 2 10-11 3-6-10zM6 5l3 16M3 11l15-3M9 21l9-13M3 11l17 7"/><circle cx="6" cy="5" r="2"/><circle cx="20" cy="18" r="2"/>',
    'omics': '<path d="M7 3c0 6 10 12 10 18M17 3C17 9 7 15 7 21M8 6h8M9 10h6M9 14h6M8 18h8"/>',
    'workflows': '<rect x="2" y="8" width="6" height="7" rx="1"/><rect x="16" y="2" width="6" height="7" rx="1"/><rect x="16" y="16" width="6" height="7" rx="1"/><path d="M8 11h4V5h4M12 11v8h4"/>',
    'ai': '<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5z"/>',
    'resources': '<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6M7 10h6M10 7v6"/>',
    'projects': '<path d="m8 3 4 4 4-4M12 7v6M4 17h16M5 13h14l2 8H3z"/>',
    'arrow': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    'external': '<path d="M14 3h7v7M21 3 10 14M10 4H4v16h16v-6"/>',
    'moon': '<path d="M20 15.5A8.5 8.5 0 0 1 8.5 4 8.5 8.5 0 1 0 20 15.5Z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/>',
    'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
}


def icon(name, css=''):
    return f'<svg class="{E(css)}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


def nav_link(key, label, href, active):
    current = ' aria-current="page"' if key == active else ''
    return f'<a class="nav-link" href="{href}"{current}>{icon(key)}<span>{E(label)}</span></a>'


def shell(title, body, active='home', description=None):
    title = E(title)
    description = E(description or DATA['description'])
    nav = nav_link('home', 'The field guide', 'index.html', active) + nav_link('start', 'Start here', 'start.html', active)
    nav += '<p class="nav-label">Choose a learning path</p>'
    nav += ''.join(nav_link(t['id'], t['short'], f"{t['id']}.html", active) for t in DATA['tracks'])
    nav += '<p class="nav-label">Put it into practice</p>'
    nav += nav_link('projects', 'Starter projects', 'projects.html', active) + nav_link('resources', 'Resource library', 'resources.html', active)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Bioinformatics Resources</title><meta name="description" content="{description}">
<meta name="theme-color" content="#425e44"><meta property="og:title" content="{title} · Bioinformatics Resources"><meta property="og:description" content="{description}"><meta property="og:type" content="website">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><script src="assets/theme.js"></script><link rel="stylesheet" href="assets/style.css"><script src="assets/app.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<aside class="sidebar" id="navigation"><a class="brand" href="index.html">{icon('structural')}<span>Bioinformatics<br>Resources<small>A curious mind’s field guide</small></span></a><nav aria-label="Main navigation">{nav}</nav><div class="sidebar-bottom"><p class="leaf">A little learning, every day.</p><p><small>Collection reviewed · 20 October 2026</small></p><a href="about.html">About &amp; contribute ↗</a></div></aside>
<div class="page-shell"><header class="topbar"><button class="menu-toggle" data-menu-toggle aria-controls="navigation" aria-expanded="false" aria-label="Open navigation">{icon('menu')}</button><span class="topbar-note">AN OPEN NOTEBOOK FOR BIOINFORMATICS</span><div class="topbar-actions"><a href="{REPO}">Explore on GitHub ↗</a><button class="theme-toggle" data-theme-toggle aria-label="Switch to dark mode" aria-pressed="false">{icon('moon', 'moon-icon')}{icon('sun', 'sun-icon')}<span data-theme-label>Dark mode</span></button></div></header>
<main class="content" id="main" tabindex="-1">{body}<footer class="footer"><p>Made for curious minds, at every stage.<span>Learn at your own pace.</span></p><p><a href="about.html">About this collection</a> &nbsp; · &nbsp; <a href="{REPO}">GitHub ↗</a><span>Original material: MIT · Linked resources retain their own terms.</span></p></footer></main></div><button class="backdrop" data-backdrop hidden aria-label="Close navigation"></button></body></html>'''


def intro(eyebrow, title, lead, color='sage'):
    return f'<div class="page-intro {color}"><p class="eyebrow">{E(eyebrow)}</p><h1>{E(title)}</h1><p class="lead">{E(lead)}</p></div>'


def art():
    return '''<svg class="hero-art" viewBox="0 0 410 370" role="img" aria-labelledby="art-title art-desc"><title id="art-title">Connected ideas in biology</title><desc id="art-desc">An abstract molecular sketch connects a sequence, a structure, and a new question.</desc><path class="art-bg" d="M85 36C146-3 228 14 281 42s96 73 99 133-40 146-106 159S123 343 71 300 4 182 22 126 49 59 85 36Z"/><g fill="none" stroke-width="1" opacity=".2" class="art-ink"><circle cx="202" cy="180" r="128"/><circle cx="202" cy="180" r="98"/><path d="M202 35v290M56 180h290"/></g><g fill="none" stroke-width="2" class="art-ink"><path d="M114 122c25-37 62-31 77-2s-8 64-33 56-3-47 23-33 51 55 33 79-60-2-45-28 64-10 81 14 7 67-23 71"/><path d="M124 130c22-31 52-22 59 0s-12 49-29 33 4-35 26-16 40 51 24 67-40-7-24-24 52-4 62 18 1 48-19 56" opacity=".45"/><path d="m114 122-27-43m140 200 27 23m-4-94 48-24" stroke-dasharray="4 5"/></g><g fill="none" stroke-width="1.5" class="art-clay"><path d="M290 64c-25 33 9 47-16 77M306 64c-25 33 9 47-16 77M287 73l15 0m-19 12h15m-14 12h15m-14 12h15m-19 12h15m-19 12h15"/></g><g class="art-node"><circle cx="87" cy="79" r="6"/><circle cx="254" cy="302" r="5"/><circle cx="299" cy="184" r="7"/><circle cx="114" cy="122" r="4"/></g><g class="art-text"><text x="45" y="57">A SEQUENCE</text><text x="260" y="168">A STRUCTURE</text><text x="182" y="332">A NEW QUESTION</text></g><g class="art-ink" fill="none" stroke-width="1.5"><path d="M54 248h15m-7.5-7.5v15M334 263h11m-5.5-5.5v11"/><circle cx="193" cy="56" r="2"/></g></svg>'''


def project_card(p):
    t = TRACKS[p['track']]
    return f'<a class="project-card {t["color"]}" href="project-{p["id"]}.html"><span class="badge">{E(p["level"])} · {E(t["short"])}</span><h3>{E(p["title"])}</h3><p>{E(p["description"])}</p><span class="text-link">Open the project {icon("arrow")}</span></a>'


def home():
    cards = ''
    for t in DATA['tracks']:
        cards += f'''<a class="path-card {t['color']}" href="{t['id']}.html"><div class="card-top"><span class="path-icon">{icon(t['id'])}</span><span class="card-number">PATH {t['number']}</span></div><h3>{E(t['title'])}</h3><p>{E(t['description'])}</p><div class="card-foot"><span>{len(t['topics'])} topics · {E(t['level'])}</span>{icon('arrow')}</div></a>'''
    return f'''<section class="hero"><div><p class="eyebrow">Your next chapter starts here</p><h1>A little curiosity.<br>A world of <em>biology.</em></h1><p class="hero-description">Find your footing in bioinformatics. Explore carefully chosen resources, follow a learning path, and turn a biological question into something you can investigate.</p><div class="hero-actions"><a class="button" href="start.html">Find your starting point {icon('arrow')}</a><a class="text-link" href="resources.html">Browse the library ↗</a></div></div>{art()}</section><div class="collection-meta"><span><strong>5</strong> learning paths</span><span><strong>{len(RESOURCES)}</strong> annotated resources</span><span><strong>3</strong> starter projects</span><span>Free-first &amp; open to everyone</span></div>
<section class="section"><div class="section-heading"><div><h2>Choose a path. Make it yours.</h2><p>Start where you are. You don’t need to learn everything at once.</p></div><a class="text-link" href="start.html">See the learning map {icon('arrow')}</a></div><div class="path-grid">{cards}</div></section>
<section class="section notebook-note">{icon('foundations')}<div><h2>You don’t need to have it all figured out.</h2><p>Start with one question, one dataset, and one small win. Build the next skill when you need it. There is room here for first steps and deeper explorations alike.</p><a class="text-link" href="start.html">Let’s find a good first step {icon('arrow')}</a></div></section>
<section class="section"><div class="section-heading"><div><h2>A little practice goes a long way.</h2><p>Small projects with a question, a dataset, and something to show for it.</p></div><a class="text-link" href="projects.html">All projects {icon('arrow')}</a></div><div class="project-grid">{''.join(project_card(p) for p in DATA['projects'])}</div></section>'''


def start():
    roadmap = (ROOT / 'site/assets/roadmap.svg').read_text()
    return intro('A gentle beginning', 'Where would you like to start?', 'You do not need every prerequisite before you begin. Choose the route closest to your background, then learn through one small project.') + f'''
<div class="route-grid"><article class="route"><h2>I come from biology.</h2><p>Keep a biological question in view while you learn to work with data.</p><ul><li>Start with either Python or R and basic file handling.</li><li>Learn sample metadata and experimental design.</li><li>Try a small structure or RNA-seq project.</li></ul><a href="foundations.html#programming">Begin with practical foundations →</a></article>
<article class="route"><h2>I come from computing.</h2><p>Build the experimental context that makes an analysis meaningful.</p><ul><li>Learn the assay, biological units, and data formats.</li><li>Study controls, replication, and confounding.</li><li>Reproduce a published tutorial before extending it.</li></ul><a href="foundations.html#biological-data">Begin with biological data →</a></article>
<article class="route"><h2>I am exploring.</h2><p>You can get a feel for the work before choosing a specialization.</p><ul><li>Inspect a protein structure or try a Galaxy tutorial.</li><li>Note the questions and methods that interest you.</li><li>Choose a track and a concrete next activity.</li></ul><a href="projects.html">Find a first project →</a></article></div>
<section class="section"><h2>A map, with room to wander.</h2><p>Two scientific tracks share a practical foundation. Workflow engineering and AI connect across them.</p><div class="roadmap">{roadmap}</div></section>
<section class="section prose"><h2>From curiosity to a first result.</h2><ol class="step-list"><li><h3>Choose a question.</h3><p>What would you like to understand: a protein structure, a treatment response, or a reproducible analysis?</p></li><li><h3>Learn the next necessary skill.</h3><p>Use each topic’s prerequisites and outcome to choose a resource. Start with one; the library is a menu, not a completion checklist.</p></li><li><h3>Reproduce a small example.</h3><p>Inspect the data and run the analysis from the beginning. Keep notes about decisions and things you cannot yet explain.</p></li><li><h3>Explain and share what you found.</h3><p>Record your dataset, versions, parameters, results, and limitations. A clear explanation is part of the result.</p></li></ol><div class="practice"><h3>How to read the difficulty labels</h3><p>Beginner means an accessible entry point. Intermediate assumes some coding or analysis experience. Advanced assumes the preceding scientific and statistical context. You can revisit the foundations whenever you need them.</p></div><p>Prefer Arabic for your first programming steps? <a href="resources.html?q=Arabic">Explore Arabic-language resources</a>. Most specialist material in this collection is currently in English; suggestions for strong Arabic resources are welcome.</p></section>'''


def reading_list(ids):
    items = []
    for rid in ids:
        r = RESOURCES[rid]
        items.append(f'<li><a href="{E(r["url"])}">{E(r["title"])} ↗</a><p>{E(r["summary"])}</p><small>{E(r["kind"])} · {E(r["level"])} · {E(r["cost"])} · {E(r["language"])}</small></li>')
    return '<ul class="reading-list">' + ''.join(items) + '</ul>'


def track_page(t):
    body = intro(f"Learning path {t['number']} · {t['level']}", t['title'], t['intro'], t['color'])
    links = ''.join(f'<a href="#{q["id"]}">{E(q["title"])}</a>' for q in t['topics'])
    related = ''.join(f'<a class="related-project" href="project-{p["id"]}.html"><small>Put it into practice</small>{E(p["title"])} →</a>' for p in DATA['projects'] if p['track'] == t['id'])
    body += f'<div class="reading-layout {t["color"]}"><div>{related}'
    for q in t['topics']:
        body += f'''<article class="topic" id="{q['id']}"><span class="badge">{E(q['level'])}</span><h2>{E(q['title'])}</h2><p class="topic-description">{E(q['description'])}</p><p class="prerequisite"><strong>Before you begin:</strong> {E(q['prerequisites'])}</p><h3>What to understand</h3><ul>{''.join('<li>'+E(c)+'</li>' for c in q['concepts'])}</ul><h3>What you’ll be able to do</h3><p>{E(q['outcome'])}</p><div class="practice"><h3>Try this</h3><p>{E(q['practice'])}</p></div><div class="interpretation"><h3>Keep in mind</h3><p>{E(q['caution'])}</p></div><h3>A few good resources</h3>{reading_list(q['resources'])}</article>'''
    body += f'</div><aside class="on-this-page" aria-label="On this page"><p>Along this path</p>{links}<a href="resources.html?track={t["id"]}">Browse related resources ↗</a></aside></div>'
    return body


def resources_page():
    body = intro('A carefully chosen collection', 'Something good to learn next.', 'Search by topic, tool, or language. Every resource has a purpose, a starting level, and a note on what you’ll need. Choose one that fits your next step.')
    options = ''.join(f'<option value="{t["id"]}">{E(t["short"])}</option>' for t in DATA['tracks'])
    body += f'''<noscript><p class="noscript">All resources are listed below. Enable JavaScript to use search, filters, and the theme button.</p></noscript><form class="filters" data-resource-filters role="search"><div class="filters-grid"><div class="filter-search"><label for="resource-search">What are you curious about?</label><input id="resource-search" type="search" name="q" placeholder="Try CITE-seq, diffusion, Python, Arabic…" autocomplete="off"></div><div><label for="resource-track">Learning path</label><select id="resource-track" name="track"><option value="">Every path</option>{options}</select></div><div><label for="resource-level">Starting level</label><select id="resource-level" name="level"><option value="">Every level</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div></div><div class="filter-bottom"><span data-result-count role="status" aria-live="polite">{len(RESOURCES)} resources</span><button type="button" class="clear-filters" data-clear-filters>Clear filters</button></div></form><div class="resource-grid">'''
    for r in DATA['resources']:
        tracks = [t['id'] for t in DATA['tracks'] if any(r['id'] in q['resources'] for q in t['topics'])]
        topic_terms = [q['title'] for t in DATA['tracks'] for q in t['topics'] if r['id'] in q['resources']]
        search = ' '.join([r['title'], r['summary'], r['language'], r['kind'], r['prerequisites'], *topic_terms]).lower()
        body += f'''<article class="resource-card" id="resource-{r['id']}" data-resource data-search="{E(search)}" data-tracks="{' '.join(tracks)}" data-level="{E(r['level'])}"><span class="badge">{E(r['level'])} · {E(r['kind'])}</span><h2><a href="{E(r['url'])}">{E(r['title'])} <span aria-hidden="true">↗</span></a></h2><p>{E(r['summary'])}</p><div class="resource-meta">{E(r['cost'])} · {E(r['language'])}<br>Collection review: {DATA['reviewed']}</div><details><summary>Before you begin</summary><p>{E(r['prerequisites'])}</p></details></article>'''
    return body + '</div><div class="empty-state" data-empty hidden><h2>No matches just yet.</h2><p>Try a broader term, another level, or clear the filters.</p></div><p class="prerequisite" style="margin-top:24px">Collection review dates describe editorial review, not certification or a guarantee of availability. Resource versions, access terms, and compute requirements can change.</p>'


def projects_page():
    return intro('Learn by doing', 'Small projects. Real understanding.', 'Each project starts with a question, identifies its data, and gives you something concrete to inspect and explain. The first two are beginner entry points; the workflow project builds on basic scripting.') + '<div class="project-grid">' + ''.join(project_card(p) for p in DATA['projects']) + '</div>'


def project_page(p, source_ref):
    return intro('Starter project · ' + p['level'], p['title'], p['description'], TRACKS[p['track']]['color']) + f'''<div class="prose project-detail"><h2>The question</h2><p>{E(p['question'])}</p><p class="prerequisite"><strong>Before you begin:</strong> {E(p['prerequisites'])}</p><h2>The data</h2><p>{E(p['data'])}</p><div class="outcomes"><h3>What you’ll make</h3><ul>{''.join('<li>'+E(x)+'</li>' for x in p['outputs'])}</ul></div><h2>Work through it</h2><ol>{''.join('<li>'+E(x)+'</li>' for x in p['steps'])}</ol><a class="button" href="{REPO}/tree/{source_ref}/projects/{p['id']}">Open code &amp; setup instructions {icon('external')}</a><h2>Read alongside the project</h2>{reading_list(p['resources'])}<p><a href="{p['track']}.html">Return to the learning path →</a></p></div>'''


def about(source_ref):
    return intro('An open, growing notebook', 'A guide for the journey.', 'Bioinformatics is a broad field. This collection offers a few considered starting points and room to keep learning.') + f'''<div class="prose"><h2>Welcome.</h2><p>This project began as Ahmed Sameh’s personal collection of bioinformatics resources. It keeps that spirit: approachable explanations, encouragement to practice, and resources selected for a clear learning purpose.</p><p>The structural and omics tracks are the scientific areas emphasized here, rather than a complete division of bioinformatics. Workflows and AI are shared skills, and the specialist topics are invitations to explore further.</p><h2>How the collection is organized</h2><p>Each topic explains its prerequisites, learning outcome, practical exercise, and interpretation limits. Resources include their format, level, language, access information, and why they are useful. Difficulty labels are guidance rather than a fixed sequence.</p><p>The current website and GitHub topic pages are generated from the same catalog. The collection was editorially reviewed on 20 October 2026. This does not mean every course or scientific workflow has been completed or independently validated by the curator.</p><h2>Help make it better.</h2><p>Found a broken link, a confusing explanation, or a resource worth adding? Please <a href="{REPO}/issues/new">open an issue</a> or send a pull request with the topic, prerequisites, access terms, and a sentence explaining its value.</p><p>Arabic-language learning resources and accessible introductions to specialist topics are especially welcome. See the <a href="{REPO}/blob/{source_ref}/CONTRIBUTING.md">contribution guide</a> for the editing and build process.</p><h2>Sources and attribution</h2><p>Links generally lead to the resource authors, maintainers, or publishers. Linked materials retain their own licenses and terms; consult those sources when reusing them. The repository’s original code and guide text use its MIT license.</p><p>The historical list and existing book folders remain available in the repository for continuity. New recommendations favor maintained source links. <a href="{REPO}/blob/{source_ref}/guides/legacy-resources.md">Read the historical list ↗</a></p></div>'''


def resource_markdown(ids):
    text = ''
    for rid in ids:
        r = RESOURCES[rid]
        text += f"\n- [{r['title']}]({r['url']}) — {r['kind']} · {r['level']} · {r['cost']} · {r['language']}. {r['summary']}\n  - Prerequisites: {r['prerequisites']}\n"
    return text


def markdown_files():
    files = {}
    notice = '<!-- Generated by scripts/build.py from content/catalog.json. Edit the catalog, then rebuild. -->\n\n'
    for t in DATA['tracks']:
        text = notice + f"# {t['title']}\n\n[← Main guide](../README.md) · [Browse resources](resources.md)\n\n{t['intro']}\n\n"
        text += '## Along this path\n\n' + '\n'.join(f"- [{q['title']}](#{q['id']})" for q in t['topics']) + '\n'
        for q in t['topics']:
            text += f"\n<a id=\"{q['id']}\"></a>\n\n## {q['title']}\n\n**Level:** {q['level']}\n\n{q['description']}\n\n**Before you begin:** {q['prerequisites']}\n\n### What to understand\n\n"
            text += '\n'.join('- ' + c for c in q['concepts']) + f"\n\n### What you’ll be able to do\n\n{q['outcome']}\n\n### Try this\n\n{q['practice']}\n\n### Keep in mind\n\n{q['caution']}\n\n### A few good resources\n" + resource_markdown(q['resources'])
        related = [p for p in DATA['projects'] if p['track'] == t['id']]
        if related:
            text += '\n## Put it into practice\n\n' + '\n'.join(f"- [{p['title']}](../projects/{p['id']}/README.md)" for p in related) + '\n'
        text += f"\nCollection reviewed: {DATA['reviewed']}. See [About](../README.md#about-this-collection) for scope and review details.\n"
        files[f"guides/{t['id']}.md"] = text
    files['guides/resources.md'] = notice + '# Resource library\n\n[← Main guide](../README.md)\n\nSelect resources by task and prerequisites. Editorial review is not a guarantee of availability or independent validation.\n\n' + f"Collection reviewed: {DATA['reviewed']}.\n" + resource_markdown(list(RESOURCES))
    files['README.md'] = notice + f'''# Bioinformatics Resources

A friendly field guide to learning bioinformatics, building reproducible analyses, and exploring modern biological research. Curated by **Ahmed Sameh**.

Start where you are. Choose one question, learn the next skill it needs, and practice with a small project. You do not need to complete every course or master advanced mathematics before beginning.

**[Explore the website]({SITE})** · **[Start here](guides/start-here.md)** · **[Browse the resource library](guides/resources.md)** · **[Try a project](projects/README.md)**

The website includes a searchable resource library, learning paths, mobile navigation, and a light/dark mode button that remembers your preference. Its first visit follows your device theme.

![Learning map: a biological question leads through shared foundations into structures or omics, supported by workflows and AI, and into a practical project.](site/assets/roadmap.svg)

## Choose a learning path

| Path | What you can explore |
| --- | --- |
''' + ''.join(f"| [{t['short']}](guides/{t['id']}.md) | {t['description']} |\n" for t in DATA['tracks']) + f'''
The scientific tracks emphasize structural bioinformatics and omics. They are two areas covered by this collection, rather than an exhaustive classification of the field. Workflow development and AI connect across both.

## Learn by doing

''' + ''.join(f"- **[{p['title']}](projects/{p['id']}/README.md):** {p['description']}\n" for p in DATA['projects']) + f'''
## What makes a resource useful here?

Each topic includes prerequisites, a learning outcome, a practice activity, and interpretation guidance. The **{len(RESOURCES)} annotated resources** include format, level, language, access information, and a reason to use them. Most materials are free to read; software, hosted services, and compute can have separate terms or costs.

Arabic-language programming material is included, and suggestions for more Arabic resources are welcome. Most specialist resources are currently in English.

## About this collection

This repository began as a personal learning list. It aims to make useful starting points available to people entering bioinformatics and to help learners connect foundations with modern research practice. It is a growing guide, not a certification or a complete curriculum for every specialty.

**Collection editorial review:** {DATA['reviewed']}. This date does not imply that every external course or workflow was completed or independently validated. Resource versions, availability, access terms, and compute requirements can change.

The [historical list](guides/legacy-resources.md) and existing book folders are retained for continuity. Current recommendations favor author, maintainer, and publisher links. Linked resources retain their own licenses and terms.

## Contribute or build the website

Found a broken link, a misleading explanation, or a resource worth sharing? [Open an issue]({REPO}/issues/new) or see [CONTRIBUTING.md](CONTRIBUTING.md).

Edit `content/catalog.json` to update topics and resources, then run:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory _site
```

Open [the local preview](http://localhost:8000). Python 3.9+ is sufficient to build the website; no package installation is needed. The same catalog generates the website and GitHub topic pages.

See [the website guide](site/README.md) for GitHub Pages publishing and theme behavior. Original guide text and code use the [MIT license](LICENSE); linked and third-party materials retain their own terms.
'''
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='_site', help='Output directory, relative to the repository or absolute.')
    parser.add_argument('--source-ref', default='main', help='GitHub branch/ref for project-source links.')
    parser.add_argument('--check', action='store_true', help='Fail when generated GitHub Markdown needs rebuilding.')
    args = parser.parse_args()
    generated = markdown_files()
    if args.check:
        changed = [name for name, text in generated.items() if not (ROOT / name).exists() or (ROOT / name).read_text() != text]
        if changed:
            raise SystemExit('Rebuild generated Markdown: ' + ', '.join(changed))
    else:
        for name, text in generated.items():
            (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / name).write_text(text)
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out = out.resolve()
    # Avoid destructive destination cleanup; only replace the assets we own.
    if out == ROOT or out in ROOT.parents:
        raise SystemExit('Output must not be the repository root or an ancestor.')
    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'site/assets', out / 'assets', dirs_exist_ok=True)
    pages = {
        'index.html': ('The field guide', home(), 'home'),
        'start.html': ('Start here', start(), 'start'),
        'resources.html': ('Resource library', resources_page(), 'resources'),
        'projects.html': ('Starter projects', projects_page(), 'projects'),
        'about.html': ('About & contribute', about(args.source_ref), ''),
    }
    for t in DATA['tracks']:
        pages[t['id'] + '.html'] = (t['short'], track_page(t), t['id'])
    for p in DATA['projects']:
        pages[f"project-{p['id']}.html"] = (p['title'], project_page(p, args.source_ref), 'projects')
    for filename, (title, body, active) in pages.items():
        (out / filename).write_text(shell(title, body, active))
    (out / '404.html').write_text(shell('Page not found', intro('A small detour', 'Let’s find your way back.', 'The page you were looking for could not be found.') + f'<a class="button" href="{SITE}">Return to the field guide →</a>'))
    (out / '.nojekyll').touch()
    print(f"Built {len(pages) + 1} pages, {len(RESOURCES)} resources, and {len(generated)} Markdown files → {out}")


if __name__ == '__main__':
    main()
