import os
import datetime
import html

folder_path = '.' 
xml_path = 'catalog.xml'

xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opds="http://opds-spec.org/2010/catalog">
  <id>urn:uuid:hmhashemali-opds-library</id>
  <title>My eBook Collection</title>
  <updated>{datetime.datetime.utcnow().isoformat()}Z</updated>
  <author><name>HM Hashem Ali</name></author>
"""

# মেইন ফোল্ডারের সব epub ফাইল খুঁজবে
for filename in os.listdir(folder_path):
    if filename.endswith('.epub'):
        raw_name = os.path.splitext(filename)[0]
        
        # ফাইলের নাম থেকে _-_ এর সাহায্যে ভাগ করা
        if "_-_" in raw_name:
            parts = raw_name.split("_-_")
            
            # প্রথম অংশটি বইয়ের নাম, আন্ডারস্কোর সরিয়ে স্পেস বসানো হলো
            book_title = parts[0].replace("_", " ").strip()
            
            # শেষের অংশটি লেখকের নাম (একাধিক _-_ থাকলেও যেন শেষেরটাই নেয়)
            author_name = parts[-1].replace("_", " ").strip()
        else:
            # যদি ফাইলের নামে _-_ না থাকে
            book_title = raw_name.replace("_", " ").strip()
            author_name = "অজানা লেখক"

        # XML-এ কোনো সমস্যা এড়াতে html.escape ব্যবহার করা হলো
        safe_title = html.escape(book_title)
        safe_author = html.escape(author_name)
        safe_filename = html.escape(filename)

        xml_content += f"""
  <entry>
    <title>{safe_title}</title>
    <author>
      <name>{safe_author}</name>
    </author>
    <id>urn:uuid:{safe_filename}</id>
    <updated>{datetime.datetime.utcnow().isoformat()}Z</updated>
    <link rel="http://opds-spec.org/acquisition" href="{safe_filename}" type="application/epub+zip" />
  </entry>"""

xml_content += "\n</feed>"

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)
    
