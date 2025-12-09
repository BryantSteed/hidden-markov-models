import numpy as np

def get_hidden_path_probability(hidden_path: str, 
                                state_to_index: dict, 
                                state_transfer_matrix: np.ndarray) -> float:
    probability = 0.5
    from_state = None
    for i in range(len(hidden_path)):
        if from_state is None:
            from_state = hidden_path[i]
            continue
        to_state = hidden_path[i]
        from_index = state_to_index[from_state]
        to_index = state_to_index[to_state]
        transition_probability = state_transfer_matrix[from_index, to_index]
        probability *= transition_probability
        from_state = to_state

    return probability


def read_input():
    with open("input.txt", "rt") as f:
        data = iter(f.readlines())
    hidden_path = next(data).strip()
    assert next(data).startswith("-")
    states = next(data).strip().split()
    n_states = len(states)
    assert next(data).startswith("-")
    matrix_headers = next(data).strip().split()
    assert matrix_headers == states
    state_to_index = {state: i for i, state in enumerate(states)}
    rows = []
    for i in range(n_states):
        row = next(data).strip().split()
        assert len(row) - 1 == n_states
        row = [float(x) for x in row[1:]]
        rows.append(row)
    state_transfer_matrix = np.array(rows)
    return hidden_path,state_to_index,state_transfer_matrix

if __name__ == "__main__":
    hidden_path, state_to_index, state_transfer_matrix = read_input()

    prob = get_hidden_path_probability(hidden_path, state_to_index, state_transfer_matrix)
    print(prob)