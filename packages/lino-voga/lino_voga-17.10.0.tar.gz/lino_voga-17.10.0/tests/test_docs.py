from atelier.test import make_docs_suite
def load_tests(loader, standard_tests, pattern):
    # return make_docs_suite("docs")
    return make_docs_suite("docs/specs", "*sales.rst")

