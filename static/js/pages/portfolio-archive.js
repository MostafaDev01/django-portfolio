(() => {
"use strict";

document.addEventListener("DOMContentLoaded", () => {
const filters = document.querySelectorAll(".archive-filters [data-filter]");
const items = document.querySelectorAll(".portfolio-container .portfolio-item");
const count = document.querySelector(".visible-count");
const emptyMessage = document.querySelector(".filter-empty");

```
if (!filters.length || !items.length) return;

function applyFilter(selectedFilter) {
  let visibleCount = 0;

  items.forEach((item) => {
    const matches =
      selectedFilter === "*" ||
      item.classList.contains(selectedFilter.slice(1));

    item.hidden = !matches;

    if (matches) visibleCount++;
  });

  if (count) count.textContent = visibleCount;
  if (emptyMessage) emptyMessage.hidden = visibleCount !== 0;
}

filters.forEach((filter) => {
  const activate = () => {
    filters.forEach((item) => {
      const active = item === filter;
      item.classList.toggle("filter-active", active);
      item.setAttribute("aria-pressed", String(active));
    });

    applyFilter(filter.dataset.filter || "*");
  };

  filter.addEventListener("click", activate);

  filter.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      activate();
    }
  });
});

applyFilter("*");
```

});
})();
