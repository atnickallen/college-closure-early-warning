"""Tests for the camps and 501(c)(7) listing folder."""

from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
sys.path.insert(0, str(ROOT / "src"))

from camp_listings.dedupe import dedupe
from camp_listings.eo_bmf import filter_bmf_text, is_subsection_07, match_club
from camp_listings.housing import housing_snippet
from camp_listings.http import Client, FetchResult
from camp_listings.maps import FIRECRAWL_MAP, FIRECRAWL_SEARCH, classify_map, find_maps
from camp_listings.pipeline import run
from camp_listings.report import render_html, satellite_maps_url
from camp_listings.schema import as_row
from camp_listings.sources import parse_news_rss, parse_summer_camp_hub


class _Response:
    def __init__(self, status, body, url="https://example.test/"):
        self.status = status
        self._body = body if isinstance(body, bytes) else body.encode()
        self._url = url

    def read(self):
        return self._body

    def geturl(self):
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_housing_snippet_requires_a_real_mention():
    assert housing_snippet("40 acres of pasture and a pond") == ""
    snippet = housing_snippet("The campus has six residence halls with 605 beds.")
    assert "residence halls" in snippet


def test_dedupe_keeps_the_curated_row():
    curated = as_row(
        {
            "name": "Camp Example",
            "state": "ME",
            "city": "Rome",
            "price_amount": "10",
            "source_url": "https://example.test/camp",
            "housing_evidence": "four cabins",
            "origin": "curated",
            "notes": "kept",
        }
    )
    fetched = as_row(
        {
            "name": "Camp Example",
            "state": "ME",
            "city": "Rome",
            "price_amount": "10",
            "source_url": "https://example.test/camp",
            "housing_evidence": "four cabins",
            "origin": "fetched",
            "beds": "40",
        }
    )
    rows = dedupe([fetched, curated])
    assert len(rows) == 1
    assert rows[0]["origin"] == "curated"
    assert rows[0]["beds"] == "40"
    assert rows[0]["notes"] == "kept"


def test_blocked_fetch_does_not_raise():
    def opener(request, timeout=20, context=None):
        raise OSError("403")

    error = OSError("nope")
    error.code = 403

    def opener_http(request, timeout=20, context=None):
        raise error

    client = Client(opener=opener_http)
    client._robots["https://blocked.test"] = None
    result = client.fetch("https://blocked.test/search")
    assert result.blocked
    assert "403" in result.reason


def test_subsection_07_filter_and_name_match():
    assert is_subsection_07("07")
    assert is_subsection_07("7")
    assert not is_subsection_07("17")
    text = (
        "EIN,NAME,ICO,STREET,CITY,STATE,ZIP,GROUP,SUBSECTION,AFFILIATION\n"
        "010022320,AUGUSTA COUNTRY CLUB,,1 MAIN,MANCHESTER,ME,04351,,07,3\n"
        "999999999,SOME CHURCH,,1 MAIN,MANCHESTER,ME,04351,,03,3\n"
    )
    rows = filter_bmf_text(text)
    assert len(rows) == 1
    hit = match_club(rows, "Augusta Country Club", "Manchester", "ME")
    assert hit["ein"] == "010022320"
    assert match_club(rows, "Augusta Country Club", "Portland", "ME") is None


def test_map_classifier_marks_pdfs_and_skips_xml_sitemaps():
    kind, is_pdf = classify_map("https://school.edu/maps/campus-map.pdf", "Campus map")
    assert kind == "campus_map"
    assert is_pdf
    assert classify_map("https://school.edu/wp-sitemap.xml", "map") is None
    assert classify_map("https://www.google.com/maps/place/x", "map") is None


def test_firecrawl_is_used_only_when_a_key_is_set_and_the_key_is_not_logged():
    secret = "super-secret-firecrawl-key"
    calls = []

    def opener(request, timeout=20, context=None):
        calls.append(request)
        body = json.dumps({"success": True, "data": {"web": [{"url": "https://camp.example/campus-map.pdf"}]}, "links": ["https://camp.example/plat.pdf"]})
        return _Response(200, body, request.full_url)

    client = Client(opener=opener)
    found = find_maps("Example Camp", client=client, listing_url="", api_key=secret, search_queries=['"Example Camp" campus map filetype:pdf'])
    assert calls
    assert calls[0].full_url == FIRECRAWL_SEARCH
    assert secret not in json.dumps(found.notes)
    assert any(hit.is_pdf and hit.source == "firecrawl" for hit in found.hits)
    map_calls = find_maps(
        "Example Camp",
        client=client,
        listing_url="https://camp.example/",
        org_url="https://camp.example/",
        api_key=secret,
        search_queries=[],
    )
    assert any(call.full_url == FIRECRAWL_MAP for call in calls)
    assert secret not in json.dumps(map_calls.notes)


def test_fallback_reads_a_map_link_without_a_key():
    html = '<html><a href="https://camp.example/files/site-map.pdf">Site map</a><meta property="og:image" content="https://camp.example/photo.jpg"></html>'

    def opener(request, timeout=20, context=None):
        return _Response(200, html, "https://camp.example/listing")

    client = Client(opener=opener)
    client._robots["https://lite.duckduckgo.com"] = None
    client._robots["https://camp.example"] = None
    found = find_maps("Quiet Camp", client=client, listing_url="https://camp.example/listing", api_key="", search_queries=[])
    assert found.image_url.endswith("photo.jpg")
    assert found.hits[0].map_type == "site_map"
    assert found.hits[0].is_pdf
    assert "super-secret" not in json.dumps(found.notes)


def test_news_rss_is_not_turned_into_a_listing_body():
    xml = """<?xml version="1.0"?><rss><channel><item><title>Campus for sale</title><link>https://news.google.com/articles/x</link><description>Long copyrighted description with dorms</description></item></channel></rss>"""
    leads = parse_news_rss(xml)
    assert leads == [{"title": "Campus for sale", "link": "https://news.google.com/articles/x"}]
    assert "copyrighted" not in json.dumps(leads)


def test_summer_hub_parser_keeps_housing_rows():
    html = "<p>Address: 1 Main, Rome, ME 04963 Current Price: $10</p>"
    # The price split looks backward, so the description has to precede the price.
    html = "<div>Rome camp with four cabins on 12 acres. Address: 1 Main, Rome, ME 04963 Current Price: $10</div>"
    rows = parse_summer_camp_hub(html, "https://summercamphub.com/summer-camps-for-sale/", "2026-10-06")
    assert len(rows) == 1
    assert rows[0]["state"] == "ME"
    assert "cabins" in rows[0]["housing_evidence"]


def test_page_escapes_satellite_links_and_badges_pdfs():
    url = satellite_maps_url("42.3", "-71.1")
    assert "center=42.3,-71.1" in url
    assert satellite_maps_url("", "1") == ""
    page = render_html(
        [
            {
                "name": "Sample Camp",
                "category": "camp",
                "state": "ME",
                "city": "Rome",
                "status": "for sale",
                "price_text": "$10",
                "price_amount": "10",
                "acreage": "4",
                "beds": "20",
                "cabin_count": "4",
                "housing_evidence": "four cabins",
                "source_name": "Example",
                "source_url": "https://example.test/camp",
                "image_url": "https://example.test/a.jpg",
                "image_credit": "Example",
                "checked_at": "2026-10-06",
                "satellite_url": url,
                "eo_ein": "",
                "maps": [{"url": "https://example.test/map.pdf", "map_type": "site_map", "is_pdf": True, "source": "page"}],
            }
        ]
    )
    assert "basemap=satellite" in page
    assert "center=42.3,-71.1" in page
    assert "class='pdf'" in page
    assert ">PDF</span>" in page


def test_skip_network_publishes_only_curated_rows_with_housing(tmp_path, monkeypatch):
    feature = tmp_path / "feature"
    (feature / "src" / "camp_listings").mkdir(parents=True)
    (feature / "data").mkdir()
    (feature / "config.yaml").write_text("checked_at: '2026-10-06'\ncurated_csv: data/curated_listings.csv\nsources: []\n", encoding="utf-8")
    # Point feature_root at this temp tree by giving it the package marker.
    (feature / "src" / "camp_listings" / "__init__.py").write_text("", encoding="utf-8")
    curated = feature / "data" / "curated_listings.csv"
    curated.write_text(
        "listing_id,name,category,status,city,state,address,price_text,price_amount,acreage,beds,cabin_count,housing_evidence,source_name,source_url,image_url,image_credit,lat,lon,listing_date,checked_at,notes,eo_ein,eo_name,map_urls,map_type,map_is_pdf,map_source,origin\n"
        "one,Has Cabins,camp,for sale,Rome,ME,,\"$1\",1,2,,2,two cabins,Src,https://example.test/one,,,,,,,,,2026-10-06,,,,,curated\n"
        "two,No Housing,camp,for sale,Rome,ME,,,,,,,,,,Src,https://example.test/two,,,,,,,,,2026-10-06,,,,,curated\n",
        encoding="utf-8",
    )
    rows = run(feature, skip_network=True, geocode=False)
    assert [row["listing_id"] for row in rows] == ["one"]
    assert (feature / "outputs" / "index.html").exists()


def test_weekly_workflow_quotes_the_folder_and_does_not_print_the_key():
    text = (REPO / ".github" / "workflows" / "camps-501c7-refresh.yml").read_text(encoding="utf-8")
    assert "contents: write" in text
    assert 'branch="camps-501c7-refresh"' in text
    assert "GITHUB_STEP_SUMMARY" in text
    assert "compare/main...camps-501c7-refresh" in text
    assert "elif gh pr create" in text
    assert "Pull request was not created" in text
    assert "git push --force-with-lease origin" in text
    assert text.strip().endswith("exit 0")
    assert text.count("FIRECRAWL_API_KEY: ${{ secrets.FIRECRAWL_API_KEY }}") == 2
    assert "workflow_dispatch" in text
    assert 'python3 "camps and 501c7\'s/scripts/run_listings.py"' in text
    assert 'python3 "camps and 501c7\'s/scripts/apply_campus_maps.py"' in text
    assert "camps and 501c7's/outputs/listings.csv" in text
    assert "data/campus/campus_land.csv" in text
    assert "outputs/top50_report.html" in text
    assert "echo \"$FIRECRAWL_API_KEY\"" not in text
    assert "printenv" not in text
    assert "set -x" not in text


def test_firecrawl_key_searches_schools_that_already_have_a_map(monkeypatch):
    import importlib.util

    script = ROOT / "scripts" / "apply_campus_maps.py"
    spec = importlib.util.spec_from_file_location("apply_campus_maps", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    stored = "https://lakeland.edu/PDFs/virtualtour/Lakeland-campus-map.pdf"
    assert module._keep_existing(stored, "Lakeland University", use_firecrawl=False)
    assert module._keep_existing(stored, "Lakeland University", use_firecrawl=True) is False

    calls = []

    def fake_find_maps(name, **kwargs):
        calls.append(kwargs["search_queries"])

        class Result:
            hits = []

        return Result()

    monkeypatch.setattr(module, "find_maps", fake_find_maps)
    monkeypatch.setattr(module, "_maps_linked_from", lambda *args, **kwargs: "")
    monkeypatch.setattr(module, "_probe", lambda *args, **kwargs: "")
    monkeypatch.setattr(module, "_org_url", lambda row: "https://lakeland.edu/")
    monkeypatch.setattr(module, "_wiki_site", lambda *args, **kwargs: "")
    monkeypatch.setattr(module, "_org_from_search", lambda *args, **kwargs: "")
    row = {"source_url": "https://lakeland.edu/", "image_credit_url": "", "image_url": stored}
    url = module._find_campus_map("Lakeland University", row, client=None, use_firecrawl=True)
    assert calls and any("filetype:pdf" in query for query in calls[0])
    assert '"Lakeland University" site map pdf' in calls[0]
    assert url == stored
