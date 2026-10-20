#!/usr/bin/env python3
"""Download experimental crambin structure 1CRN and report its first model."""
import csv
import platform
from pathlib import Path
from urllib.request import Request, urlopen

try:
    import Bio
    from Bio.PDB import MMCIFParser
    from Bio.PDB.MMCIF2Dict import MMCIF2Dict
except ImportError as error:
    raise SystemExit('Install Biopython first: python3 -m pip install -r requirements.txt') from error


def main():
    data = Path('data')
    results = Path('results')
    data.mkdir(exist_ok=True)
    results.mkdir(exist_ok=True)
    cif = data / '1CRN.cif'
    url = 'https://files.rcsb.org/download/1CRN.cif'
    if not cif.exists():
        request = Request(url, headers={'User-Agent': 'BioinformaticsResourcesTeachingProject/1.0'})
        with urlopen(request, timeout=60) as response:
            content = response.read()
        if not content.lstrip().startswith(b'data_'):
            raise SystemExit('The download was not a valid mmCIF data block.')
        cif.write_bytes(content)
    structure = MMCIFParser(QUIET=True).get_structure('1CRN', str(cif))
    metadata = MMCIF2Dict(str(cif))
    model = next(structure.get_models())
    rows = []
    for chain in model:
        for residue in chain:
            # Hetero groups and waters are not counted as protein residues here.
            if residue.id[0] != ' ' or 'CA' not in residue:
                continue
            atom = residue['CA']
            rows.append({
                'chain': chain.id, 'residue_number': residue.id[1],
                'insertion_code': residue.id[2].strip(), 'residue_name': residue.resname,
                'ca_x': f'{atom.coord[0]:.3f}', 'ca_y': f'{atom.coord[1]:.3f}',
                'ca_z': f'{atom.coord[2]:.3f}', 'ca_b_factor': f'{atom.bfactor:.2f}',
            })
    if not rows:
        raise SystemExit('No standard residues with C-alpha atoms were found.')
    with (results / 'residues.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    method = ', '.join(metadata.get('_exptl.method', ['Not reported']))
    resolution = ', '.join(metadata.get('_refine.ls_d_res_high', ['Not reported']))
    report = [
        '# Structure inspection: 1CRN', '', f'Source: {url}',
        f'Experimental method: {method}', f'Reported resolution (angstrom): {resolution}',
        f'First model: {model.id}; protein chains represented: {", ".join(sorted({r["chain"] for r in rows}))}',
        f'Standard residues with C-alpha atoms in the first model: {len(rows)}',
        f'Python: {platform.python_version()}; Biopython: {Bio.__version__}', '',
        'The residue table contains C-alpha coordinates and experimental B-factors.',
        'These B-factors are not AlphaFold pLDDT confidence scores.',
        'This simple summary is not a structure validation report or a biological-assembly analysis.',
        'Inspect the RCSB entry and validation information: https://www.rcsb.org/structure/1CRN',
    ]
    (results / 'report.md').write_text('\n\n'.join(report) + '\n')
    print(f'Wrote {len(rows)} residue rows and results/report.md')


if __name__ == '__main__':
    main()
