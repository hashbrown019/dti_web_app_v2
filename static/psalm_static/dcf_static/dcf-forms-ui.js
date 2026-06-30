(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    decorateEditModals();

    var match = window.location.pathname.match(/^\/dcf\/form(1|2|3|4|5|6|7|9|10|11)\/?$/);
    if (!match) return;

    var formNumber = match[1];
    document.documentElement.classList.add("dcf-form-document");
    document.body.classList.add("dcf-form-page", "dcf-form-" + formNumber);

    var contentRoot = document.querySelector(".main_container");
    var formRoot = document.querySelector(".x-card") ||
      document.querySelector(".tab-container") ||
      document.querySelector(".tab-content");
    if (!contentRoot || !formRoot) return;

    var pageShell = document.createElement("main");
    pageShell.className = "dcf-form-shell";
    formRoot.parentNode.insertBefore(pageShell, formRoot);

    var current = formRoot;
    while (current) {
      var next = current.nextSibling;
      pageShell.appendChild(current);
      current = next;
    }

    initializeDcfTooltips(pageShell);

    var legacyHeading = pageShell.querySelector(":scope > .x-card > center:first-child h2:first-child");
    if (legacyHeading) legacyHeading.classList.add("dcf-original-form-heading");

    Array.prototype.forEach.call(pageShell.querySelectorAll("h2"), function (heading) {
      if (heading.classList.contains("dcf-original-form-heading")) return;
      if (heading.closest(".x_title")) return;
      heading.classList.add("dcf-form-section-title");
    });

    Array.prototype.forEach.call(pageShell.querySelectorAll("table"), function (table) {
      table.classList.add("dcf-form-table");
      decorateCompactTable(table);
      decorateTableGroups(table);
      var wrapper = table.parentElement;
      if (wrapper && wrapper.classList.contains("x-table-responsive-wrap")) {
        wrapper.classList.add("dcf-form-table-wrap");
      }
    });
    decorateAddRowButtons(pageShell);

    Array.prototype.forEach.call(pageShell.querySelectorAll('input[readonly], textarea[readonly]'), function (field) {
      field.classList.add("dcf-readonly-field");
    });

    var primaryFormCard = pageShell.querySelector(":scope > .x-card");
    Array.prototype.forEach.call(pageShell.querySelectorAll("button"), function (button) {
      if (/^\s*submit\s*$/i.test(button.textContent || "")) {
        button.classList.add("dcf-submit-button");
        if (!button.querySelector(".dcf-submit-icon")) {
          var icon = document.createElement("i");
          icon.className = "fa fa-paper-plane dcf-submit-icon";
          icon.setAttribute("aria-hidden", "true");
          button.insertBefore(icon, button.firstChild);
        }

        var legacyHolder = button.closest("p#submit_btn_holder");
        var holder = legacyHolder || button.closest(".card-footer, .submit_btn_holder, .x-row");
        if (!holder) return;

        holder.classList.add("dcf-form-actions");
        holder.classList.remove("x-right");

        // Forms 1-10 place Submit inside floated paragraphs in differently
        // nested rows. Move only that visual container to the form-card footer.
        // The button and its original onclick handler remain unchanged.
        if (legacyHolder && primaryFormCard && legacyHolder.parentNode !== primaryFormCard) {
          primaryFormCard.appendChild(legacyHolder);
        }
      }
    });

    if (formNumber === "4") {
      var headings = pageShell.querySelectorAll(":scope > .x-card > center:first-child h2");
      if (headings.length > 1) headings[1].classList.add("dcf-form-notice");
    }

    initializeEmbeddedFormHeight(pageShell);
  });

  function initializeEmbeddedFormHeight(pageShell) {
    if (window.parent === window || !pageShell) return;

    var reportTimer = null;
    var lastHeight = 0;

    function reportHeight() {
      var shellBounds = pageShell.getBoundingClientRect();
      var bodyStyles = window.getComputedStyle(document.body);
      var bottomPadding = parseFloat(bodyStyles.paddingBottom) || 0;
      var height = Math.ceil(shellBounds.bottom + window.scrollY + bottomPadding);

      if (height > 0 && Math.abs(height - lastHeight) > 1) {
        lastHeight = height;
        window.parent.postMessage({
          type: "dcf-form-content-height",
          height: height
        }, window.location.origin);
      }
    }

    function queueHeightReport() {
      window.clearTimeout(reportTimer);
      reportTimer = window.setTimeout(reportHeight, 60);
    }

    window.addEventListener("load", queueHeightReport);
    window.addEventListener("resize", queueHeightReport);

    if (window.ResizeObserver) {
      new ResizeObserver(queueHeightReport).observe(pageShell);
    } else if (window.MutationObserver) {
      new MutationObserver(queueHeightReport).observe(pageShell, {
        childList: true,
        subtree: true,
        attributes: true
      });
    }

    queueHeightReport();
  }

  function decorateEditModals() {
    var allowedForms = /^(1|2|3|4|5|6|7|9|10|11)$/;
    var editModals = document.querySelectorAll('.modal[id^="form"][id*="edit"]');

    Array.prototype.forEach.call(editModals, function (modal) {
      var idMatch = modal.id.match(/^form(\d+)edit/);
      if (!idMatch || !allowedForms.test(idMatch[1])) return;

      modal.classList.add("dcf-edit-modal", "dcf-edit-modal-form-" + idMatch[1]);
      initializeDcfTooltips(modal);

      Array.prototype.forEach.call(modal.querySelectorAll("h2"), function (heading) {
        heading.classList.add("dcf-edit-section-title");
      });

      Array.prototype.forEach.call(modal.querySelectorAll("table"), function (table) {
        table.classList.add("dcf-edit-table");
        decorateCompactTable(table);
        decorateTableGroups(table);
        var wrapper = table.closest(".x-table-responsive-wrap, .table-responsive");
        if (wrapper) wrapper.classList.add("dcf-edit-table-wrap");
      });
      decorateAddRowButtons(modal);

      Array.prototype.forEach.call(modal.querySelectorAll('input[readonly], textarea[readonly]'), function (field) {
        field.classList.add("dcf-edit-readonly");
      });

      Array.prototype.forEach.call(modal.querySelectorAll("button, input[type='submit']"), function (button) {
        var text = button.textContent || button.value || "";
        if (/update|save/i.test(text)) button.classList.add("dcf-edit-save");
      });
    });
  }

  function decorateAddRowButtons(root) {
    Array.prototype.forEach.call(root.querySelectorAll('button[onclick*="add_row"]'), function (button) {
      button.classList.add("dcf-add-row-button");
      button.removeAttribute("style");
      button.setAttribute("aria-label", "Add row");
      button.setAttribute("title", "Add another row");
      button.innerHTML =
        '<i class="fa fa-plus-circle" aria-hidden="true"></i>' +
        '<span class="dcf-add-row-label">Add Row</span>';

      if (!button.dataset.dcfTableRefreshBound) {
        button.addEventListener("click", function () {
          window.setTimeout(function () {
            var table = button.closest("table");
            if (!table) return;
            decorateCompactTable(table);
            decorateTableGroups(table);
          }, 0);
        });
        button.dataset.dcfTableRefreshBound = "true";
      }
    });

    Array.prototype.forEach.call(
      root.querySelectorAll('button[onclick*="delete_row"], button[onclick*="remove_row"]'),
      function (button) {
        if (!/remove|delete/i.test(button.textContent || "")) return;
        button.classList.add("dcf-remove-row-button");
        button.removeAttribute("style");
        button.setAttribute("aria-label", "Remove empty row");
        button.setAttribute("title", "Remove an empty row");
        button.innerHTML =
          '<i class="fa fa-trash" aria-hidden="true"></i>' +
          '<span class="dcf-remove-row-label">Remove Empty Row</span>';
      }
    );
  }

  function decorateTableGroups(table) {
    if (!table.rows || table.rows.length < 2) return;

    var headerRow = Array.prototype.find.call(table.rows, function (row) {
      var spanningCells = Array.prototype.filter.call(row.cells, function (cell) {
        return parseInt(cell.getAttribute("colspan") || "1", 10) > 1;
      });
      return spanningCells.length >= 2;
    });
    if (!headerRow) return;

    table.classList.add("dcf-grouped-table");
    headerRow.classList.add("dcf-group-title-row");

    var headerCells = Array.prototype.slice.call(headerRow.cells);
    var groupStarts = [];
    var columnIndex = 0;

    headerCells.forEach(function (cell, groupIndex) {
      var span = parseInt(cell.getAttribute("colspan") || "1", 10);
      cell.classList.add("dcf-group-header", "dcf-group-" + ((groupIndex % 2) + 1));
      if (columnIndex > 0) {
        cell.classList.add("dcf-group-start");
        groupStarts.push(columnIndex);
      }
      columnIndex += span;
    });

    Array.prototype.slice.call(table.rows, headerRow.rowIndex + 1).forEach(function (row) {
      var logicalColumn = 0;

      Array.prototype.forEach.call(row.cells, function (cell) {
        var cellSpan = parseInt(cell.getAttribute("colspan") || "1", 10);
        var groupIndex = 0;

        for (var i = 0; i < groupStarts.length; i += 1) {
          if (logicalColumn >= groupStarts[i]) groupIndex = i + 1;
        }

        cell.classList.add("dcf-group-" + ((groupIndex % 2) + 1));
        if (groupStarts.indexOf(logicalColumn) !== -1) {
          cell.classList.add("dcf-group-start");
        }

        logicalColumn += cellSpan;
      });
    });
  }

  function decorateCompactTable(table) {
    if (!table.rows || !table.rows.length) return;

    var maxColumns = Array.prototype.reduce.call(table.rows, function (maximum, row) {
      var columns = Array.prototype.reduce.call(row.cells, function (total, cell) {
        return total + parseInt(cell.getAttribute("colspan") || "1", 10);
      }, 0);
      return Math.max(maximum, columns);
    }, 0);

    if (maxColumns <= 4) {
      table.classList.add("dcf-compact-table");
      var wrapper = table.closest(".x-table-responsive-wrap, .table-responsive");
      if (wrapper) wrapper.classList.add("dcf-compact-table-wrap");
    }
  }

  function initializeDcfTooltips(root) {
    var tools = root.querySelectorAll(".tool[data-tip]");
    if (!tools.length) return;

    var tooltip = document.getElementById("dcf-floating-tooltip");
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.id = "dcf-floating-tooltip";
      tooltip.className = "dcf-floating-tooltip";
      tooltip.setAttribute("role", "tooltip");
      tooltip.setAttribute("aria-hidden", "true");
      document.body.appendChild(tooltip);
    }

    function positionTooltip(tool) {
      var rect = tool.getBoundingClientRect();
      var gap = 10;
      var viewportPadding = 12;
      var tooltipRect = tooltip.getBoundingClientRect();
      var left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
      var top = rect.top - tooltipRect.height - gap;

      left = Math.max(
        viewportPadding,
        Math.min(left, window.innerWidth - tooltipRect.width - viewportPadding)
      );

      if (top < viewportPadding) {
        top = rect.bottom + gap;
        tooltip.classList.add("dcf-tooltip-below");
      } else {
        tooltip.classList.remove("dcf-tooltip-below");
      }

      tooltip.style.left = Math.round(left) + "px";
      tooltip.style.top = Math.round(top) + "px";
    }

    function showTooltip(tool) {
      var message = tool.getAttribute("data-tip");
      if (!message) return;

      tooltip.textContent = message;
      tooltip.classList.add("is-visible");
      tooltip.setAttribute("aria-hidden", "false");
      tooltip._dcfAnchor = tool;
      positionTooltip(tool);
    }

    function hideTooltip(tool) {
      if (tooltip._dcfAnchor && tooltip._dcfAnchor !== tool) return;
      tooltip.classList.remove("is-visible", "dcf-tooltip-below");
      tooltip.setAttribute("aria-hidden", "true");
      tooltip._dcfAnchor = null;
    }

    Array.prototype.forEach.call(tools, function (tool) {
      if (tool.dataset.dcfTooltipBound) return;

      tool.classList.add("dcf-tooltip-trigger");
      tool.setAttribute("aria-describedby", "dcf-floating-tooltip");
      tool.addEventListener("mouseenter", function () { showTooltip(tool); });
      tool.addEventListener("mouseleave", function () { hideTooltip(tool); });
      tool.addEventListener("focus", function () { showTooltip(tool); });
      tool.addEventListener("blur", function () { hideTooltip(tool); });
      tool.dataset.dcfTooltipBound = "true";
    });

    if (!window.__dcfTooltipViewportBound) {
      window.addEventListener("scroll", function () {
        if (tooltip._dcfAnchor && tooltip.classList.contains("is-visible")) {
          positionTooltip(tooltip._dcfAnchor);
        }
      }, true);
      window.addEventListener("resize", function () {
        if (tooltip._dcfAnchor && tooltip.classList.contains("is-visible")) {
          positionTooltip(tooltip._dcfAnchor);
        }
      });
      window.__dcfTooltipViewportBound = true;
    }
  }
})();
