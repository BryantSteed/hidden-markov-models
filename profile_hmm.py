from typing import Dict, Set

class ProfileCalculator:
    def __init__(self, alignment, alphabet, threshold):
        self.alignment = alignment
        self.count = len(alignment)
        self.len = len(alignment[0])
        self.alphabet = alphabet
        self.threshold = threshold
        self.transfer_frequencies: Dict[str, Dict[str, int]] = {}
        self.emission_frequencies: Dict[str, Dict[str, int]] = {}
        self.ignore_cols: Set[int] = self.get_ignored_columns()
        self.match_count: int = None

    def get_ignored_columns(self):
        ig_cols = set()
        for col in range(self.len):
            gap_total = 0
            for seq in self.alignment:
                if seq[col] == '-':
                    gap_total += 1

            if gap_total / self.count >= self.threshold:
                ig_cols.add(col)
        return ig_cols

    def calculate(self):
        for sequence in self.alignment:
            self.process_sequence(sequence)

        transfer_fractions = {}
        emission_fractions = {}
        for state in self.transfer_frequencies:
            transfer_fractions[state] = {}
            total = sum(self.transfer_frequencies[state].values())
            for next_state in self.transfer_frequencies[state]:
                transfer_fractions[state][next_state] = self.transfer_frequencies[state][next_state] / total
        
        for state in self.emission_frequencies:
            emission_fractions[state] = {}
            total = sum(self.emission_frequencies[state].values())
            for symbol in self.emission_frequencies[state]:
                emission_fractions[state][symbol] = self.emission_frequencies[state][symbol] / total
        return transfer_fractions, emission_fractions, self.match_count

    def process_sequence(self, sequence):
        curr_state = 'S'
        for i, symbol in enumerate(sequence):
            if i in self.ignore_cols:
                if symbol == '-':
                    continue
                if curr_state == "S":
                    next_state = "I0"
                elif curr_state.startswith("I"):
                    next_state = curr_state
                elif curr_state.startswith("D") or curr_state.startswith("M"):
                    next_state = f"I{curr_state[1:]}"
                self.record_transition(curr_state, next_state, symbol)
            else:
                if symbol == "-":
                    if curr_state == "S":
                        next_state = "D1"
                    else:
                        state_count = int(curr_state[1:]) + 1
                        next_state = f"D{state_count}"
                else:
                    if curr_state == "S":
                        next_state = "M1"
                    else:
                        state_count = int(curr_state[1:]) + 1
                        next_state = f"M{state_count}"
                self.record_transition(curr_state, next_state, symbol)
            curr_state = next_state
        
        if curr_state not in self.transfer_frequencies:
            self.transfer_frequencies[curr_state] = {}
        if "E" not in self.transfer_frequencies[curr_state]:
            self.transfer_frequencies[curr_state]["E"] = 0
        self.transfer_frequencies[curr_state]["E"] += 1

        self.match_count = int(curr_state[1:])


    def record_transition(self, curr_state, next_state, symbol):
        if curr_state not in self.transfer_frequencies:
            self.transfer_frequencies[curr_state] = {}
        if next_state not in self.transfer_frequencies[curr_state]:
            self.transfer_frequencies[curr_state][next_state] = 0
        self.transfer_frequencies[curr_state][next_state] += 1

        if next_state.startswith("I") or next_state.startswith("M"):
            if next_state not in self.emission_frequencies:
                self.emission_frequencies[next_state] = {}
            if symbol not in self.emission_frequencies[next_state]:
                self.emission_frequencies[next_state][symbol] = 0
            self.emission_frequencies[next_state][symbol] += 1



def compute_profile_hmm(alignment, alphabet, threshold):
    profile_calculator = ProfileCalculator(alignment, alphabet, threshold)
    transfer_fractions, emission_fractions, match_count = profile_calculator.calculate()
    return transfer_fractions, emission_fractions, match_count
    

def read_input():
    with open("input.txt", "rt") as file:
        data = iter(file.readlines())
    threshold = float(next(data).strip())
    assert next(data).strip().startswith("-")
    alphabet = next(data).strip().split()
    assert next(data).strip().startswith("-")
    alignment = []
    for line in data:
        if not line.isspace():
            alignment.append(line.strip())
    return alignment, alphabet, threshold

def print_transfer_fractions(transfer_fractions: Dict[str, Dict[str, float]], match_count: int, file):
    matrix_headers = ["S", "I0"]
    for i in range(match_count):
        matrix_headers.append(f"M{i+1}")
        matrix_headers.append(f"D{i+1}")
        matrix_headers.append(f"I{i+1}")
    matrix_headers.append("E")
    header_print = "\t".join([""] + matrix_headers)
    print(header_print, file=file)
    for state in matrix_headers:
        row = [state]
        for next_state in matrix_headers:
            value = transfer_fractions.get(state, {}).get(next_state, 0)
            row.append(f"{value}")
        print("\t".join(row), file=file)

def print_emission_fractions(emission_fractions: Dict[str, Dict[str, float]], alphabet: list, match_count: int, file):
    matrix_headers = list(alphabet)
    header_print = "\t".join([""] + matrix_headers)
    print(header_print, file=file)
    states = ["S", "I0"]
    for i in range(match_count):
        states.append(f"M{i+1}")
        states.append(f"D{i+1}")
        states.append(f"I{i+1}")
    states.append("E")
    for state in states:
        row = [state]
        for symbol in matrix_headers:
            value = emission_fractions.get(state, {}).get(symbol, 0)
            row.append(f"{value}")
        print("\t".join(row), file=file)


if __name__ == "__main__":
    alignment, alphabet, threshold = read_input()
    transfer_fractions, emission_fractions, match_count = compute_profile_hmm(alignment, alphabet, threshold)
    # Feel Free to use sys.stdout as the output file descriptor if you want
    with open ("output.txt", "wt") as output_file:
        print_transfer_fractions(transfer_fractions, match_count, file=output_file)
        print("--------", file=output_file)
        print_emission_fractions(emission_fractions, alphabet, match_count, file=output_file)