## ATE Analysis

Code back in my first ever internship at Spectra7 - the code does simple dimensionality reduction and some other unsupervised learning. It was my first time learning R at the time. Looking back some of this code is very badly written but it did the job at the time. 

### This repository contains the following:
* Conversion of STDF (Standard Testing Data Format) from binary to csv with pipeline built on top of pystdf
* Automated Dimensionality Reduction of multivariable data using PCA, exploting dimensionality reduction to reduce testing time.
* Automated regression modelling scripts to automate the generation of regression models based on PCA analysis.
* Rscripts for automated generation of batch reports and distributions of STDF files.
* And finally our final model based on analysis which is an OLS multiple regression model. (multipleRegression.py)


##### Note: This repo is for personal use please contact me at ragy202@gmail.com if you have any questions about automated testing data.


### Final Models Specs:
#### Multiple Regression Model I specs:
Dependant variables:
* Continuity <> ADDR_DEF
* Continuity <> SDA
* Continuity <> TX_EN


