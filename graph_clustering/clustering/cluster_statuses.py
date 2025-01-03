import requests

def cluster_statuses(statuses, url):

    """
    Generate labels by clustering user posts using Carrot2 REST API 
    https://github.com/carrot2/carrot2

    Args:
        statuses (str): The list to split.
        url (str): Number of parts to split into.

    Returns:
        dict: A dictionary where keys are cluster labels and values are dictionaries with counts (no. of elements) and elements.
    """

    postElements = []
    for posts in statuses:
        if posts.get('language', None) == 'en' or (posts.get('reblog', {}) and posts.get('reblog', {}).get('language', None) == 'en'):
            postElements.append(posts)

    # Filter Content 
    titleTexts = [item['card']['title'] for item in postElements]
    descriptionTexts = [item['card']['description'] for item in postElements]

    # Generate the payload
    payload = {
    "algorithm": "Lingo",
    "language": "English",
    "documents": [{"title": title, "body": text} for title, text in zip(titleTexts, descriptionTexts)]
    }

    # Send the POST request to Carrot2 instance
    response = requests.post(url, json=payload)

    # Check the response
    clusterLabels = {}
    if response.status_code == 200:
        # Group Labels and Statuses based on results obtained
        carrotResponse = response.json()
        for cluster in carrotResponse['clusters']:
            for label in cluster['labels']:
                clusterLabels[label] = {
                    "count": len(cluster['documents']),
                    "elements": [postElements[doc_id] for doc_id in cluster['documents']]
                }

        # Print the formatted output (For Verification)
        # for cluster in carrotResponse['clusters']:
        #     for label in cluster['labels']:
        #         clusterLabels.append(f"Label: {label}")
        #         for doc_id in cluster['documents']:
        #             clusterLabels.append(f"Post: {descriptionTexts[doc_id]}")
        #         clusterLabels.append("")  
        # print("\n".join(clusterLabels))
    else:
        print("Error:", response.status_code, response.text)

    return clusterLabels