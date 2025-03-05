import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import math

# Set page configuration
st.set_page_config(
    page_title="Sell Target Forward Derivatives Simulation",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better formatting
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff4b4b;
    }
    .info-box {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4B8BF5;
        margin-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .katex {
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("Sell Target Forward Derivatives Simulation")
st.markdown("""
<div class="info-box">
<h3>The 2008 Case of Aracruz Celulose</h3>
<p>This application simulates the risk dynamics of sell target forward derivatives, which contributed to Aracruz Celulose's $2.13 billion loss during the 2008 financial crisis. The app allows you to explore how these complex derivatives work and how they can lead to significant financial exposure when market conditions change rapidly.</p>
</div>
""", unsafe_allow_html=True)

# App navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to:",
    ["Introduction", "Sell Target Forward Simulator", "Market Scenario Analysis", "Risk Management Insights", "Aracruz Case Study"]
)

# Define a function to calculate sell target forward losses
def calculate_stf_losses(notional_value, initial_rate, current_rate, strike_price, months_remaining):
    """
    Calculate losses from a sell target forward contract.
    
    Parameters:
    notional_value (float): Notional value of the contract in USD
    initial_rate (float): Initial exchange rate (BRL/USD)
    current_rate (float): Current exchange rate (BRL/USD)
    strike_price (float): Strike price agreed in the contract (BRL/USD)
    months_remaining (int): Number of months remaining in the contract
    
    Returns:
    float: Calculated loss in USD
    """
    # As per the paper (p. 245): l = n·2t(X-S)
    # Where:
    # l = amount of losses
    # n = notional value of the contract
    # X = strike exchange-rate
    # S = actual exchange-rate
    # t = number of months left in the contract
    # 2 is due to the double effect from the derivative as it's composed of an NDF and an exchange-rate option
    
    if current_rate <= strike_price:
        return 0  # No loss if current rate is above strike price
    
    loss_brl = notional_value * 2 * months_remaining * (strike_price - current_rate)
    loss_usd = loss_brl / current_rate
    
    return loss_usd

# Define a function to calculate percentage loss
def calculate_percentage_loss(current_rate, strike_price, months_remaining):
    """
    Calculate percentage loss in USD due to changes in exchange rate.
    
    Parameters:
    current_rate (float): Current exchange rate (BRL/USD)
    strike_price (float): Strike price agreed in the contract (BRL/USD)
    months_remaining (int): Number of months remaining in the contract
    
    Returns:
    float: Percentage loss relative to notional value
    """
    # As per the paper (p. 245): Dp = 2t(X-S)*100/S
    # Where:
    # Dp = percentage loss in USD
    # X = strike exchange-rate
    # S = actual exchange-rate
    # t = number of months left in the contract
    
    if current_rate <= strike_price:
        return 0  # No loss if current rate is above strike price
    
    percentage_loss = 2 * months_remaining * (strike_price - current_rate) * 100 / current_rate
    
    return percentage_loss

# Section 1: Introduction
if section == "Introduction":
    st.header("Understanding Sell Target Forward Derivatives")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### What is a Sell Target Forward?
        
        A sell target forward is a structured derivative that combines:
        
        1. **Short position in a Non-Deliverable Forward (NDF)**: An agreement to sell a specified amount of foreign currency at a predetermined rate.
        
        2. **Short position in exchange-rate options**: The seller (the company) sells options on the exchange rate, receiving a premium that allows them to obtain better FX rates than the market.
        
        The contract typically runs for a year with monthly settlements that bring the value of the whole contract to the present. This is important because it's the source of the major financial risk implicit in the contract.
        
        ### Key Features of Sell Target Forwards
        
        - **Monthly Settlement**: The contract settles monthly over its one-year duration
        - **Unlimited Downside**: There is no limit to how much the company can lose
        - **Limited Upside**: There is a ceiling on potential profits
        - **Leverage Effect**: The potential loss can be several times the notional value of the contract
        - **Double Exposure**: Loss calculations involve a factor of 2 due to the combined effect of the NDF and options components
        """)
        
        st.markdown("""
        ### Why Companies Used These Derivatives
        
        Before the 2008 financial crisis, many companies in Brazil (like Aracruz) used these instruments because:
        
        - The Brazilian Real had been appreciating against the US Dollar for years
        - Export-oriented companies were seeing declining revenues in local currency terms
        - These derivatives offered better exchange rates than conventional hedging instruments
        - Companies were effectively speculating that the appreciation trend would continue
        """)
    
    with col2:
        # Simple diagram showing the structure of a sell target forward
        st.markdown("### Structure of a Sell Target Forward")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        
        # Draw a rectangle for the contract
        rect = plt.Rectangle((0.1, 0.3), 0.8, 0.4, fill=True, color='lightblue', alpha=0.3)
        ax.add_patch(rect)
        
        # Add labels
        ax.text(0.5, 0.8, 'Sell Target Forward Contract', ha='center', va='center', fontsize=14, fontweight='bold')
        ax.text(0.3, 0.55, 'Short Position\nin NDF', ha='center', va='center', fontsize=12)
        ax.text(0.7, 0.55, 'Short Position in\nExchange-Rate Options', ha='center', va='center', fontsize=12)
        ax.text(0.5, 0.4, '+', ha='center', va='center', fontsize=18, fontweight='bold')
        ax.text(0.5, 0.2, 'Monthly Settlement Over 12 Months', ha='center', va='center', fontsize=12, style='italic')
        
        st.pyplot(fig)
        
        # Add a visual representation of the risk profile
        st.markdown("### Risk Profile")
        
        # Create data for the plot
        exchange_rates = np.linspace(1.4, 2.4, 100)
        strike_price = 1.65
        months = 12
        
        # Calculate percentage loss for each exchange rate
        losses = [calculate_percentage_loss(rate, strike_price, months) for rate in exchange_rates]
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(exchange_rates, losses, 'r-', linewidth=2)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=strike_price, color='green', linestyle='--', label=f'Strike Price: {strike_price}')
        ax.set_xlabel('Exchange Rate (BRL/USD)')
        ax.set_ylabel('Percentage Loss on Notional Value (%)')
        ax.set_title('Risk Profile of Sell Target Forward')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Highlight the risk area
        ax.fill_between(exchange_rates, losses, 0, where=(exchange_rates < strike_price), 
                        color='red', alpha=0.2, label='Loss Zone')
        
        st.pyplot(fig)

# Section 2: Sell Target Forward Simulator
elif section == "Sell Target Forward Simulator":
    st.header("Sell Target Forward Simulator")
    
    st.markdown("""
    <div class="info-box">
    <p>This simulator allows you to explore the mechanics of a sell target forward derivative contract. Adjust the parameters below to see how different market conditions and contract terms affect potential gains or losses.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Contract Parameters")
        
        # Contract parameters
        notional_value = st.number_input("Notional Value (USD millions)", min_value=1.0, max_value=5000.0, value=15.0, step=5.0)
        notional_value_millions = notional_value  # For display purposes
        notional_value = notional_value * 1_000_000  # Convert to actual value for calculations
        
        initial_rate = st.number_input("Initial Exchange Rate (BRL/USD)", min_value=1.0, max_value=3.0, value=1.60, step=0.01)
        strike_price = st.number_input("Strike Price (BRL/USD)", min_value=1.0, max_value=3.0, value=1.65, step=0.01)
        contract_duration = st.slider("Contract Duration (months)", min_value=1, max_value=12, value=12)
        
    with col2:
        st.subheader("Market Scenario")
        
        # Market scenario
        st.markdown("#### Simulate an Exchange Rate Shock")
        current_rate = st.slider("Current Exchange Rate (BRL/USD)", min_value=1.0, max_value=3.0, value=1.60, step=0.01)
        months_elapsed = st.slider("Months Elapsed Since Contract Start", min_value=0, max_value=contract_duration, value=0)
        months_remaining = contract_duration - months_elapsed
        
        # Display the change in exchange rate as a percentage
        if current_rate != initial_rate:
            pct_change = ((current_rate - initial_rate) / initial_rate) * 100
            change_direction = "depreciation" if pct_change > 0 else "appreciation"
            st.markdown(f"**Exchange Rate Change**: {abs(pct_change):.2f}% {change_direction} of BRL against USD")
    
    # Calculate the loss
    loss_usd = calculate_stf_losses(notional_value, initial_rate, current_rate, strike_price, months_remaining)
    percentage_loss = calculate_percentage_loss(current_rate, strike_price, months_remaining)
    
    # Display results
    st.header("Simulation Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Format the loss for display
        if loss_usd == 0:
            st.metric("Loss (USD)", "$0", "No Loss")
        else:
            st.metric("Loss (USD)", f"${loss_usd/1_000_000:.2f} million", f"-{loss_usd/notional_value*100:.2f}% of notional")
    
    with col2:
        # Show the formula used
        formula_text = "l = n × 2t × (X - S)"
        if current_rate > strike_price:
            calc_text = f"${notional_value_millions:.1f}M × 2 × {months_remaining} × ({strike_price:.2f} - {current_rate:.2f})"
            st.metric("Formula", formula_text, calc_text)
        else:
            st.metric("Formula", formula_text, "No Loss (S <= X)")
    
    with col3:
        # Express loss as a multiple of the notional value
        if loss_usd < 0:
            multiple = loss_usd / notional_value
            st.metric("Loss Multiple", f"{multiple:.2f}x", f"{multiple:.2f} times the notional value")
        else:
            st.metric("Loss Multiple", "0x", "No loss incurred")
    
    # Visualization of loss vs exchange rate
    st.subheader("Loss Profile Across Exchange Rates")
    
    # Generate exchange rate values around the current one
    exchange_rates = np.linspace(max(1.0, current_rate * 0.7), current_rate * 1.3, 100)
    
    # Calculate losses for each exchange rate
    losses = [calculate_stf_losses(notional_value, initial_rate, rate, strike_price, months_remaining) / 1_000_000 for rate in exchange_rates]
    percentage_losses = [calculate_percentage_loss(rate, strike_price, months_remaining) for rate in exchange_rates]
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Loss Amount (USD)", "Percentage Loss"])
    
    with tab1:
        fig = go.Figure()
        
        # Add the loss curve
        fig.add_trace(go.Scatter(
            x=exchange_rates,
            y=losses,
            mode='lines',
            name='Loss (USD millions)',
            line=dict(color='red', width=3)
        ))
        
        # Mark the strike price
        fig.add_vline(x=strike_price, line_dash="dash", line_color="green",
                     annotation_text=f"Strike Price: {strike_price}", annotation_position="top right")
        
        # Mark the current exchange rate
        fig.add_vline(x=current_rate, line_dash="dot", line_color="blue",
                     annotation_text=f"Current Rate: {current_rate}", annotation_position="top left")
        
        # Enhance the layout
        fig.update_layout(
            title="Potential Loss vs Exchange Rate",
            xaxis_title="Exchange Rate (BRL/USD)",
            yaxis_title="Loss (USD millions)",
            hovermode="x unified",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = go.Figure()
        
        # Add the percentage loss curve
        fig.add_trace(go.Scatter(
            x=exchange_rates,
            y=percentage_losses,
            mode='lines',
            name='Percentage Loss',
            line=dict(color='red', width=3)
        ))
        
        # Mark the strike price
        fig.add_vline(x=strike_price, line_dash="dash", line_color="green",
                     annotation_text=f"Strike Price: {strike_price}", annotation_position="top right")
        
        # Mark the current exchange rate
        fig.add_vline(x=current_rate, line_dash="dot", line_color="blue",
                     annotation_text=f"Current Rate: {current_rate}", annotation_position="top left")
        
        # Enhance the layout
        fig.update_layout(
            title="Percentage Loss vs Exchange Rate",
            xaxis_title="Exchange Rate (BRL/USD)",
            yaxis_title="Percentage Loss on Notional Value (%)",
            hovermode="x unified",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Explanation of the results
    st.markdown("""
    ### Understanding the Results
    
    #### Key Insights:
    
    1. **Loss Calculation**: The loss is calculated as `notional_value × 2 × months_remaining × (strike_price - current_rate)`. The factor of 2 represents the double exposure from the combined NDF and option components.
    
    2. **Asymmetric Risk Profile**: The profit is limited to the premium received on the options, but the loss potential is unlimited if the exchange rate drops significantly.
    
    3. **Time Factor**: The losses are multiplied by the remaining months in the contract. The earlier a negative shock happens in the contract lifecycle, the larger the potential loss.
    
    4. **Leverage Effect**: The structure of sell target forwards can lead to losses that are several times the notional value of the contract.
    """)
    
    # Show a warning if the loss is substantial
    if percentage_loss > 50:
        st.warning(f"""
        **Warning: High Risk Exposure**
        
        The current scenario shows a loss of {percentage_loss:.2f}% of the notional value. This level of exposure would be considered extremely high and potentially threatening to a company's financial stability.
        
        In the Aracruz case, the company faced losses of US$2.13 billion, which was 3.7 times greater than their annual EBIT and represented 30% of their market capitalization.
        """)

# Section 3: Market Scenario Analysis
elif section == "Market Scenario Analysis":
    st.header("Market Scenario Analysis")
    
    st.markdown("""
    <div class="info-box">
    <p>This section allows you to explore how different market scenarios impact the performance of sell target forward contracts. You can analyze the effect of gradual or sudden changes in exchange rates over time.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contract parameters
    col1, col2 = st.columns(2)
    
    with col1:
        # Define the contract parameters
        notional_value = st.number_input("Notional Value (USD millions)", min_value=1.0, max_value=5000.0, value=15.0, step=5.0)
        notional_value_millions = notional_value  # For display purposes
        notional_value = notional_value * 1_000_000  # Convert to actual value for calculations
        
        strike_price = st.number_input("Strike Price (BRL/USD)", min_value=1.0, max_value=3.0, value=1.65, step=0.01)
        
    with col2:
        # Define the market scenario
        initial_rate = st.number_input("Initial Exchange Rate (BRL/USD)", min_value=1.0, max_value=3.0, value=1.60, step=0.01)
        final_rate = st.number_input("Final Exchange Rate (BRL/USD)", min_value=1.0, max_value=3.0, value=2.0, step=0.01)
    
    # Scenario type selection
    scenario_type = st.radio(
        "Select scenario type:",
        ["Gradual Change", "Sudden Shock", "Typical Pre-2008 Pattern", "2008 Crisis Pattern"]
    )
    
    # Generate exchange rate data for each month based on the scenario
    months = list(range(1, 13))
    
    if scenario_type == "Gradual Change":
        # Linear change from initial to final rate
        exchange_rates = [initial_rate + (final_rate - initial_rate) * (i-1) / 11 for i in months]
        scenario_description = """
        In this scenario, the exchange rate changes gradually from the initial to the final rate over the 12-month contract period.
        This represents a steady market movement without sudden shocks.
        """
    
    elif scenario_type == "Sudden Shock":
        # Sudden change at a specific month
        shock_month = st.slider("Month of Shock", min_value=1, max_value=12, value=6)
        exchange_rates = [initial_rate if i < shock_month else final_rate for i in months]
        scenario_description = f"""
        This scenario simulates a sudden shock in month {shock_month}, where the exchange rate jumps from {initial_rate} to {final_rate}.
        Such shocks can occur during financial crises or following unexpected economic or political events.
        """
    
    elif scenario_type == "Typical Pre-2008 Pattern":
        # Appreciation of BRL (decreasing BRL/USD exchange rate)
        start_rate = 2.2
        end_rate = 1.6
        exchange_rates = [start_rate - (start_rate - end_rate) * (i-1) / 11 for i in months]
        scenario_description = """
        This scenario simulates the typical pattern observed in Brazil before the 2008 financial crisis,
        where the Brazilian Real (BRL) was steadily appreciating against the US Dollar (USD).
        This trend led many export-oriented companies to use sell target forwards to improve their revenue in local currency.
        """
    
    elif scenario_type == "2008 Crisis Pattern":
        # Stable or appreciating BRL followed by sudden depreciation
        pre_crisis_months = 8
        pre_crisis_rates = [initial_rate - 0.02 * (i-1) for i in range(1, pre_crisis_months + 1)]
        crisis_rates = [initial_rate + (final_rate - initial_rate) * (i-pre_crisis_months) / (12-pre_crisis_months) 
                      for i in range(pre_crisis_months + 1, 13)]
        exchange_rates = pre_crisis_rates + crisis_rates
        scenario_description = """
        This scenario recreates the pattern observed during the 2008 financial crisis:
        1. A period of stability or slight appreciation of the BRL against the USD
        2. Followed by a sudden and sharp depreciation as the crisis hit emerging markets
        This pattern caught many companies off guard, magnifying their losses on derivative positions.
        """
    
    # Display the scenario description
    st.markdown(f"""
    ### Scenario Description
    
    {scenario_description}
    """)
    
    # Calculate monthly losses
    monthly_losses_usd = []
    cumulative_losses_usd = 0
    
    for i, rate in enumerate(exchange_rates):
        months_remaining = 12 - i
        monthly_loss = calculate_stf_losses(notional_value, initial_rate, rate, strike_price, 1)
        monthly_losses_usd.append(monthly_loss / 1_000_000)  # Convert to millions for display
        cumulative_losses_usd += monthly_loss
    
    cumulative_losses_usd_millions = cumulative_losses_usd / 1_000_000
    
    # Create a DataFrame for the data
    df = pd.DataFrame({
        'Month': months,
        'Exchange Rate (BRL/USD)': exchange_rates,
        'Monthly Loss (USD millions)': monthly_losses_usd,
        'Cumulative Loss (USD millions)': np.cumsum(monthly_losses_usd)
    })
    
    # Display the results
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Loss", f"${cumulative_losses_usd_millions:.2f} million", 
                 f"{cumulative_losses_usd/notional_value*100:.2f}% of notional")
    
    with col2:
        # Calculate maximum monthly loss
        max_monthly_loss = min(monthly_losses_usd)
        max_loss_month = monthly_losses_usd.index(max_monthly_loss) + 1
        
        st.metric("Maximum Monthly Loss", f"${max_monthly_loss:.2f} million", 
                 f"Month {max_loss_month}")
    
    # Create visualization tabs
    tab1, tab2, tab3 = st.tabs(["Exchange Rate Path", "Monthly Losses", "Cumulative Losses"])
    
    with tab1:
        fig = px.line(
            df, x='Month', y='Exchange Rate (BRL/USD)', 
            title='Exchange Rate Path Over Contract Duration',
            markers=True
        )
        
        # Add the strike price line
        fig.add_hline(y=strike_price, line_dash="dash", line_color="green", 
                     annotation_text="Strike Price", annotation_position="right")
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.bar(
            df, x='Month', y='Monthly Loss (USD millions)',
            title='Monthly Losses Over Contract Duration',
            color='Monthly Loss (USD millions)', color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.line(
            df, x='Month', y='Cumulative Loss (USD millions)',
            title='Cumulative Losses Over Contract Duration',
            markers=True
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Display the data table
    st.subheader("Monthly Data")
    st.dataframe(df.style.format({
        'Exchange Rate (BRL/USD)': '{:.4f}',
        'Monthly Loss (USD millions)': '{:.2f}',
        'Cumulative Loss (USD millions)': '{:.2f}'
    }))
    
    # Analysis and interpretation
    st.subheader("Analysis and Interpretation")
    
    if scenario_type == "Gradual Change":
        st.markdown("""
        ### Insights from Gradual Change Scenario
        
        - **Predictable Progression**: A gradual change allows companies time to adjust their strategies and possibly unwind positions.
        - **Accumulated Impact**: Even small monthly changes can accumulate to significant total losses over the contract period.
        - **Management Opportunity**: With gradual changes, risk management has more opportunity to intervene before losses become catastrophic.
        """)
    
    elif scenario_type == "Sudden Shock":
        st.markdown(f"""
        ### Insights from Sudden Shock Scenario
        
        - **Limited Reaction Time**: A sudden shock leaves little time for risk management to respond.
        - **Exposure Magnitude**: The earlier the shock occurs in the contract lifecycle, the greater the potential loss due to more remaining months.
        - **Contract Structure Impact**: The "double exposure" feature of sell target forwards (factor of 2 in the formula) magnifies the impact of sudden shocks.
        
        The shock in month {shock_month} resulted in immediate losses of ${monthly_losses_usd[shock_month-1]:.2f} million, demonstrating how quickly these instruments can generate significant losses.
        """)
    
    elif scenario_type == "Typical Pre-2008 Pattern":
        st.markdown("""
        ### Insights from Pre-2008 Pattern
        
        - **False Security**: The appreciating BRL created an environment where these derivatives appeared to be profitable.
        - **Hidden Risks**: The seemingly favorable trend masked the enormous potential downside risks.
        - **Strategic Misalignment**: Many companies, including Aracruz, increased their exposure to these instruments based on the belief that the trend would continue.
        
        This pattern explains why many Brazilian companies were willing to enter into sell target forward contracts, as they appeared to be beneficial in the prevailing market conditions.
        """)
    
    elif scenario_type == "2008 Crisis Pattern":
        st.markdown("""
        ### Insights from 2008 Crisis Pattern
        
        - **Devastating Reversal**: The sudden reversal of the long-standing trend caught companies unprepared.
        - **Magnified Impact**: The structure of sell target forwards turned a market correction into catastrophic losses.
        - **Systemic Effect**: Multiple companies facing similar losses created systemic pressure on the Brazilian financial system.
        
        This scenario closely mimics what happened to Aracruz and other companies during the 2008 crisis, where years of strategy based on an appreciating BRL were undone in a matter of weeks.
        """)
    
    # Risk management lessons
    st.markdown("""
    ### Key Risk Management Lessons
    
    1. **Stress Testing**: Companies should regularly stress test their derivative positions against extreme market movements.
    
    2. **Transparency**: The full risk exposure of complex derivatives must be clearly understood and communicated to senior management and the board.
    
    3. **Position Limits**: Clear limits on maximum exposure should be established and enforced.
    
    4. **Diversification**: Avoid concentration in a single type of derivative instrument.
    
    5. **Governance**: Strong risk governance is needed to prevent speculative positions disguised as hedging.
    """)

# Section 4: Risk Management Insights
elif section == "Risk Management Insights":
    st.header("Risk Management Insights")
    
    st.markdown("""
    <div class="info-box">
    <p>This section explores the risk management aspects of derivatives use, focusing on the lessons learned from the Aracruz case and how companies can improve their risk management practices.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use tabs for different aspects of risk management
    tab1, tab2, tab3 = st.tabs(["Hedging vs. Speculation", "Risk Governance", "Optimal Hedging Analysis"])
    
    with tab1:
        st.subheader("The Blurred Line Between Hedging and Speculation")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            ### When Does Hedging Become Speculation?
            
            The Aracruz case demonstrates how the line between hedging and speculation can become blurred. The company began with legitimate hedging needs as an exporter but gradually moved toward speculative positions.
            
            #### Legitimate Hedging:
            - Aims to reduce existing business risk exposure
            - Position size corresponds to actual business exposure
            - Derivatives match the timeframe of the underlying business activity
            - Limited downside risk relative to the exposure being hedged
            
            #### Signs of Speculation:
            - Position size exceeds the underlying business exposure
            - Complex structures with leverage or multiplier effects
            - Contracts with asymmetric risk-reward profiles (limited upside, unlimited downside)
            - Focus on enhancing returns rather than reducing risk
            - Positions based on market directional views
            
            ### Case Analysis
            
            Aracruz started with conventional hedging but shifted to increasingly complex instruments with higher risk profiles. By 2008, they had:
            
            1. Increased their hedged position from approximately USD 1 billion to over USD 6 billion
            2. Adopted complex OTC derivatives with embedded leverage
            3. Positioned themselves based on a directional view of continued BRL appreciation
            4. Created exposure that was several times their optimal hedge ratio
            
            This transformation from hedger to speculator happened gradually, making it difficult for governance mechanisms to identify and address the increasing risk.
            """)
        
        with col2:
            # Create visual representation of the hedging-speculation spectrum
            st.markdown("### Hedging-Speculation Spectrum")
            
            # Create a visualization of the spectrum
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Create the gradient bar
            gradient = np.linspace(0, 1, 100).reshape(1, -1)
            ax.imshow(gradient, cmap='RdYlGn_r', aspect='auto', extent=[0, 10, 0, 1])
            
            # Add markers for different positions
            positions = [
                (1, "Pure Hedging"),
                (3, "Traditional FWD/FUT"),
                (5, "Vanilla Options"),
                (7, "Exotic Derivatives"),
                (9, "Pure Speculation")
            ]
            
            for x, label in positions:
                ax.plot(x, 0.5, 'ko', markersize=10)
                ax.text(x, 0.2, label, ha='center', fontsize=9)
            
            # Mark Aracruz's position
            ax.plot(7.5, 0.5, 'ro', markersize=15)
            ax.text(5, 0.8, "Aracruz Position\nwith Sell Target Forwards", ha='center', fontsize=10, color='red')
            
            # Format the chart
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Hedging-Speculation Spectrum")
            
            st.pyplot(fig)
            
            # Risk-reward profile
            st.markdown("### Risk-Reward Profile Comparison")
            
            instruments = ["Spot Market", "Forward Contract", "Long Option", "Sell Target FWD"]
            downside_risk = [5, 3, 1, 10]
            upside_potential = [10, 3, 10, 2]
            
            risk_df = pd.DataFrame({
                'Instrument': instruments,
                'Downside Risk': downside_risk,
                'Upside Potential': upside_potential
            })
            
            fig = px.scatter(
                risk_df, x='Downside Risk', y='Upside Potential', 
                text='Instrument', size=[10, 10, 10, 15],
                color='Instrument', 
                color_discrete_map={
                    'Sell Target FWD': 'red',
                    'Forward Contract': 'blue',
                    'Long Option': 'green',
                    'Spot Market': 'orange'
                }
            )
            
            fig.update_traces(textposition='top center')
            # Move the legend below the graph
            fig.update_layout(
                legend=dict(
                    orientation="h",  # Horizontal layout
                    yanchor="top",  # Anchor the legend to the top
                    y=-0.2,  # Push the legend below the plot
                    xanchor="center",  # Center the legend horizontally
                    x=0.5  # Place it in the middle
                )
            )            

            st.plotly_chart(fig, use_container_width=True)
            
            
    with tab2:
        st.subheader("Risk Governance and Management Framework")
        
        st.markdown("""
        ### Elements of Effective Derivatives Risk Management
        
        The Aracruz case highlights several critical failings in risk governance that allowed speculative positions to build up unchecked. An effective risk management framework for derivatives should include:
        """)
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Policy and Oversight
            
            - **Board-Level Oversight**: Clear board reporting on derivatives positions and their risks
            - **Risk Policy**: Well-defined policy that distinguishes between hedging and speculative activities
            - **Exposure Limits**: Explicit limits on maximum exposure, notional amounts, and potential losses
            - **Product Approval**: Formal process for approving new derivative instruments
            """)
            
            st.markdown("""
            #### Risk Measurement
            
            - **Scenario Analysis**: Regular testing of positions against various market scenarios
            - **Stress Testing**: Extreme scenario analysis to quantify worst-case losses
            - **Value-at-Risk (VaR)**: Quantitative measure of potential losses over specified time horizons
            - **Risk-Adjusted Performance**: Evaluation of positions on a risk-adjusted basis
            """)
        
        with col2:
            st.markdown("""
            #### Operational Controls
            
            - **Segregation of Duties**: Separation between trading, risk monitoring, and accounting functions
            - **Position Monitoring**: Regular, independent monitoring of positions and risks
            - **Mark-to-Market**: Daily valuation of positions by independent personnel
            - **Limit Monitoring**: Automated monitoring of position limits and alerts
            """)
            
            st.markdown("""
            #### Transparency and Reporting
            
            - **Management Reporting**: Regular, comprehensive reporting to senior management
            - **Disclosure**: Appropriate disclosure of risks in financial statements
            - **Risk Metrics**: Clear communication of risk metrics that capture the true risk profile
            - **Escalation Procedures**: Well-defined processes for limit breaches and exceptions
            """)
        
        # Aracruz's risk management failings
        st.subheader("What Went Wrong at Aracruz?")
        
        with st.expander("Governance Failings"):
            st.markdown("""
            - **Lack of Board Oversight**: The treasury department was responsible for both proposing and executing risk management strategies
            - **Limited Understanding**: Complex derivatives were not fully understood by decision-makers
            - **Inadequate Limits**: No clear limits on the maximum exposure or potential losses
            - **Poor Disclosure**: Risk exposure was not transparently communicated
            """)
        
        with st.expander("Risk Assessment Failings"):
            st.markdown("""
            - **Underestimation of Risk**: The true risk profile of sell target forwards was not accurately assessed
            - **Insufficient Stress Testing**: Extreme market scenarios were not adequately tested
            - **Directional Bias**: Strategies assumed continued BRL appreciation without considering reversals
            - **Correlation Risks**: Failed to account for how a global crisis could impact both operations and hedge positions
            """)
        
        with st.expander("Operational Failings"):
            st.markdown("""
            - **Weak Controls**: Insufficient independent review of derivative positions
            - **Complexity Management**: Inability to properly manage and monitor complex OTC derivatives
            - **Risk Aggregation**: Failed to aggregate risks across all derivative instruments
            - **Rapid Response**: No effective mechanism to rapidly reduce exposure when market conditions changed
            """)
        
        # Risk governance checklist
        st.subheader("Risk Governance Checklist")
        
        # Create an interactive checklist
        st.markdown("Use this checklist to evaluate your organization's derivatives risk management:")
        
        governance_items = [
            "Board-approved policy for derivatives use with clear objectives",
            "Distinction between hedging and speculative activities",
            "Pre-defined exposure limits as a percentage of key financial metrics",
            "Regular stress testing of positions with extreme scenarios",
            "Independent risk monitoring separate from trading function",
            "Regular reporting of positions, risks, and limit utilization",
            "Formal approval process for new derivative instruments",
            "Clear understanding of all derivative structures at senior management level",
            "Regular review of hedging effectiveness",
            "Contingency plans for market disruptions"
        ]
        
        for i, item in enumerate(governance_items):
            st.checkbox(item, key=f"governance_{i}")
            
            
    with tab3:
        st.subheader("Optimal Hedging Analysis")
        
        st.markdown("""
        ### Determining the Optimal Hedge Ratio
        
        The optimal hedge ratio helps companies determine how much of their exposure should be hedged. For companies like Aracruz with foreign exchange exposure, this is critical to ensure they're not under-hedged or over-hedged.
        
        This section explores the Bodnar and Marston (2001) model referenced in the paper to calculate the optimal hedge ratio for a company with foreign currency exposure.
        """)
        
        # Input parameters for the optimal hedge calculation
        st.markdown("#### Enter Company Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            h1 = st.slider("Foreign Currency Revenue (% of Total Revenue)", 0.0, 100.0, 95.0) / 100
            h2 = st.slider("Foreign Currency Costs (% of Total Costs)", 0.0, 100.0, 25.0) / 100
        
        with col2:
            r = st.slider("Profit Margin (EBIT/Revenue %)", 0.0, 50.0, 25.0) / 100
            ebit = st.number_input("EBIT (USD millions)", min_value=0.0, value=500.0, step=10.0)
            ebit_value = ebit * 1_000_000  # Convert to actual value for calculations
        
        # Calculate the optimal hedge ratio using the Bodnar and Marston model
        # δ = h₁ + (h₁ - h₂)(1/r - 1)
        delta = h1 + (h1 - h2) * (1/r - 1)
        optimal_hedge = delta * ebit_value
        
        # Display the results
        st.markdown("#### Optimal Hedge Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Optimal Hedge Ratio (δ)", f"{delta:.2f}")
        
        with col2:
            st.metric("Optimal Hedge Amount", f"${optimal_hedge/1_000_000:.2f} million")
        
        with col3:
            st.metric("As % of EBIT", f"{delta*100:.2f}%")
        
        # Formula explanation
        st.markdown("""
        #### Bodnar and Marston Model Explanation
        
        The model calculates the optimal hedge ratio (δ) as:
        
        **δ = h₁ + (h₁ - h₂)(1/r - 1)**
        
        Where:
        - **h₁** = Foreign currency revenue as a percentage of total revenue
        - **h₂** = Foreign currency costs as a percentage of total costs
        - **r** = Profit margin (EBIT/Revenue)
        
        The optimal hedge amount is then calculated by multiplying δ by the company's EBIT.
        """)
        
        # Sensitivity analysis
        st.subheader("Sensitivity Analysis")
        
        st.markdown("""
        The optimal hedge ratio is sensitive to changes in the company's financial structure. 
        This analysis shows how changes in profit margin affect the optimal hedge ratio.
        """)
        
        # Create data for sensitivity analysis
        profit_margins = np.linspace(0.05, 0.5, 100)  # 5% to 50%
        delta_values = [h1 + (h1 - h2) * (1/margin - 1) for margin in profit_margins]
        
        # Create the sensitivity plot
        fig = px.line(
            x=profit_margins * 100, y=delta_values,
            labels={'x': 'Profit Margin (%)', 'y': 'Optimal Hedge Ratio (δ)'},
            title='Sensitivity of Optimal Hedge Ratio to Profit Margin'
        )
        
        # Add a marker for the current profit margin
        fig.add_scatter(
            x=[r * 100], y=[delta],
            mode='markers',
            marker=dict(size=12, color='red'),
            name='Current Position'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("""
        #### Key Insights on Optimal Hedging
        
        1. **Inverse Relationship with Profitability**: As profit margins decrease, the optimal hedge ratio increases. This is because lower margins make the company more sensitive to exchange rate movements.
        
        2. **Revenue-Cost Gap**: The difference between foreign currency revenue and costs (h₁ - h₂) amplifies the impact of profitability changes on the optimal hedge ratio.
        
        3. **Over-Hedging Risk**: Companies may inadvertently over-hedge if they don't adjust their hedging strategy when profitability changes.
        
        4. **Warning Sign from Aracruz**: The paper shows that Aracruz's real hedge position in 2008 was approximately USD 6.3 billion, while their optimal hedge was only USD 1.3 billion - a clear sign of speculative positioning.
        """)
        
        # Compare with actual hedge
        st.subheader("Compare with Your Company's Actual Hedge")
        
        actual_hedge = st.number_input("Actual Hedged Amount (USD millions)", min_value=0.0, value=1000.0, step=100.0)
        actual_hedge_value = actual_hedge * 1_000_000
        
        # Calculate the ratio of actual to optimal hedge
        hedge_ratio = actual_hedge_value / optimal_hedge if optimal_hedge > 0 else 0
        
        # Categorize the hedging stance
        if hedge_ratio < 0.8:
            hedging_stance = "Under-hedged"
            stance_color = "orange"
        elif hedge_ratio <= 1.2:
            hedging_stance = "Appropriately hedged"
            stance_color = "green"
        elif hedge_ratio <= 2.0:
            hedging_stance = "Moderately over-hedged"
            stance_color = "yellow"
        else:
            hedging_stance = "Significantly over-hedged (potential speculation)"
            stance_color = "red"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Actual/Optimal Ratio", f"{hedge_ratio:.2f}x")
        
        with col2:
            st.markdown(f"<h3 style='color:{stance_color}'>{hedging_stance}</h3>", unsafe_allow_html=True)
        
        # Visualization of optimal vs actual hedge
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar([0, 1], [optimal_hedge/1_000_000, actual_hedge], width=0.6)
        
        # Color the bars based on the comparison
        bars[0].set_color('blue')
        if hedge_ratio < 0.8:
            bars[1].set_color('orange')
        elif hedge_ratio <= 1.2:
            bars[1].set_color('green')
        elif hedge_ratio <= 2.0:
            bars[1].set_color('yellow')
        else:
            bars[1].set_color('red')
        
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Optimal Hedge', 'Actual Hedge'])
        ax.set_ylabel('USD Millions')
        ax.set_title('Optimal vs. Actual Hedge Comparison')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'${height:.1f}M',
                    ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Hedging best practices
        st.markdown("""
        ### Hedging Best Practices
        
        1. **Regular Reassessment**: Recalculate the optimal hedge ratio when profit margins, revenue mix, or cost structure changes.
        
        2. **Partial Hedging**: Consider hedging less than 100% of the optimal amount to account for uncertainties.
        
        3. **Layered Approach**: Use a combination of different hedging instruments and maturities.
        
        4. **Simpler Instruments**: Prioritize simpler, more transparent derivatives over complex structures.
        
        5. **Risk Budget**: Establish a risk budget that limits the maximum potential loss from hedging activities.
        """)
        
        st.info("""
        **Educational Note**: The Bodnar and Marston model provides a useful framework, but it has limitations. It assumes constant cash flows and doesn't account for quantity risk or competition. More sophisticated models might be needed for companies with complex risk profiles.
        """)                    
    
    
# Section 5: Aracruz Case Study
elif section == "Aracruz Case Study":
    st.header("Aracruz Celulose: A Case Study in Derivatives Mismanagement")
    
    st.markdown("""
    <div class="info-box">
    <p>This section provides a detailed timeline and analysis of the Aracruz Celulose case, one of the most significant derivatives losses in corporate history.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Company overview
    st.subheader("Company Overview (Pre-Crisis)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Aracruz Celulose
        
        Aracruz was once Brazil's largest pulp producer and a global leader:
        
        - **Market Position**: Largest world producer of bleached eucalyptus pulp with 26% global market share
        - **Financial Strength**: Market capitalization of US$7.1 billion (July 2008)
        - **Revenue**: Net revenue of US$1.42 billion
        - **Credit Rating**: Investment grade ('BBB' flat rating by Moody's, S&P, and Fitch)
        - **Operations**: Self-sufficient in wood with 593,000 hectares of land and three production sites
        - **Export Orientation**: More than 95% of revenue came from exports
        - **Profitability**: Historical average of 50% EBITDA margin
        
        The company was known for good corporate governance:
        - First Brazilian company listed on NYSE (1992)
        - First Brazilian company to publish audited financial statements in English quarterly
        - Had a Board-approved financial policy accessible on the company's website
        - Part of the Dow Jones Sustainability Index
        """)
    
    with col2:
        # Financial metrics visualization
        metrics = {
            'Year': [2003, 2004, 2005, 2006, 2007, '2008 (Q2)'],
            'EBIT (US$M)': [423, 456, 442, 502, 571, 245],
            'Profit Margin (%)': [36.4, 31.3, 27.3, 24.5, 23.2, 13.9]
        }
        
        metrics_df = pd.DataFrame(metrics)
        
        fig = px.bar(
            metrics_df, x='Year', y='EBIT (US$M)',
            title='Aracruz Financial Performance (2003-2008)',
            text='EBIT (US$M)'
        )
        
        # Add profit margin as a line
        fig.add_scatter(
            x=metrics_df['Year'], 
            y=metrics_df['Profit Margin (%)'],
            mode='lines+markers',
            name='Profit Margin (%)',
            yaxis='y2'
        )
        
        # Update layout for dual axis
        fig.update_layout(
            yaxis2=dict(
                title='Profit Margin (%)',
                overlaying='y',
                side='right'
            ),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline of events
    st.subheader("Timeline of Events")

    # Use more specific dates and ensure they're in a format convertible to datetimes
    events = [
        {"date_start": "2003-01-01", "date_end": "2007-12-31", "event": "Brazilian Real (BRL) steadily appreciates against USD", "category": "Market"},
        {"date_start": "2003-01-01", "date_end": "2007-12-31", "event": "Aracruz begins increasing its hedging activity", "category": "Company"},
        {"date_start": "2008-01-01", "date_end": "2008-03-31", "event": "Aracruz starts using sell target forwards and exotic swaps", "category": "Company"},
        {"date_start": "2008-04-01", "date_end": "2008-06-30", "event": "Aracruz's exposure to derivatives jumps from ~US$1B to ~US$7B", "category": "Company"},
        {"date_start": "2008-09-15", "date_end": "2008-09-15", "event": "Lehman Brothers bankruptcy triggers global financial crisis", "category": "Market"},
        {"date_start": "2008-09-01", "date_end": "2008-09-30", "event": "BRL depreciates sharply against USD", "category": "Market"},
        {"date_start": "2008-09-25", "date_end": "2008-09-30", "event": "Aracruz announces losses from currency derivatives", "category": "Company"},
        {"date_start": "2008-10-03", "date_end": "2008-10-08", "event": "Aracruz announces total loss of US$1.95B (later amended to US$2.13B)", "category": "Company"},
        {"date_start": "2008-10-01", "date_end": "2008-10-31", "event": "Aracruz stock plunges from R$12 to less than R$1.5", "category": "Market"},
        {"date_start": "2008-11-01", "date_end": "2008-11-30", "event": "Brazilian stockholders sue Aracruz's former CFO", "category": "Legal"},
        {"date_start": "2008-11-15", "date_end": "2008-11-30", "event": "American stockholders join class action against the Board", "category": "Legal"},
        {"date_start": "2009-01-01", "date_end": "2009-03-31", "event": "Aracruz is acquired by Votorantim Papel e Celulose (VCP)", "category": "Company"},
        {"date_start": "2009-06-01", "date_end": "2009-06-30", "event": "Resulting company is renamed Fibria", "category": "Company"}
    ]

    timeline_df = pd.DataFrame(events)

    # Create a timeline visualization
    fig = px.timeline(
        timeline_df, 
        x_start="date_start", 
        x_end="date_end", 
        y="event",
        color="category",
        color_discrete_map={"Market": "blue", "Company": "red", "Legal": "green"},
        title="Aracruz Crisis Timeline"
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)    
    # Derivative exposure analysis
    st.subheader("Derivative Exposure Analysis")
    
    # Quarterly exposure data
    exposure_data = {
        'Quarter': ['Q4 2007', 'Q1 2008', 'Q2 2008', 'Q3 2008', 'Q4 2008'],
        'Liabilities (US$M)': [929, 929, 1110, 1578, 2888],
        'Assets (US$M)': [370, 403, 451, 418, 375],
        'Exchange-traded Derivatives (US$M)': [150, 270, 0, 538, 0],
        'Sell Target Forward (US$M)': [0, 0, 5280, 8640, 0],
        'Exotic Swap (US$M)': [0, 0, 600, 2400, 3600],
        'Other OTC Derivatives (US$M)': [334, 346, 559, 305, 215],
        'Effective Hedge (US$M)': [1043, 1143, 7098, 11967, 6329]
    }
    
    exposure_df = pd.DataFrame(exposure_data)
    
    # Visualization of exposure growth
    fig = px.bar(
        exposure_df, x='Quarter', y='Effective Hedge (US$M)',
        title='Aracruz Derivative Exposure Growth (2007-2008)',
        text='Effective Hedge (US$M)'
    )
    
    # Add a reference line for optimal hedge
    fig.add_hline(y=1300, line_dash="dash", line_color="green", 
                 annotation_text="Approximate Optimal Hedge", annotation_position="right")
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Breakdown of Q3 2008 exposure
    st.subheader("Breakdown of Q3 2008 Exposure (Peak)")
    
    q3_data = {
        'Component': ['Sell Target Forward', 'Exotic Swap', 'Exchange-traded Derivatives', 
                     'Other OTC Derivatives', 'Net Liabilities'],
        'Amount (US$M)': [8640, 2400, 538, 305, 1160],
        'Percentage': [72.2, 20.1, 4.5, 2.5, 0.7]
    }
    
    q3_df = pd.DataFrame(q3_data)
    
    fig = px.pie(
        q3_df, values='Amount (US$M)', names='Component',
        title='Components of Aracruz Q3 2008 Derivative Exposure (US$11.97B Total)'
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Exchange rate impact
    st.subheader("Impact of Exchange Rate Movements")
    
    # Create visualization of BRL/USD exchange rate
    exchange_data = {
        'Date': ['Jan 2008', 'Feb 2008', 'Mar 2008', 'Apr 2008', 'May 2008', 'Jun 2008', 
                'Jul 2008', 'Aug 2008', 'Sep 2008', 'Oct 2008', 'Nov 2008', 'Dec 2008'],
        'Rate': [1.77, 1.73, 1.75, 1.69, 1.63, 1.61, 1.57, 1.63, 1.91, 2.18, 2.33, 2.34]
    }
    
    fx_df = pd.DataFrame(exchange_data)
    
    fig = px.line(
        fx_df, x='Date', y='Rate',
        title='BRL/USD Exchange Rate (2008)',
        markers=True
    )
    
    # Add the strike price line
    fig.add_hline(y=1.65, line_dash="dash", line_color="red", 
                 annotation_text="Typical Strike Price", annotation_position="left")
    
    # Add annotations for key events
    fig.add_annotation(
        x='Sep 2008', y=1.91,
        text="Lehman Brothers Bankruptcy",
        showarrow=True,
        arrowhead=1
    )
    
    fig.add_annotation(
        x='Oct 2008', y=2.18,
        text="Aracruz Announces Losses",
        showarrow=True,
        arrowhead=1
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial impact analysis
    st.subheader("Financial Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock price impact
        stock_data = {
            'Date': ['Jan 2008', 'Feb 2008', 'Mar 2008', 'Apr 2008', 'May 2008', 'Jun 2008', 
                    'Jul 2008', 'Aug 2008', 'Sep 2008', 'Oct 2008', 'Nov 2008', 'Dec 2008'],
            'Price (BRL)': [12.2, 11.9, 11.7, 11.8, 11.9, 12.1, 12.0, 11.8, 8.2, 1.5, 1.4, 1.4]
        }
        
        stock_df = pd.DataFrame(stock_data)
        
        fig = px.line(
            stock_df, x='Date', y='Price (BRL)',
            title='Aracruz Stock Price (2008)',
            markers=True
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Loss vs financial metrics
        metrics_data = {
            'Metric': ['Derivative Loss', 'Annual EBIT (2007)', 'Market Cap (Jul 2008)'],
            'Amount (US$B)': [2.13, 0.57, 7.1],
            'Color': ['red', 'blue', 'green']
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        
        fig = px.bar(
            metrics_df, x='Metric', y='Amount (US$B)',
            title='Derivative Loss vs Financial Metrics',
            text='Amount (US$B)',
            color='Color',
            color_discrete_map={'red': 'red', 'blue': 'blue', 'green': 'green'}
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Key lessons from the case
    st.subheader("Key Lessons from the Aracruz Case")
    
    st.markdown("""
    ### 1. Hidden Risks in Complex Derivatives
    
    Sell target forwards had a deceptively simple structure but contained embedded leverage and unlimited downside risk. The true risk exposure was much larger than the notional value suggested.
    
    ### 2. Speculation Disguised as Hedging
    
    What began as a legitimate hedging program gradually transformed into speculative positions, with exposure far exceeding the company's optimal hedge needs.
    
    ### 3. Governance and Oversight Failures
    
    The treasury department had authority to both propose and execute risk management strategies without sufficient independent oversight, creating conflicts of interest.
    
    ### 4. Behavioral Finance Factors
    
    The paper suggests that behavioral issues such as hubris may have contributed to the excessive risk-taking. Years of successful hedging during BRL appreciation created overconfidence.
    
    ### 5. Directional Market Bias
    
    The strategy was predicated on a directional view of continued BRL appreciation, without adequate safeguards against a market reversal.
    
    ### 6. Crisis Amplification
    
    The structure of the derivatives, with their monthly settlements and double exposure effect, amplified the impact of market movements during the crisis.
    
    ### 7. Lack of Transparency
    
    The true extent of derivative exposure was not clearly communicated to stakeholders until after losses materialized.
    """)
    
    # Discussion questions
    st.subheader("Discussion Questions for Students")
    
    questions = [
        "How could Aracruz have better managed its foreign exchange risk without resorting to complex derivatives?",
        "What governance structures could have prevented the excessive risk-taking in Aracruz's treasury department?",
        "Why didn't market forces or external stakeholders (analysts, regulators, auditors) identify the risks earlier?",
        "How did the financial crisis expose weaknesses in Aracruz's risk management that might have otherwise remained hidden?",
        "What are the ethical considerations around using complex financial instruments when their risks may not be fully understood?",
        "How should companies balance the desire for favorable hedging rates with the additional risks of complex derivatives?",
        "What parallels exist between the Aracruz case and other derivatives disasters such as Metallgesellschaft?"
    ]
    
    for i, question in enumerate(questions):
        st.markdown(f"**Question {i+1}:** {question}")
    
    # Simulation exercise
    st.subheader("Class Simulation Exercise")
    
    st.markdown("""
    Use this app to conduct the following classroom simulation exercise:
    
    1. **Board Meeting Scenario**: Divide the class into groups representing:
       - Treasury Department
       - Risk Management Committee
       - Board of Directors
       - External Auditors
       - Shareholders
    
    2. **Decision Point**: Set the scenario to Q2 2008, just before the crisis hit, when the company had already increased its exposure.
    
    3. **Group Tasks**:
       - Treasury Department: Prepare a justification for the current derivatives strategy
       - Risk Management: Develop questions to assess the risk
       - Board: Prepare a risk oversight plan
       - Auditors: Develop disclosure recommendations
       - Shareholders: Prepare questions about the risk exposure
    
    4. **Role-Playing Discussion**: Conduct a simulated board meeting where each group presents their perspective
    
    5. **Post-Crisis Analysis**: After the simulation, use the app to show what actually happened and discuss what went wrong
    """)
    
    # Final conclusions
    st.subheader("Final Thoughts")
    
    st.markdown("""
    The Aracruz case provides a powerful reminder of how derivatives, when misused or misunderstood, can lead to catastrophic losses. The company's collapse from a market leader to an acquisition target within months demonstrates the importance of:
    
    1. **Proper Risk Management**: Understanding the true risk profile of all derivatives positions
    
    2. **Strong Governance**: Independent oversight of treasury activities
    
    3. **Appropriate Hedging**: Maintaining derivative exposures in line with underlying business needs
    
    4. **Stress Testing**: Regularly testing positions against extreme market scenarios
    
    5. **Transparency**: Clear communication of risks to all stakeholders
    
    As financial markets continue to evolve with increasingly complex instruments, the lessons from Aracruz remain highly relevant for corporate risk managers, board members, and finance professionals.
    """)
    
# Footer
st.divider()
st.caption("© 2025 Derivatives Study Case Teaching Tool | Developed for educational purposes")
st.caption("Prof. José Américo – Coppead")
