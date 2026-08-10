/* Render NGL protein viewers on the static Jupyter Book page.
   nglview works against a live Jupyter kernel in VS Code. The published book
   has no kernel, so this script mirrors PDB-based nglview examples directly
   with NGL.js while leaving the Python examples unchanged. */
(function () {
  "use strict";

  function loadNGL() {
    if (window.NGL) return Promise.resolve();
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/ngl@2.0.0-dev.39/dist/ngl.js";
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  function pdbIdFromCode(text) {
    var patterns = [
      /show_pdbid\s*\(\s*["']([A-Za-z0-9]{4})["']\s*\)/,
      /show_pdb\s*\(\s*["']([A-Za-z0-9]{4})["']\s*\)/,
      /rcsb:\/\/([A-Za-z0-9]{4})/i
    ];
    for (var i = 0; i < patterns.length; i++) {
      var match = text.match(patterns[i]);
      if (match) return match[1].toUpperCase();
    }
    return null;
  }

  function representationFromCode(text) {
    if (/add_surface|surface/i.test(text)) return "surface";
    if (/add_ball_and_stick|ball\+stick|ball_and_stick/i.test(text)) return "ball+stick";
    if (/add_licorice|licorice/i.test(text)) return "licorice";
    if (/add_spacefill|spacefill/i.test(text)) return "spacefill";
    return "cartoon";
  }

  function addViewer(block, pdbId, representation) {
    var cell = block.closest("div.cell") || block.parentElement;
    if (!cell || cell.dataset.nglStaticAdded === "true") return;
    cell.dataset.nglStaticAdded = "true";

    var wrapper = document.createElement("div");
    wrapper.className = "ngl-static-wrapper";
    wrapper.style.margin = "0.8rem 0 1.4rem";

    var note = document.createElement("div");
    note.textContent = "Interactive NGL viewer — drag to rotate, scroll to zoom.";
    note.style.fontSize = "0.9rem";
    note.style.marginBottom = "0.35rem";
    note.style.opacity = "0.8";

    var viewer = document.createElement("div");
    viewer.style.width = "100%";
    viewer.style.height = "480px";
    viewer.style.border = "1px solid rgba(0,0,0,.12)";
    viewer.style.borderRadius = "8px";
    viewer.style.overflow = "hidden";

    wrapper.appendChild(note);
    wrapper.appendChild(viewer);
    cell.insertAdjacentElement("afterend", wrapper);

    loadNGL().then(function () {
      var stage = new NGL.Stage(viewer, { backgroundColor: "white" });
      stage.loadFile("rcsb://" + pdbId, { defaultRepresentation: false }).then(function (component) {
        if (representation === "surface") {
          component.addRepresentation("cartoon", { colorScheme: "residueindex" });
          component.addRepresentation("surface", { opacity: 0.35, colorScheme: "hydrophobicity" });
        } else {
          component.addRepresentation(representation, { colorScheme: "residueindex" });
        }
        component.autoView();
      });
      window.addEventListener("resize", function () { stage.handleResize(); });
    }).catch(function () {
      note.textContent = "The interactive NGL viewer could not be loaded. The Python example can still be run in VS Code.";
    });
  }

  function boot() {
    if (!window.location.pathname.includes("/docs/data_handling/molecular_visualisation")) return;
    document.querySelectorAll("div.highlight, pre").forEach(function (block) {
      var text = block.textContent || "";
      if (!/nglview|\bnv\.|show_pdb|rcsb:\/\//i.test(text)) return;
      var pdbId = pdbIdFromCode(text);
      if (pdbId) addViewer(block, pdbId, representationFromCode(text));
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
