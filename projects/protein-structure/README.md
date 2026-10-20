# Read your first protein structure

[← Projects](../README.md) · [Structural learning path](../../guides/structural.md)

**Question:** What does an experimental protein structure show, and what information should accompany a structural interpretation?

**Starting level:** basic Python and protein biology.

## Data and setup

The script downloads the mmCIF file for [RCSB PDB entry 1CRN](https://www.rcsb.org/structure/1CRN), an experimental structure of crambin. Read the entry for its source publication, experimental method, resolution, and validation information. This is not a predicted structure.

Use Python 3.10+ in an isolated environment. From this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 inspect_structure.py
```

On Windows, activate with `.venv\Scripts\activate` instead. The initial package installation and structure download need internet access. Later runs reuse `data/1CRN.cif`.

## Inspect the outputs

- `data/1CRN.cif`: the downloaded structure file.
- `results/residues.csv`: standard residues with C-alpha atoms from the first coordinate model, including chain/residue identifiers, coordinates, and C-alpha B-factors.
- `results/report.md`: a small metadata summary and Python/Biopython versions.

For the current 1CRN entry, the teaching script should report 46 protein residues in chain A. Check the entry and file rather than assuming this count is a general rule for all structures. Water and hetero groups are excluded from the residue table. The script summarizes the first coordinate model; it does not reconstruct biological assemblies or resolve every alternate-conformation case.

## Explain what you found

1. Open the mmCIF in a molecular viewer, such as [ChimeraX](https://www.rbvi.ucsf.edu/chimerax/tutorials.html), subject to its current software terms.
2. Identify the experimental method and reported resolution. Find the entry's validation information.
3. Identify chains and secondary structure. Do the residue identifiers match what you expected?
4. Explain what an experimental B-factor describes and why it should not be labeled as AlphaFold confidence.
5. Write a short report separating observations, interpretations, and unresolved questions.

## Extend the project

Choose another protein with experimental and predicted structures. Check sequence correspondence, construct boundaries, and residue numbering before comparing coordinates. Then inspect [prediction confidence](https://www.ebi.ac.uk/training/online/courses/alphafold/inputs-and-outputs/evaluating-alphafolds-predicted-structures-using-confidence-scores/) and explain which regions are meaningfully comparable.

This metadata summary is not a complete validation report. Continue with [PDB-101](https://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/introduction) and the [Biopython tutorial](https://biopython.org/docs/latest/Tutorial/).
