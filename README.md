# Hong Kong Horse Race Predictor

- Authors: Derek Kruszewski, Yi Liu, Rob Blumberg, Carlina Kim

Data analysis project for Group 302 for DSCI (Data Science Workflows): a Master of Data Science Course at the University of British Columbia.

## About

This project attempts to build a regression model to answer the research question:

**Given a set of features related to racing horses, can we predict the outcome of a race?**

The produced model is able to predict finish times with an R^2 correaltion of 0.909.

The dataset used to answer this question is the _Hong Kong Horse Racing Dataset for Experts_, publicly available through Kaggle (HorseBaby 2018). This data has been rehosted on github for use with this project's scripts:

https://raw.githubusercontent.com/v5y8/horse_race_data/master

Please use the above github repository for downloading via setup.sh.

## Final Report

The final report can be found [here](https://github.com/UBC-MDS/DSCI_522_Group_302/blob/master/doc/final_report.Rmd).

## Usage

To replicate the above analysis, please run the following bash script:

```
bash setup.sh
```

## Dependencies
Our project uses the following libraries:

Python:
- [pandas](https://pandas.pydata.org/getpandas.html)
- [docopt](https://github.com/docopt/docopt)
- [numpy](https://numpy.org/)
- [scikit-learn](https://scikit-learn.org/stable/install.html)
- [altair](https://altair-viz.github.io/)
- [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)
- [selenium](https://pypi.org/project/selenium/)

R:
- [knitr](https://yihui.org/knitr/)
- [tidyverse](https://www.tidyverse.org/)
- [docopt](https://github.com/docopt/docopt)

Please install these packages for use with this project.

## Contributions
We welcome all contributions to this project! If you notice a bug, or have a feature request, please open up an issue [here](https://github.com/UBC-MDS/DSCI_522_Group_302/issues/new). If you'd like to contribute a feature or bug fix, you can fork our repo and submit a pull request. We will review pull requests within 7 days. All contributors must abide by our [code of conduct](https://github.com/v5y8/DSCI_522_Group_302/blob/master/CODE_OF_CONDUCT.md).

## References

<div id="refs" class="references">

<div id="ref-Dataset">

HorseBaby. 2018. “Horse Racing Dataset for Experts (Hong Kong).”
<https://www.kaggle.com/hrosebaby/horse-racing-dataset-for-experts-hong-kong>.

</div>

</div>