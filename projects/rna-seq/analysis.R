#!/usr/bin/env Rscript
# Run from this project directory: Rscript analysis.R
# Install dependencies first; see README.md. Do not transform counts before DESeq2.
required <- c("airway", "DESeq2", "ggplot2")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) {
  stop("Install the packages listed in README.md first: ", paste(missing, collapse = ", "))
}
suppressPackageStartupMessages({
  library(airway)
  library(DESeq2)
  library(ggplot2)
})
set.seed(42)
dir.create("results", showWarnings = FALSE)
data("airway", package = "airway")
airway$dex <- relevel(factor(airway$dex), ref = "untrt")
airway$cell <- factor(airway$cell)
metadata <- as.data.frame(colData(airway))
write.csv(metadata, "results/sample-metadata.csv", row.names = TRUE)

# The four cell lines each have treated and untreated observations.
stopifnot(ncol(airway) == 8L, all(table(airway$cell, airway$dex) == 1L))
dds <- DESeqDataSet(airway, design = ~ cell + dex)
# A transparent teaching filter; justify filtering for your actual study.
dds <- dds[rowSums(counts(dds) >= 10) >= 4, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("dex", "trt", "untrt"), alpha = 0.05)
res <- res[order(res$padj, na.last = TRUE), ]
result_table <- cbind(gene_id = rownames(res), as.data.frame(res))
write.csv(result_table, "results/differential-expression.csv", row.names = FALSE)

vsd <- vst(dds, blind = FALSE)
pca <- plotPCA(vsd, intgroup = c("dex", "cell"), returnData = TRUE)
percent <- round(100 * attr(pca, "percentVar"))
p <- ggplot(pca, aes(PC1, PC2, color = dex, shape = cell)) +
  geom_point(size = 3) + theme_minimal(base_size = 12) +
  labs(title = "Airway: exploratory sample relationships",
       x = paste0("PC1: ", percent[1], "% variance"),
       y = paste0("PC2: ", percent[2], "% variance"),
       color = "Treatment", shape = "Cell line")
ggsave("results/pca.pdf", p, width = 7, height = 5)
pdf("results/ma.pdf", width = 7, height = 5)
plotMA(res, main = "Dexamethasone: treated versus untreated", ylim = c(-5, 5))
dev.off()
writeLines(capture.output(sessionInfo()), "results/session-info.txt")
writeLines(c(
  "Dataset: Bioconductor airway; see package citation and provenance.",
  "Design: ~ cell + dex; contrast: trt versus untrt.",
  "Filter: at least four samples with at least ten counts.",
  "Positive log2 fold change means higher expression in treated samples.",
  "Unshrunken effect estimates are reported; see DESeq2 guidance on shrinkage.",
  "This example starts from counts, not raw reads."
), "results/analysis-notes.txt")
message("Wrote outputs to results/. Inspect sample metadata and PCA before interpreting the table.")
