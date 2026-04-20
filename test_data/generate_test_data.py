#!/usr/bin/env python3
"""Generate synthetic paired-end FASTQ reads for workflow testing."""
import random
import gzip
import os

random.seed(42)

READ_LEN    = 150
N_READS     = 5000
GENOME_LEN  = 20000
INSERT_SIZE = 350

_comp = str.maketrans('ACGT', 'TGCA')

def rev_comp(seq):
    return seq.translate(_comp)[::-1]

def add_errors(seq, error_rate=0.002):
    bases = list(seq)
    for i in range(len(bases)):
        if random.random() < error_rate:
            bases[i] = random.choice('ACGT')
    return ''.join(bases)

def phred_qual(seq, min_q=30, max_q=37):
    return ''.join(chr(random.randint(min_q, max_q) + 33) for _ in seq)

genome = ''.join(random.choices('ACGT', k=GENOME_LEN))

r1_reads, r2_reads, r1_quals, r2_quals = [], [], [], []
for _ in range(N_READS):
    pos  = random.randint(0, GENOME_LEN - INSERT_SIZE)
    frag = genome[pos:pos + INSERT_SIZE]
    r1   = add_errors(frag[:READ_LEN])
    r2   = add_errors(rev_comp(frag[-READ_LEN:]))
    r1_reads.append(r1)
    r2_reads.append(r2)
    r1_quals.append(phred_qual(r1))
    r2_quals.append(phred_qual(r2))

out_dir = os.path.dirname(os.path.abspath(__file__))

def write_fastq_gz(path, reads, quals, label):
    with gzip.open(path, 'wt') as fh:
        for i, (seq, q) in enumerate(zip(reads, quals)):
            fh.write(f'@{label}_read{i+1}\n{seq}\n+\n{q}\n')

write_fastq_gz(os.path.join(out_dir, 'test_R1.fastq.gz'), r1_reads, r1_quals, 'synth')
write_fastq_gz(os.path.join(out_dir, 'test_R2.fastq.gz'), r2_reads, r2_quals, 'synth')
print(f'Generated {N_READS} paired reads ({READ_LEN} bp, {INSERT_SIZE} bp insert) in {out_dir}/')
print('Files: test_R1.fastq.gz, test_R2.fastq.gz')
