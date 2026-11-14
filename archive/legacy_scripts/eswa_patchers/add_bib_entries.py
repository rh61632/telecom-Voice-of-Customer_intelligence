from pathlib import Path

bib_file = Path("paper/eswa_latex/references.bib")

new_entries = """
@inproceedings{barman2014code,
  author    = {Barman, Utsab and Das, Amitava and Wagner, Joachim and Foster, Jennifer},
  title     = {Code Mixing: A Challenge for Language Identification in the Language of Social Media},
  booktitle = {Proceedings of the First Workshop on Computational Approaches to Code Switching},
  pages     = {13--23},
  year      = {2014},
  publisher = {Association for Computational Linguistics},
  doi       = {10.3115/v1/W14-3902}
}

@inproceedings{gamback2016comparing,
  author    = {Gamb{\\"a}ck, Bj{\\"o}rn and Das, Amitava},
  title     = {Comparing the Level of Code-Switching in Corpora},
  booktitle = {Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC'16)},
  pages     = {1850--1855},
  year      = {2016},
  publisher = {European Language Resources Association (ELRA)}
}

@article{draskovic2025aspect,
  author    = {Dra{\\v{s}}kovi{\\'{c}}, Bo{\\v{z}}o and Milanovi{\\'{c}}, Milan},
  title     = {Aspect-based sentiment analysis of user-generated content from a microblogging platform},
  journal   = {Journal of Big Data},
  volume    = {12},
  number    = {1},
  pages     = {1--31},
  year      = {2025},
  publisher = {SpringerOpen},
  doi       = {10.1186/s40537-025-01244-0}
}
"""

with open(bib_file, "r", encoding="utf-8") as f:
    existing = f.read()

if "barman2014code" not in existing:
    with open(bib_file, "a", encoding="utf-8") as f:
        f.write("\n" + new_entries.strip() + "\n")
    print("Successfully appended new entries to references.bib")
else:
    print("Entries already present.")
