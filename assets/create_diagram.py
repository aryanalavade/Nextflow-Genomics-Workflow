#!/usr/bin/env python3
"""Generate workflow DAG diagram as PNG."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
fig.patch.set_facecolor('#f8f9fa')

COLORS = {
    'box':    '#2c3e50',
    'arrow':  '#555555',
    'label':  'white',
    'sub':    '#bdc3c7',
    'par':    '#e8f4f8',
    'border': '#2980b9',
}

def draw_box(ax, x, y, w, h, title, subtitle, color='#2c3e50'):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle='round,pad=0.08',
                         facecolor=color, edgecolor='#1a252f',
                         linewidth=1.8, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.62, title,
            ha='center', va='center', fontsize=12, fontweight='bold',
            color='white', zorder=4)
    ax.text(x + w/2, y + h*0.28, subtitle,
            ha='center', va='center', fontsize=9,
            color='#bdc3c7', zorder=4)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=COLORS['arrow'],
                                lw=2.0, mutation_scale=18),
                zorder=2)

# ── Title ────────────────────────────────────────────────────────────────────
ax.text(6, 6.5, 'Genomics QC-Assembly Workflow',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color='#2c3e50')

# ── Input label ──────────────────────────────────────────────────────────────
ax.text(2.1, 5.7, 'Raw paired-end\nFASTQ reads',
        ha='center', va='center', fontsize=8.5, color='#555')
arrow(ax, 2.1, 5.45, 2.1, 5.0)

# ── Boxes ────────────────────────────────────────────────────────────────────
draw_box(ax, 0.4, 3.8, 3.4, 1.2, 'Module 1: FASTP', 'Quality Trimming & Filtering', '#1a6b3c')
draw_box(ax, 5.0, 4.8, 3.4, 1.2, 'Module 2: SPADES', 'De Novo Genome Assembly',      '#1a4f7a')
draw_box(ax, 5.0, 2.8, 3.4, 1.2, 'Module 3: SEQKIT STATS', 'Read Quality Metrics',   '#7a3a1a')

# ── Output labels ─────────────────────────────────────────────────────────────
ax.text(6.7, 4.55, 'contigs.fasta', ha='center', fontsize=7.5, color='#555', style='italic')
ax.text(6.7, 2.55, 'read_stats.tsv', ha='center', fontsize=7.5, color='#555', style='italic')

# ── Arrows ───────────────────────────────────────────────────────────────────
# fastp → spades (sequential)
arrow(ax, 3.8, 4.95, 5.0, 5.40)
# fastp → seqkit (parallel with spades)
arrow(ax, 3.8, 4.25, 5.0, 3.40)

# ── Sequential / Parallel labels ─────────────────────────────────────────────
ax.text(4.4, 5.35, 'sequential', ha='center', va='bottom', fontsize=8,
        color='#27ae60', style='italic')
ax.text(4.4, 3.95, 'sequential', ha='center', va='bottom', fontsize=8,
        color='#27ae60', style='italic')

# Parallel brace
brace = FancyBboxPatch((4.75, 2.65), 0.18, 2.75,
                        boxstyle='round,pad=0.05',
                        facecolor='#f0f7ff', edgecolor='#2980b9',
                        linewidth=1.2, linestyle='--', zorder=1)
ax.add_patch(brace)
ax.text(4.6, 4.0, 'parallel\nexecution', ha='center', va='center',
        fontsize=7.5, color='#2980b9', rotation=90)

# ── Legend ───────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(facecolor='#1a6b3c', label='Module 1 (fastp)'),
    mpatches.Patch(facecolor='#1a4f7a', label='Module 2 (spades)'),
    mpatches.Patch(facecolor='#7a3a1a', label='Module 3 (seqkit stats)'),
]
ax.legend(handles=legend_items, loc='lower left', fontsize=9,
          framealpha=0.9, edgecolor='#ccc')

plt.tight_layout()
out = 'assets/workflow_diagram.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f'Saved diagram: {out}')
