import os
import random
import re
import sys
from numpy.random import choice

DAMPING = 0.85
SAMPLES = 10_000

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
    all_pages = corpus.keys()
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
                trans_model[page] = round(base_prob + (damping_factor / (num_all_pages - 1)), 3)
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
    pagerank = {k:-1 for k in page_names}
    current_page = ""
    for i in range(n):
        if current_page == "":
            current_page = random.choice(page_names)
        trans_model = transition_model(corpus, current_page, damping_factor)
        candidates = list(trans_model.keys())
        prob_dist = list(trans_model.values())
        current_page = choice(candidates, 1, prob_dist)[0]
        pagerank[current_page] += 1

    pagerank = {k:v/n for (k,v) in pagerank.items()}
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()