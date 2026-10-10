// Notebook download affordances for the Quarto site.
//
// 1. On a rendered tutorial-notebook page (/tutorials/notebooks/<name>.html),
//    inject a prominent "Download this notebook" button linking to the raw
//    .ipynb copied to /downloads/notebooks/ by scripts/copy-notebooks.sh.
//    This is the Quarto replacement for mkdocs-jupyter's `page.nb_url` button.
// 2. Force any link that points at a .ipynb file to download rather than
//    navigate (the behaviour of the old force-ipynb-download2.js).
document.addEventListener("DOMContentLoaded", () => {
  const m = window.location.pathname.match(/\/tutorials\/notebooks\/([^\/]+)\.html$/);
  if (m) {
    const file = m[1] + ".ipynb";
    // Root-relative: correct on the live site and under `quarto preview`.
    const href = "/downloads/notebooks/" + file;
    const a = document.createElement("a");
    a.href = href;
    a.setAttribute("download", file);
    a.className = "nb-download-button";
    a.textContent = "⬇️  Download this notebook (.ipynb)";
    const main =
      document.querySelector("main#quarto-document-content") ||
      document.querySelector("main.content") ||
      document.querySelector("main");
    if (main) main.insertBefore(a, main.firstChild);
  }

  document.querySelectorAll('a[href$=".ipynb"]').forEach((a) => {
    const name = (a.getAttribute("href") || "notebook.ipynb").split("/").pop();
    a.setAttribute("download", name);
  });
});
