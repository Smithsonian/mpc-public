console.log("force-ipynb-download.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href$=".ipynb"]').forEach((a) => {
    const url = new URL(a.getAttribute("href"), window.location.href);
    if (url.origin !== window.location.origin) return;
    a.setAttribute("download", url.pathname.split("/").pop() || "notebook.ipynb");
  });
});


