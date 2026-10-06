"""Self-contained listings page, CSV, and JSON."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from camp_listings.schema import COLUMNS


def satellite_maps_url(lat: str, lon: str) -> str:
    try:
        lat_n = float(str(lat).strip())
        lon_n = float(str(lon).strip())
    except (TypeError, ValueError):
        return ""
    if not (-90.0 <= lat_n <= 90.0 and -180.0 <= lon_n <= 180.0):
        return ""

    def _coord(number: float) -> str:
        return f"{number:.6f}".rstrip("0").rstrip(".")

    return (
        "https://www.google.com/maps/@?api=1&map_action=map"
        f"&center={_coord(lat_n)},{_coord(lon_n)}&zoom=17&basemap=satellite"
    )


def _maps(row: dict) -> list[dict]:
    raw = row.get("maps")
    if isinstance(raw, list):
        return raw
    urls = [part for part in (row.get("map_urls") or "").split("|") if part]
    if not urls:
        return []
    kind = row.get("map_type") or "property_map"
    is_pdf = str(row.get("map_is_pdf") or "").lower() == "true"
    source = row.get("map_source") or ""
    return [{"url": url, "map_type": kind, "is_pdf": is_pdf or url.lower().split("?")[0].endswith(".pdf"), "source": source} for url in urls]


def write_outputs(path_dir: Path, rows: list[dict], log_lines: list[str]) -> None:
    path_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(path_dir / "listings.csv", rows)
    payload = []
    for row in rows:
        item = {column: row.get(column, "") for column in COLUMNS}
        item["maps"] = _maps(row)
        item["satellite_url"] = satellite_maps_url(row.get("lat", ""), row.get("lon", ""))
        payload.append(item)
    (path_dir / "listings.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (path_dir / "index.html").write_text(render_html(payload), encoding="utf-8")
    (path_dir / "fetch_log.md").write_text("# Fetch log\n\n" + "\n".join(f"- {line}" for line in log_lines) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(COLUMNS), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in COLUMNS})


def render_html(rows: list[dict]) -> str:
    data = json.dumps(rows).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Camps, campuses, and 501(c)(7) clubs for sale</title>
  <style>
    body {{ font-family: Georgia, serif; margin: 1.5rem auto; max-width: 1100px; padding: 0 1rem; color: #222; }}
    h1 {{ font-size: 1.6rem; }}
    .note {{ background: #fff6e5; border: 1px solid #e0c48a; padding: 0.7rem 1rem; }}
    .tabs button, #state {{ font: inherit; margin: 0.2rem 0.3rem 0.2rem 0; padding: 0.3rem 0.7rem; }}
    .tabs button.active {{ background: #1f4b3a; color: #fff; border-color: #1f4b3a; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }}
    article {{ border: 1px solid #ddd; padding: 0.8rem 1rem; }}
    article img {{ width: 100%; height: auto; display: block; }}
    .credit, .meta {{ color: #555; font-size: 0.9rem; }}
    .pdf {{ display: inline-block; background: #7a1f1f; color: #fff; font-size: 0.72rem; padding: 0 0.3rem; margin-left: 0.25rem; }}
    .empty {{ color: #666; }}
  </style>
</head>
<body>
  <h1>Properties for sale with housing</h1>
  <p class="note">Colleges and campuses, summer camps and retreats, and 501(c)(7)-type clubs that are listed for sale and show dorms, cabins, bunkhouses, or a lodge with beds. Prices and counts are copied from the listing page. A blank price means the page did not state one. An IRS EIN appears only when the name and city match the EO BMF subsection 07 file.</p>
  <p id="counts"></p>
  <div class="tabs">
    <button type="button" data-cat="all" class="active">All</button>
    <button type="button" data-cat="college">Colleges</button>
    <button type="button" data-cat="camp">Camps</button>
    <button type="button" data-cat="501c7">501(c)(7)</button>
    <label>State <select id="state"><option value="">All states</option></select></label>
  </div>
  <div id="grid" class="grid"></div>
  <script id="listing-data" type="application/json">{data}</script>
  <script>
    const rows = JSON.parse(document.getElementById("listing-data").textContent);
    const state = document.getElementById("state");
    const states = [...new Set(rows.map(r => r.state).filter(Boolean))].sort();
    for (const code of states) {{
      const opt = document.createElement("option");
      opt.value = code; opt.textContent = code; state.appendChild(opt);
    }}
    let category = "all";
    function esc(value) {{
      return String(value ?? "").replace(/[&<>"']/g, ch => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[ch]));
    }}
    function money(row) {{
      return row.price_text || (row.price_amount ? "$" + Number(row.price_amount).toLocaleString("en-US") : "Price not stated");
    }}
    function maps(row) {{
      const items = row.maps || [];
      if (!items.length) return "<p class='meta'>Maps: none found on the public pages checked</p>";
      const links = items.map(item => {{
        const badge = item.is_pdf ? "<span class='pdf'>PDF</span>" : "";
        const label = (item.map_type || "map").replaceAll("_", " ");
        return `<a href="${{esc(item.url)}}">${{esc(label)}}${{badge}}</a>`;
      }});
      return "<p class='maps'>Maps: " + links.join(" · ") + "</p>";
    }}
    function card(row) {{
      const photo = row.image_url
        ? `<img src="${{esc(row.image_url)}}" alt="Photo of ${{esc(row.name)}}" loading="lazy"><p class="credit">${{esc(row.image_credit || row.source_name || "Listing photo")}}</p>`
        : "";
      const sat = row.satellite_url ? `<a href="${{esc(row.satellite_url)}}">Satellite view</a>` : "";
      const ein = row.eo_ein ? `<p class="meta">IRS 501(c)(7) EIN ${{esc(row.eo_ein)}} (${{esc(row.eo_name || "")}})</p>` : "";
      return `<article>
        ${{photo}}
        <h2>${{esc(row.name)}}</h2>
        <p class="meta">${{esc(row.category)}} · ${{esc(row.city)}} ${{esc(row.state)}} · ${{esc(row.status)}}</p>
        <p><strong>${{esc(money(row))}}</strong>
          · ${{row.acreage ? esc(row.acreage) + " acres" : "acreage not stated"}}
          · ${{row.beds ? esc(row.beds) + " beds" : "beds not stated"}}
          ${{row.cabin_count ? " · " + esc(row.cabin_count) + " cabins" : ""}}</p>
        <p>${{esc(row.housing_evidence)}}</p>
        ${{ein}}
        ${{maps(row)}}
        <p><a href="${{esc(row.source_url)}}">Listing</a>
          ${{sat ? " · " + sat : ""}}</p>
        <p class="meta">Checked ${{esc(row.checked_at)}} · ${{esc(row.source_name)}}</p>
      </article>`;
    }}
    function draw() {{
      const picked = rows.filter(row => (category === "all" || row.category === category) && (!state.value || row.state === state.value));
      const counts = {{college: 0, camp: 0, "501c7": 0}};
      for (const row of rows) if (counts[row.category] !== undefined) counts[row.category] += 1;
      document.getElementById("counts").textContent =
        `${{rows.length}} listings · ${{counts.college}} colleges · ${{counts.camp}} camps · ${{counts["501c7"]}} 501(c)(7) · showing ${{picked.length}}`;
      document.getElementById("grid").innerHTML = picked.length ? picked.map(card).join("") : "<p class='empty'>No listings in this filter.</p>";
    }}
    document.querySelectorAll(".tabs button").forEach(button => {{
      button.addEventListener("click", () => {{
        category = button.dataset.cat;
        document.querySelectorAll(".tabs button").forEach(el => el.classList.toggle("active", el === button));
        draw();
      }});
    }});
    state.addEventListener("change", draw);
    draw();
  </script>
</body>
</html>
"""
