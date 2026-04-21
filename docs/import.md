# BIOL7210 Workflow Assignment Brief

Build a Nextflow DSL2 pipeline that demonstrates sequential and parallel module execution on bacterial short-read sequencing data.

## Requirements

- Minimum three modules
- At least one sequential dependency (output of module A feeds module B)
- At least one parallel execution (two or more modules consuming the same channel simultaneously)
- Real (non-synthetic) test data from a public repository
- Pipeline must run end-to-end with a single `nextflow run` command
- Submit repo URL as a gzipped text file to Canvas
