#!/bin/bash

# to run all tests first execute this script !

julia<<EOL
Pkg.add("DataFrames")
EOL

pip3 install pandas

R --vanilla <<EOL
install.packages("reshape2", repos="http://cran.us.r-project.org");
EOL
