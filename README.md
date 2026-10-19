# DataWorks AI Interpretability Lab

A UCSD DataWorks research group reproducing and extending Anthropic's [The Assistant Axis](https://arxiv.org/abs/2601.10387) (Lu, Gallagher, Michala, Fish, and Lindsey, 2026).

**Leads and instructors:** Rami Abukhater, Alec Min, and Akshar Sinha.

In person we only cover the high-level ideas. Setup, reading, and the notebook are homework. This repository holds the student notebook and a static website that walks students through all of it on their own:

- **Setup on Kaggle**: account, phone verification, OpenRouter key, the Gemma 2 license, GPU T4 x2, model inputs, secrets, the smoke test, quota, saving, and troubleshooting.
- **Seven concept pages**, in the order the notebook uses them, each with intuition, a diagram, the link to the paper, a code walkthrough with tensor shapes, click-to-reveal questions, and common mistakes.
- **Homework 0**: a short introduction post in the general research chat on Discord, due Friday, October 23. Homework 1 is due Wednesday, October 28 (a screenshot of the PCA plot with the student's projected personas, posted in the homework submissions channel on Discord), and Homework 2 is due Friday, October 30 (a reply and reaction to Rami's message in that channel).
- **Calendar**: meetings every Wednesday and Thursday, 7 to 8 pm, three workshops, homework deadlines, the final paper (Sun Nov 29), the lab dinner (Dec 3), and the tentative showcase (Dec 4–5).
- **Homework 1** (setup, smoke test, Sections 1 and 2) and **Homework 2** (choose and propose a research extension from a menu of six ideas), each on its own page.
- **Resources**: sources, a glossary, and introductory interpretability reading.

Students run an adapted version of ARENA's notebook 4.4, *LLM Psychology & Persona Vectors*, on Kaggle's free tier with Gemma 2 9B Instruct (`gemma-2-9b-it`). The scope is Section 1 (Mapping Persona Space) and Section 2 up to steering along the Assistant Axis. Activation capping and ARENA's Sections 3 and 4 are out of scope for now.

## Viewing the site

**Locally.** Open `docs/index.html` in a browser. Every link is relative and nothing is fetched at runtime, so the site works straight from the file system. (Fonts, KaTeX, and Prism load from CDNs, so you need to be online for those.)

**On GitHub Pages.** The site is plain HTML in `docs/`, so no build step or Actions workflow is needed.

1. Push this repository to GitHub.
2. Go to the repository's **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Set **Branch** to `main` and the folder to `/docs`, then click **Save**.
5. After a minute or so the page shows the site's address, usually `https://<user-or-org>.github.io/<repo-name>/`.

`docs/.nojekyll` tells GitHub Pages to serve the files as they are, without Jekyll processing.

## Repository layout

```
README.md               this file
LICENSE                 MIT for code, CC BY 4.0 for written content
.gitignore
notebooks/
  persona_axis_kaggle_exercises.ipynb   the student notebook (the one students import)
  persona_axis_kaggle_solutions.ipynb   leaders only; gitignored, never committed
  KAGGLE_NOTEBOOK_NOTES.md              leader notes: what changed from ARENA, run modes, testing status
  README.md                             which notebook to import into Kaggle and how
  smoke_test_pca_2b.png                 PCA plot from the leader's CPU smoke test
  helper_cells/                         the Homework 1 Part C cells, as plain .py (also inside the notebooks)
scripts/
  class_persona_map.py  leads: combine students' personas into one class-wide map
docs/                   the website (GitHub Pages serves this folder)
  notebooks/            a copy of the student notebook, so the site can link to it as a download
  index.html            home
  setup.html            setup on Kaggle (the most important page)
  concepts/             01-personas.html … 07-steering.html
  calendar.html         key dates, month view, and all meetings
  homework-0.html       Discord introduction post, due Fri Oct 23
  homework-1.html       setup, smoke test, Sections 1 and 2
  homework-2.html       extension menu (6 idea cards, theme filters) and proposal checklist
  resources.html        sources and glossary
  assets/css/style.css  all styles; light and dark themes follow the system setting
  assets/js/site.js     sidebar, prev/next links, footer, copy buttons, screenshot slots, math
  assets/img/           favicon, and setup/ for screenshots
```

### Editing the site

- Pages are plain HTML. Edit them directly.
- The page order, sidebar, prev/next links, and step numbers all come from the `PAGES` list at the top of `docs/assets/js/site.js`. To add or reorder a page, edit that list and give the new page's `<body>` a matching `data-page` id and the right `data-root` (`""` at the top level, `"../"` inside `concepts/`). Copy an existing page as a template.
- The footer (names and attribution) is also in `site.js`.
- Math uses KaTeX with `\( … \)` for inline and `\[ … \]` for display.
- Code blocks are `<pre><code class="language-python">…</code></pre>`. Highlighting and the copy button are added automatically. Escape `<` and `&` inside code as `&lt;` and `&amp;`.
- Click-to-reveal answers and hints are native `<details>` elements, so they work without JavaScript.

## The notebooks

The student notebook is [`notebooks/persona_axis_kaggle_exercises.ipynb`](notebooks/persona_axis_kaggle_exercises.ipynb). Leader notes on how it differs from ARENA's original, its run modes, and what has and has not been tested are in [`notebooks/KAGGLE_NOTEBOOK_NOTES.md`](notebooks/KAGGLE_NOTEBOOK_NOTES.md).

**The site links to a copy.** GitHub Pages only serves `docs/`, so the site's download links point to `docs/notebooks/persona_axis_kaggle_exercises.ipynb`. After editing the student notebook, copy it over so the two stay identical:

```bash
cp notebooks/persona_axis_kaggle_exercises.ipynb docs/notebooks/
```

**Keep the site in sync.** The code on the concept pages and the setup page is quoted from the student notebook (function names, variables, flags, layer choices, cache paths, error messages). If you change one of those in the notebook, search the HTML for it and update the matching page.

> **Never commit the solutions notebook.** `persona_axis_kaggle_solutions.ipynb` can sit in `notebooks/` locally because `.gitignore` ignores `*solutions*.ipynb`, but keep the shared copy in a private repository or shared drive. (Like ARENA's, the student notebook does include collapsible reference solutions under each exercise. Homework 1's unique personas are what show a student did the work.)

## Unique personas in Homework 1 (checking individual work)

The notebook scaffolding and ARENA's published solutions mean finished code alone does not show a student did the work. So Homework 1, Part C asks every student to add **two personas of their own** on top of the shared set, run them through the whole pipeline (prompt, generation, judging, activation extraction), and project them onto the **shared** PCA. Every student's plot is different, and because everyone uses the same axes, the leads can combine them into one class-wide persona map.

**Why a shared PCA file?** Each student generates their own responses, so their own Section 1 PCA comes out slightly different (axes can rotate or flip sign). Coordinates from different students' fits cannot go on one map. The leads therefore run the shared set once on 9B and publish the result. Every student's helper cell projects onto that one file.

### Leads: setup before Homework 1 opens

1. **Sign-up sheet.** Make a Google Sheet with columns **Name, Persona 1, Persona 2, Prediction for Persona 1, Prediction for Persona 2, Substitutes**. Paste the shared persona list (the keys of `PERSONAS`) into a second tab so students can check for duplicates. Put the link in `docs/homework-1.html` (`PERSONA_SIGNUP_SHEET`).
2. **Shared PCA.** Run the leader solutions notebook on `gemma-2-9b-it` (`SMOKE_TEST = False`, default persona list). The cell under "Leaders: save the shared PCA", right after the Section 1 PC1 check, writes `/kaggle/working/shared_pca.json` (shared mean, first two components, Assistant vector, shared coordinates, and a `basis_id` fingerprint). Publish that file as a public Kaggle Dataset and put its name in `docs/homework-1.html` (`SHARED_PCA_DATASET`). Do not regenerate it mid-quarter; a new file means a new `basis_id`, and the map script only combines files that match.
3. **Student cell.** The "Your two personas (Homework 1, Part C)" cell is already in the student notebook right after the PC1 check. The leader notebook has the same cell with a worked example filled in (`tax_auditor` and `stage_magician`), so a full leader run tests it end to end. The plain-Python copies in [`notebooks/helper_cells/`](notebooks/helper_cells/) are the source; if you edit a cell, edit both the `.py` file and the notebooks.
4. **Kaggle usernames** of the leads, for students to share their notebooks with (`LEAD_KAGGLE_USERNAMES`).

What the student cell does: generates, judges (always, even when `RUN_JUDGE_FILTER` is off), and extracts activations for the two personas at `EXTRACTION_LAYER`, reusing cached results in `CACHE_DIR/my_personas/` (under `/kaggle/working/persona_cache/`). It warns if fewer than half of a persona's responses survive judging, then projects onto the attached `shared_pca.json`. If the file is missing, or was made for a different model size or layer (for example the 2B smoke test), it falls back to the student's own fit and marks the result `basis_source: "own"`. It then prints PC1, PC2 and cosine to the Assistant next to the shared PC1 range, and saves `my_personas_plot.png` and `my_personas.json`.

### Leads: making the class map

Collect each student's `my_personas.json` (from the Output tab of their shared Kaggle version) into one folder, then run:

```bash
python scripts/class_persona_map.py --shared shared_pca.json --students submissions/ --out class_persona_map.png --csv class_personas.csv
```

It plots the shared personas in grey, the Assistant as a star, and every student persona coloured by student and labelled. It also writes a CSV sorted by PC1. Files made against a student's own fit, or with no surviving responses, are skipped and listed with the reason. It needs `numpy` and `matplotlib`.

**How this was tested** (on a Mac CPU, without Kaggle, a GPU, or the real OpenRouter judge):

- **Inside the real notebook.** The leader solutions notebook was run top to bottom in smoke-test mode with the two Part C cells in place. It used `transformers` 4.46 and a tiny random Gemma 2 test model (`hf-internal-testing/tiny-random-Gemma2ForCausalLM`, 4 layers) in a fake `/kaggle/input`, plus a fake OpenRouter client that scores one test persona 1 and everything else 3. The leader cell wrote `shared_pca.json`. The student cell then:
  - generated and judged both personas with the notebook's own functions;
  - warned about the persona the judge filtered out and skipped it;
  - projected the other onto the published shared PCA;
  - saved the plot and JSON.

  The random model means the geometry is meaningless; this checks that names, shapes and files line up. The only failing cells were ARENA's judge and autorater checks, which the fake judge cannot pass by design.
- **Against a stand-in notebook.** Both cells and the map script also passed 16 checks against fake persona vectors with a known Assistant direction:
  - no shared file attached;
  - a fully filtered persona;
  - re-running from cache;
  - a shared file from the wrong model size;
  - two students whose near and far personas landed on the predicted sides;
  - the class map with 2 and 14 students.

Run the leader notebook once on Kaggle (smoke test, then 9B) before Homework 1 opens.

## Still waiting on the leads

- [ ] **Run the leader notebook on Kaggle** once with `SMOKE_TEST = True` and once with `SMOKE_TEST = False`, before Homework 1 opens. Nothing has run on Kaggle hardware or against the real OpenRouter judge yet (see the testing notes in `notebooks/KAGGLE_NOTEBOOK_NOTES.md`). The 9B run times on the site are estimates until then.
- [ ] **Publish the shared PCA** from that 9B run as a Kaggle Dataset (see above).
- [ ] **Calendar details**: meeting locations and the lab dinner's time and place are marked tentative in `docs/calendar.html`. When they are confirmed, replace the "Location tentative" and "Time and location tentative" text. To change dates, edit the Key dates table, the month tables, and the All meetings table in that file.
- [ ] **Homework 1, Part C setup**: the persona sign-up sheet (`PERSONA_SIGNUP_SHEET`), the published shared PCA dataset (`SHARED_PCA_DATASET`), and `LEAD_KAGGLE_USERNAMES`, all in `docs/homework-1.html`. The cells themselves are already in the notebooks.
- [ ] **Screenshots**: 12 placeholders, listed below.

### Screenshot placeholders

Each placeholder on the setup page shows a striped box with a description until the matching file exists. **To add one, save a PNG with exactly the file name below into `docs/assets/img/setup/`.** The page picks it up automatically; no HTML edits needed. Blur any API key, email address, or phone number before saving.

| File (in `docs/assets/img/setup/`) | Setup step | What it should show |
|---|---|---|
| `01-kaggle-phone-verification.png` | 2 | Kaggle Settings page with the Phone verification section visible, showing a verified status |
| `02-openrouter-credits.png` | 3 | OpenRouter Credits page showing a small positive balance after adding credit |
| `03-openrouter-create-key.png` | 3 | OpenRouter Create API Key dialog with a name filled in and a credit limit set, key value blurred |
| `04-gemma-license.png` | 4 | Gemma 2 model page on Kaggle with the "Access Gemma 2 on Kaggle" box and its Request Access button |
| `05-import-notebook.png` | 5 | Kaggle notebook editor with the File menu open and Import Notebook highlighted, plus the import dialog |
| `06-session-options.png` | 6 | Session options panel with Accelerator set to GPU T4 x2 and the Internet switch on |
| `07-add-input-gemma.png` | 7 | Add Input dialog filtered to Models, with Gemma 2 by Google selected and Framework set to Transformers |
| `08-model-variation.png` | 7 | Input panel listing both gemma-2-9b-it and gemma-2-2b-it under Gemma 2 / Transformers |
| `09-add-secret.png` | 8 | Add-ons → Secrets dialog with a secret labelled OPENROUTER_API_KEY, value hidden, and its checkbox ticked |
| `10-smoke-test-output.png` | 9 | Notebook output from the smoke test: the model-load message for gemma-2-2b-it followed by the first printed persona responses |
| `11-gpu-quota.png` | 10 | Kaggle quota display showing GPU hours used and remaining for the week |
| `12-save-version.png` | 11 | Save Version dialog showing the Quick Save and Save & Run All (Commit) options |

## Facts checked against live sources (2026-10-19)

Things that change over time were checked on the live sites on **19 October 2026**. Re-check them each term.

| Fact | Where it is used | Source |
|---|---|---|
| Kaggle T4 x2 = 2 × NVIDIA T4, 4 CPU cores, 29 GB RAM; 12-hour GPU sessions; 20-minute idle timeout; 20 GB saved in `/kaggle/working`; Quick Save vs Save & Run All | Setup steps 6, 10, 11 | [Kaggle Notebooks docs](https://www.kaggle.com/docs/notebooks) |
| Weekly GPU quota: Kaggle's docs give no fixed number; about 30 hours/week is the commonly reported figure, shown in account settings | Setup step 10 | Kaggle docs (no number stated); independent reports |
| Phone verification gates GPU and Internet in notebooks | Setup step 2 | Kaggle UI messages as reported by course guides; not stated in Kaggle's docs page |
| Gemma 2 on Kaggle requires "Request Access"; Transformers variations `gemma-2-9b-it`, `gemma-2-2b-it` (version 2) exist, alongside PyTorch, Flax, GGUF, Gemma C++, and TFLite | Setup steps 4, 7 | [Kaggle model page](https://www.kaggle.com/models/google/gemma-2) and its public API |
| OpenRouter pages: `openrouter.ai/settings/credits`, `openrouter.ai/settings/keys` (`/keys` redirects there); keys can have a credit limit and are shown once | Setup step 3 | openrouter.ai |
| OpenRouter error codes 401 (invalid key), 402 (insufficient credits), 429 (rate limited) | Troubleshooting | [OpenRouter errors docs](https://openrouter.ai/docs/api_reference/errors-and-debugging) |
| Judge models: `anthropic/claude-3.5-haiku` **not available**; the notebook's `anthropic/claude-haiku-5.5` ($0.10 / $0.50 per million input / output tokens) and `google/gemma-2-27b-it` available | Concept 2, troubleshooting | OpenRouter `/api/v1/models` |
| Paper claims (sections, figures, 275 roles, 5 prompts per role, 240 questions, 0–3 judge scale with gpt-4.1-mini, PC1 cosine > 0.71 at the middle layer, Section 2.3 "one extreme of PC1", Figure 4 and Figure 7 findings) | Concept pages | [arXiv 2601.10387 (HTML)](https://arxiv.org/html/2601.10387) |
| Model sizes: Gemma 2 9B has 42 layers and d_model 3584; 2B has 26 and 2304; 27B has 46 and 4608 | Concepts 3 and 5 | `config.json` from public mirrors of the 9B and 2B models (Google's own are gated); 27B shape stated in the ARENA notebook |
| JailbreakBench (JBB-Behaviors) and HarmBench are public and MIT-licensed | Homework 2, idea 2 | GitHub and Hugging Face |
| All external links on the site return successfully | Every page | Checked with curl and the browser |

## Licensing and attribution

**Our content.** Code in this repository (`docs/assets/js`, `docs/assets/css`, and the HTML structure) is under the **MIT License**. Written content on the site (explanations, diagrams, questions, homework) is under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. See [`LICENSE`](LICENSE).

**Third-party material.** Code excerpts quoted on the concept pages, and the adapted notebook, come from:

- **ARENA**, notebook 4.4 *LLM Psychology & Persona Vectors*, in [ARENA-education/ARENA_materials](https://github.com/ARENA-education/ARENA_materials). As of 2026-10-19 that repository **has no license file and states no license**, which by default means all rights are reserved. We therefore link to it, attribute it, write every explanation in our own words, and quote only the code students need to see (function signatures, docstrings, and provided helper cells, not exercise solutions). Those excerpts remain ARENA's and are not covered by our license. **Recommendation:** before making this repository public with the adapted notebook in it, ask the ARENA team for permission or a license statement.
- **The Assistant Axis** code, [safety-research/assistant-axis](https://github.com/safety-research/assistant-axis), by Christina Lu, Jack Gallagher, Jonathan Michala, Kyle Fish, and Jack Lindsey. Its README states the **MIT License** (the repository has no separate LICENSE file). The notebook clones this repository at runtime for its transcripts and does not redistribute it here.
- **Gemma 2** weights are used under Google's [Gemma Terms of Use](https://ai.google.dev/gemma/terms), which each student accepts on Kaggle. No weights are stored in this repository.

The site footer on every page credits ARENA and the paper's authors.

### Citation

```bibtex
@misc{lu2026assistant,
  title         = {The Assistant Axis: Situating and Stabilizing the Default Persona of Language Models},
  author        = {Christina Lu and Jack Gallagher and Jonathan Michala and Kyle Fish and Jack Lindsey},
  year          = {2026},
  eprint        = {2601.10387},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL},
  url           = {https://arxiv.org/abs/2601.10387}
}
```

## Credits

Built for UCSD DataWorks by Rami Abukhater, Alec Min, and Akshar Sinha. The exercises adapt ARENA's notebook 4.4, and the science is that of Lu et al. (2026).
