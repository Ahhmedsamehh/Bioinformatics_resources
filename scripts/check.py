#!/usr/bin/env python3
"""Check catalog references, generated pages/links, and the teaching computation."""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.headings = set(), [], 0
        self.duplicates = []
        self.lang = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.duplicates.append(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang') == 'en'
        if tag == 'h1':
            self.headings += 1
        for attribute in ('href', 'src'):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])


def check_catalog():
    data = json.loads((ROOT / 'content/catalog.json').read_text())
    resources = data['resources']
    ids = [r['id'] for r in resources]
    require(len(ids) == len(set(ids)), 'Duplicate resource IDs')
    used = set()
    all_topic_ids = []
    for track in data['tracks']:
        require(re.fullmatch(r'[a-z0-9-]+', track['id']), 'Invalid track ID')
        for topic in track['topics']:
            all_topic_ids.append(topic['id'])
            require(topic['level'] in ('Beginner', 'Intermediate', 'Advanced'), 'Invalid topic level')
            for rid in topic['resources']:
                require(rid in ids, f'Unknown resource: {rid}')
                used.add(rid)
    require(len(all_topic_ids) == len(set(all_topic_ids)), 'Duplicate topic IDs')
    require(used == set(ids), f'Unreferenced resources: {set(ids) - used}')
    for resource in resources:
        for field in ('title', 'summary', 'kind', 'level', 'cost', 'language', 'prerequisites'):
            require(bool(resource[field]), f'Missing {field}: {resource["id"]}')
        require(urlsplit(resource['url']).scheme == 'https', 'Resource URL must use HTTPS')
    for project in data['projects']:
        require(project['track'] in {t['id'] for t in data['tracks']}, 'Unknown project track')
        require((ROOT / 'projects' / project['id'] / 'README.md').exists(), 'Missing project instructions')
    print(f'Catalog: {len(data["tracks"])} tracks, {len(all_topic_ids)} topics, {len(resources)} resources')


def check_site():
    site = ROOT / '_site'
    pages = {path.resolve(): Page(path) for path in site.glob('*.html')}
    require(bool(pages), 'Build the website before checking it')
    for path, page in pages.items():
        require(page.lang and page.headings == 1, f'Expected lang=en and one h1: {path.name}')
        require(not page.duplicates, f'Duplicate HTML IDs: {path.name}: {page.duplicates}')
        for href in page.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            require(not parsed.path.startswith('/'), f'Root-relative URL breaks project hosting: {href}')
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            require(target.is_relative_to(site.resolve()), f'Link escapes published site: {href}')
            require(target.exists(), f'Broken local link in {path.name}: {href}')
            if parsed.fragment and target in pages:
                require(unquote(parsed.fragment) in pages[target].ids, f'Missing anchor: {path.name}: {href}')
    print(f'Website: {len(pages)} pages; local links, fragments, IDs, and headings passed')


def check_markdown():
    paths = [ROOT / 'README.md', ROOT / 'CONTRIBUTING.md', ROOT / 'site/README.md']
    paths += list((ROOT / 'guides').glob('*.md')) + list((ROOT / 'projects').rglob('README.md'))
    for path in paths:
        if path.name == 'legacy-resources.md':
            continue  # Historical links are intentionally outside the current catalog.
        for href in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            require(target.exists(), f'Broken Markdown file link: {path.relative_to(ROOT)}: {href}')
    print('GitHub documentation: local file links passed')


def check_computation():
    project = ROOT / 'projects/workflow-basics'
    with tempfile.TemporaryDirectory() as temp:
        out = Path(temp) / 'gc.csv'
        subprocess.run([sys.executable, str(project / 'gc_content.py'), str(project / 'sequences.fasta'), str(out)], check=True)
        require(out.read_text() == (project / 'expected.csv').read_text(), 'GC reference result differs')
        spec = importlib.util.spec_from_file_location('teaching_gc', project / 'gc_content.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        require(module.summarize('NNRY') == (4, 4, 'NA'), 'Ambiguous-only GC denominator')
        require(module.summarize('ACGTNN') == (6, 2, '50.00'), 'Mixed ambiguous GC denominator')
        for text in ('>a\n\n', '>a\nAC\n>a\nGT', 'ACGT', '>a\nAX'):
            fasta = Path(temp) / 'invalid.fasta'
            fasta.write_text(text)
            try:
                for _, sequence in module.records(fasta):
                    module.summarize(sequence)
            except ValueError:
                continue
            raise AssertionError('Invalid FASTA unexpectedly accepted')
    print('Teaching computation: reference output and meaningful input edge cases passed')


if __name__ == '__main__':
    check_catalog()
    check_site()
    check_markdown()
    check_computation()
    subprocess.run([sys.executable, str(ROOT / 'scripts/build.py'), '--check'], check=True)
    print('All local checks passed.')
