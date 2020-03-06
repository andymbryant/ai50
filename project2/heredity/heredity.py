import csv
import itertools
import sys
import numpy

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initialize people_prob dict for use throughout
    people_prob = {}
    # Loop through all people
    for person in people:
        people_prob[person] = None
        # Get the number of copies of the gene
        person_num_copies = get_num_copies(person, one_gene, two_genes)
        # Check if person has the trait
        has_trait = check_has_trait(person, have_trait)
        # Get the prob of trait given the number of copies and if has trait
        has_trait_prob = PROBS["trait"][person_num_copies][has_trait]
        # Get parent information
        mother = people[person]['mother']
        father = people[person]['father']
        # If no parent information
        if mother is None and father is None:
            has_gene_prob = PROBS['gene'][person_num_copies]
        else:
            # Get the number of gene copies for parents
            mother_num_copies = get_num_copies(mother, one_gene, two_genes)
            father_num_copies = get_num_copies(father, one_gene, two_genes)
            # Calculate prob of inheritance by each parent
            mother_gives_gene = get_prob_parent_gives_gene(mother_num_copies)
            father_gives_gene = get_prob_parent_gives_gene(father_num_copies)
            # Calculate inheritance prob, based on number of copies person has
            if person_num_copies == 0:
                # If 0, multiply both exclusive possibilities
                has_gene_prob = (mother_gives_gene + (1 - father_gives_gene)) * ((1 - mother_gives_gene) + father_gives_gene)
            elif person_num_copies == 1:
                # If 1, add both exclusive  possibilities
                has_gene_prob = (mother_gives_gene * (1 - father_gives_gene)) + ((1 - mother_gives_gene) * father_gives_gene)
            else:
                # If 2, multiply inclusive possibilities (they can both pass one gene)
                has_gene_prob = mother_gives_gene * father_gives_gene
        # Multiply by prob that has trait and store in people_prob dict
        people_prob[person] = has_gene_prob * has_trait_prob
    # multiply all values in people_prob dict and return (this is the joint probability)
    return numpy.prod(list(people_prob.values()))

def get_prob_parent_gives_gene(num_copies):
    '''
    This helper function takes in the number of gene copies from a parent
    and returns the probability that they will pass it on to their child.
    '''
    if num_copies == 0:
        return PROBS["mutation"]
    elif num_copies == 1:
        return 0.5
    elif num_copies == 2:
        return 1 - PROBS["mutation"]
    else:
        raise ValueError('Number of copies must be 0, 1, or 2.')

def get_num_copies(person, one_gene, two_genes):
    '''
    This helper function determines if person has one, two, or zero genes,
    based on sets provided.
    '''
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0

def check_has_trait(person, have_trait):
    '''
    This helper function checks if person is in have_trait set.
    '''
    if person in have_trait:
        return True
    else:
        return False

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Loop through probabilities
    for person in probabilities:
        # Get number of copies in this iteration and add p to that part of the probabilities dict
        num_copies = get_num_copies(person, one_gene, two_genes)
        probabilities[person]["gene"][num_copies] += p
        # Get has_trait this iteration and add p to that part of the probabilities dict
        has_trait = check_has_trait(person, have_trait)
        probabilities[person]["trait"][has_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    keys = ['gene', 'trait']
    # Loop through probabilities and access the keys in each person dict
    for person in probabilities:
        for key in keys:
            all_key_probs = []
            # Get all values and add to new list
            for val in probabilities[person][key].values():
                all_key_probs.append(val)
            # Add all values together
            sum_all_key_probs = sum(all_key_probs)

            for k in probabilities[person][key].keys():
                # Loop through all probability values again, normalizing with sum of all value probs
                probabilities[person][key][k] = probabilities[person][key][k] / sum_all_key_probs

if __name__ == "__main__":
    main()