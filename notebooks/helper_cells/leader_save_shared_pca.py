# ==============================================================================
# LEADERS ONLY: save the shared PCA basis for the class persona map
# Paste into the leader solutions notebook right after the Section 1 PCA cell,
# and run it on gemma-2-9b-it (SMOKE_TEST = False).
#
# TODO, sync with final notebook: the names used here (persona_vectors,
# mean_vector, pca, DEFAULT_PERSONAS, EXTRACTION_LAYER, MODEL_NAME) follow
# ARENA notebook 4.4. Rename them if the final notebook differs.
#
# It writes /kaggle/working/shared_pca.json containing the shared mean, the
# first two principal components, the Assistant vector, and the shared
# personas' coordinates. Publish that file as a Kaggle Dataset (for example
# "dataworks-shared-pca") and have every student add it as an Input. The
# student helper cell projects onto it, so every student's personas land on
# the same axes, and scripts/class_persona_map.py reads it to draw the map.
# ==============================================================================
import hashlib
import json
from pathlib import Path

import numpy as np


def _np(x):
    """Torch tensor (any device or dtype) or array -> float64 numpy array."""
    if hasattr(x, "detach"):
        x = x.detach().float().cpu().numpy()
    return np.asarray(x, dtype=np.float64)


def basis_id(mean, components):
    """Short fingerprint of a PCA basis, so files from different bases are never mixed."""
    payload = np.round(np.concatenate([np.ravel(mean), np.ravel(components)]), 4).astype(np.float32)
    return hashlib.sha1(payload.tobytes()).hexdigest()[:12]


_names = list(persona_vectors.keys())
_V = np.stack([_np(persona_vectors[n]) for n in _names])          # (n_personas, d_model), uncentered
_mean = _np(mean_vector) + _np(pca.mean_)                         # PCA was fit on (v - mean_vector)
_comps = _np(pca.components_[:2])                                 # (2, d_model)
_assistant = _np(np.mean([_np(persona_vectors[n]) for n in DEFAULT_PERSONAS if n in persona_vectors], axis=0))

# round once, and compute every number below from the rounded values, so the
# student cell (which reads this file) reproduces them exactly
_mean, _comps, _assistant = (np.round(a, 6) for a in (_mean, _comps, _assistant))
_coords = (_V - _mean) @ _comps.T                                 # (n_personas, 2)

shared = {
    "model": globals().get("MODEL_NAME", "gemma-2-9b-it"),
    "layer": int(EXTRACTION_LAYER),
    "d_model": int(_V.shape[1]),
    "basis_id": basis_id(_mean, _comps),
    "explained_variance_ratio": [float(r) for r in pca.explained_variance_ratio_[:2]],
    "default_personas": [n for n in DEFAULT_PERSONAS if n in persona_vectors],
    "mean": _mean.tolist(),
    "components": _comps.tolist(),
    "assistant_vector": _assistant.tolist(),
    "assistant_xy": [float(c) for c in (_assistant - _mean) @ _comps.T],
    "personas": [
        {"name": n, "pc1": float(_coords[i, 0]), "pc2": float(_coords[i, 1])} for i, n in enumerate(_names)
    ],
}

_out = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")
(_out / "shared_pca.json").write_text(json.dumps(shared))
print(f"Saved {_out / 'shared_pca.json'}: {len(_names)} shared personas, layer {shared['layer']}, "
      f"d_model {shared['d_model']}, basis {shared['basis_id']}")
