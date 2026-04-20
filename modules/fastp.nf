process FASTP {
    tag "${meta.id}"
    publishDir "${params.outdir}/fastp/${meta.id}", mode: 'copy'

    conda 'bioconda::fastp=0.23.4'

    input:
    tuple val(meta), path(reads)

    output:
    tuple val(meta), path(["${meta.id}_trimmed_R1.fastq.gz",
                            "${meta.id}_trimmed_R2.fastq.gz"]), emit: reads
    path "${meta.id}_fastp.json", emit: json
    path "${meta.id}_fastp.html", emit: html

    script:
    def prefix = meta.id
    """
    fastp \\
        --in1 ${reads[0]} \\
        --in2 ${reads[1]} \\
        --out1 ${prefix}_trimmed_R1.fastq.gz \\
        --out2 ${prefix}_trimmed_R2.fastq.gz \\
        --json ${prefix}_fastp.json \\
        --html ${prefix}_fastp.html \\
        --thread ${task.cpus}
    """
}
