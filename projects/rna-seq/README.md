# Your first RNA-seq comparison

[← Projects](../README.md) · [Omics learning path](../../guides/omics.md)

**Question:** Which genes show evidence of a treatment-associated expression change when comparing dexamethasone-treated and untreated airway cells while accounting for cell line?

**Starting level:** basic R, count matrices, and introductory experimental design. This is a count-based teaching analysis, not a raw FASTQ processing pipeline.

## Data and provenance

The [Bioconductor airway package](https://bioconductor.org/packages/airway/) provides a packaged RNA-seq example with four cell lines measured under two treatment conditions. Consult the package's documentation and `citation("airway")` for the original experiment and data provenance. No separate download of FASTQ files is needed for this example.

## Set up and run

Use a current R version supported by a compatible Bioconductor release. From R, install:

```r
install.packages("BiocManager")
BiocManager::install(c("airway", "DESeq2"))
install.packages("ggplot2")
```

From this directory, run:

```sh
Rscript analysis.R
```

Package installation needs internet access. The script stops with a dependency message rather than installing software itself. Record your R and Bioconductor versions; they influence package availability and exact results.

## Inspect the outputs

- `results/sample-metadata.csv`: eight samples with their treatment and cell-line metadata.
- `results/pca.pdf`: exploratory sample relationships; inspect outliers and treatment/cell-line patterns.
- `results/differential-expression.csv`: gene identifiers, unshrunken log2 fold changes, standard errors, test statistics, p-values, and adjusted p-values.
- `results/ma.pdf`: expression changes plotted against mean expression.
- `results/session-info.txt` and `results/analysis-notes.txt`: software versions and key decisions.

The design is `~ cell + dex`, and the contrast is treated versus untreated. Positive log2 fold changes indicate greater expression in treated samples. A teaching filter retains genes with at least ten counts in at least four samples. The script asserts the expected sample layout before fitting.

## Explain what you found

1. Why does the design include cell line? Draw the experiment as four paired comparisons.
2. Which samples are close in the PCA, and what would make you investigate an apparent outlier?
3. Choose three genes and report effect sizes, adjusted p-values, and any missing values. Avoid treating an arbitrary threshold as a biological conclusion.
4. What would change if treatment and cell line were confounded?
5. Why should counts be supplied to DESeq2 without first converting them to log-expression or TPM?

Exact gene totals and p-values can change with package versions and analysis choices. Unshrunken effect sizes can be unstable for low-information genes; read the DESeq2 shrinkage guidance before interpreting a ranking based on fold change. This study-specific comparison does not establish a universal response across cell types or a mechanism.

## Continue learning

- [DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)
- [Gene-level RNA-seq workflow](https://bioconductor.org/packages/release/workflows/html/rnaseqGene.html), including how raw reads become counts
- [Project validation status](../../VALIDATION.md)
