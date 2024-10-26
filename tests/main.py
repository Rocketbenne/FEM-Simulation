import csv
from argparse import ArgumentParser

def read_csv(filepath):
    with open(filepath, mode = 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
    

def read_column_from_csv(filepath, column_index):
    with open(filepath, mode = 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        values = []
        for row in reader:
            value = float(row[0].split(';')[1])
            values.append(value)

    return values

# Checks if the file contains the same values as the reference
def test_csv(name: str):
    reference_path = 'tests/references/' + name + '.csv'
    program_output_path = 'results/' + name + '.csv'

    reference_content = read_column_from_csv(reference_path, 1)
    program_output_content = read_column_from_csv(program_output_path, 1)

    # Checks: same amount of nodes
    assert len(reference_content) == len(program_output_content)

    TOLERANCE = 0.1

    for i, value in enumerate(reference_content):
        diff = abs(reference_content[i] - program_output_content[i])
        assert diff <= TOLERANCE


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--name', type=str, help="Name of the Testcase")
    args = parser.parse_args()

    test_csv(args.name)
