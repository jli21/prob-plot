import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time 

def calculate_expected_value(p, max_tries, pity_count=None):
    if pity_count is not None and pity_count <= max_tries:
        expected_attempts_within_pity = sum([(1-p)**(n-1) * p * n for n in range(1, pity_count)])
        probability_not_won_by_pity = (1-p)**(pity_count-1)
        expected_value = expected_attempts_within_pity + probability_not_won_by_pity * pity_count
    else:
        expected_value = 1 / p if p > 0 else float('inf')
    return expected_value

def monte_carlo_simulation(prize_probs, num_simulations=50000):
    total_tries = []
    for _ in range(num_simulations):
        uncollected_prizes = list(range(len(prize_probs)))  
        tries = 0
        
        while uncollected_prizes:
            tries += 1
            for i in list(uncollected_prizes): 
                if np.random.random() < prize_probs[i]:
                    uncollected_prizes.remove(i)  
                
        total_tries.append(tries)
        
    expected_tries = np.mean(total_tries)
    return expected_tries, np.array(total_tries)


def app():
    st.title("Interactive Probability Chart")

    tab1, tab2 = st.tabs(["Probability Chart", "Monte Carlo Simulation"])

    with tab1:
        p_input = st.text_input("Enter the probability of winning per try (as a percentage)", value="1.2")
        try:
            p = float(p_input) / 100
        except ValueError:
            st.error("Please enter a valid probability value.")
            return

        max_tries = st.slider("Select the maximum number of tries", 1, 1000, 200)
        pity_count = st.number_input("Enter pity count (leave 0 for no pity)", min_value=0, max_value=max_tries, value=0, format="%d")

        if pity_count > 0:
            expected_tries = calculate_expected_value(p, max_tries, pity_count)
        else:
            expected_tries = calculate_expected_value(p, max_tries)

        st.write(f"Expected number of tries to win a prize: {expected_tries:.2f}")

        n_tries = np.arange(1, max_tries + 1)
        if pity_count > 0 and pity_count <= max_tries:
            probabilities = np.array([1 - (1 - p)**n if n < pity_count else 1 for n in n_tries])
        else:
            probabilities = 1 - (1 - p) ** n_tries

        fig = go.Figure(data=go.Scatter(x=n_tries, y=probabilities, mode='lines+markers', line=dict(color='red')))
        fig.update_layout(title='Probability of Winning At Least One Prize in N Tries', xaxis_title='Number of Tries', yaxis_title='Probability', hovermode='closest')

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        num_prizes = st.number_input("Enter the number of different prizes", min_value=1, max_value=100, value=2, format="%d")
        default_probs = [1.2, 2]  # Default probabilities
        prize_probs = []

        for i in range(num_prizes):
            default_value = str(default_probs[i]) if i < len(default_probs) else "0"
            prob_input = st.text_input(f"Enter the probability of winning prize {i+1} (as a percentage)", value=default_value, key=f"prob_{i}")
            try:
                prob = float(prob_input)
                prize_probs.append(prob / 100)
            except ValueError:
                st.error(f"Please enter a valid probability value for prize {i+1}.")
                return


        if st.button("Run Monte Carlo Simulation"):
            start_time = time.time()
            expected_tries, tries_distribution = monte_carlo_simulation(prize_probs)
            elapsed_time = time.time() - start_time
            st.info(f"Simulation took {elapsed_time:.2f} seconds to run.")
            st.write(f"Expected number of tries to win all prizes: {expected_tries:.2f}")

            fig = go.Figure(data=go.Histogram(x=tries_distribution))
            fig.update_layout(title='Distribution of Tries to Win All Prizes', xaxis_title='Number of Tries', yaxis_title='Count', hovermode='closest')
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
