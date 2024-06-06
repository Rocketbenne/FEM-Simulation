import pytest
import csv

def read_csv(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Checks if the file contains the same values as the reference
def test_csv():
    reference_path = 'tests/reference.csv'
    program_output_path = 'program_output.csv'

    reference_content = read_csv(reference_path)
    program_output_content = read_csv(program_output_path)

    assert reference_content == program_output_content


if __name__ == '__main__':
  pytest.main()