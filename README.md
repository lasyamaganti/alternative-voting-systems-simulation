# Rerunning 2024: A Simulation of Alternative Voting Rules

A Python simulation exploring how different voting systems could have affected the **2024 U.S. presidential election**. Using real vote shares from seven battleground states, I generated synthetic ranked ballots and compared outcomes under **plurality, Instant Runoff Voting (IRV), Condorcet voting, and approval voting**.

## How It Works

Because real election data does not include complete voter rankings, I modeled voter preferences by:

* Using actual 2024 vote shares to generate first-choice preferences
* Assigning second- and third-choice preferences using weighted probabilities based on ideological similarity
* Simulating elections with both **1,000 and 100,000 voters per state**
* Running the same electorate through four different voting systems
* Testing approval voting with different numbers of approved candidates

## Key Findings

Plurality, IRV, and Condorcet produced the same winner across all seven states in the larger simulations. **Approval voting produced the most variation**, with outcomes changing as voters were allowed to approve more candidates.

The results demonstrate how election outcomes depend not only on voter preferences, but also on the rules used to aggregate those preferences.

## Technologies & Concepts

**Python • Simulation • Probability • Synthetic Data • Social Choice Theory • Voting Systems**

## Future Improvements

* Model complete voter rankings using weighted preferences
* Test different assumptions about voter behavior
* Add more advanced approval-voting thresholds
* Expand the simulation to all 50 states
