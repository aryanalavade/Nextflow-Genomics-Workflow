#!/usr/bin/env bash
# Fetch 50,000 paired-end reads from SRR2584863 (E. coli K-12 MG1655) via EBI ENA
# and write them to test_data/test_R1.fastq.gz and test_data/test_R2.fastq.gz.
set -euo pipefail

OUTDIR="$(dirname "$0")/../assets/data/test"
ENA_BASE="https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR258/003/SRR2584863"
READS=50000
LINES=$(( READS * 4 ))

echo "Fetching R1..."
curl -s "${ENA_BASE}/SRR2584863_1.fastq.gz" \
  | gunzip -c | head -n "${LINES}" | gzip > "${OUTDIR}/test_R1.fastq.gz"

echo "Fetching R2..."
curl -s "${ENA_BASE}/SRR2584863_2.fastq.gz" \
  | gunzip -c | head -n "${LINES}" | gzip > "${OUTDIR}/test_R2.fastq.gz"

echo "Done. ${READS} paired reads written to ${OUTDIR}/"
