process SEQKIT_STATS {
    tag "${meta.id}"
    publishDir "${params.outdir}/seqkit", mode: 'copy'

    conda 'bioconda::seqkit=2.8.2'

    input:
    tuple val(meta), path(reads)

    output:
    path '*.seqkit.stats.tsv', emit: stats

    script:
    def prefix = meta.id
    """
    seqkit stats -a ${reads} > ${prefix}.seqkit.stats.tsv
    """
}
