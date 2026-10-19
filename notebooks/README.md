# Notebooks

> **TODO:** the final notebook files have not been added yet. Update this file when they are.

## Which notebook to import

| File | Who it is for | In this repo? |
|---|---|---|
| `persona_axis_kaggle_exercises.ipynb` | Students. Exercise functions are stubs to fill in. | Yes, once provided |
| `persona_axis_kaggle_solutions.ipynb` | Leaders only. Every exercise filled in. | **No.** Kept in a private repo or shared drive, because the notebook is graded homework. |

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

`helper_cells/` holds cells to paste into the notebooks until the final versions include them. See "Unique personas in Homework 1" in the main README.

| File | Paste into | Where |
|---|---|---|
| `my_personas_cell.py` | Student and leader notebooks | Right after the Section 1 PCA exercise |
| `leader_save_shared_pca.py` | Leader solutions notebook only | Right after the Section 1 PCA cell, on the 9B run |
