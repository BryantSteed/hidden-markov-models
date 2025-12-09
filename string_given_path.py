import numpy as np

def get_string_probability(hidden_path, state_to_index, emission_to_index, emission_path, emission_matrix):
    prob = 1.0
    for i in range(len(hidden_path)):
        state = hidden_path[i]
        emission = emission_path[i]
        state_idx = state_to_index[state]
        emission_idx = emission_to_index[emission]
        prob *= emission_matrix[emission_idx, state_idx]
    return prob

def read_input():
    with open("input.txt", "rt") as f:
        data = iter(f.readlines())
    hidden_path = next(data).strip()
    assert next(data).startswith("-")
    states = next(data).strip().split()
    n_states = len(states)
    assert next(data).startswith("-")

    emission_path = next(data).strip()
    assert next(data).startswith("-")
    emissions = next(data).strip().split()
    n_emissions = len(emissions)

    assert next(data).startswith("-")


    matrix_headers = next(data).strip().split()
    assert matrix_headers == states
    state_to_index = {state: i for i, state in enumerate(states)}
    emission_to_index = {emission: i for i, emission in enumerate(emissions)}
    rows = []
    for i in range(n_emissions):
        row = next(data).strip().split()
        assert len(row) - 1 == n_states
        row = [float(x) for x in row[1:]]
        rows.append(row)
    emission_matrix = np.array(rows)
    return hidden_path, state_to_index, emission_to_index, emission_path, emission_matrix

if __name__ == "__main__":
    hidden_path, state_to_index, emission_to_index, emission_path, output_matrix = read_input()

    prob = get_string_probability(hidden_path, state_to_index, emission_to_index, emission_path, output_matrix)
    print(prob)