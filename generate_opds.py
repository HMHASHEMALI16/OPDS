import os
import datetime
import html

folder_path = '.' 
xml_path = 'catalog.xml'

# ⚠️ নিচে 'YOUR_REPO_NAME' মুছে আপনার গিটহাব রিপোজিটরির সঠিক নাম বসান
# উদাহরণ: repo_name = "My-eBook-Library"
repo_name = "YOUR_REPO_NAME" 

# আইকনের সরাসরি গিটহাব র-লিংক তৈরি করা হলো
icon_url = f"https://raw.githubusercontent.com/HMHASHEMALI16/{repo_name}/main/Bookicon.png"

xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opds="http://opds-spec.org/2010/catalog">
  <id>urn:uuid:hmhashemali-opds-library</id>
  <title>My eBook Collection</title>
  <updated>{datetime.datetime.utcnow().isoformat()}Z</updated>
  <author><name>HM Hashem Ali</name></author>
"""

books = []

# মেইন ফোল্ডারের সব epub ফাইল খুঁজবে
for filename in os.listdir(folder_path):
    if filename.endswith('.epub'):
        raw_name = os.path.splitext(filename)[0]
        
        # নাম ও লেখক আলাদা করা
        if "_-_" in raw_name:
            parts = raw_name.split("_-_")
            book_title = parts[0].replace("_", " ").strip()
            author_name = parts[-1].replace("_", " ").strip()
        else:
            book_title = raw_name.replace("_", " ").strip()
            author_name = "অজানা লেখক"

        books.append({
            'title': book_title,
            'author': author_name,
            'filename': filename
        })

# বাংলা বর্ণমালা অনুযায়ী সাজানো
books.sort(key=lambda x: x['title'])

# XML এন্ট্রি তৈরি
for book in books:
    safe_title = html.escape(book['title'])
    safe_author = html.escape(book['author'])
    safe_filename = html.escape(book['filename'])
    safe_icon = html.escape(icon_url)

    xml_content += f"""
  <entry>
    <title>{safe_title}</title>
    <author>
      <name>{safe_author}</name>
    </author>
    <id>urn:uuid:{safe_filename}</id>
    <updated>{datetime.datetime.utcnow().isoformat()}Z</updated>
    <link rel="http://opds-spec.org/image/thumbnail" href="{safe_icon}" type="image/png" />
    <link rel="http://opds-spec.org/image" href="{safe_icon}" type="image/png" />
    <link rel="http://opds-spec.org/acquisition" href="{safe_filename}" type="application/epub+zip" />
  </entry>"""

xml_content += "\n</feed>"

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)
    
