# ==============================================================================
# REQUIRED FOR HOMEWORK 1, PART C: YOUR TWO PERSONAS
# This cell sits right after the Section 1 PCA check in
# persona_axis_kaggle_exercises.ipynb. It needs your finished Section 1
# exercises (judge prompt, generate_all_responses, extract_persona_vectors).
#
# What it does:
#   1. generates, judges, and extracts activations for YOUR two personas, using
#      the notebook's own functions, the same layer, and the same questions;
#   2. projects them onto the SHARED PCA (it never refits PCA);
#   3. prints their PC1 and PC2 coordinates and cosine similarity to the Assistant;
#   4. saves my_personas_plot.png and my_personas.json in /kaggle/working.
# Re-running it is cheap: responses, scores, and vectors are cached.
# In smoke-test mode it runs on 2B against your own PCA; for Homework 1 run it on 9B.
# ==============================================================================
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch as t

# ---- 1. Fill these in --------------------------------------------------------
STUDENT_NAME = "Your Name"  # exactly as on the persona sign-up sheet

MY_PERSONAS = {
    # name: system prompt, written in the same style as the shared PERSONAS.
    # One you expect NEAR the Assistant end, one you expect FAR from it.
    "EXAMPLE_near": "You are a ... who ...",   # replace this example
    "EXAMPLE_far": "You are a ... who ...",    # replace this example
}
# -----------------------------------------------------------------------------

MY_DIR = CACHE_DIR / "my_personas"  # next to the shared run's cache, so it is per model and mode
MY_DIR.mkdir(parents=True, exist_ok=True)
SCORE_THRESHOLD = 3  # same role-play filter as the paper: keep only fully in-character responses


def _np(x):
    """Torch tensor (any device or dtype) or array -> float64 numpy array."""
    if hasattr(x, "detach"):
        x = x.detach().float().cpu().numpy()
    return np.asarray(x, dtype=np.float64)


def basis_id(mean, components):
    """Short fingerprint of a PCA basis (identical to the leaders' cell)."""
    payload = np.round(np.concatenate([np.ravel(mean), np.ravel(components)]), 4).astype(np.float32)
    return hashlib.sha1(payload.tobytes()).hexdigest()[:12]


def _key(name, prompt):
    """Cache key that changes whenever you edit a prompt, so stale results are never reused."""
    return f"{name}::{hashlib.sha1(prompt.encode()).hexdigest()[:10]}"


def _load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


# ---- checks before spending any GPU time or API credit ----------------------
assert len(MY_PERSONAS) == 2, "MY_PERSONAS must contain exactly two personas."
for _name, _prompt in MY_PERSONAS.items():
    assert not _name.startswith("EXAMPLE_"), "Replace the EXAMPLE personas with the two you claimed on the sign-up sheet."
    assert _name not in PERSONAS, f"'{_name}' is already in the shared persona list. Pick a different persona."
    assert _prompt.strip() and "..." not in _prompt, f"Write a real system prompt for '{_name}'."
assert STUDENT_NAME != "Your Name", "Set STUDENT_NAME."

# ---- 2. generate responses (cached) -----------------------------------------
_resp_path = MY_DIR / "responses.json"
_responses_cache = _load(_resp_path, {})
for _name, _prompt in MY_PERSONAS.items():
    _k = _key(_name, _prompt)
    if _k not in _responses_cache:
        print(f"Generating {len(EVAL_QUESTIONS)} responses for '{_name}' ...")
        _gen = generate_all_responses({_name: _prompt}, EVAL_QUESTIONS, max_tokens=RESPONSE_MAX_TOKENS)
        _responses_cache[_k] = [_gen.get((_name, i), "") for i in range(len(EVAL_QUESTIONS))]
        _resp_path.write_text(json.dumps(_responses_cache))
my_responses = {
    (_name, i): r
    for _name, _prompt in MY_PERSONAS.items()
    for i, r in enumerate(_responses_cache[_key(_name, _prompt)])
}

# ---- 3. judge every response (cached), even if RUN_JUDGE_FILTER is off ------
_score_path = MY_DIR / "judge_scores.json"
_scores_cache = _load(_score_path, {})
for _name, _prompt in MY_PERSONAS.items():
    _k = _key(_name, _prompt)
    _have = _scores_cache.get(_k, [None] * len(EVAL_QUESTIONS))
    for i, q in enumerate(EVAL_QUESTIONS):
        if _have[i] is None and my_responses[(_name, i)]:
            try:
                _have[i] = int(judge_role_response(question=q, response=my_responses[(_name, i)], character=_name))
            except Exception as e:  # a failed or unparseable judge call counts as not surviving
                print(f"  judge error on {_name} q{i}: {e}")
    _scores_cache[_k] = _have
    _score_path.write_text(json.dumps(_scores_cache))
my_scores = {
    (_name, i): (s if s is not None else 0)
    for _name, _prompt in MY_PERSONAS.items()
    for i, s in enumerate(_scores_cache[_key(_name, _prompt)])
}

print("\nResponses that survived the judge filter (score 3 = fully in character):")
survived = {}
for _name in MY_PERSONAS:
    _s = [my_scores[(_name, i)] for i in range(len(EVAL_QUESTIONS))]
    survived[_name] = sum(1 for x in _s if x >= SCORE_THRESHOLD)
    print(f"  {_name}: {survived[_name]}/{len(_s)} survived   scores: {_s}")
    if survived[_name] < len(_s) / 2:
        print(f"  !! WARNING: fewer than half of '{_name}' responses survived. Report these scores in your\n"
              f"     write-up, then claim a substitute persona on the sign-up sheet and run it too.")

# ---- 4. extract persona vectors at the SAME layer as the shared run (cached) -
_vec_path = MY_DIR / f"my_persona_vectors_L{EXTRACTION_LAYER}.pt"
_vec_cache = t.load(_vec_path) if _vec_path.exists() else {}
my_vectors = {}
for _name, _prompt in MY_PERSONAS.items():
    _k = _key(_name, _prompt)
    if survived[_name] == 0:
        print(f"  Skipping '{_name}': no responses survived, so there is nothing to average.")
        continue
    if _k not in _vec_cache:
        _vec_cache[_k] = extract_persona_vectors(
            model=model, tokenizer=tokenizer,
            personas={_name: _prompt}, questions=EVAL_QUESTIONS,
            responses=my_responses, layer=EXTRACTION_LAYER,
            scores=my_scores, score_threshold=SCORE_THRESHOLD,
        )[_name].detach().float().cpu()
        t.save(_vec_cache, _vec_path)
    my_vectors[_name] = _np(_vec_cache[_k])

# ---- 5. the shared basis: the leads' file if attached, else your own shared fit
_shared_files = sorted(KAGGLE_INPUT.glob("**/shared_pca.json")) if KAGGLE_INPUT.exists() else []
_d_model = len(next(iter(persona_vectors.values())))
basis = None
if _shared_files:
    _s = json.loads(_shared_files[0].read_text())
    if _s["d_model"] == _d_model and _s["layer"] == EXTRACTION_LAYER:
        basis = {
            "source": "leads", "id": _s["basis_id"],
            "mean": np.array(_s["mean"]), "components": np.array(_s["components"]),
            "assistant": np.array(_s["assistant_vector"]),
            "evr": _s["explained_variance_ratio"],
            "shared": [(p["name"], p["pc1"], p["pc2"]) for p in _s["personas"]],
        }
        print(f"\nProjecting onto the leads' shared PCA ({_shared_files[0]}).")
    else:
        print(f"\n!! The attached shared_pca.json is for d_model={_s['d_model']}, layer {_s['layer']}, but this run is "
              f"d_model={_d_model}, layer {EXTRACTION_LAYER}. Are you on the 2B smoke-test model? Run Part C on 9B.")
if basis is None:
    _names = list(persona_vectors.keys())
    _mean = _np(mean_vector) + _np(pca.mean_)   # the same centering the shared fit used
    _comps = _np(pca.components_[:2])
    _V = np.stack([_np(persona_vectors[n]) for n in _names])
    _xy = (_V - _mean) @ _comps.T
    basis = {
        "source": "own", "id": basis_id(_mean, _comps), "mean": _mean, "components": _comps,
        "assistant": np.mean([_np(persona_vectors[n]) for n in DEFAULT_PERSONAS if n in persona_vectors], axis=0),
        "evr": [float(r) for r in pca.explained_variance_ratio_[:2]],
        "shared": [(n, float(_xy[i, 0]), float(_xy[i, 1])) for i, n in enumerate(_names)],
    }
    print("\nProjecting onto YOUR OWN shared PCA fit. That is fine for your plot, but for the class map add the "
          "leads' shared-PCA dataset as an Input and re-run this cell.")


# ---- 6. project (never refit): z_k = (v - shared mean) . u_k -------------------
def project(v):
    return (_np(v) - basis["mean"]) @ basis["components"].T


def cos_to_assistant(v):
    a, b = _np(v) - basis["mean"], basis["assistant"] - basis["mean"]
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


_shared_pc1 = [p[1] for p in basis["shared"]]
_asst_xy = project(basis["assistant"])
results = []
print(f"\nShared personas span PC1 from {min(_shared_pc1):.2f} to {max(_shared_pc1):.2f} "
      f"(the Assistant sits at {_asst_xy[0]:.2f}).")
print(f"{'persona':<24}{'PC1':>10}{'PC2':>10}{'cos to Assistant':>19}{'survived':>10}")
for _name, _v in my_vectors.items():
    _xy = project(_v)
    _c = cos_to_assistant(_v)
    results.append({"name": _name, "prompt": MY_PERSONAS[_name], "pc1": float(_xy[0]), "pc2": float(_xy[1]),
                    "cos_to_assistant": _c, "responses_survived": survived[_name],
                    "responses_total": len(EVAL_QUESTIONS)})
    print(f"{_name:<24}{_xy[0]:>10.2f}{_xy[1]:>10.2f}{_c:>19.3f}{survived[_name]:>7}/{len(EVAL_QUESTIONS)}")
for _name in MY_PERSONAS:
    if _name not in my_vectors:
        results.append({"name": _name, "prompt": MY_PERSONAS[_name], "pc1": None, "pc2": None,
                        "cos_to_assistant": None, "responses_survived": 0, "responses_total": len(EVAL_QUESTIONS)})

# ---- 7. plot: shared personas muted, Assistant marked, yours highlighted ------
fig, ax = plt.subplots(figsize=(9, 6.5))
for n, x, y in basis["shared"]:
    ax.scatter(x, y, s=35, color="#9aa3ad", zorder=2)
    ax.annotate(n, (x, y), xytext=(4, 4), textcoords="offset points", fontsize=8, color="#6b7480")
ax.scatter(*_asst_xy, marker="*", s=420, color="#1f4e79", edgecolor="white", linewidth=1, zorder=4,
           label="Assistant (mean of default personas)")
for r, col in zip([r for r in results if r["pc1"] is not None], ["#e8590c", "#c2255c"]):
    ax.scatter(r["pc1"], r["pc2"], s=260, color=col, edgecolor="black", linewidth=1.2, zorder=5, label=r["name"])
    ax.annotate(r["name"], (r["pc1"], r["pc2"]), xytext=(9, 9), textcoords="offset points",
                fontsize=12, fontweight="bold", color=col)
ax.axhline(0, color="#dddddd", lw=0.8, zorder=1)
ax.axvline(0, color="#dddddd", lw=0.8, zorder=1)
ax.set_xlabel(f"PC1 ({basis['evr'][0]:.1%} of shared variance)")
ax.set_ylabel(f"PC2 ({basis['evr'][1]:.1%} of shared variance)")
ax.set_title(f"{STUDENT_NAME}: my personas on the shared PCA ({MODEL_VARIANT}, layer {EXTRACTION_LAYER})")
ax.legend(loc="best", fontsize=9)
fig.tight_layout()
_png = WORK_DIR / "my_personas_plot.png"
fig.savefig(_png, dpi=150)
plt.show()

# ---- 8. save coordinates for the class map ----------------------------------
_record = {
    "student": STUDENT_NAME,
    "model": MODEL_VARIANT,
    "layer": int(EXTRACTION_LAYER),
    "basis_source": basis["source"],
    "basis_id": basis["id"],
    "personas": results,
}
_json = WORK_DIR / "my_personas.json"
_json.write_text(json.dumps(_record, indent=2))
print(f"\nSaved {_png} and {_json}. Submit the plot, and keep both files by saving a Kaggle version.")
