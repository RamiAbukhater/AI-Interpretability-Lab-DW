# Notebooks

Leader notes on how the notebook differs from ARENA's original, and what has and hasn't been tested, are in [KAGGLE_NOTEBOOK_NOTES.md](KAGGLE_NOTEBOOK_NOTES.md).

## Which notebook to import

| File | Who it is for | In this repo? |
|---|---|---|
| `persona_axis_kaggle_exercises.ipynb` | Students. Exercise functions are stubs to fill in. | Yes |
| `persona_axis_kaggle_solutions.ipynb` | Leaders only. Every exercise filled in. | **No.** It is gitignored, so a local copy can sit in this folder, but it is never committed, because the notebook is graded homework. |

Students import **only** `persona_axis_kaggle_exercises.ipynb`.

## How to import it into Kaggle

The full walkthrough, with screenshots and troubleshooting, is on the site's [Setup page](../docs/setup.html). In short:

1. Download the `.ipynb` file from this folder on GitHub (open it, then **Download raw file**).
2. On Kaggle: **Code → New Notebook**, then in the editor **File → Import Notebook**, and upload the file.
3. **Session options:** Accelerator **GPU T4 x2**, **Internet** on.
4. **Add Input → Models → Gemma 2**, framework **Transformers**, variations **gemma-2-9b-it** and **gemma-2-2b-it** (accept the Gemma license first).
5. **Add-ons → Secrets:** label exactly `OPENROUTER_API_KEY`, value your OpenRouter key, box ticked.
6. Run once with `SMOKE_TEST = True`, then set it to `False` and restart for the full 9B run.

Results are cached under `/kaggle/working/persona_cache/`. They are lost when the session ends unless you use **Save Version**.

## Helper cells

`helper_cells/` holds plain-Python copies of the Homework 1, Part C cells. Both are already in the notebooks, right after the Section 1 PC1 check; the `.py` files are the source, so edit both if you change one. See "Unique personas in Homework 1" in the main README.

| File | In which notebook |
|---|---|
| `my_personas_cell.py` | Student notebook (with `EXAMPLE_` placeholders) and leader notebook (with a worked example) |
| `leader_save_shared_pca.py` | Leader solutions notebook only |

The course site links to a copy of the student notebook in `docs/notebooks/`. After editing `persona_axis_kaggle_exercises.ipynb`, copy it there: `cp notebooks/persona_axis_kaggle_exercises.ipynb docs/notebooks/`.
