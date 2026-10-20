nextflow.enable.dsl = 2

params.fasta = "${projectDir}/sequences.fasta"
params.outdir = "${projectDir}/results/nextflow"

process GC_CONTENT {
    tag "${fasta.simpleName}"
    publishDir params.outdir, mode: 'copy', overwrite: true
    input:
    path fasta
    path analysis
    output:
    path 'gc.csv'
    script:
    """
    python3 "${analysis}" "${fasta}" gc.csv
    """
}

workflow {
    GC_CONTENT(file(params.fasta, checkIfExists: true), file("${projectDir}/gc_content.py", checkIfExists: true))
}
