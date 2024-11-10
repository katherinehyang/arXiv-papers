# Parses through XML data

import xml.etree.ElementTree as ET

def parse_arxiv_response(response_data):
    tree = ET.ElementTree(ET.fromstring(response_data))
    root = tree.getroot()
    entries = []
    
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        abstract = entry.find("{http://www.w3.org/2005/Atom}summary").text
        citation_count = entry.find("{http://arxiv.org/schemas/atom}arxiv:comment").text if entry.find("{http://arxiv.org/schemas/atom}arxiv:comment") is not None else "N/A"
        
        entries.append({
            'title': title,
            'authors': authors,
            'published': published,
            'abstract': abstract,
            'citation_count': citation_count
        })
    
    return entries