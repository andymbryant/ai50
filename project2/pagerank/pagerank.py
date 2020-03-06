import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """s
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize transition model dict
    trans_model = {}
    # Get all inks on page
    links = corpus[page]
    # Get number of links
    num_links = len(links)
    # If the page has no links, return an even prob distribution of all pages
    if num_links < 1:
        return {k:1/len(corpus) for k,v in corpus.items()}
    else:
        # Calculate base probability based on damping factor and amount of other pages
        # Round for consistency
        base_prob = round((1 - damping_factor) / len(corpus), 3)
        # Set the trans_model for the current page to the base probability
        trans_model[page] = base_prob
        for link in links:
            # For the links, set it to the damping_factor divided by number of links and the base prob
            trans_model[link] = round(((damping_factor / num_links) + base_prob), 3)
        # Normalize the trans_model and return
        return normalize_dict(trans_model)

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get all page names
    page_names = list(corpus.keys())
    # Initialize pagerank dict with zero values
    pagerank = {k:0 for k in page_names}
    # Make a random choice for current page
    current_page = random.choice(page_names)
    # Iterate n times
    for i in range(n):
        # Get the transition mode, given the current page
        trans_model = transition_model(corpus, current_page, damping_factor)
        # Increment that page in the pagerank dict
        pagerank[current_page] += 1
        # Get all possible pages and their probability distributions
        candidates = []
        prob_dist = []
        for k, v in trans_model.items():
            candidates.append(k)
            prob_dist.append(v)
        # Select the next current page based on those params
        current_page = random.choices(candidates, prob_dist)[0]
    # Convert integer ranks to decimal
    pagerank = {k:v/n for (k, v) in pagerank.items()}
    # Normalize decimal ranks and return
    return normalize_dict(pagerank)

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get all page names
    page_names = list(corpus.keys())
    # Get number of pages
    num_pages = len(page_names)
    # Initialize a starting pagerank dict
    start_pagerank_dict = {k:1/num_pages for k in page_names}
    # Initialize an ending pagerank dict with nonsense values
    end_pagerank_dict = {k:1000/num_pages for k in page_names}
    first = True
    # Do pagerank calculation until values of start and end dicts converge
    while not values_have_converged(start_pagerank_dict, end_pagerank_dict, 0.01):
        if not first:
            start_pagerank_dict = copy.deepcopy(end_pagerank_dict)
        first = False
        end_pagerank_dict = get_pagerank_dict(corpus, start_pagerank_dict, damping_factor)
    return end_pagerank_dict

def values_have_converged(start_dict, end_dict, threshold):
    '''
    This helper function indicates if the values in the two dicts have converged or not.
    '''
    # Get values in each dict
    start_values = list(start_dict.values())
    end_values = list(end_dict.values())
    # Confirm len is equal between two lists of values
    if len(start_values) != len(end_values):
        raise ValueError('Dicts must be same length')
    else:
        value_checks = []
        # Loop through both lists of values and get difference
        for i, val in enumerate(start_values):
            diff = abs(start_values[i] - end_values[i])
            # If the difference is less than the threshold, add True to the value checks
            # Otherwise, add false
            if diff < threshold:
                value_checks.append(True)
            else:
                value_checks.append(False)
        # Return check of all values
        return all(value_checks)

def get_pagerank_dict(corpus, pagerank_dict, damping_factor):
    '''
    This helper function creates a new pagerank dict form a deep copy
    '''
    new_pagerank_dict = copy.deepcopy(pagerank_dict)
    for page in pagerank_dict:
        new_pagerank_dict[page] = get_pagerank(corpus, pagerank_dict, page, damping_factor)
    return new_pagerank_dict

def get_pagerank(corpus, pagerank_dict, target_page, damping_factor):
    '''
    This function calculates the pagerank based on incoming links
    '''
    num_pages = len(corpus)
    incoming_links = get_links(corpus, target_page, True)
    # Get random probability
    rand = (1 - damping_factor) / num_pages
    # Get alternative probability, based on pagerank algorithm with incoming, outgoing links, current page, and existing pagerank
    alt = damping_factor * sum([pagerank_dict[i]/len(get_links(corpus, i, False)) for i in incoming_links])
    # Return the union of these two approaches
    return rand + alt

def get_links(corpus, target_page, incoming):
    '''
    This helper function gets links for a page. Incoming flag indicates if incoming or outgoing is desired.
    '''
    linked_pages = set()
    for page in corpus:
        # Incoming links (pages that link to target_page)
        if incoming:
            if target_page in corpus[page]:
                linked_pages.add(page)
        # Outgoing links (pages that the target_page links to)
        else:
            if page in corpus[target_page]:
                linked_pages.add(page)
    return linked_pages

def normalize_dict(raw_dict):
    '''
    This helper functions normalizes dicts without mutating the original.
    '''
    # Deep copy of original
    _dict = copy.deepcopy(raw_dict)
    # Calculate the normalizing factor based on existing values
    norm_factor = 1/sum(_dict.values())
    # Generate normalized dict with normalizing factor
    normalized_dict = {k:v*norm_factor for k, v in _dict.items()}
    return normalized_dict

if __name__ == "__main__":
    main()
