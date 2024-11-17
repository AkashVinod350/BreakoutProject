# CSV Web Scraper Dashboard

## Project Description
The CSV Web Scraper Dashboard is an interactive Streamlit application designed to process data from CSV files, perform web scraping, and generate concise, relevant insights. With integrated APIs, it provides a seamless user experience to extract and display results from search queries for each row of a selected column.

## Setup Instructions
Follow these steps to set up and run the project:

### 1. Install Required Dependencies
Ensure you have Python installed. Use the following command to install required packages:
 
pip install streamlit pandas requests groq

### 2. Run the Application
Execute the application using the command:
streamlit run app.py

### 3. Upload CSV File
Upload a CSV file with appropriate data to use the dashboard features.

## Usage Guide
### 1. Uploading a CSV File

Launch the dashboard and navigate to the "Upload Your CSV File" section.
Upload a CSV file to view and analyze its contents.
### 2. Selecting a Column

Choose a column from the uploaded CSV file to apply queries.
### 3. Entering a Query

Input a query to perform web scraping for each row in the selected column.
### 4.Viewing Results

The application fetches search snippets and links for each row and displays the results in the table.
### 5. Export Results

View or export the enriched CSV file with additional columns for search results and corresponding links.

## API Keys and Environment Variables
This project uses the following API keys and environment variables:

### 1. SerpAPI Key

Enter your SerpAPI key (api_key) in the scrapWeb method. Replace:

api_key = "your_serpapi_key_here"

### 2. Groq API Key

Enter your Groq API key in the getRes method. Replace:

client = Groq(api_key="your_groq_api_key_here")

## Optional Features
### Dynamic Query Generation:
Customize search queries based on specific column data and user input.
### Integration with Groq API:
Provides one-word summaries for insights.
### Interactive Data Display:
View processed data dynamically within the dashboard.
### Error Handling:
Handles missing API keys, connection issues, and invalid responses gracefully.

Handles missing API keys, connection issues, and invalid responses gracefully.
Contribution
Feel free to fork, improve, or contribute to this project by submitting a pull request. For any issues, please raise an issue in the repository.

Happy Scraping!
