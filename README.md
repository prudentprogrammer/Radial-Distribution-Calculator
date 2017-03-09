This is the README for the Gofr Simulation. 

## Structure

Highlighted below are the important files and how to run them:

* gofr_class.py: This file represents the main file to be run which utilizes the other files and generates the intermediate
output file 
* gofr.py: Represents the file which runs the actual radial distribution function on the provided data.
* gofr_config.py: Represents the configuration file
* qbox_xyz.py: This file performs progressive parsing based on the input XML data
* report_latex_files: This file has the output generated latex files
* sax_handler.py: This file has important quantities required for XML parsing
* unitcell.py: Represents a 3-d representation of a molecule
* visualizer.py: Generates the html webpage containing the visualized data according to the intermediate file

## Running the actual file

Phase 1: Generating the intermediate gofr file
To perform this, simply type:
$ python run_gofr.py

Phase 2: Generating the output html webpage containing the output
To perform this , simply type:

$ ./visualizer.py intr_files/cum_counts.txt intr_files/cum_counts2.txt


## Description
First Phase

This program reads the configuration parameters from the file, extracts the data from the input XML source(s), and runs the calculation of the radial distribution function. As a result an output text file called cum_counts.txt and a second file (if applicable), cum_counts2.txt is generated for the visualization phase. This file contains the cumulative counts recorded at every nth step. A usage of the script is shown below:

Second Phase:

After this phase, the gofr algorithm is run on the given data and the intermediate values are recorded for visualization. The second step is as easy as the first and merely involves
running the visualizer.py script. This script is executed in a very similar manner to the run gofr.py script, however the user can specify certain options such as x and y limits if needed. For instance, python visualizer.py cum_counts.txt -x 5 -y 5 will generate a output html page with x and y bounds of 5 and 5. The x and y represent the maximum ranges of the x and y axis in the generated graph. If the user does not specify x and y, then the visualizer automatically sets the bounds for the diagram


