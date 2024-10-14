# Codet5_Pyspark_Generator
---
### Data Extraction and Pre-procesing
- Training data was WebScraped from the official Pyspark (Version 3.5.0) documentation web pages (https://spark.apache.org/docs/3.5.0/api/python/reference/pyspark.sql/) 
- Data was cleansed and refined to create a training dataset containing Code Desciptions and Code Snippets

### Data Standadization
- Columns names used as argments in the code snippet like 'c1', 'age', 'A1' etc were replaced with standard tokens like COL_A, COL B etc usisng regex
- Literals were standardized with tokens such as LIT_STR_1, LIT_INT_1, LIT_DEC_1 etc using regex
![image](https://github.com/user-attachments/assets/3b375592-2420-40d7-9bc1-93bd2e2623b1)


### Data Augmentation
- Initial webscraped dataset size was very small (~700 records) due to which additional data augmentation techniques were explored
- [IN PROGRESS] Text Augmentation techniques are being explored to rephrase or paraphrase the code desciptions to increase dataset diversity
- Standardized Tokens were replaced with ets of real world values which allowed to inflate the size of the dataset to a desired scale (~ 20K records)
![image](https://github.com/user-attachments/assets/d2b0b7f2-9e91-418b-86f9-ba6ae87207b2)

### Model Training
- The CODET5_SMALL Model was trained for up to 100 iterations with the below training parameters
![image](https://github.com/user-attachments/assets/9bed31f7-497e-4c0c-9a0e-fe2fedcc5b69)

### Model Predictions
- Despite the lower sized training data, the trained model was able to do a decent job in predicting the code.
- The Code was not entirely accurate but was semantically similar to pyspark code.
- Hallucinations were seen probably due to the smaller sized dataset

![image](https://github.com/user-attachments/assets/5d9b373f-2d2f-44d3-9fbf-aed585d1e099)



### ETL Pipeline UI
- A GUI was built using Streamlit to demonstrate how the model will be used to create ETL pipelines
- The main UI page allows users to add components and associate these components and the ETL flow is displayed in the GRAPH VIEW section
![image](https://github.com/user-attachments/assets/6527ad10-e646-45ef-be63-6be1d692300b)
- In the COLUMN MAPPER section, for a dataset, users can provide the mapping rules in the form of text prompts and the AI model will generate the corresponding code in the CODE VIEW section
