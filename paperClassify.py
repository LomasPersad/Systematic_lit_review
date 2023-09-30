# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 11:11:44 2023

@author: LPersad
"""
import pandas as pd
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
# from ipywidgets import IntProgress
import re
import nltk



# Load model directly
# from transformers import AutoTokenizer, AutoModelForMaskedLM

# tokenizer = AutoTokenizer.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext")
# model = AutoModelForMaskedLM.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext")

def df_to_json(csv_file, output_file):
    """
    Convert a DataFrame with 'title' and 'abstract' columns into a JSON file.

    Args:
        csv_file (str): Path to the CSV file containing 'title' and 'abstract' columns.
        output_file (str): Path to the output JSON file.

    Returns:
        None
    """
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    data = []

    for _, row in df.iterrows():
        title = row['Title']
        abstract = row['Abstract']
        keywords = row['Keywords']

        data.append({'title': title, 'abstract': abstract, 'keywords': keywords })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)   
    
    # return json.dumps(data)



def classify_papers(papers, tokenizer, model):
    # Create an empty list to store the results
    results_data = []

    for paper in papers:
        # Combine title, abstract, and keywords (if available)
        # text = f"{paper['title']}. "
        # if "abstract" in paper:
        #     text += paper["abstract"]
        # if "keywords" in paper:
        #     text += " ".join(paper["keywords"])
        
        text = paper["abstract"]
        
        

        # Tokenize the text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)

        # Get the predicted label and score
        label = outputs.logits.argmax().item()
        score = outputs.logits.softmax(dim=1)[0, label].item()

        # Map label to category (you may need to define your own mapping)
        categories = ["Category 1", "Category 2", "Category 3"]
        category = categories[label]

        # Append the result as a dictionary
        results_data.append({"Title": paper["title"], "Category": category, "Score": score})

    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(results_data, columns=["Title", "Category", "Score"])
    
    return results_df

def classify_papersv2(papers, tokenizer, model):
    regexp_tag = r'\<andsystem\-candidate\>'

    for paper in papers:
        # Combine title, abstract, and keywords (if available)
        text = f"{paper['title']}. "
        if "abstract" in paper:
            text += paper["abstract"]
        pmid=paper['Ref']
        abstract = text.rstrip()
        input_seq = tokenizer.encode( abstract, add_special_tokens = True )
        
        if ( len( input_seq ) < 512 ):
            inputs = tokenizer( abstract, return_tensors = "pt" )
            labels = torch.tensor( [ 1 ] ).unsqueeze( 0 )
            outputs = model( **inputs, labels = labels )

            predicition = outputs.logits.softmax( dim = -1 ).tolist()
        else:
            while len( input_seq ) >= 512:
                abstract_split = []
                abstract_split = nltk.sent_tokenize( abstract )
                lp2 = len( re.findall( regexp_tag, abstract_split[ -1 ] ) )
                
                if ( lp2 < 1 ):
                    abstract = abstract.replace( abstract_split[ -1 ], '' )
                else:
                    abstract = abstract.replace( abstract_split[ 0 ], '' )
                
                input_seq = tokenizer.encode( abstract, add_special_tokens = True )
                        
            inputs = tokenizer( abstract, return_tensors = "pt" )
            labels = torch.tensor( [ 1 ] ).unsqueeze( 0 ) # Batch size 1
            outputs = model( **inputs, labels = labels )
    
            predicition = outputs.logits.softmax( dim = -1 ).tolist()
    
        print( str( pmid ), " ", predicition[ 0 ][ 0 ], " ", predicition[ 0 ][ 1 ] )
    
        counter += 1


        
        # text = paper["abstract"]
    

if __name__ == '__main__':
    #----load and save title,abstract, keywords
    # csv_file = '.\\R\\review_243232_irrelevant_csv_20230909042812_processed.csv'
    # output_file='.\\R\\irrelevantData.json'
    # # Convert the DataFrame to JSON
    # json_data = df_to_json(csv_file,output_file)    
    # Print the JSON data
    # # print(json_data)
    
    #--- modeling part
    with open('.\\R\\irrelevantData.json', 'r', encoding='utf-8') as f:
        irrelevantJSONData = json.load(f)
        # print(irrelevantJSONData[0])
        f.close()
    
    # for paper in irrelevantJSONData:
    #     title = paper["title"]
    #     abstract = paper["abstract"]
    #     keywords = paper["keywords"]
    
    #     # Now you can work with the individual data elements for each paper
    #     print(f"Title: {title}")
    #     print(f"Abstract: {abstract}")
    #     print(f"Keywords: {keywords}")
    #     print("\n")    
    
    #----------Model work
    # model_name = "allenai/scibert_scivocab_uncased"
    
    model_name = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
   
    results = classify_papers(irrelevantJSONData,tokenizer,model)

    # Display the classification results
    print(results)
    

    