// Force same-origin .ipynb links to download instead of rendering JSON
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href$=".ipynb"]').forEach((a) => {
    try {
      const url = new URL(a.getAttribute("href"), window.location.href);

      // Only apply to same-origin links (download attribute is more reliable)
      if (url.origin !== window.location.origin) return;

      // Add the download attribute so the browser downloads it
      const filename = url.pathname.split("/").pop() || "notebook.ipynb";
      a.setAttribute("download", filename);

      // Optional: avoid opening in a new tab
      if (a.getAttribute("target") === "_blank") a.removeAttribute("target");
    } catch (e) {
      // ignore malformed hrefs
    }
  });
});
