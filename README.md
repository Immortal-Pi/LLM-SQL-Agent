
# SQL Agent vs RAG 

## objective 

Employee's in a workspace might not be familiar with SQL or programming languages and might know few basic SQL operations. This took enhances their operations by writing queries based on the prompt entered to the chatbot and gives results.

An application where you can upload the CSV file and it stores the data into SQLite database. Impleted langchain SQLAgent for queries. 

This application also compares the results from traditional RAG and SQLAgent.


## API Reference

#### Hugging Face Token
#### OpenAI 

```http
  AzureOpenAI 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `OpenAI` | `API KEY` | **Required**. Your API key |
| `AzureOpenAI` | `API KEY` | **Required**. Your API key |




## Documentation

- streamlit and gradio for webpage 
- OpenAI LLM (GPT 3.5 turbo)  AzureOpenAI embeddings for RAG
- ChromaDB vector database 
- SQLite relational database


## Screenshots

### upload dataset/CSV file
![App Screenshot](https://github.com/Immortal-Pi/LLM-SQL-Agent/blob/main/output/1.png)

### chat with the documents
![App Screenshot](https://github.com/Immortal-Pi/LLM-SQL-Agent/blob/main/output/2.png)

![App Screenshot](https://github.com/Immortal-Pi/LLM-SQL-Agent/blob/main/output/3.png)

![App Screenshot](https://github.com/Immortal-Pi/LLM-SQL-Agent/blob/main/output/4.png)

![App Screenshot](https://github.com/Immortal-Pi/LLM-SQL-Agent/blob/main/output/5.png)

![App Screenshot](https://github.com/Immortal-Pi/LLM-SQL-Agent/blob/main/output/6.png)


## Tech stack

python, AzureOpenAI, langchain, streamlit 

## Conclusion 

Performance: RAG had a faster response time, but SQL Agent provided perfect answers most of the time.

Accuracy: Direct SQL queries maintained high precision, especially with relational data.

Scalability: SQL-based solutions scaled better with larger tables, reducing the operational complexity associated with embedding-heavy RAG setups.

RAG is still a powerful tool for dynamic and contextual queries, but SQL Agent proved to be the clear winner for this use case.
