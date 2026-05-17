"""
OPDS Catalog Auto-Generator
============================
books/ ফোল্ডারের সব epub ও pdf স্ক্যান করে,
ফাইলের ভেতর থেকে নাম-লেখক বের করে,
index.xml তৈরি করে।

কোনো metadata না থাকলে filename থেকে নাম নেয়।
"""

import os
import uuid
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ── কনফিগ ──────────────────────────────────────────────
BASE_URL   = "https://hmhashemali16.github.io/OPDS"
BOOKS_DIR  = "books"
OUT_FILE   = "index.xml"
LIB_TITLE  = "HM Hashem Ali – Digital Library"
LIB_AUTHOR = "HM Hashem Ali"
# ────────────────────────────────────────────────────────

MIME = {".epub": "application/epub+zip", ".pdf": "application/pdf"}


# ══════════════════════════════════════════════
#  EPUB metadata (zipfile + xml, no extra deps)
# ══════════════════════════════════════════════
def _epub_meta(path):
    try:
        with zipfile.ZipFile(path, "r") as z:
            container = ET.fromstring(z.read("META-INF/container.xml"))
            ns_c = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
            rf = container.find(".//c:rootfile", ns_c)
            if rf is None:
                return None, None
            opf = ET.fromstring(z.read(rf.get("full-path")))
            ns  = {"dc": "http://purl.org/dc/elements/1.1/"}
            t = opf.find(".//dc:title",   ns)
            a = opf.find(".//dc:creator", ns)
            title  = (t.text or "").strip() or None
            author = (a.text or "").strip() or None
            return title, author
    except Exception as e:
        print(f"    [epub-meta error] {e}")
        return None, None


# ══════════════════════════════════════════════
#  PDF metadata (PyMuPDF – installed by Actions)
# ══════════════════════════════════════════════
def _pdf_meta(path):
    try:
        import fitz                    # PyMuPDF
        doc  = fitz.open(path)
        meta = doc.metadata
        doc.close()
        title  = (meta.get("title",  "") or "").strip() or None
        author = (meta.get("author", "") or "").strip() or None
        return title, author
    except Exception as e:
        print(f"    [pdf-meta error] {e}")
        return None, None


# ══════════════════════════════════════════════
#  Filename → readable title (fallback)
# ══════════════════════════════════════════════
def _title_from_name(filename):
    stem = os.path.splitext(filename)[0]
    return stem.replace("_", " ").replace("-", " ").strip()


# ══════════════════════════════════════════════
#  XML escaping
# ══════════════════════════════════════════════
def esc(s):
    return (s or "").\
        replace("&", "&amp;").\
        replace("<", "&lt;").\
        replace(">", "&gt;").\
        replace('"', "&quot;")


# ══════════════════════════════════════════════
#  One <entry> block
# ══════════════════════════════════════════════
def make_entry(filename):
    ext  = os.path.splitext(filename)[1].lower()
    mime = MIME.get(ext)
    if not mime:
        return ""

    filepath = os.path.join(BOOKS_DIR, filename)
    print(f"  📖 {filename}")

    if ext == ".epub":
        title, author = _epub_meta(filepath)
    else:
        title, author = _pdf_meta(filepath)

    if not title:
        title = _title_from_name(filename)
        print(f"      → metadata নেই, filename ব্যবহার করা হচ্ছে: {title}")
    else:
        print(f"      → title: {title}  |  author: {author or 'অজানা'}")

    uid  = str(uuid.uuid5(uuid.NAMESPACE_URL, filename))
    href = f"{BASE_URL}/{BOOKS_DIR}/{filename}"
    now  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    auth_tag = f"\n    <author><name>{esc(author)}</name></author>" if author else ""

    return f"""
  <entry>
    <title>{esc(title)}</title>
    <id>urn:uuid:{uid}</id>
    <updated>{now}</updated>{auth_tag}
    <link rel="http://opds-spec.org/acquisition"
          href="{esc(href)}"
          type="{mime}"/>
  </entry>"""


# ══════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════
def generate():
    print(f"\n🔍 Scanning '{BOOKS_DIR}/' ...\n")
    entries = ""
    count   = 0

    if os.path.isdir(BOOKS_DIR):
        for fname in sorted(os.listdir(BOOKS_DIR)):
            if os.path.splitext(fname)[1].lower() in MIME:
                entries += make_entry(fname)
                count += 1
    else:
        print(f"⚠️  '{BOOKS_DIR}' ফোল্ডার পাওয়া যায়নি!")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:dc="http://purl.org/dc/terms/"
      xmlns:opds="http://opds-spec.org/2010/catalog">

  <id>{BASE_URL}/index.xml</id>
  <title>{esc(LIB_TITLE)}</title>
  <updated>{now}</updated>
  <author>
    <name>{esc(LIB_AUTHOR)}</name>
  </author>

  <link rel="self"
        href="{BASE_URL}/index.xml"
        type="application/atom+xml;profile=opds-catalog;kind=acquisition"/>
  <link rel="start"
        href="{BASE_URL}/index.xml"
        type="application/atom+xml;profile=opds-catalog;kind=acquisition"/>
{entries}
</feed>
"""

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"\n✅  {OUT_FILE} তৈরি হয়েছে — মোট {count}টি বই।\n")


if __name__ == "__main__":
    generate()
