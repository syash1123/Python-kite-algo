import csv



def write_to_csv(data: dict, file_path: str, cols: list):
    req_data = {}
    for key in cols:
        req_data[key] = data[key]
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=cols)
        # writer.writeheader()
        writer.writerow(req_data)
