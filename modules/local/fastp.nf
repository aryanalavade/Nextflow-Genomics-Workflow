process FASTP {
    tag "${meta.id}"
    publishDir "${params.outdir}/fastp", mode: 'copy'

    conda 'bioconda::fastp=0.23.4'

    input:
    tuple val(meta), path(reads)

    output:
    tuple val(meta), path('*.trim.fastq.gz'), emit: reads
    path '*.fastp.json',                      emit: json
    path '*.fastp.html',                      emit: html

    script:
    def prefix = meta.id
    """
    fastp \\
        --in1 ${reads[0]} \\
        --in2 ${reads[1]} \\
        --out1 ${prefix}_R1.trim.fastq.gz \\
        --out2 ${prefix}_R2.trim.fastq.gz \\
        --json ${prefix}.fastp.json \\
        --html ${prefix}.fastp.html \\
        --thread ${task.cpus}
    """
}
