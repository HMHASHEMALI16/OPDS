import os
import datetime

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
        title = os.path.splitext(filename)[0]
        xml_content += f"""
  <entry>
    <title>{title}</title>
    <id>urn:uuid:{filename}</id>
    <updated>{datetime.datetime.utcnow().isoformat()}Z</updated>
    <link rel="http://opds-spec.org/acquisition" href="{filename}" type="application/epub+zip" />
  </entry>"""

xml_content += "\n</feed>"

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)
    
