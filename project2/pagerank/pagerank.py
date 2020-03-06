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

def transition_model(corpus, current_page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    trans_model = {}
    all_pages = list(corpus.keys())
    num_all_pages = len(all_pages)
    base_prob = (1 - damping_factor) / num_all_pages

    for page in corpus:
        num_links = len(corpus[page])
        if num_links < 1:
            for p in corpus:
                trans_model[p] = round((1 / num_all_pages), 3)
            return trans_model
        else:
            if page != current_page:
                trans_model[page] = round(
                    base_prob + (damping_factor / (num_all_pages - 1)), 3)
            else:
                trans_model[page] = round(base_prob, 3)
    return trans_model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_names = list(corpus.keys())
    pagerank = {k:0 for k in page_names}
    current_page = random.choice(page_names)
    for i in range(n):
        trans_model = transition_model(corpus, current_page, damping_factor)
        pagerank[current_page] += 1
        candidates = []
        prob_dist = []
        for k, v in trans_model.items():
            candidates.append(k)
            prob_dist.append(v)
        print(prob_dist)
        current_page = random.choices(candidates, prob_dist)
        print(current_page)
    # TODO normalize
    pagerank = {k:v/n for (k, v) in pagerank.items()}
    norm_factor = 1/sum(pagerank.values())
    normalized_pagerank = {k:v*norm_factor for k, v in pagerank.items()}
    return normalized_pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_names = list(corpus.keys())
    num_pages = len(page_names)
    start_pagerank_dict = {k:1/num_pages for k in page_names}
    end_pagerank_dict = {k:1000/num_pages for k in page_names}
    first = True
    while abs(start_pagerank_dict['1.html'] - end_pagerank_dict['1.html']) > 0.01:
        if not first:
            start_pagerank_dict = copy.deepcopy(end_pagerank_dict)
        first = False
        end_pagerank_dict = get_pagerank_dict(
            corpus, start_pagerank_dict, damping_factor)
    return end_pagerank_dict

def get_pagerank_dict(corpus, pagerank_dict, damping_factor):
    new_pagerank_dict = copy.deepcopy(pagerank_dict)
    for page in pagerank_dict:
        new_pagerank_dict[page] = get_pagerank(
            corpus, pagerank_dict, page, damping_factor)
    return new_pagerank_dict

def get_pagerank(corpus, pagerank_dict, target_page, damping_factor):
    num_pages = len(corpus)
    incoming_links = get_links(corpus, target_page, True)
    rand = (1 - damping_factor) / num_pages
    if len(incoming_links) == 0:
        alt = 0
    else:
        # alt = damping_factor * sum( [get_pagerank(corpus, i, damping_factor)/get_links(corpus, i, False) for i in incoming_links])
        alt = damping_factor * \
            sum([pagerank_dict[i]/len(get_links(corpus, i, False))
                 for i in incoming_links])
    return rand + alt

def get_links(corpus, target_page, incoming):
    linked_pages = set()
    for page in corpus:
        # If you want incoming pages (pages that link to target_page)
        if incoming:
            if target_page in corpus[page]:
                linked_pages.add(page)
        # If you want outgoing pages (pages that the target_page links to)
        else:
            if page in corpus[target_page]:
                linked_pages.add(page)
    return linked_pages

if __name__ == "__main__":
    main()
