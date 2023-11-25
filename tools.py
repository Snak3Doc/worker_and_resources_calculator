# tools.py --
### Notes ###
#- Conveyor Engine Throughput 600t/d (Direct Connection is much higher)

# Calculates mine output in tons
def calc_mine_output(ore_purity_percent, max_prod_per_worker, max_workers, num_workers=None):
    if num_workers is None:
        actual_workers = max_workers
    else:
        actual_workers = num_workers

    # Convert % to ratio
    ore_purity_ratio = ore_purity_percent / 100

    # Calculate total production
    total_daily_prod = round(max_prod_per_worker * actual_workers * ore_purity_ratio, 2)

    return ["Mine", actual_workers, total_daily_prod] # name, tons

# Calculates factory/processing plant output in tons/m3
def calc_factory_output(max_output, max_inputs_lst, max_workers, num_workers=None):
    if num_workers is None:
        actual_workers = max_workers
    else:
        actual_workers = num_workers

    # Calculate the worker ratio
    worker_ratio = actual_workers / max_workers

    # Calculate utilization %
    utilization_percent = int(round((worker_ratio * 100), 0))
    
    # Calculate the actual output
    actual_output = max_output * worker_ratio

    # Calculate the actual inputs
    actual_inputs = [max_input * worker_ratio for max_input in max_inputs_lst]

    return ["Factory/Plant", actual_workers, actual_output, actual_inputs, utilization_percent] # n, ot, it, %, w


if __name__ == '__main__':
    mine = calc_mine_output(100, 4.2, 220)
    fact = calc_factory_output(120, [210], 15, 10)

    print(f"Type: {mine[0]}\nWorkers: {mine[1]}\nOutput: {mine[2]}t\n")
    print(f"Type: {fact[0]}\nWorkers: {fact[1]}\nOutput: {fact[2]}t\nInputs: {fact[3]}t\nUtilization: {fact[4]}%\n")