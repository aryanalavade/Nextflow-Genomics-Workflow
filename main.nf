#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { FASTP        } from './modules/fastp'
include { SPADES       } from './modules/spades'
include { SEQKIT_STATS } from './modules/seqkit'

workflow {
    // Build input channel: (meta, [R1, R2])
    Channel
        .fromFilePairs(params.reads, checkIfExists: true)
        .map { id, files ->
            def meta = [id: id, single_end: false]
            [meta, files]
        }
        .set { reads_ch }

    // Module 1: quality-trim with fastp  (sequential gate)
    FASTP(reads_ch)

    // Module 2 + 3 both consume fastp output — Nextflow runs them in parallel
    SPADES(FASTP.out.reads)        // Module 2: de novo assembly
    SEQKIT_STATS(FASTP.out.reads)  // Module 3: read statistics
}
