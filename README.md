# GWget

GWget automatises the download of the PE samples and sensitivity estimate files released as part of the different iterations of the GWTC catalogue by the LIGO-Virgo-KAGRA collaboration. These files are scattered around a number of Zenodo repositories and in a number of different versions: this package is an effort to simplify the collection of the files necessary to perform population studies.

GWget comes with two command-line interfaces: 
    - `gwget [-o OUTPUT -c CATALOGUE --no_injections]` downloads the files corresponding to the specified GWTC (default: latest). In addition to this, it creates additional sub-catalogues with symlinks pointing at the BBH events used for population studies of GWTC-3, GWTC-4 and GWTC-5.
    - `makecat -e FOLDER -l LIST` can be used to create a custom sub-catalogue with the events specified in a `.txt` file (e.g., for ad-hoc studies).
Beware that, as of today, the total size of the files that are downloaded by default is around 130 GB, and it can take quite a while to finish. 
You can install GWget either via pip
```
pip install gwget
```
or from the repository
```
git clone git@github.com:sterinaldi/gwget.git
cd gwget
pip install .
```
***Disclaimer:*** this repository is not mantained nor endorsed by the LVK collaboration nor any of its members and it is provided *as-is*, with no guarantees (other than the best effort of the author, who uses this very routine in his papers) of correctness and absence of bugs.
