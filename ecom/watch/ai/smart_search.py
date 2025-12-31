import re

def extract_filters(query):
    query = query.lower()
    filters = {}

    categories = ["mens","womens","kids","accessories"]
    for c in categories:
        if c in query:
            filters["category"] = c.rstrip("s")

    section = ["shirt","shirts","pants","pant","gown","kurta","western suit","black suit","short puff sleeve"]   
    for s in section:
        if s in query:
            filters["section"] = s   

    colors = ["red","blue","pink","navy","black"] 
    for color in colors:
        if color in query:
            filters["color"] = color    

    price_match = re.search(r"under\s?(\d+)",query)
    if price_match:
        filters["price__lte"] = int(price_match.group(1))      

    return filters         