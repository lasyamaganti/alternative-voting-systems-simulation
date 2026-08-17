import random

# List of candidates
candidates = ["Trump", "Harris", "Kennedy", "Stein", "West", "Oliver"]

# First-choice per state 
state_poll_shares = {
    "AZ": {
        "Trump": 52.2,
        "Harris": 46.7,
        "Kennedy": 0.0,
        "Stein": 0.5,
        "West": 0.0,
        "Oliver": 0.5
    },
    "GA": {
        "Trump": 50.7,
        "Harris": 48.5,
        "Kennedy": 0.0,
        "Stein": 0.3,
        "West": 0.0,
        "Oliver": 0.4
    },
    "PA": {
        "Trump": 50.4,
        "Harris": 48.6,
        "Kennedy": 0.0,
        "Stein": 0.5,
        "West": 0.0,
        "Oliver": 0.5
    },
    "MI": {
        "Trump": 49.7,
        "Harris": 48.3,
        "Kennedy": 0.5,
        "Stein": 0.8,
        "West": 0.1,
        "Oliver": 0.4
    },
    "WI": {
        "Trump": 49.6,
        "Harris": 48.7,
        "Kennedy": 0.5,
        "Stein": 0.4,
        "West": 0.1,
        "Oliver": 0.3
    },
    "NV": {
        "Trump": 50.6,
        "Harris": 47.5,
        "Kennedy": 0.0,
        "Stein": 0.0,
        "West": 0.0,
        "Oliver": 0.4
    },
    "NC": {
        "Trump": 50.9,
        "Harris": 47.6,
        "Kennedy": 0.0,
        "Stein": 0.4,
        "West": 0.2,
        "Oliver": 0.4
    }
}

# weights for second choice based on similarity of ideals
second_pref_weights = {
    "Trump": {
        "Harris": 0.10,
        "Kennedy": 0.30,
        "Stein": 0.10,
        "West": 0.10,
        "Oliver": 0.40
    },

    "Harris": {
        "Trump": 0.05,
        "Kennedy": 0.20,
        "Stein": 0.40,
        "West": 0.30,
        "Oliver": 0.05
    },

    "Kennedy": {
        "Trump": 0.30,
        "Harris": 0.30,
        "Stein": 0.10,
        "West": 0.10,
        "Oliver": 0.20
    },

    "West": {
        "Trump": 0.05,
        "Harris": 0.30,
        "Kennedy": 0.20,
        "Stein": 0.40,
        "Oliver": 0.05
    },

    "Stein": {
        "Trump": 0.05,
        "Harris": 0.30,
        "Kennedy": 0.20,
        "West": 0.40,
        "Oliver": 0.05
    },

    "Oliver": {
        "Trump": 0.40,
        "Harris": 0.15,
        "Kennedy": 0.30,
        "Stein": 0.075,
        "West": 0.075
    }
}

# Number of voters to simulate
NUM_VOTERS = 100000

# GENERATE RANKED BALLOTS

def choose_first_choice(poll_shares, candidates):
    """
    Choose a first-choice candidate using the poll percentages.
    """
    total = sum(poll_shares[c] for c in candidates)
    r = random.random() * total
    running = 0.0
    for c in candidates:
        running += poll_shares[c]
        if r <= running:
            return c
    return candidates[-1] 


def weighted_choice(options, weights):
    """
    Choose one option from a list, with probabilities proportional to weights.
    """
    total = sum(weights)
    if total <= 0:
        return random.choice(options)

    r = random.random() * total
    running = 0.0
    for i in range(len(options)):
        running += weights[i]
        if r <= running:
            return options[i]
    return options[-1]


def make_one_ballot(candidates, poll_shares, second_pref_weights):
    """
    Pick first choice using poll_shares, pick second and third choice using second_pref_weights based on first choice.
    """
    first = choose_first_choice(poll_shares, candidates)

    # second choices (everyone except first)
    others = [c for c in candidates if c != first]

    weights_row = second_pref_weights.get(first, {})

    weights = []
    for c in others:
        base = weights_row.get(c, 0.1)
        # small random jitter so different electorates are slightly different
        jitter = random.uniform(-0.05, 0.05)
        w = max(0.01, base + jitter) 
        weights.append(w)


    # choose second choice with weights
    second = weighted_choice(others, weights)

    # remaining candidates after choosing second
    remaining = [c for c in others if c != second]

    # use second choice weights to do third choice
    third_weights_row = second_pref_weights.get(second, {})
    
    third_weights = []
    for c in remaining:
        base = third_weights_row.get(c, 0.1)
        jitter = random.uniform(-0.05, 0.05)
        w = max(0.01, base + jitter)
        third_weights.append(w)
       
    third = weighted_choice(remaining, third_weights)
    
    rest = [c for c in remaining if c != third]
    random.shuffle(rest)
    ballot = [first, second, third] + rest
    return ballot


def generate_ballots(num_voters, candidates, poll_shares, second_pref_weights):
    """
    Make ranked ballots.
    """
    ballots = []
    for i in range(num_voters):
        ballots.append(make_one_ballot(candidates, poll_shares, second_pref_weights))
    return ballots

# PLURALITY VOTING

def plurality_winner(ballots, candidates):
    counts = {}
    for c in candidates:
        counts[c] = 0

    for ballot in ballots:
        first = ballot[0]
        counts[first] += 1

    winner = None
    max_votes = -1
    for c in candidates:
        if counts[c] > max_votes:
            max_votes = counts[c]
            winner = c

    return winner, counts


# IRV 

def irv_winner(ballots, candidates):
    remaining = candidates[:]  # copy so removes eliminated candidate without affecting the original list

    while True:
        counts = {}
        for c in remaining:
            counts[c] = 0

        total_active = 0

        for ballot in ballots:
            # find first candidate on this ballot who is still remaining
            for c in ballot:
                if c in remaining:
                    counts[c] += 1
                    total_active += 1
                    break

        if len(remaining) == 0:
            return None

        # check for majority
        for c in remaining:
            if counts[c] > total_active / 2.0:
                return c

        # eliminate lowest candidate
        min_votes = min(counts[c] for c in remaining)
        lowest = [c for c in remaining if counts[c] == min_votes]

        elim = random.choice(lowest)
        remaining.remove(elim)

        if len(remaining) == 1:
            return remaining[0]


# CONDORCET WINNER

def prefers_over(ballot, a, b):
    # include try/except in case candidate is not in ballot
    try:
        pos_a = ballot.index(a)
    except ValueError:
        pos_a = 999
    try:
        pos_b = ballot.index(b)
    except ValueError:
        pos_b = 999
    return pos_a < pos_b


def condorcet_winner(ballots, candidates):
    num_voters = len(ballots)

    for a in candidates:
        wins_all = True
        for b in candidates:
            if a == b:
                continue

            count_a_over_b = 0
            for ballot in ballots:
                if prefers_over(ballot, a, b):
                    count_a_over_b += 1

            if count_a_over_b <= num_voters / 2.0: # checks if more than half the voters prefer a over b 
                wins_all = False
                break

        if wins_all:
            return a

    return None


# APPROVAL VOTING

def ranked_to_approval(ballot, k):
    return ballot[:k]


def approval_winner_from_ranked(ballots, candidates, k):
    counts = {}
    for c in candidates:
        counts[c] = 0

    for ballot in ballots:
        approved = ranked_to_approval(ballot, k)
        for c in approved:
            counts[c] += 1

    max_approvals = max(counts.values())
    tied = [c for c in candidates if counts[c] == max_approvals]

    # break ties randomly
    winner = random.choice(tied)

    return winner, counts



# RUN 

if __name__ == "__main__":
    #random.seed(1)

    for state, poll_shares in state_poll_shares.items():
        print("---------------------")
        print("State:", state)
        print("---------------------")

        # Generate ballots
        ballots = generate_ballots(NUM_VOTERS, candidates, poll_shares, second_pref_weights)

        # Plurality
        pl_w, pl_counts = plurality_winner(ballots, candidates)
        print("Plurality winner:", pl_w)
        print("Plurality counts:", pl_counts)
        print()

        # IRV
        irv_w = irv_winner(ballots, candidates)
        print("IRV winner:", irv_w)
        print()

        # Condorcet
        cond_w = condorcet_winner(ballots, candidates)
        print("Condorcet winner:", cond_w)
        print()

        # Approval voting for k = 1, 2, 3
        for k in [1, 2, 3]:
            appr_w, appr_counts = approval_winner_from_ranked(ballots, candidates, k=k)
            print(f"Approval winner (top {k} approved): {appr_w}")
            print("\n")
