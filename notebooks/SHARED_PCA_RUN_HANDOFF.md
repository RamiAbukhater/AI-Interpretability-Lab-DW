# Handoff: run the leader notebook on Kaggle and publish the shared PCA

## Goal

Run the leader notebook, `persona_axis_kaggle_solutions.ipynb`, once on Kaggle with Gemma 2 9B. Then publish the `shared_pca.json` file it writes as a **public Kaggle Dataset**, and report back the dataset's URL and a few numbers from the run.

Why this matters: every student's Homework 1, Part C projects their own two personas onto this one file, so the whole class shares the same axes. The course site has a placeholder (`SHARED_PCA_DATASET`) waiting for the dataset's name. Homework 1 is due **Wednesday, October 28, 2026**, so the dataset should be public as soon as possible, ideally by **Thursday, October 22**.

This run is also the **first test of the notebook on real Kaggle hardware with the real judge model**. Report anything that goes wrong, exactly as you see it.

## Before you start: what the human must already have done

You work in Rami's browser, signed in to Kaggle as **`ramiabukhater`**. **Do not type any password, API key, or token.** If something below is missing, stop and ask Rami to do it.

1. Signed in to [kaggle.com](https://www.kaggle.com) as `ramiabukhater`, with phone verification done. Without it, the GPU and Internet options are locked.
2. Gemma 2 access accepted at [kaggle.com/models/google/gemma-2](https://www.kaggle.com/models/google/gemma-2). If that page still shows a "Request Access" box, access is not granted yet.
3. An OpenRouter API key saved in Kaggle **Add-ons → Secrets** under the label exactly `OPENROUTER_API_KEY`, with some credit on the OpenRouter account. The run makes a few hundred cheap judge calls to `anthropic/claude-haiku-5.5`, well under a dollar. **Never enter or view the key yourself.** If the secret does not exist yet, stop and ask Rami to add it.
4. The notebook file is on this computer at:
   `/Users/ramiabukhater/Desktop/ClaudeOS/dataworks-ai-interpretability-lab/notebooks/persona_axis_kaggle_solutions.ipynb`
   It is gitignored on purpose; it contains the answers to graded homework.

## Rules

- **Keep the notebook private.** It is the solutions notebook. Never make it public or share it.
- **The dataset must be public.** It only holds `shared_pca.json`, a few numbers per persona and no answers.
- **Change only the four flags** in the notebook's first code cell (step 4 below). Don't edit any other code. If something fails, report it; don't patch it.
- **Publish once.** After the dataset is public, don't regenerate or replace the file. Each file has a fingerprint (`basis_id`), and the class-map script only combines students' results made against the same one.
- **Stop the Kaggle session when you are done**, to save Rami's GPU quota (about 30 hours a week).

## Steps

### 1. Import the notebook

1. On Kaggle, click **Code** in the left menu, then **New Notebook**.
2. In the editor's menu, choose **File → Import Notebook** and upload the `.ipynb` file from the path above.
3. Rename the notebook (click its title, top left) to `dataworks-leader-shared-pca`. Leave it **private**.

### 2. Session options

In the right-hand panel, under **Session options**:
- **Accelerator:** `GPU T4 x2`. Not P100 (too little memory for 9B) and not None.
- **Internet:** on.

### 3. Inputs and secret

1. **Add Input → Models**, search "Gemma 2", choose the one by Google, framework **Transformers**, variation **`gemma-2-9b-it`**, then add it.
2. **Add-ons → Secrets**: tick the box next to `OPENROUTER_API_KEY` so it is attached to this notebook. Do not open or edit the value.

### 4. Set the run flags

In the **first code cell** (the "Run configuration" cell), set:

```python
SMOKE_TEST = False
USE_FULL_PERSONA_LIST = False
GENERATION_BACKEND = "local"
RUN_JUDGE_FILTER = False
```

These must match what students run (9B, the 53-persona workshop list, local generation, no judge filter). Otherwise the shared axes will not match theirs.

### 5. Run the whole notebook as a saved version

Click **Save Version** (top right) → **Save & Run All (Commit)** → **Save**. Kaggle runs the notebook top to bottom in a fresh session. The estimate is 25 to 40 minutes, but it has never been timed on Kaggle. Watch progress under the notebook's **Versions** list, or by opening the running version and its **Logs**.

### 6. Check the run

Open the finished version. The status should be complete, not "Error". In its output or logs, confirm and **copy down**:

1. The loading cell prints `NUM_LAYERS=42, D_MODEL=3584, EXTRACTION_LAYER=27`.
2. The float16 check prints `No NaN or inf in logits or hidden states.`, plus the "Largest absolute hidden-state value" line. Copy that line.
3. The persona cell prints `Using 53 personas`.
4. The PCA cell prints `Assistant Axis norm: 1.0000` and `PCA explained variance: PC1=…, PC2=…`. Copy both percentages.
5. The PC1 check prints `Correlation between PC1 and Assistant Axis projection = …` and the PC1 ranks of `assistant` and the four default personas. Copy them.
6. **The key line.** Under "Leaders: save the shared PCA", the cell prints:
   `Saved /kaggle/working/shared_pca.json: 53 shared personas, layer 27, d_model 3584, basis <12 characters>`
   Copy the `basis` value.
7. The next cell, the worked example with `tax_auditor` and `stage_magician`, prints a survival line and a PC1/PC2/cosine row for each persona. Copy them.
8. In the version's **Output** tab, `shared_pca.json` is listed (roughly 100 to 200 KB).

**If the run fails:**
- **NaN or inf error from the float16 check:** the documented fix is 8-bit loading. Do not do it yourself. Report the error and stop.
- **Failure *after* step 6's "Saved … shared_pca.json" line** (for example a judge test or the autorater sanity check): the file was still written. Recover it this way. Open the notebook editor, run cells interactively from the top through the "Leaders: save the shared PCA" cell, download `shared_pca.json` from the right-hand **Output** panel (`/kaggle/working`), and use it in step 7. Report the failing cell's name and the full error text.
- **Failure *before* that line:** stop and report the cell and the full error text.

### 7. Publish the dataset

1. From the finished version's **Output** tab, use **New Dataset**. Or go to [kaggle.com/datasets](https://www.kaggle.com/datasets) → **New Dataset** and upload the downloaded `shared_pca.json`.
2. Title: `DataWorks Shared PCA`. URL slug: `dataworks-shared-pca`.
3. Visibility: **Public**. Then **Create**.
4. Open the dataset page and confirm that `shared_pca.json` is listed and the dataset shows as public.

### 8. Clean up

Stop any running interactive session: the power icon in the editor's top bar, or **View Active Events** in the left menu.

## What to report back

Paste this back to Rami, filled in:

```
Dataset URL:            https://www.kaggle.com/datasets/ramiabukhater/dataworks-shared-pca
Dataset slug:           ramiabukhater/dataworks-shared-pca
Visibility:             Public (confirmed)
basis_id:               <from step 6.6>
Model / layer / d_model: gemma-2-9b-it / 27 / 3584
Explained variance:     PC1 = …%, PC2 = …%
PC1 vs axis correlation: …
PC1 ranks:              assistant …/53, default …/53, default_assistant …/53, default_llm …/53, default_helpful …/53
Largest hidden-state value (float16 check): …
Worked example:         tax_auditor survived …/5, PC1 …, cos …; stage_magician survived …/5, PC1 …, cos …
Total run time:         … minutes (from the version page)
Problems or warnings:   <full error text and cell names, or "none">
```

Rami will pass this to the agent maintaining the course site. That agent will replace the `SHARED_PCA_DATASET` placeholder on the Homework 1 page and record the run in the README and the leader notes.
