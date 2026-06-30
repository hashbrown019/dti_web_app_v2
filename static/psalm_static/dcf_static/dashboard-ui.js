(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var match = window.location.pathname.match(/\/form(1|2|3|4|5|6|7|9|10|11)_dashboard\/?$/);
    if (!match) return;

    var formNumber = match[1];
    var dashboards = {
      "1": ["DIP Profile Dashboard", "Monitor DIPs, farming households, commodities, and enterprise participation.", "fa-bar-chart"],
      "2": ["Market Access Tracker Dashboard", "Track partnerships, members, agreements, commodities, and sales performance.", "fa-bar-chart"],
      "3": ["BDSP Dashboard", "Review registered service providers, expertise, and accreditation coverage.", "fa-bar-chart"],
      "4": ["CapBuild Dashboard", "Explore training reach across organizations, MSMEs, and individual participants.", "fa-bar-chart"],
      "5": ["Investment Tracker Dashboard", "Follow expansion, rehabilitation, and productive investment implementation.", "fa-bar-chart"],
      "6": ["Product Dev Dashboard", "Monitor technical activities, participants, products, systems, and certifications.", "fa-bar-chart"],
      "7": ["Trade Promotion Dashboard", "Track assisted enterprises, market linkages, activities, and generated sales.", "fa-bar-chart"],
      "9": ["Enablers Activity Dashboard", "Review enabling activities, delivery records, and implementation details.", "fa-bar-chart"],
      "10": ["Negosyo Center Dashboard", "Monitor Negosyo Center records, coverage, and operational information.", "fa-bar-chart"],
      "11": ["Access to Finance Dashboard", "Understand financial-service access among farmers, FOs, and MSMEs.", "fa-bar-chart"]
    };
    var meta = dashboards[formNumber];
    var contentRoot = document.querySelector(".right_col") || document.querySelector(".main_container");
    if (!contentRoot || !meta) return;

    document.title = meta[0];
    document.body.classList.add("dcf-dashboard-page");
    document.body.classList.add("dcf-dashboard-form-" + formNumber);

    var hero = document.createElement("section");
    hero.className = "dcf-dashboard-hero";
    hero.setAttribute("aria-labelledby", "dcf-dashboard-title");
    hero.innerHTML =
      '<div class="dcf-dashboard-hero-copy">' +
        '<div class="dcf-dashboard-eyebrow"><i class="fa fa-line-chart"></i> Data Capture Forms</div>' +
        '<h1 id="dcf-dashboard-title">' + meta[0] + '</h1>' +
        '<p>' + meta[1] + '</p>' +
      '</div>' +
      '<div class="dcf-dashboard-actions" aria-label="Dashboard shortcuts">' +
        '<button type="button" class="dcf-hero-action dcf-hero-action-primary" data-dashboard-action="records">' +
          '<i class="fa fa-table" aria-hidden="true"></i><span>View records</span>' +
        '</button>' +
        '<button type="button" class="dcf-hero-action" data-dashboard-action="export">' +
          '<i class="fa fa-cloud-download" aria-hidden="true"></i><span>Export data</span>' +
        '</button>' +
        '<button type="button" class="dcf-hero-action" data-dashboard-action="import">' +
          '<i class="fa fa-exchange" aria-hidden="true"></i><span>Import tools</span>' +
        '</button>' +
      '</div>';
    Array.prototype.forEach.call(contentRoot.querySelectorAll(".tile-stats"), function (tile) {
      var column = tile.parentElement;
      if (column) column.classList.add("dcf-tile-column");

      var labelElement = tile.querySelector("h3");
      var label = labelElement ? labelElement.textContent.trim().toLowerCase() : "";
      var iconClass = "fa-list-alt";
      var iconRules = [
        [/negosyo center/, "fa-university"],
        [/total sales|investment|financ/, "fa-money"],
        [/products certified/, "fa-certificate"],
        [/products? (developed|improved)/, "fa-cube"],
        [/systems? (developed|introduced)/, "fa-cogs"],
        [/total activities/, "fa-calendar-check-o"],
        [/linked/, "fa-link"],
        [/with cpa/, "fa-list-alt"],
        [/rehabilitation/, "fa-wrench"],
        [/expansion/, "fa-expand"],
        [/productive inves/, "fa-line-chart"],
        [/large enterprise/, "fa-building"],
        [/medium enterprises?/, "fa-industry"],
        [/small enterprises?/, "fa-briefcase"],
        [/micro enterprises?/, "fa-shopping-bag"],
        [/bdsp/, "fa-briefcase"],
        [/fsp/, "fa-bank"],
        [/fo\/msme|msme/, "fa-industry"],
        [/\bfo\b/, "fa-sitemap"],
        [/farmer|shf/, "fa-leaf"],
        [/participants?|members?/, "fa-users"],
        [/\bfemale\b/, "fa-female"],
        [/\bmale\b/, "fa-male"],
        [/\bpwd\b/, "fa-wheelchair"],
        [/\byouth\b/, "fa-child"],
        [/\bip\b/, "fa-globe"],
        [/\bsc\b/, "fa-user"],
        [/\bdips?\b/, "fa-list-alt"],
        [/entries/, "fa-list-alt"]
      ];
      iconRules.some(function (rule) {
        if (!rule[0].test(label)) return false;
        iconClass = rule[1];
        return true;
      });

      var icon = document.createElement("span");
      icon.className = "dcf-kpi-icon";
      icon.setAttribute("aria-hidden", "true");
      icon.innerHTML = '<i class="fa ' + iconClass + '"></i>';
      tile.insertBefore(icon, tile.firstChild);
    });

    var tileGroups = {
      "1": [
        { start: 0, label: "DIP and Household Overview", primary: true },
        { start: 3, label: "Enterprise Participation" }
      ],
      "2": [
        { start: 0, label: "Core Engagement Metrics", primary: true },
        { start: 4, label: "Participant Profile" },
        { start: 8, label: "Partnership Agreements" }
      ],
      "4": [
        { start: 0, label: "Training Overview", primary: true },
        { start: 3, label: "Participant Profile" }
      ],
      "6": [
        { start: 0, label: "Activity Overview", primary: true },
        { start: 2, label: "Participant Profile" },
        { start: 8, label: "Product and System Outputs" }
      ],
      "7": [
        { start: 0, label: "Assistance Coverage", primary: true },
        { start: 4, label: "Market Linkages and Sales" }
      ]
    };
    var groupConfig = tileGroups[formNumber];
    var topTiles = contentRoot.querySelector(".top_tiles");
    var firstKpiTile = contentRoot.querySelector(".tile-stats");
    var kpiContainer = topTiles || (firstKpiTile && firstKpiTile.closest(".row"));
    if (kpiContainer) kpiContainer.classList.add("dcf-kpi-container");
    if (groupConfig && kpiContainer) {
      var tileColumns = Array.prototype.slice.call(kpiContainer.children).filter(function (child) {
        return child.querySelector && child.querySelector(".tile-stats");
      });
      groupConfig.forEach(function (group, groupIndex) {
        var targetColumn = tileColumns[group.start];
        if (!targetColumn) return;
        var label = document.createElement("div");
        label.className = "dcf-kpi-group-label";
        label.textContent = group.label;
        kpiContainer.insertBefore(label, targetColumn);
        if (group.primary) {
          var nextStart = groupConfig[groupIndex + 1] ? groupConfig[groupIndex + 1].start : tileColumns.length;
          tileColumns.slice(group.start, nextStart).forEach(function (column) {
            column.classList.add("dcf-primary-kpi");
          });
        }
      });
    }

    var regionFilter = document.getElementById("regionFilter");
    var filterRow = null;
    if (regionFilter) {
      filterRow = regionFilter.closest(".row");
      if (filterRow) filterRow.classList.add("dashboard-toolbar");
    }

    var firstTile = contentRoot.querySelector(".tile-stats");
    var firstPanel = contentRoot.querySelector(".x_panel");
    var firstDashboardRow = filterRow ||
      (firstTile && firstTile.closest(".row")) ||
      (firstPanel && (firstPanel.closest(".row") || firstPanel.parentElement));
    if (firstDashboardRow && firstDashboardRow.parentNode) {
      firstDashboardRow.parentNode.classList.add("dcf-dashboard-shell");
      firstDashboardRow.parentNode.insertBefore(hero, firstDashboardRow);
    }

    if (formNumber === "2" && regionFilter) {
      var actionContainer = hero.querySelector(".dcf-dashboard-actions");
      var importAction = hero.querySelector('[data-dashboard-action="import"]');
      var existingFilterLabel = filterRow ? filterRow.querySelector('label[for="regionFilter"]') : null;
      var filterControl = document.createElement("div");
      filterControl.className = "dcf-hero-filter";

      var filterLabel = document.createElement("label");
      filterLabel.setAttribute("for", "regionFilter");
      filterLabel.innerHTML = '<i class="fa fa-filter" aria-hidden="true"></i> Filter records by region';
      filterControl.appendChild(filterLabel);
      filterControl.appendChild(regionFilter);

      if (actionContainer) actionContainer.insertBefore(filterControl, importAction);
      if (existingFilterLabel) existingFilterLabel.remove();
      if (filterRow) filterRow.remove();
    }

    Array.prototype.forEach.call(contentRoot.querySelectorAll(".panel_toolbox li"), function (tool) {
      if (tool.querySelector(".dropdown-toggle, .close-link")) tool.classList.add("dcf-unused-tool");
    });

    function insertSection(label, panel, beforeColumn) {
      if (!panel) return;
      var column = panel.closest('[class*="col-"]');
      var target = beforeColumn && column ? column : panel;
      if (!target.parentNode) return;
      var heading = document.createElement("div");
      heading.className = "dcf-section-heading";
      if (target === column) heading.classList.add("dcf-section-heading-row");
      heading.textContent = label;
      target.parentNode.insertBefore(heading, target);
    }

    if (firstTile) {
      var overviewRow = firstTile.closest(".row");
      if (overviewRow && overviewRow.parentNode) {
        var overviewHeading = document.createElement("div");
        overviewHeading.className = "dcf-section-heading";
        overviewHeading.textContent = "Overview";
        overviewRow.parentNode.insertBefore(overviewHeading, overviewRow);
      }
    }

    var panels = Array.prototype.slice.call(contentRoot.querySelectorAll(".x_panel"));
    var firstAnalyticsPanel = panels.find(function (panel) {
      var heading = panel.querySelector(".x_title h2");
      var title = heading ? heading.textContent : "";
      return !/data|spreadsheet management/i.test(title);
    });
    if (firstAnalyticsPanel) {
      insertSection("Insights and Performance", firstAnalyticsPanel, true);
    }

    var dataPanel = panels.find(function (panel) {
      var heading = panel.querySelector(".x_title h2");
      return heading && /^data\b/i.test(heading.textContent.trim());
    });
    var recordsTable = Array.prototype.find.call(contentRoot.querySelectorAll("table"), function (table) {
      return Array.prototype.some.call(table.querySelectorAll("thead th"), function (header) {
        return /^action$/i.test(header.textContent.trim());
      });
    });
    var recordsPanel = recordsTable ? recordsTable.closest(".x_panel") : dataPanel;
    if (recordsPanel) dataPanel = recordsPanel;
    if (dataPanel) insertSection("Detailed Records", dataPanel, false);

    var managementPanel = panels.find(function (panel) {
      var heading = panel.querySelector(".x_title h2");
      return heading && /spreadsheet management/i.test(heading.textContent);
    });
    if (managementPanel) {
      var managementParent = managementPanel.parentNode;
      var managementColumn = managementPanel.closest('[class*="col-"]');
      if (managementColumn) managementColumn.classList.add("dcf-management-column");

      var managementSection = document.createElement("section");
      managementSection.className = "dcf-management-section";
      managementParent.insertBefore(managementSection, managementPanel);

      var managementHeading = document.createElement("div");
      managementHeading.className = "dcf-section-heading";
      managementHeading.textContent = "Data Management";
      managementSection.appendChild(managementHeading);
      managementSection.appendChild(managementPanel);
    }

    function scrollToDashboardElement(element) {
      if (!element) return;
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    Array.prototype.forEach.call(hero.querySelectorAll("[data-dashboard-action]"), function (button) {
      button.addEventListener("click", function () {
        var action = button.getAttribute("data-dashboard-action");
        if (action === "records") {
          scrollToDashboardElement(recordsPanel || recordsTable || dataPanel);
          return;
        }
        if (action === "import") {
          scrollToDashboardElement(managementSection || managementPanel);
          return;
        }
        if (action === "export") {
          if (!managementPanel) return;
          var exportButton = Array.prototype.find.call(
            managementPanel.querySelectorAll("button, .btn"),
            function (candidate) {
              return /export/i.test(candidate.textContent || "");
            }
          );
          if (exportButton) exportButton.click();
          else scrollToDashboardElement(managementSection || managementPanel);
        }
      });
    });
  });
})();
