import csv
import sys

def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

def filter_results(data, conf1, conf2):
    filtered_data = {conf1+"_Ex": [], conf2+"_Ex": [], conf1+"_"+conf2+"_common": []}

    for row in data:
        benchmark = row['benchmark']

        if row['configuration'] == conf1 and (row['result'] == 'SAT-VERIFIED' or row ['result'] == 'UNSAT'):
            # Check if the result column for conf2 is 'UNKNOWN' for the same benchmark
            if any(entry['configuration'] == conf2 and entry['benchmark'] == benchmark and entry['result'] == 'UNKNOWN' for entry in data):
                filtered_data[conf1+"_Ex"].append(row)
        elif row['configuration'] == conf2 and (row['result'] == 'SAT-VERIFIED' or row ['result'] == 'UNSAT'):
            # Check if the result column for conf1 is 'UNKNOWN' for the same benchmark
            if any(entry['configuration'] == conf1 and entry['benchmark'] == benchmark and entry['result'] == 'UNKNOWN' for entry in data):
                filtered_data[conf2+"_Ex"].append(row)
        elif row['configuration'] == conf1 and (row['result'] == 'SAT-VERIFIED' or row ['result'] == 'UNSAT'):
            # Check if the result column for both conf1 and conf2 is 'UNKNOWN' for the same benchmark
            if any(entry['configuration'] == conf2 and entry['benchmark'] == benchmark and entry['result'] == 'SAT-VERIFIED' for entry in data):
                filtered_data[conf1+"_"+conf2+"_common"].append(row)
        # elif row['configuration'] == conf1 and row['result'] == 'SAT-VERIFIED' and row['configuration'] != conf2 and float(row['cputime']) > float(data[row['benchmark']][conf2]['cputime']):
        #     filtered_data[conf1+"+"].append(row)
        # elif row['configuration'] == conf2 and row['result'] == 'SAT-VERIFIED' and row['configuration'] != conf1 and float(row['cputime']) > float(data[row['benchmark']][conf1]['cputime']):
        #     filtered_data[conf2+"+"].append(row)

    return filtered_data

def average_cputime(data):
    averages = {}
    for key, rows in data.items():
        cputimes = [float(row['cputime']) for row in rows]
        averages[key] = sum(cputimes) / len(cputimes) if len(cputimes) > 0 else 0
    return averages

def main():

    file_path, conf1, conf2 = sys.argv[1], sys.argv[2], sys.argv[3]

    data = read_csv(file_path)
    filtered_data = filter_results(data, conf1, conf2)
    
    for k, v in filtered_data.items ():
        #if 'nthrestart' in k:
            print (k)
            for b in [[e ['benchmark'], e ['result'] ] for e in v]:
                print (b [0], end=' ')
                print (b [1])
        
    #averages = average_cputime(filtered_data)


    # print(f"Average cputime for ({conf1}_Ex): {averages[conf1+'_Ex']}")
    # print(f"Average cputime for ({conf2}_Ex): {averages[conf2+'_Ex']}")
    # print(f"Average cputime for ({conf1}_{conf2}_common): {averages[conf1+'_'+conf2+'_common']}")
    # print(f"Average cputime for ({conf1}+): {averages[conf1+'+']}")
    # print(f"Average cputime for ({conf2}+): {averages[conf2+'+']}")

if __name__ == "__main__":
    main()

