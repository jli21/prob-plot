import streamlit as st
import plotly.graph_objects as go
import numpy as np

def app():
    st.title("Interactive Probability Chart")

    st.write("Probability of a prize win after \(n\) times.")

    p = st.number_input("Enter the probability of winning per try (as a percentage)", min_value=0.0, max_value=100.0, value=1.2) / 100
    expected_tries = 1 / p if p > 0 else 0
    st.write(f"Expected number of tries to win a prize: {expected_tries:.2f}")

    max_tries = st.slider("Select the maximum number of tries", 1, 1000, 200)

    n_tries = np.arange(1, max_tries + 1)
    probabilities = 1 - (1 - p) ** n_tries

    fig = go.Figure(data=go.Scatter(x=n_tries, y=probabilities, mode='lines+markers',
                                line=dict(color='red')))

    fig.update_layout(
        title='Probability of Winning At Least One Prize in N Tries',
        xaxis_title='Number of Tries',
        yaxis_title='Probability',
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
