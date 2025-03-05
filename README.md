# Sell Target Forward Derivatives Simulation

## Overview

This Streamlit application simulates the risk dynamics of sell target forward derivatives, focusing on the case study of Aracruz Celulose during the 2008 financial crisis. The app serves as an educational tool for postgraduate finance students to understand how these complex derivatives work and the potential financial exposure they can create when market conditions change rapidly.

## Features

The application consists of five main sections:

1. **Introduction**: Explains the structure and characteristics of sell target forward derivatives
2. **Sell Target Forward Simulator**: Interactive tool to explore the mechanics of these derivatives
3. **Market Scenario Analysis**: Analyze different exchange rate scenarios and their impact
4. **Risk Management Insights**: Examines the line between hedging and speculation, governance frameworks, and optimal hedging strategies
5. **Aracruz Case Study**: Detailed analysis of the Aracruz Celulose derivatives disaster

## Requirements

To run this application, you'll need:

```
streamlit>=1.28.0
pandas>=1.5.3
numpy>=1.24.3
matplotlib>=3.7.1
plotly>=5.18.0
```

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Detailed Description

### Introduction Section
Provides a clear explanation of sell target forward derivatives, their structure, and why companies used them before the 2008 financial crisis. Visual aids illustrate the risk profile and structure of these instruments.

### Sell Target Forward Simulator
This interactive simulator allows users to adjust:
- Notional value
- Initial exchange rate
- Strike price
- Contract duration
- Current exchange rate
- Months elapsed

The simulator calculates potential losses and visualizes them in real-time, illustrating the asymmetric risk profile of these instruments.

### Market Scenario Analysis
Analyze four different exchange rate scenarios:
- Gradual Change
- Sudden Shock
- Typical Pre-2008 Pattern
- 2008 Crisis Pattern

Interactive visualizations show how these scenarios impact monthly and cumulative losses.

### Risk Management Insights
This section explores:
- The blurred line between hedging and speculation
- Risk governance frameworks
- Optimal hedging analysis using the Bodnar and Marston (2001) model

Interactive tools allow users to calculate optimal hedge ratios and compare them with actual hedge positions.

### Aracruz Case Study
A comprehensive analysis of the Aracruz Celulose case:
- Company overview before the crisis
- Timeline of events
- Derivative exposure analysis
- Exchange rate impact
- Financial consequences
- Key lessons and discussion questions

## Educational Use

This app is designed for educational purposes in postgraduate finance courses, particularly those focusing on derivatives, risk management, and financial crises. It includes:

- Interactive simulations
- Visualization tools
- Theoretical frameworks
- Case study analysis
- Discussion prompts for classroom use

## Credits

This application is based on research by Zeidan, R., & Rodrigues, B. (2013), "The failure of risk management for nonfinancial companies in the context of the financial crisis: lessons from Aracruz Celulose and hedging with derivatives," published in Applied Financial Economics, 23(3), 241-250.

## License

[MIT License]
