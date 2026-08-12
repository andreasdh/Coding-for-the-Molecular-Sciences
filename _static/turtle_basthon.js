/* Add selected interactive Basthon examples to the loops chapter. */
(function () {
  "use strict";

  function insertExample(codeMarkers, filename, leadText, height) {
    var blocks = Array.from(document.querySelectorAll("div.highlight, pre"));
    var block = blocks.find(function (node) {
      var text = node.textContent || "";
      return codeMarkers.every(function (marker) { return text.includes(marker); });
    });

    if (!block || block.dataset.basthonEmbedded === "true") return;
    block.dataset.basthonEmbedded = "true";

    var container = block.closest("div.cell") || block.parentElement;
    var paragraph = document.createElement("p");
    paragraph.textContent = leadText;

    var iframe = document.createElement("iframe");
    iframe.src = "../../basthon/?from=examples/" + filename;
    iframe.width = "100%";
    iframe.height = String(height || 560);
    iframe.frameBorder = "0";
    iframe.loading = "lazy";
    iframe.allowFullscreen = true;
    iframe.title = "Interactive Python editor: " + filename.replace(/_/g, " ").replace(/\.py$/, "");

    container.insertAdjacentElement("afterend", paragraph);
    paragraph.insertAdjacentElement("afterend", iframe);
  }

  function boot() {
    if (!window.location.pathname.includes("/docs/fundamental_programming/loops")) return;

    insertExample(
      ['shape("turtle")', 'forward(80)', 'left(60)'],
      "loops_turtle_intro.py",
      "Try the turtle commands in the interactive editor below.",
      540
    );
    insertExample(
      ["number_of_sides = 6", "turning_angle = 360 / number_of_sides"],
      "loops_turtle_benzene.py",
      "Run the hexagon example below and experiment with the number of sides, side length, and turning angle.",
      600
    );
    insertExample(
      ["possible_directions = [0, 90, 180, 270]", "number_of_steps = 200"],
      "loops_turtle_random_walk.py",
      "Explore the random-walk model in the editor below. Repeated runs will normally produce different trajectories.",
      620
    );
    insertExample(
      ["for measurement in range(5)", "Performing measurement number"],
      "loops_for_measurements.py",
      "Try changing the range and predict the output before running the code.",
      500
    );
    insertExample(
      ["amount_mg = 10.0", "for _ in range(5)"],
      "loops_half_life.py",
      "Use the editor below to explore repeated halving.",
      520
    );
    insertExample(
      ["k = 0.15", "number_of_steps = int(end_time / dt)"],
      "loops_kinetic_model.py",
      "Run the kinetic model below and investigate how the result changes with the time step.",
      650
    );
    insertExample(
      ["for number_of_half_lives in range(11)", "amount = amount / 2"],
      "loops_radioactive_sequence.py",
      "Explore the recursive half-life sequence in the editor below.",
      540
    );
    insertExample(
      ["number_of_terms = 100", "term = (2 / 3)**n"],
      "loops_geometric_series.py",
      "Use the editor below to investigate how the partial sum approaches its limiting value.",
      560
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

/* Give learning outcomes and theory/definition admonitions distinct visual roles. */
(function () {
  "use strict";

  var style = document.createElement("style");
  style.id = "molecular-sciences-admonition-roles";
  style.textContent = [
    "div.admonition.theory-definition { border-left-color:#3a7a9c !important; background-color:#eef5fa !important; }",
    "div.admonition.theory-definition > p.admonition-title { background-color:#3a7a9c !important; color:#faf7f2 !important; }",
    "div.admonition.learning-outcomes { border-left-color:#58745d !important; background-color:#eef5ef !important; }",
    "div.admonition.learning-outcomes > p.admonition-title { background-color:#58745d !important; color:#faf7f2 !important; }"
  ].join("\n");
  document.head.appendChild(style);

  function classifyAdmonitions() {
    var semanticClasses = ["tip", "note", "warning", "dropdown", "important", "caution", "attention", "danger", "error", "seealso"];

    document.querySelectorAll("div.admonition > p.admonition-title").forEach(function (title) {
      var box = title.closest("div.admonition");
      if (!box) return;

      var label = (title.textContent || "").trim().toLowerCase();
      if (label === "learning outcomes") {
        box.classList.add("learning-outcomes");
        return;
      }

      var alreadyTyped = semanticClasses.some(function (name) {
        return box.classList.contains(name);
      });
      if (!alreadyTyped) box.classList.add("theory-definition");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", classifyAdmonitions);
  } else {
    classifyAdmonitions();
  }
})();
