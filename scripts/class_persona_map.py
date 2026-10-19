"""Draw the class-wide persona map from every student's my_personas.json.

Usage:
    python scripts/class_persona_map.py --shared shared_pca.json --students submissions/ --out class_persona_map.png

--shared    shared_pca.json written by notebooks/helper_cells/leader_save_shared_pca.py
--students  a folder of student my_personas.json files (any file names; searched recursively)
--out       image to write (PNG, or PDF/SVG by extension)
--csv       optional: also write a table of every student persona

Only student files projected onto the same shared basis (matching basis_id) are plotted.
Files made against a student's own PCA fit, or on another layer, are listed and skipped,
because their coordinates are in a different coordinate system.

Needs: numpy, matplotlib.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def natural_key(text):
    """Sort "Student 2" before "Student 10"."""
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", text)]


def load_students(folder, shared):
    plotted, skipped = [], []
    for path in sorted(Path(folder).rglob("*.json")):
        try:
            rec = json.loads(path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            skipped.append((path, "not valid JSON"))
            continue
        if "personas" not in rec or "basis_id" not in rec:
            skipped.append((path, "not a my_personas.json file"))
            continue
        if rec["basis_id"] != shared["basis_id"]:
            why = "projected onto the student's own PCA fit" if rec.get("basis_source") == "own" else "different basis"
            skipped.append((path, f"{why} (basis {rec['basis_id']}, expected {shared['basis_id']})"))
            continue
        for p in rec["personas"]:
            if p.get("pc1") is None:
                skipped.append((path, f"persona '{p['name']}' has no vector (no responses survived judging)"))
                continue
            plotted.append({"student": rec.get("student", path.stem), "file": str(path), **p})
    return plotted, skipped


def draw(shared, students, out):
    fig, ax = plt.subplots(figsize=(12, 8.5))
    for p in shared["personas"]:
        ax.scatter(p["pc1"], p["pc2"], s=40, color="#9aa3ad", zorder=2)
        ax.annotate(p["name"], (p["pc1"], p["pc2"]), xytext=(4, 4), textcoords="offset points",
                    fontsize=8, color="#6b7480")
    ax.scatter(*shared["assistant_xy"], marker="*", s=500, color="#1f4e79", edgecolor="white", zorder=4,
               label="Assistant (mean of default personas)")

    # one colour per student from ten distinct colours; after ten, the marker shape changes too
    cmap = plt.get_cmap("tab10")
    shapes = ["o", "s", "D", "^", "v", "P", "X", "h"]
    names = sorted({s["student"] for s in students}, key=natural_key)
    colour = {n: cmap(i % 10) for i, n in enumerate(names)}
    marker = {n: shapes[(i // 10) % len(shapes)] for i, n in enumerate(names)}
    for s in students:
        ax.scatter(s["pc1"], s["pc2"], s=120, color=colour[s["student"]], marker=marker[s["student"]],
                   edgecolor="black", linewidth=0.8, zorder=5)
        ax.annotate(s["name"], (s["pc1"], s["pc2"]), xytext=(6, 5), textcoords="offset points",
                    fontsize=9, fontweight="bold", color=colour[s["student"]])

    evr = shared.get("explained_variance_ratio", [float("nan"), float("nan")])
    ax.axhline(0, color="#dddddd", lw=0.8, zorder=1)
    ax.axvline(0, color="#dddddd", lw=0.8, zorder=1)
    ax.set_xlabel(f"PC1 ({evr[0]:.1%} of shared variance)")
    ax.set_ylabel(f"PC2 ({evr[1]:.1%} of shared variance)")
    ax.set_title(f"Class persona map: {len(students)} student personas from {len(names)} students "
                 f"on the shared axes ({shared.get('model', '')}, layer {shared.get('layer', '?')})")
    handles = [plt.Line2D([], [], marker="o", ls="", color="#9aa3ad", label="shared personas"),
               plt.Line2D([], [], marker="*", ls="", markersize=14, color="#1f4e79", label="Assistant")]
    handles += [plt.Line2D([], [], marker=marker[n], ls="", markeredgecolor="black", color=colour[n], label=n)
                for n in names]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8, title="Students")
    fig.tight_layout()
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shared", required=True, type=Path)
    ap.add_argument("--students", required=True, type=Path)
    ap.add_argument("--out", default=Path("class_persona_map.png"), type=Path)
    ap.add_argument("--csv", type=Path)
    args = ap.parse_args(argv)

    shared = json.loads(args.shared.read_text())
    students, skipped = load_students(args.students, shared)
    if args.shared.resolve().parent == args.students.resolve():
        skipped = [s for s in skipped if s[0].resolve() != args.shared.resolve()]

    for path, why in skipped:
        print(f"skipped {path}: {why}", file=sys.stderr)
    if not students:
        print("No student personas on the shared basis to plot.", file=sys.stderr)
        return 1

    draw(shared, students, args.out)
    print(f"Wrote {args.out} with {len(students)} student personas from "
          f"{len({s['student'] for s in students})} students.")

    if args.csv:
        cols = ["student", "name", "pc1", "pc2", "cos_to_assistant", "responses_survived", "responses_total", "prompt"]
        with args.csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(sorted(students, key=lambda s: s["pc1"]))
        print(f"Wrote {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
