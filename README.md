[![ka-decision logo](documentation/images/ka-decision-logo.png)](https://github.com/kadirkirda/ka-decision)
## ka-decision - Multi-Method MCDM Software

**ka-decisions** is a software with a user-friendly interface that makes it possible to use more than one MCDM method at the same time and integrate the results.

## Installation of ka-decision

**Requirements**
```yaml
python (version >= 3.7)
```
**Installation**

Installation of all of the required packages
```bash
$ pip install -r requirements.txt
```

## Application Overview

This document describes the **ka-decision** Desktop Application which can run standalone in users computer.

### Features

- Including a number of selected MCDM methods.
- It has an intuitive usage feature. With routing messages, it is possible for the user to understand what to do.
- Excel file format is used for input-output operations.
- It offers the opportunity to use more than one method at the same time.
- Provides detailed process tables for each method in addition to summary results.
- It has the feature of integrating the ranking results.
- In addition, there are solutions for the newly developed REF-I and REF-II methods in the literature.

### Usage of The Software

When the software is started, an interface consisting data operations, selection of methods, selection of weighting method, calculation, reporting and aggregation is opened.

<img src="documentation/images/user-interface.png"> 

On this page, if required, empty xlsx file to be imported can be created by the program by entering the criteria and alternative numbers.

In order to import the data, the "Import Data" button is clicked and the relevant data file is selected. In case of any error, the program guides the user to make the necessary corrections.

The methods to be included in the calculation are selected from the "MCDM Method Selection" list on the left.

One of the following options can be preferred for weighting the criteria:
- Default values
- Equal weighting
- Entropy weighting
- Critic weighting

When the "Calculate" button is clicked, all of the calculations are complated.

After that, the "Show Ranking" button is clicked and the summary results are displayed as follows.

<img src="documentation/images/results-presentation.png"> 

Detailed tables of the methods included in the calculation can be saved by clicking the "Save Output Tables" button. Each page of the file (in xlsx format) shows a calculation step of a method as shown below.

<img src="documentation/images/detailed-outputs.png">

For the aggregation process, a method is selected in the "Aggregation" section and then the "Aggregate" button is clicked. Currently, only the Borda method is available.

<img src="documentation/images/aggregation-results.png"> 

 # License

 - [MIT-License](LICENSE)
