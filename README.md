# Nextflow Genomics Workflow

A minimal Nextflow DSL2 pipeline demonstrating **sequential + parallel** module
execution on bacterial short-read data:

1. **`FASTP`** — adapter/quality trim of paired-end reads *(sequential upstream)*
2. **`SPADES`** — de novo assembly from trimmed reads *(runs in parallel with Module 3)*
3. **`SEQKIT_STATS`** — read-metrics summary from the same trimmed reads *(runs in parallel with Module 2)*

## Workflow Diagram

![Workflow](assets/workflow_diagram.png)

`FASTP.out.reads` is consumed independently by both `SPADES` and `SEQKIT_STATS`,
so Nextflow schedules them concurrently (trace proof below).

## Requirements

| Component | Version used for testing |
|---|---|
| Nextflow | **24.10.5** |
| Conda | ≥ 24.1 (Miniconda or Miniforge) |
| OS | macOS (Darwin 24.6.0) |
| Architecture | arm64 (Apple Silicon) |

Any Nextflow ≥ 24.04 should work. Conda must be installed before launch; module environments are created automatically on first run.

## Test Data

- **Sample:** *Escherichia coli* K-12 MG1655 — SRA accession [`SRR2584863`](https://www.ncbi.nlm.nih.gov/sra/SRR2584863) (Illumina paired-end, 150 bp).
- **Location:** `test_data/test_R1.fastq.gz` and `test_data/test_R2.fastq.gz` (~6 MB × 2, 50,000 reads per mate).
- **Provenance:** Fetched from EBI ENA and subsampled via `scripts/fetch_test_data.sh`. Regenerate with `bash scripts/fetch_test_data.sh`.

Not reused from any prior BIOL7210 homework.

## How to Run

```bash
# 1. Create / activate the Nextflow runtime env (one-time)
conda create -n nf -c bioconda nextflow=24.10.5 -y && conda activate nf

# 2. Run the workflow with the bundled test data
nextflow run main.nf -profile conda,test
```

Two copy-paste lines. First run creates conda environments (~few minutes); subsequent runs hit the cache. Typical end-to-end runtime on a laptop: **< 15 minutes** for the test dataset.

Add `-resume` to any subsequent invocation to skip previously successful steps.

## Outputs

```
results/
├── fastp/test/     test_trimmed_R1.fastq.gz, test_trimmed_R2.fastq.gz, test_fastp.{json,html}
├── spades/test/    test_contigs.fasta
└── seqkit/test/    test_read_stats.tsv
```

## Proof of Parallel Execution

From `results/pipeline_info/trace.txt` after a clean run:

| task | submit (HH:MM:SS.ms) | duration |
|---|---|---|
| FASTP | 22:41:31.970 | 845 ms |
| SPADES | 22:41:32.839 | 4.8 s |
| SEQKIT_STATS | 22:41:32.843 | 617 ms |

`SPADES` and `SEQKIT_STATS` were submitted within milliseconds of each other, both immediately after `FASTP` completed — they ran concurrently on the local executor.

## Repo Layout

```
.
├── main.nf                  # workflow entry; wires channels
├── nextflow.config          # params, conda profile, test profile
├── modules/
│   ├── fastp.nf
│   ├── spades.nf
│   └── seqkit.nf
├── test_data/
│   ├── test_R1.fastq.gz     # Real E. coli reads, SRR2584863 (R1)
│   └── test_R2.fastq.gz     # Real E. coli reads, SRR2584863 (R2)
├── assets/
│   ├── workflow_diagram.png # rendered workflow diagram (shown above)
│   └── create_diagram.py    # script to regenerate diagram
└── scripts/
    └── fetch_test_data.sh   # regenerate test data from ENA
```

## Conda Environments (pinned)

- `bioconda::fastp=0.23.4`
- `bioconda::spades=3.15.5`
- `bioconda::seqkit=2.8.2`
