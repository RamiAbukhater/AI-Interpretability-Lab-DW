# DataWorks AI Interpretability Lab

A UCSD DataWorks research group reproducing and extending Anthropic's [The Assistant Axis](https://arxiv.org/abs/2601.10387) (Lu, Gallagher, Michala, Fish, and Lindsey, 2026).

**Leads and instructors:** Rami Abukhater, Alec Min, and Akshar Sinha.

In person we only cover the high-level ideas. Setup, reading, and the notebook are homework. This repository holds the student notebook and a static website that walks students through all of it on their own:

- **Setup on Kaggle**: account, phone verification, OpenRouter key, the Gemma 2 license, GPU T4 x2, model inputs, secrets, the smoke test, quota, saving, and troubleshooting.
- **Seven concept pages**, in the order the notebook uses them, each with intuition, a diagram, the link to the paper, a code walkthrough with tensor shapes, click-to-reveal questions, and common mistakes.
- **Calendar**: meetings every Wednesday and Thursday, 7 to 8 pm, through the end of Fall 2026 instruction.
- **Homework 1** (setup, smoke test, Sections 1 and 2) and **Homework 2** (an extension proposal), each on its own page.
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
  README.md             which notebook to import into Kaggle and how
  (student notebook goes here)
docs/                   the website (GitHub Pages serves this folder)
  index.html            home
  setup.html            setup on Kaggle (the most important page)
  concepts/             01-personas.html … 07-steering.html
  calendar.html         meeting calendar (Wed and Thu, 7–8 pm)
  homework-1.html       setup, smoke test, Sections 1 and 2
  homework-2.html       extension proposal
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

## Adding the notebooks

The final notebooks have not been added yet. When they are ready:

1. Put the **student** notebook in `notebooks/` (the adaptation's README names it `persona_axis_kaggle_exercises.ipynb`).
2. In `docs/setup.html`, step 5, replace `NOTEBOOK_IMPORT_LINK` with the GitHub link to the file and remove that step's TODO banner.
3. Go through every block marked **"TODO, sync with final notebook"** (search the HTML for `todo-banner`) and replace the ARENA stand-in code with the real cells. Function names, variable names, flags, layer choices, and file paths on the site must match the notebook exactly.
4. Update `notebooks/README.md` if the file names or settings differ.

> **Do not put the solutions notebook in this repository if it is public.** The notebook is graded homework. Leaders keep `persona_axis_kaggle_solutions.ipynb` in a private repository or a shared drive. `.gitignore` also ignores `*solutions*.ipynb` as a safety net.

## Still waiting on the leads

- [ ] **Final notebook files**: the student notebook in `notebooks/`, and the solutions notebook kept privately.
- [ ] **Notebook import link**: `NOTEBOOK_IMPORT_LINK` in `docs/setup.html` (step 5).
- [ ] **Code blocks marked TODO**: 14 banners, which are:
  - `docs/setup.html`: 4 (import link, secret-loading cell, run-mode flags, troubleshooting error text)
  - `docs/concepts/01-personas.html`: 1 (persona and question definitions, including how `SMOKE_TEST` and `USE_FULL_PERSONA_LIST` choose them)
  - `docs/concepts/02-responses-and-judging.html`: 2 (default `GENERATION_BACKEND` and judge model; local generation cell with `GEN_BATCH_SIZE`)
  - `docs/concepts/03-residual-stream.html`: 1 (model loading from `/kaggle/input`, float16 or 8-bit fallback, extraction functions)
  - `docs/concepts/04-cosine-similarity.html`: 1
  - `docs/concepts/05-pca-assistant-axis.html`: 2 (PCA code; which 27B reference plots are drawn)
  - `docs/concepts/06-hooks-and-drift.html`: 1 (transcripts loaded, `max_assistant_turns`)
  - `docs/concepts/07-steering.html`: 1 (suggested alpha values)
- [ ] **Judge model name.** ARENA's `AUTORATER_MODEL = "anthropic/claude-3.5-haiku"` **is no longer listed on OpenRouter** (checked 2026-10-19), so any judge or autorater call using it will fail. Currently listed options include `anthropic/claude-haiku-4.5` and `openai/gpt-4.1-mini` (the judge the paper used). Make sure the final notebook uses one that exists, and update `concepts/02-responses-and-judging.html` to match.
- [ ] **Homework due dates and submission method**: `DUE_DATE_HW1` and `SUBMISSION_METHOD` in `docs/homework-1.html`; `DUE_DATE_HW2` and `SUBMISSION_METHOD` in `docs/homework-2.html`.
- [ ] **Meeting location**: `LOCATION` placeholders in `docs/calendar.html`. Also confirm the date range (Wed Oct 21 to Thu Dec 3, 2026) and that there is no meeting on Veterans Day (Nov 11) or Thanksgiving (Nov 26). To change dates, edit the month tables and the "All meetings" table in that file directly.
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
| Judge models: `anthropic/claude-3.5-haiku` **not available**; `anthropic/claude-haiku-4.5`, `openai/gpt-4.1-mini`, `google/gemma-2-27b-it` available | Concept 2, troubleshooting | OpenRouter `/api/v1/models` |
| Paper claims (sections, figures, 275 roles, 5 prompts per role, 240 questions, 0–3 judge scale with gpt-4.1-mini, PC1 cosine > 0.71 at the middle layer, Section 2.3 "one extreme of PC1", Figure 4 and Figure 7 findings) | Concept pages | [arXiv 2601.10387 (HTML)](https://arxiv.org/html/2601.10387) |
| Model sizes: Gemma 2 9B has 42 layers and d_model 3584; 2B has 26 and 2304; 27B has 46 and 4608 | Concepts 3 and 5 | `config.json` from public mirrors of the 9B and 2B models (Google's own are gated); 27B shape stated in the ARENA notebook |
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
