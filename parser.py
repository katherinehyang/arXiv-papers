# Parses through XML data

import xml.etree.ElementTree as ET

def parse_arxiv_response(response_data):
    tree = ET.ElementTree(ET.fromstring(response_data))
    root = tree.getroot()

    # total_results = int(root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
    # print(f"Total results found: {total_results}")

    entries = []
    
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text if entry.find("{http://www.w3.org/2005/Atom}title") is not None else "Untitled"
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        abstract = entry.find("{http://www.w3.org/2005/Atom}summary").text
        
        entries.append({
            'title': title,
            'authors': authors,
            'published': published,
            'abstract': abstract
        })
    
    return entries