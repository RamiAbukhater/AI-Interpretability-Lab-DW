/* DataWorks AI Interpretability Lab — shared page behaviour.
   No framework, no fetch: everything works from file:// as well as GitHub Pages.

   Each page's <body> carries:
     data-page  the page id from PAGES below
     data-root  relative path back to docs/ ("" for top-level pages, "../" for concepts/)

   To add, remove or reorder pages, edit PAGES. The sidebar, the prev/next
   links and the step numbers all come from this one list. */

(function () {
  "use strict";

  var PAGES = [
    { id: "home", href: "index.html", title: "Home", group: "Start", icon: "&#8962;" },
    { id: "calendar", href: "calendar.html", title: "Calendar", group: "Start", icon: "&#9638;" },
    { id: "setup", href: "setup.html", title: "Setup on Kaggle", group: "Start", step: true },
    { id: "c1", href: "concepts/01-personas.html", title: "Personas and the persona selection model", short: "Personas", group: "Concepts", step: true },
    { id: "c2", href: "concepts/02-responses-and-judging.html", title: "Role-play responses and LLM judges", short: "Responses and judging", group: "Concepts", step: true },
    { id: "c3", href: "concepts/03-residual-stream.html", title: "The residual stream and extracting activations", short: "Residual stream and activations", group: "Concepts", step: true },
    { id: "c4", href: "concepts/04-cosine-similarity.html", title: "Persona vectors and cosine similarity", short: "Cosine similarity", group: "Concepts", step: true },
    { id: "c5", href: "concepts/05-pca-assistant-axis.html", title: "PCA and the Assistant Axis", short: "PCA and the Assistant Axis", group: "Concepts", step: true },
    { id: "c6", href: "concepts/06-hooks-and-drift.html", title: "PyTorch hooks and monitoring persona drift", short: "Hooks and persona drift", group: "Concepts", step: true },
    { id: "c7", href: "concepts/07-steering.html", title: "Steering along the Assistant Axis", short: "Steering", group: "Concepts", step: true },
    { id: "hw1", href: "homework-1.html", title: "Homework 1: Setup, smoke test, Sections 1 and 2", short: "Homework 1: Notebook", group: "Homework", step: true },
    { id: "hw2", href: "homework-2.html", title: "Homework 2: Propose an extension", short: "Homework 2: Extension", group: "Homework", step: true },
    { id: "resources", href: "resources.html", title: "Resources and glossary", short: "Resources and glossary", group: "Reference", icon: "&#9733;" }
  ];

  var INSTRUCTORS = "Rami Abukhater, Alec Min, and Akshar Sinha";

  var body = document.body;
  var root = body.getAttribute("data-root") || "";
  var current = body.getAttribute("data-page");
  var idx = PAGES.findIndex(function (p) { return p.id === current; });

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* ---------- header extras (menu button, quick links) ---------- */
  var header = document.getElementById("site-header");
  if (header) {
    var spacer = document.createElement("span");
    spacer.className = "spacer";
    header.appendChild(spacer);

    var links = document.createElement("nav");
    links.className = "header-links";
    links.setAttribute("aria-label", "Quick links");
    links.innerHTML =
      '<a href="' + root + 'calendar.html">Calendar</a>' +
      '<a href="' + root + 'setup.html">Setup</a>' +
      '<a href="' + root + 'homework-1.html">Homework</a>' +
      '<a href="' + root + 'resources.html">Glossary</a>';
    header.appendChild(links);

    var toggle = document.createElement("button");
    toggle.className = "nav-toggle";
    toggle.type = "button";
    toggle.setAttribute("aria-controls", "sidebar");
    toggle.setAttribute("aria-expanded", "false");
    toggle.textContent = "Contents";
    toggle.addEventListener("click", function () {
      var open = body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    header.appendChild(toggle);
  }

  /* ---------- sidebar: the learning path ---------- */
  var sidebar = document.getElementById("sidebar");
  if (sidebar) {
    var html = "";
    var group = null;
    var n = -1; // Setup is step 0, so concept pages keep their own numbers 1 to 7
    PAGES.forEach(function (p, i) {
      if (p.group !== group) {
        if (group !== null) html += "</ol>";
        group = p.group;
        html += '<div class="path-label">' + esc(group) + "</div>";
        html += '<ol class="path' + (p.group === "Concepts" ? " steps" : "") + '">';
      }
      var num = p.step ? String(++n) : (p.icon || "&#8226;");
      var cls = i < idx && p.step ? ' class="done"' : "";
      var cur = i === idx ? ' aria-current="page"' : "";
      html += '<li><a href="' + root + p.href + '"' + cls + cur + ">" +
        '<span class="num" aria-hidden="true">' + num + "</span>" +
        '<span class="label">' + esc(p.short || p.title) + "</span></a></li>";
    });
    html += "</ol>";
    html += '<p class="meta">Work through the numbered pages in order: setup (0), concepts 1 to 7, then Homework 1 (8) and Homework 2 (9).</p>';
    sidebar.innerHTML = html;

    // close the drawer on phone after choosing a page, or on Escape
    sidebar.addEventListener("click", function (e) {
      if (e.target.closest("a")) body.classList.remove("nav-open");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") body.classList.remove("nav-open");
    });
    document.addEventListener("click", function (e) {
      if (body.classList.contains("nav-open") && !e.target.closest(".sidebar") && !e.target.closest(".nav-toggle")) {
        body.classList.remove("nav-open");
      }
    });
  }

  /* ---------- prev / next ---------- */
  var pager = document.getElementById("pager");
  if (pager && idx !== -1) {
    var prev = PAGES[idx - 1];
    var next = PAGES[idx + 1];
    var ph = "";
    if (prev) {
      ph += '<a class="prev" href="' + root + prev.href + '" rel="prev"><span class="dir">&larr; Previous</span><span class="ttl">' + esc(prev.title) + "</span></a>";
    }
    if (next) {
      ph += '<a class="next" href="' + root + next.href + '" rel="next"><span class="dir">Next &rarr;</span><span class="ttl">' + esc(next.title) + "</span></a>";
    }
    pager.innerHTML = ph;
    pager.setAttribute("aria-label", "Previous and next page");
  }

  /* ---------- footer ---------- */
  var footer = document.getElementById("site-footer");
  if (footer) {
    footer.innerHTML =
      "<p><strong>DataWorks AI Interpretability Lab</strong>, UCSD DataWorks. Leads and instructors: " + INSTRUCTORS + ".</p>" +
      '<p>Adapted from ARENA\'s notebook 4.4, <a href="https://github.com/ARENA-education/ARENA_materials/tree/main/chapter4_alignment_science/exercises/part4_persona_vectors">LLM Psychology &amp; Persona Vectors</a> (ARENA), ' +
      'which reproduces <a href="https://arxiv.org/abs/2601.10387">The Assistant Axis</a> by Christina Lu, Jack Gallagher, Jonathan Michala, Kyle Fish, and Jack Lindsey ' +
      '(<a href="https://github.com/safety-research/assistant-axis">code</a>, MIT). Explanations on this site are our own; code excerpts are quoted from those sources for teaching.</p>' +
      '<p>Site text CC BY 4.0, site code MIT. See the repository README for details.</p>';
  }

  /* ---------- copy buttons on code blocks ---------- */
  function copyWithTextarea(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (err) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  function copyText(text) {
    // Clipboard API first; fall back to execCommand, which also works from file://
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () {
        if (!copyWithTextarea(text)) throw new Error("copy failed");
      });
    }
    return copyWithTextarea(text) ? Promise.resolve() : Promise.reject(new Error("copy failed"));
  }
  function selectContents(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }
  document.querySelectorAll("pre > code").forEach(function (code) {
    var pre = code.parentElement;
    if (pre.parentElement.classList.contains("code-wrap")) return;
    var wrap = document.createElement("div");
    wrap.className = "code-wrap";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.setAttribute("aria-label", "Copy code to clipboard");
    btn.addEventListener("click", function () {
      copyText(code.textContent).then(function () {
        btn.textContent = "Copied";
        btn.classList.add("copied");
      }, function () {
        // could not copy: select the code so Ctrl+C / Cmd+C works
        selectContents(code);
        btn.textContent = "Selected, press Ctrl+C";
      });
      setTimeout(function () { btn.textContent = "Copy"; btn.classList.remove("copied"); }, 1800);
    });
    wrap.appendChild(btn);
  });

  /* ---------- screenshot slots ----------
     <figure class="shot" data-img="assets/img/setup/06-session-options.png">
     shows a placeholder until the image file exists, then shows the image.
     A leader only has to drop the PNG into docs/assets/img/setup/. */
  document.querySelectorAll("figure[data-img]").forEach(function (fig) {
    var src = root + fig.getAttribute("data-img");
    var img = new Image();
    img.onload = function () {
      var holder = fig.querySelector(".shot-placeholder");
      img.alt = (fig.querySelector(".ph-desc") || {}).textContent || "";
      img.loading = "lazy";
      if (holder) holder.replaceWith(img);
    };
    img.src = src;
  });

  /* ---------- math ---------- */
  function renderMath() {
    if (window.renderMathInElement) {
      window.renderMathInElement(document.querySelector(".content") || document.body, {
        delimiters: [
          { left: "\\[", right: "\\]", display: true },
          { left: "\\(", right: "\\)", display: false }
        ],
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
        throwOnError: false
      });
    }
  }
  if (document.readyState === "complete") renderMath();
  else window.addEventListener("load", renderMath);
})();
