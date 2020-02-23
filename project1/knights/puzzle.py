from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # If A is a knight we know is both a knight and knave
    Biconditional(AKnight, And(AKnight, AKnave)),
    # If A is a knave we know is not both a knight and a knave
    Biconditional(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Base knowledge
    # A and B can either be a knave or a knight
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    Biconditional(AKnight, And(AKnave, BKnave)),
    Biconditional(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # If A is a knight then we know A and B are the same
    Biconditional(AKnight, And(AKnight, BKnight)),
    Biconditional(AKnight, And(AKnave, BKnave)),
    # If A is a knave then we know A and B are not the same
    Biconditional(AKnave, Not(And(AKnight, BKnight))),
    Biconditional(AKnave, Not(And(AKnave, BKnave))),

    # If b is a knight then we know A and B are not the same
    Biconditional(BKnight, Not(And(AKnight, BKnight))),
    Biconditional(BKnight, Not(And(AKnave, BKnave))),

    # If b is a knave then we know A and B are the same
    Biconditional(BKnave, And(AKnave, BKnave)),
    Biconditional(BKnave, And(AKnight, BKnight)),
)

# Puzzle 3
# 1 A says either "I am a knight." or "I am a knave.", but you don't know which.
# 2 B says "A said 'I am a knave'."
# 3 B says "C is a knave."
# 4 C says "A is a knight."
knowledge3 = And(

    # 1
    # If A is a knight we know he either said he is a knight or knave
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),
    # If A is a knave we know he either said he is a knave or knight
    Or(Biconditional(AKnave, AKnave),Biconditional(AKnave, AKnight)),

    # 2
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, Biconditional(AKnave, AKnight)),

    Biconditional(BKnave, Not(Biconditional(AKnight, AKnave))),
    Biconditional(BKnave, Not(Biconditional(AKnave, AKnight))),

    # 3
    Biconditional(BKnight, CKnave),
    Biconditional(BKnave, CKnight),

    # 4
    Biconditional(CKnight, AKnight),
    Biconditional(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
