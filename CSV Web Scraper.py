import streamlit as st
import pandas as pd
import requests
from groq import Groq
import json  
import time
import concurrent.futures

class CSVUploaderApp:
    def __init__(self):
        self.df = None

    def upload_csv(self):
        """Handles the file upload and displays the CSV content."""
        st.header("1. Upload Your CSV File")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file:
            self.df = pd.read_csv(uploaded_file)
            st.subheader("CSV File Contents:")
            st.dataframe(self.df)
            return self.df
        else:
            st.info("Please upload a CSV file to view its contents.")

    def select_column(self):
        """Displays a dropdown to select a column if a CSV is uploaded."""
        if self.df is not None:
            st.header("2. Select a Column")
            column_options = self.df.columns.tolist()
            selected_column = st.selectbox("Choose a column to display", column_options)

            if selected_column:
                st.write("You selected the column:", selected_column)
                return selected_column
        else:
            st.info("Upload a CSV file to enable column selection.")

    def input_text(self,col):
        """Displays a text input box for additional user input."""
        st.header("3. Additional Input")
        user_input = st.text_input("Enter additional information",placeholder="Enter your query to perfrom on"+ col)

        if user_input:
            st.write("You entered:", user_input)
            return user_input

    def scrapWeb(self, rowValue, query):
        """Scrapes web results and returns snippets and links."""
        res = []
        api_key = "Enter your serp api key here"
        url = "https://serpapi.com/search.json"
        params = {
            "q": query+" of "+rowValue,           # Search query
            "hl": "en",           # Language (e.g., 'en' for English)
            "gl": "us",           # Country (e.g., 'us' for the United States)
            "google_domain": "google.com",  # Google domain
            "api_key": api_key,
            "num": 4  # The number of results to fetch
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Extracting snippets and links
            for result in data.get("organic_results", []):
                snippet = result.get('snippet', '')
                link = result.get('link', '')
                res.append({"snippet": snippet, "link": link})
        else:
            st.error(f"Error: {response.status_code}")
            st.error(response.text)
        
        return res

    def getRes(self, webRes, prompt):
        """Generates a one-word response using the Groq API."""
        try:
            client = Groq(api_key="Enter your groq api key here")

            # Limit the length of webRes to avoid exceeding context length
            max_length = 1000
            webRes_str = json.dumps(webRes, indent=2) if isinstance(webRes, dict) else str(webRes)

            # Request a single word answer
            messages = [{
                "role": "user",
                "content": f"query: {prompt}\nAnswer the following question with only a single word based on the text: {webRes_str}\nAnswer:"
            }]
            
            # Send the request to the Groq API
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192",
                max_tokens=50  # Reduce tokens to encourage a shorter response
            )
            
            # Get the response and strip extra spaces or characters
            res = chat_completion.choices[0].message.content.strip()

            # You can apply additional filtering here to ensure the response is a single word (e.g., regex or text processing)
            return res.split()[0]  # Return only the first word of the response

        except Exception as e:
            st.error(f"Error while generating response: {e}")
            return "Error"

    def process_webscraping(self, row_value, prompt):
        """Handles applying the web scraping and Groq API to each row, returning one word."""
        web_results = self.scrapWeb(row_value, prompt)
        if web_results:
            snippets = "\n".join([result['snippet'] for result in web_results])
            links = "\n".join([result['link'] for result in web_results])
            
            # Get a one-word response using Groq API
            one_word_answer = self.getRes(web_results, prompt)
            
            return one_word_answer, links  # Return one word answer and links
        else:
            return "No data found", ""

    def run(self):
        """Runs the entire application."""
        df = self.upload_csv()
        if df is not None:
            col = self.select_column()
            inp = self.input_text(col)

            if inp:
                # Apply web scraping to each row of the selected column
                df['results'], df['links'] = zip(*df[col].apply(lambda row_value: self.process_webscraping(row_value, inp)))
                
                st.subheader("Updated CSV File Contents with Results and Links:")
                st.dataframe(df)

# Run the Streamlit application
if __name__ == "__main__":
    app = CSVUploaderApp()
    app.run()
