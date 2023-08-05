# Example Julia conversion script
# September  27, 2016 -- Alex Hunziker

module conversion

# ---> 1.) load required package (optional)

using DataFrames

function convert(raw_file, output_file)

  # ---> 2.) read file

  if(!isfile(raw_file))
    error("Error: raw_file does not exist.")
  end

  # the header line contains non-utf8 encoded characters, so we skip this:
  dataraw = DataFrame(readtable(raw_file, separator = '\t', skipstart=1, header=false))

  names!(dataraw, map(Symbol, ["Date Time", "Water Level", "Average Flow Velocity", "Flow",
                               "Temperature", "Surface Flow Velocity", "Distance",
                               "Distance Reading Count", "Surcharge Level",
                               "Peak to Mean Ratio", "Number of Samples", "Battery Voltage"]))

  ## ---> 3.) test properties

  if(size(dataraw, 2) != 12)
    error("Input File has wrong number of columns.")
  end

  ## ---> 4.) add additional information (optional)

  #Define coordinate
  xcoor = 682558
  ycoor = 239404
  zcoor = ""

  ## ---> 5.) reformate data

  selCol = Symbol("Date Time")
  time = Dates.DateTime(dataraw[selCol], "dd.mm.yyyy HH:MM")
  dataraw[selCol] = Dates.format(time, "yyyy-mm-dd HH:MM:SS")

  dataForm = stack(dataraw, names(dataraw)[2:12], selCol)
  dataForm = dataForm[:, [selCol, :variable, :value]]
  dataForm[4] = xcoor
  dataForm[5] = ycoor
  dataForm[6] = zcoor
  names!(dataForm, [:timestamp, :parameter, :value, :x, :y, :z])

  deleterows!(dataForm, find(isna(dataForm[:, Symbol("value")])))

  ## ---> 6.) write file

  writetable(output_file, dataForm, separator = ';')

end

end
