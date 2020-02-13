# iri-regression

This is a repository that includes all kind of regression tests that we use for IRI. The files in the roof folder are legacy tests used by Travis. We are still running them because they catch errors.

### In order to run travis locally
1. Clone the repository
2. Inside the main folder create `iri/target` directories and put inside an iri-X.X.X.jar (must have this name, just use the correct version).
3. run `./run_all_stable_tests.sh X.X.X

One can look at `travis.yml` to see exactly how those tests are ran
