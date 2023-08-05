library(reshape2)

convert <- function(raw_file, output_file){

   data.raw <- utils::read.table(raw_file, sep="\t", skip=1, header=F)
   names(data.raw) <- c("Date Time", "Water Level", "Average Flow Velocity", "Flow",
                        "Temperature", "Surface Flow Velocity", "Distance",
                        "Distance Reading Count",  "Surcharge Level", "Peak to Mean Ratio",
                        "Number of Samples", "Battery Voltage")

   if(ncol(data.raw) !=12 )
       stop(paste("Error: Input File has", ncol(data.raw),
                  "columns, instead of the expected 12 columns."))

   if(!all(sapply(data.raw[2:ncol(data.raw)], is.numeric)==TRUE))
       stop("Error: Non-numeric input where numeric values were expected.")

   # define coordinate
   xcoor <- 682558
   ycoor <- 239404
   zcoor <- ""

   ## reformat data

   time <- strptime(data.raw$"Date Time", "%d.%m.%Y %H:%M")
   data.raw$"Date Time" <- format(time, "%Y-%m-%d %H:%M:%S")

   data.form <- reshape2::melt(data.raw, id.vars = c("Date Time"))

   colnames(data.form) <- c("timestamp", "parameter", "value")
   data.form$x <- xcoor
   data.form$y <- ycoor
   data.form$z <- zcoor

   # remove NA values
   data.form <- stats::na.omit(data.form)

   utils::write.table(data.form, file=output_file, row.names=FALSE, col.names=TRUE,
                      quote=FALSE, sep=";")

}
