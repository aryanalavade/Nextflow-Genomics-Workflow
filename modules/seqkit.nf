process SEQKIT_STATS {
    tag "${meta.id}"
    publishDir "${params.outdir}/seqkit/${meta.id}", mode: 'copy'

    conda 'bioconda::seqkit=2.8.2'

    input:
    tuple val(meta), path(reads)

    output:
    path '*_read_stats.tsv', emit: stats

    script:
    def prefix = meta.id
    """
    seqkit stats -a ${reads} > ${prefix}_read_stats.tsv
    """
}
