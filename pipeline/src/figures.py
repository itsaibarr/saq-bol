"""Result figures for the write-up (static PNG, light surface).

fig_recall_by_language.png : recall on real-test headline scams at <=1% everyday-chat false alarms, Kazakh vs Russian,
                             one row per model, Wilson 95% interval whiskers (dot-and-whisker, 2 series).
fig_keyboard_kazakh.png    : same real Kazakh scams, original spelling vs keyboard-folded (dumbbell, paired).
usage: python figures.py <out_dir> name=label:report_path ...
"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
S1, S2 = "#2a78d6", "#eb6834"  # categorical slots 1-2 (reference palette, validated pair)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})


def load(spec):
    label, path = spec.split("=", 1)[1].split(":", 1)
    rep = json.load(open(path))
    return label, rep.get("test", rep)


def rec(r):
    return (r.get("rate"), r.get("wilson95"), r.get("k"), r.get("n"))


def recall_by_language(models, out):
    fig, ax = plt.subplots(figsize=(9.0, 0.62 * len(models) + 2.0))
    for i, (label, t) in enumerate(models):
        y = len(models) - 1 - i
        for lang, col, dy, name in [("kk", S1, 0.13, "Kazakh"), ("ru", S2, -0.13, "Russian")]:
            r = t["recall_by_language"].get(lang)
            if not r or r.get("rate") is None:
                continue
            p, (lo, hi), k, n = rec(r)
            ax.plot([lo, hi], [y + dy, y + dy], color=col, lw=2, solid_capstyle="round")
            ax.plot(p, y + dy, "o", ms=8, color=col, mec=SURFACE, mew=2, label=name if i == 0 else None)
            if i == len(models) - 1 or label.startswith("Ours"):
                ax.annotate(f"{p:.0%}", (hi, y + dy), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9, color=INK2)
    ax.set_yticks(range(len(models)), [m[0] for m in models][::-1])
    ax.set_xlim(0, 1); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.set_xlabel("Real scams caught (recall) at each model's strict threshold")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False)
    fig.suptitle("Real Kazakhstan scam texts: Kazakh vs Russian", x=0.01, ha="left", fontsize=12, color=INK)
    fig.text(0.01, 0.01, "Threshold set on dev: ≤1 false alarm per 100 everyday messages and ≤1 per 20 bank SMS (keyword rule: its own ≥1-red-flag setting).\nDots: recall on 254 real-test scam messages and call phrases (5+ words). Lines: Wilson 95% interval.", fontsize=8.5, color=INK2)
    fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(out, dpi=180); plt.close(fig)


def keyboard(models, out):
    rows = [(l, t["kbd_paired"]) for l, t in models if "kbd_paired" in t]
    fig, ax = plt.subplots(figsize=(9.0, 0.55 * len(rows) + 2.0))
    for i, (label, kb) in enumerate(rows):
        y = len(rows) - 1 - i
        a, b = kb["original_recall"]["rate"], kb["folded_recall"]["rate"]
        ax.plot([a, b], [y, y], color=GRID, lw=2.5, zorder=1)
        ax.plot(a, y, "o", ms=13, mfc="none", mec=S1, mew=2.2, zorder=2, label="Kazakh letters (қ, ү, ә…)" if i == 0 else None)
        ax.plot(b, y, "o", ms=8, color=S2, mec=SURFACE, mew=2, zorder=2, label="Typed on a Russian keyboard (к, у, а…)" if i == 0 else None)
        t = kb["test"]
        ax.annotate(f"+{t['only_second']} / −{t['only_first']}", (max(a, b), y), xytext=(8, 0), textcoords="offset points", va="center", fontsize=9, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.set_xlim(0, 1); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.set_xlabel(f"Recall on the same {rows[0][1]['test']['n']} real Kazakh scam texts")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=9)
    fig.suptitle("Does keyboard-Kazakh spelling hide a scam?", x=0.01, ha="left", fontsize=12, color=INK)
    fig.text(0.01, 0.01, "+a / −b: scams caught only after folding / only before folding (paired).", fontsize=8.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out, dpi=180); plt.close(fig)


if __name__ == "__main__":
    outdir = sys.argv[1]
    models = [load(a) for a in sys.argv[2:]]
    recall_by_language(models, f"{outdir}/fig_recall_by_language.png")
    keyboard(models, f"{outdir}/fig_keyboard_kazakh.png")
    print("ok")
