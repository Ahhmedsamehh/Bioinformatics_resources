# One analysis, two workflow engines

[← Projects](../README.md) · [Workflow learning path](../../guides/workflows.md)

**Question:** How can explicit dependencies make a small analysis easier to run and verify?

The same Python script calculates GC content for three tiny, synthetic DNA sequences. Nextflow and Snakemake wrap that computation. Choose one engine initially; the paired examples let you compare concepts later.

## Start with the analysis

Python 3.9+ and no additional packages are required for this step. From this directory:

```sh
python3 gc_content.py sequences.fasta results/plain/gc.csv
diff expected.csv results/plain/gc.csv
```

On Windows, compare the two files in your editor or use the site's cross-platform checker. A successful `diff` prints nothing and exits with status zero.

Expected result:

```csv
sequence_id,length,ambiguous_bases,gc_percent
sequence_a,8,0,50.00
sequence_b,6,2,100.00
sequence_c,6,0,0.00
```

The GC denominator includes only A/C/G/T bases. Ambiguous IUPAC bases are counted separately; an entirely ambiguous sequence has `NA` GC percentage. Empty records, duplicate identifiers, and non-IUPAC DNA characters are rejected.

## Choose Nextflow

Install Nextflow and its supported Java runtime using the [official setup instructions](https://docs.seqera.io/nextflow/getting-started/installation). Then run:

```sh
nextflow run main.nf
diff expected.csv results/nextflow/gc.csv
nextflow run main.nf -resume
```

The FASTA and analysis script are both declared inputs. The process stages them into its work directory and publishes the result. Change a sequence and rerun with `-resume` to investigate how caching responds to changed inputs.

## Or choose Snakemake

Install Snakemake following its [official installation instructions](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html). Then run:

```sh
snakemake --cores 1 --dry-run
snakemake --cores 1
diff expected.csv results/snakemake/gc.csv
```

The output target determines the rule dependencies. The script and FASTA are explicit inputs. Inspect the [current documentation](https://snakemake.readthedocs.io/en/stable/) for graph and report options supported by your installed version.

## Explain what happened

1. Identify the task, inputs, output, and dependency graph in each implementation.
2. Change the input and rerun. Which step executes, and why?
3. Change the analysis script. How does each engine detect that change?
4. Add a quality-check step before GC calculation. What contract should it enforce?
5. Record `python3 --version` and your engine's version. How would you capture the environment for a collaborator?

This intentionally small example uses your local Python environment and does not pin an operating system or container. Add versioned environments and appropriate compute profiles when progressing to a research workflow. Validation status is recorded in [VALIDATION.md](../../VALIDATION.md).
