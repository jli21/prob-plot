import streamlit as st
import plotly.graph_objects as go
import numpy as np

def calculate_expected_value(p, max_tries, pity_count=None):
    if pity_count is not None and pity_count <= max_tries:
        expected_attempts_within_pity = sum([(1-p)**(n-1) * p * n for n in range(1, pity_count)])
        probability_not_won_by_pity = (1-p)**(pity_count-1)
        expected_value = expected_attempts_within_pity + probability_not_won_by_pity * pity_count
    else:
        expected_value = 1 / p if p > 0 else float('inf')
    return expected_value

def app():
    st.title("Interactive Probability Chart")

    st.write("Probability of a prize win after \(n\) times.")

    p = st.number_input("Enter the probability of winning per try (as a percentage)", min_value=0.0, max_value=100.0, value=1.2) / 100
    max_tries = st.slider("Select the maximum number of tries", 1, 1000, 200)
    pity_count = st.number_input("Enter pity count (leave 0 for no pity)", min_value=0, max_value=max_tries, value=0, format="%d")

    # Adjust the expected tries calculation based on pity count
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

if __name__ == "__main__":
    app()
