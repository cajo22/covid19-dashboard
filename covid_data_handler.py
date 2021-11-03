def parse_csv_data(csv_filename : str) -> str:

    # Each line (row) of file {csv_filename} is appended to a list, not including line breaks.
    # This list is then returned.

    src_csv = open(csv_filename, "r")
    data = []
    for line in src_csv:
        data.append(line[:-2])
    src_csv.close()
    return(data)
