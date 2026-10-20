#!/usr/bin/env python3
"""Summarize a small DNA FASTA. Ambiguous bases are excluded from GC %."""
import argparse
import csv
from pathlib import Path


def records(path):
    name, sequence, seen = None, [], set()
    for number, raw in enumerate(Path(path).read_text().splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith('>'):
            if name is not None:
                yield name, ''.join(sequence)
            name = line[1:].strip().split()[0] if line[1:].strip() else ''
            if not name or name in seen:
                raise ValueError(f'Empty or duplicate FASTA identifier at line {number}')
            seen.add(name)
            sequence = []
        else:
            if name is None:
                raise ValueError(f'Sequence before a FASTA header at line {number}')
            bases = ''.join(line.split()).upper()
            if set(bases) - set('ACGTRYSWKMBDHVN'):
                raise ValueError(f'Non-IUPAC DNA characters at line {number}')
            sequence.append(bases)
    if name is not None:
        yield name, ''.join(sequence)


def summarize(sequence):
    if not sequence:
        raise ValueError('Empty sequence record')
    known = sum(sequence.count(base) for base in 'ACGT')
    gc = sequence.count('G') + sequence.count('C')
    return len(sequence), len(sequence) - known, f'{100 * gc / known:.2f}' if known else 'NA'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fasta')
    parser.add_argument('output')
    args = parser.parse_args()
    rows = [(name, *summarize(seq)) for name, seq in records(args.fasta)]
    if not rows:
        raise SystemExit('No FASTA records found')
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        writer.writerow(['sequence_id', 'length', 'ambiguous_bases', 'gc_percent'])
        writer.writerows(rows)


if __name__ == '__main__':
    main()
