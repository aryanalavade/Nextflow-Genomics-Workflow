process SPADES {
    tag "${meta.id}"
    publishDir "${params.outdir}/spades/${meta.id}", mode: 'copy'

    conda 'bioconda::spades=4.0.0'

    input:
    tuple val(meta), path(reads)

    output:
    tuple val(meta), path('*_contigs.fasta'), emit: contigs

    script:
    def prefix   = meta.id
    def mem_gb   = task.memory ? task.memory.toGiga() : 4
    """
    spades.py \\
        -1 ${reads[0]} \\
        -2 ${reads[1]} \\
        -o spades_out \\
        --threads ${task.cpus} \\
        --memory ${mem_gb}

    cp spades_out/contigs.fasta ${prefix}_contigs.fasta
    """
}
