"""
    Español flash cards...
"""

from src.kernel import kernel

SOURCE = "data/espanol_1.csv"

if __name__ == "__main__":
    # Handle command line interface specific to sp.lang. Can be absorbed into kernel?

    k = kernel(SOURCE, SIDE = "A", CATEGORY="verb")
    # e.g., modes:
    # sp2en
    # en2sp

    # set number of cards in a session (30 default)

    print("---sp.lang---\n")
    k.run_default(n = 20)

    # print(k.list_all_cards[5].PRESENT)
    # print(k.list_all_cards[3].MODE)

