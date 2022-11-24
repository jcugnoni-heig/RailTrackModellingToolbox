list_of_files = ["_Nominal",
                 "_EL",
                 "_EN",
                 "_ET",
                 "_GLN",
                 "_GLT",
                 "_GTN",
                 "_NULN",
                 "_NULT",
                 "_NUTN"]

data = {}


for file in list_of_files:
    list_of_lines = []
    with open("results/eigenFrequencies" + file + ".txt","r") as f:
        for line in f:
            list_of_lines.append(line)
        for i in range(12):
            data["mode_" + str(i+1) + file] = list_of_lines[i+11].strip().split("  ")[1]

with open("matrix.txt", "w") as myF:
    myF.write("modes ; Nominal ; EL ; EN ; ET ; GLN ; GLT ; GTN ; NULN ; NULT ; NUTN\n")
    for i in range(12):
        myF.write("mode " + str(i+1) + " ; ")
        nominal_value = float(data["mode_" + str(i+1) + "_Nominal"])
        for file in list_of_files:
            if(file == "_Nominal"):
                myF.write(str(round(nominal_value)) + " Hz ; ")
            elif(file == "_NUTN"):
                to_write = 100*round((float(data["mode_" + str(i+1) + file])-(nominal_value)) /(nominal_value), 2)
                if(to_write == 0.0):
                    myF.write("-")
                else:
                    myF.write(str(to_write) + " %")
            else:
                to_write = 100*round((float(data["mode_" + str(i+1) + file])-(nominal_value)) /(nominal_value), 2)
                if(to_write == 0.0):
                    myF.write("- ; ")
                else:
                    myF.write(str(to_write) + " % ; ")
        myF.write("\n")