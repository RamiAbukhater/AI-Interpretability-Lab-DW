# <div align="center">DataWorks AI Interpretability Lab</div>
### <div align="center">UC San Diego DataWorks Research Group</div>
#### <div align="center">Reproducing and extending Anthropic's <em>Assistant Axis</em></div>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-notebooks-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-forward%20hooks-EE4C2C?style=flat-square&logo=pytorch&logoColor=white">
  <img alt="Hugging Face Transformers" src="https://img.shields.io/badge/Transformers-Gemma%202%209B-FFD21E?style=flat-square&logo=huggingface&logoColor=black">
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-GPU%20T4%20x2-20BEFF?style=flat-square&logo=kaggle&logoColor=white">
  <img alt="OpenRouter" src="https://img.shields.io/badge/OpenRouter-LLM%20judge-111111?style=flat-square">
  <img alt="GitHub Pages" src="https://img.shields.io/badge/GitHub%20Pages-course%20site-222222?style=flat-square&logo=github&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT%20%2B%20CC%20BY%204.0-2E7D32?style=flat-square">
</p>

<p align="center"><strong><a href="https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/">Course site: ramiabukhater.github.io/AI-Interpretability-Lab-DW</a></strong></p>

Repository for the UC San Diego DataWorks AI Interpretability Lab. It holds the lab notebook, which runs on Kaggle's free GPUs, and the course site, which walks students through setup, every concept the notebook covers, and the homework.

In meetings we cover the ideas at a high level. Setup, reading, and the notebook are done as homework, so the site is written to be followed on your own.

> **AI-generated content.** The course site's pages were written with Claude, an AI model, and may contain inaccuracies or mistakes. If something looks wrong, please point it out to Rami or Akshar so it can be fixed.

## Abstract

Language models learn to play many characters during pre-training, and post-training makes one of them, the helpful Assistant, the default. [The Assistant Axis](https://arxiv.org/abs/2601.10387) (Lu, Gallagher, Michala, Fish, and Lindsey, 2026) finds a single direction in a model's activations that separates the Assistant from everything else. Projecting onto that direction shows when a conversation is pulling the model out of character, and adding it during generation steers the model's behaviour.

This lab reproduces the core results on Gemma 2 9B Instruct, using an adapted version of [ARENA's notebook 4.4](https://github.com/ARENA-education/ARENA_materials/blob/main/chapter4_alignment_science/exercises/part4_persona_vectors/4.4_LLM_Psychology_%26_Persona_Vectors_exercises.ipynb). Students map persona space, build the Assistant Axis, monitor drift in real transcripts, and steer the model. Then each team proposes an extension of its own.

- **Organization**: UC San Diego DataWorks
- **Leads and instructors**: Rami Abukhater, Akshar Sinha
- **Paper**: [arXiv 2601.10387](https://arxiv.org/abs/2601.10387) · [code](https://github.com/safety-research/assistant-axis)

## Project Goals

- Reproduce the Assistant Axis on a model that fits on free hardware (Gemma 2 9B on Kaggle's T4 x2).
- Give every student a self-contained path from setup to results, with each concept explained in plain language.
- Make individual work checkable: each student adds two personas of their own and projects them onto a shared PCA.
- Combine the class's personas into one shared persona map.
- Seed student research extensions, from multi-agent drift to personality structure.

## Repository Structure

```text
AI-Interpretability-Lab-DW/
├── README.md
├── LICENSE                          # MIT for code, CC BY 4.0 for written content
├── docs/                            # the course site, served by GitHub Pages
│   ├── index.html                   # home
│   ├── calendar.html                # meetings, workshops, deadlines
│   ├── setup.html                   # Kaggle setup walkthrough
│   ├── concepts/                    # seven concept pages, 01 to 07
│   ├── homework-0.html … homework-2.html
│   ├── resources.html               # sources and glossary
│   ├── notebooks/                   # download copy of the student notebook
│   └── assets/                      # css, js, favicon
├── notebooks/
│   ├── persona_axis_kaggle_exercises.ipynb   # the student notebook
│   ├── helper_cells/                # Homework 1 Part C cells as plain Python
│   └── README.md
└── scripts/
    └── class_persona_map.py         # combines students' personas into one class map
```

## Quick Start

**Students.** Open the [course site](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/) and start with [Setup on Kaggle](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/setup.html). In short:

1. Download [`persona_axis_kaggle_exercises.ipynb`](notebooks/persona_axis_kaggle_exercises.ipynb) and import it into Kaggle (**File → Import Notebook**).
2. In **Session options**, set Accelerator to **GPU T4 x2** and turn on **Internet**.
3. In **Add Input → Models**, add **Gemma 2**, framework **Transformers**, variations `gemma-2-9b-it` and `gemma-2-2b-it`.
4. In **Add-ons → Secrets**, add your OpenRouter key with the label exactly `OPENROUTER_API_KEY`, and tick it.
5. Run once with `SMOKE_TEST = True`, then set it to `False` for the full 9B run (about 12 minutes).

**Viewing the site locally.** Open `docs/index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000 --directory docs
```

## Recommended Reading Order

1. [Home](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/) and the [Calendar](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/calendar.html)
2. [Homework 0](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/homework-0.html): introduce yourself on Discord
3. [Setup on Kaggle](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/setup.html)
4. Concepts 1 to 7: [personas](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/concepts/01-personas.html), judging, the residual stream, cosine similarity, PCA and the Assistant Axis, hooks and drift, steering
5. [Homework 1](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/homework-1.html): run the notebook and place two personas of your own
6. [Homework 2](https://ramiabukhater.github.io/AI-Interpretability-Lab-DW/homework-2.html): choose and propose an extension

## Development Workflow

The site is plain HTML, CSS, and a little JavaScript, with no build step. Commit to `main` and GitHub Pages republishes `docs/` within a minute or two.

- **Pages:** edit the files in `docs/` directly. The page order, sidebar, and prev/next links come from the `PAGES` list in `docs/assets/js/site.js`, and the footer is defined there too. Math uses KaTeX (`\( … \)` and `\[ … \]`); code blocks are `<pre><code class="language-python">`.
- **Notebook:** the concept pages quote the student notebook's code. If you change a function, variable, or flag in the notebook, update the matching page. After editing the notebook, refresh the site's download copy:

  ```bash
  cp notebooks/persona_axis_kaggle_exercises.ipynb docs/notebooks/
  ```

- **Homework 1, Part C cells:** these live both in `notebooks/helper_cells/` and inside the notebook, so edit both.
- **Shared PCA:** the published [DataWorks Shared PCA](https://www.kaggle.com/datasets/ramiabukhater/dataworks-shared-pca) dataset (basis `8ac3ff730a74`) must not be regenerated mid-quarter. Students' results only combine on the class map when they use the same basis.
- **Class map:** collect students' `my_personas.json` files into one folder, then run:

  ```bash
  python scripts/class_persona_map.py --shared shared_pca.json --students submissions/ --out class_persona_map.png --csv class_personas.csv
  ```

- **Never commit** the solutions notebook or the leaders' notes. Both are gitignored on purpose; the notebook is graded homework.

## Acknowledgments

The exercises adapt ARENA's notebook 4.4, *LLM Psychology & Persona Vectors* ([ARENA](https://github.com/ARENA-education/ARENA_materials)), and the science is that of Lu et al. (2026), [The Assistant Axis](https://arxiv.org/abs/2601.10387) ([code](https://github.com/safety-research/assistant-axis), MIT). Explanations on the site are our own; code excerpts are quoted from those sources for teaching. ARENA's repository states no license, so its material remains its authors'. Gemma 2 is used under Google's [Gemma Terms of Use](https://ai.google.dev/gemma/terms).

Our code is MIT-licensed and our written content is CC BY 4.0; see [`LICENSE`](LICENSE).

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

## Contacts

* Rami Abukhater: [@RamiAbukhater](https://github.com/RamiAbukhater)
* Akshar Sinha
* Lab members: the general research chat on the DataWorks Discord
