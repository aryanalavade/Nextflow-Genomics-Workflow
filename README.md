# Nextflow Genomics Workflow
**BIOL7210 — Workflow Exercise**

A three-step Nextflow DSL2 pipeline for bacterial short-read data that chains quality control into two concurrently executing downstream modules:

1. **`FASTP`** — adapter/quality trim of paired-end reads *(sequential upstream)*
2. **`SPADES`** — de novo assembly from trimmed reads *(runs in parallel with Module 3)*
3. **`SEQKIT_STATS`** — read-metrics summary from the same trimmed reads *(runs in parallel with Module 2)*

## Workflow Diagram

![DAG](assets/dag.png)

Because both `SPADES` and `SEQKIT_STATS` subscribe to the same `FASTP.out.reads` channel, Nextflow dispatches them simultaneously — see the trace table below for timing evidence.

## Requirements

| Component | Version used for testing |
|---|---|
| Nextflow | **25.10.4** |
| Conda | **25.7.0** (Miniconda or Miniforge) |
| OS | macOS (Darwin 24.6.0) |
| Architecture | arm64 (Apple Silicon) |

Any Nextflow ≥ 24.04 should work. Conda must be installed before launch; module environments are created automatically on first run.

## Test Data

- **Sample:** *Escherichia coli* K-12 MG1655 — SRA accession [`SRR2584863`](https://www.ncbi.nlm.nih.gov/sra/SRR2584863) (Illumina paired-end, 150 bp).
- **Location:** `assets/data/test/test_R1.fastq.gz` and `assets/data/test/test_R2.fastq.gz` (~6 MB × 2, 50,000 reads per mate).
- **Provenance:** Fetched from EBI ENA and subsampled via `scripts/fetch_test_data.sh`. Regenerate with `bash scripts/fetch_test_data.sh`.

Not reused from any prior BIOL7210 homework.

## How to Run

```bash
# 1. Create / activate the Nextflow runtime env (one-time)
conda create -n nf -c bioconda -c conda-forge nextflow=25.10.4 -y && conda activate nf

# 2. Run the workflow with the bundled test data
nextflow run main.nf -profile conda,test
```

Two copy-paste lines. First run creates conda environments (~few minutes); subsequent runs hit the cache. Typical end-to-end runtime on a laptop: **< 1 minute** for the test dataset.

Add `-resume` to any subsequent invocation to skip previously successful steps.

## Outputs

```
results/
├── fastp/          test.fastp.{json,html}, test_R{1,2}.trim.fastq.gz
├── spades/test/    contigs.fasta, scaffolds.fasta, spades.log
├── seqkit/         test.seqkit.stats.tsv
└── pipeline_info/  dag.png, report.html, timeline.html, trace.txt
```

## Proof of Parallel Execution

From `results/pipeline_info/trace.txt` after a clean run:

| task | submit (HH:MM:SS.ms) | duration |
|---|---|---|
| FASTP | 23:07:22.318 | 1.1 s |
| SEQKIT_STATS | 23:07:23.557 | 730 ms |
| SPADES | 23:07:23.607 | 29.3 s |

`SEQKIT_STATS` and `SPADES` were submitted 50 ms apart, both immediately after `FASTP` completed — they ran concurrently on the local executor.

## Repo Layout

```
.
├── main.nf                  # workflow entry; wires channels
├── nextflow.config          # params, conda profile, test profile
├── modules/local/
│   ├── fastp.nf
│   ├── spades.nf
│   └── seqkit.nf
├── assets/
│   ├── dag.png              # rendered workflow diagram (shown above)
│   └── data/test/
│       ├── test_R1.fastq.gz # Real E. coli reads, SRR2584863 (R1)
│       └── test_R2.fastq.gz # Real E. coli reads, SRR2584863 (R2)
├── scripts/
│   └── fetch_test_data.sh   # regenerate test data from ENA
└── docs/
    └── import.md            # assignment brief
```

## Conda Environments (pinned)

- `bioconda::fastp=0.23.4`
- `bioconda::spades=4.0.0`
- `bioconda::seqkit=2.8.2`
