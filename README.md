
# Integrated Token Analysis Dashboard

This project provides a comprehensive dashboard for analyzing cryptocurrency tokens, combining historical price data with related Twitter activity.

## Features

1. Token Price Visualization
   - Interactive line chart displaying historical price data for selected tokens
   - Ability to select different tokens for analysis

2. Token Relationship Graph
   - Network graph showing relationships between the selected token and Twitter accounts mentioning it
   - Visual representation of token popularity among different Twitter users

3. Tweet Search and Display
   - Search functionality to find tweets mentioning specific tokens
   - Display of relevant tweets with details such as timestamp, favorite count, retweet count, and reply count
   - Option to filter tweets by specific authors

## Technical Stack

- Backend: Flask (Python)
- Frontend: HTML, JavaScript (likely using a charting library for visualizations)
- Database: SQL Server (for storing Twitter data)
- Data Processing: pandas, networkx
- Visualization: matplotlib (for generating the network graph)

## Setup and Installation

[Include steps for setting up the project, such as:]

1. Clone the repository
2. Install required Python packages: `pip install -r requirements.txt`
3. Set up SQL Server database and import Twitter data
4. Configure database connection in `integrate.py`
5. Run the Flask application: `python integrate.py`

## Usage

1. Access the dashboard through a web browser at `http://localhost:5001`
2. Select a token from the dropdown menu to view its price history
3. Click "Generate Graph" to see the token's relationship with Twitter accounts
4. Use the search function to find specific tweets mentioning the token

## Data Sources

- Historical token price data: CSV files stored in `F:\py demos\coindata\historical_data`
- Twitter data: Stored in SQL Server database

## Future Improvements

[Suggestions for future enhancements, such as:]

- Add more data sources for comprehensive analysis
- Implement real-time data updates
- Enhance the user interface for better interactivity
- Add more advanced analytics features
![微信图片_20240729104134](https://github.com/user-attachments/assets/d0ed808f-e24c-4533-8c54-0bf859e3e6e3)

