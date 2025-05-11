# TO RUN

In a local environment:
```shell
streamlit run home.py
```

To run inside of a docker container:
```shell
docker build -t climatechat
docker run -p 8501:8501 -v $(pwd):/app climatechat
```
NOTE: Ensure that streamlit is installed as a python library and you are utilizing Python 3.11

```
Copy config_sample.py and name the copy config.py. Import your API keys in there.
```

# ClimateDataChat
Intelligent Chatbot for Climate Data Recommendation

Team Information:
Erica Schermerhorn, Esther Omotayo Oyedele, Richard James Heiman, Joel Nathan Gujjarlamudi, and Maksim Kirillov

AI Problem
The problem we aim to solve is assisting users in identifying relevant climate-related datasets for predictive machine learning analytics based on categorizing datasets into three categories – time-relevant, fidelity level, and size. Currently, finding suitable datasets for climate modeling or analysis can be time-consuming and overwhelming due to the vast number of available datasets spread across various public repositories. Our AI-powered chatbot will address this challenge by providing personalized recommendations, guiding users to the most relevant datasets based on their queries. Additionally, the chatbot can be expanded to offer boilerplate code for data analysis and conduct exploratory data analysis (EDA), making it a useful tool for researchers, students, and professionals working in climate sciences and predictive analytics.

Initial Project Proposal
Scope of Work
•	Chatbot Development: We will implement a conversational AI chatbot using the OpenAI API. Then, we will design an intuitive user interface that allows users to input queries related to climate data and predictive modeling.
•	Dataset Recommendation System: We will integrate APIs or web scraping techniques to fetch climate datasets from open data platforms starting with Kaggle, then potentially incorporating further datasets such as UCI Machine Learning Repository, NOAA, and NASA. Following this, we will develop a ranking or filtering mechanism to recommend datasets based on user queries. The user queries will be broken down into dataset requirements and dataset preferences, with the preferences being categorized into time-relevance, fidelity level, and dataset size.
•	Enhancements and Expansion: We will provide users with boilerplate Python code for loading and preprocessing datasets (using Pandas, NumPy, and Scikit-learn). In addition, we will offer an automated EDA feature to visualize key trends, summarize dataset statistics, and identify potential features for machine learning models.

Technologies and Tools
For the chatbot framework, we will use OpenAI’s Python API. We will host the chatbot on a Streamlit server, which will directly call our dataset search model with a set of standard engineered inputs generated from the chatbot. We will use Pandas, Numpy, Matplotlib, Seaborn and Scikit-learn for the data processing and analysis. Our data sources will be Kaggle API, UCI Repository, NOAA Climate Data, NASA Open Data.

Expected Outcomes
A functional chatbot that can understand user queries and recommend relevant climate datasets, a system that ranks and filters datasets based on user needs, and optional features such as boilerplate code generation and automated EDA to support initial data analysis and enhance user experience.