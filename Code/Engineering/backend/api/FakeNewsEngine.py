"""
    Single instance of fake detector
"""
import torch
from transformers import BertTokenizer
import os
import numpy as np

class FakeNewsEngine():

  def __init__(self):
    # Load the model
    model_path = os.path.join(os.getcwd(), 'models', 'fake_model_attention')
    print('Loading fake news model from base path: ', model_path)
    self.model = torch.load(model_path, map_location='cpu')
    self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    print('Model loaded successfully')
    pass

  def preprocess (self, text):
    token_text = self.tokenizer(list([text]), 
                          max_length = 128,           # Pad & truncate all sentences.
                          padding = 'max_length',
                          truncation=True,
                          return_attention_mask = True,   # Construct attn. masks.
                          return_tensors = 'pt'     # Return pytorch tensors.
    )
    seq = torch.tensor(token_text['input_ids']).to('cpu')
    mask = torch.tensor(token_text['attention_mask']).to('cpu')

    return seq, mask, token_text
  
  def extract_importance (self, input_ids_all, attentions_all):
    html = []
    for input_ids, attention in zip(input_ids_all, attentions_all): 
        # print('test index', input_ids.shape)
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        first_layer = attention[0]
        count_dict = dict()
        for token, attention_128 in zip(tokens, first_layer): 
            # print(token, attention_128.shape)
          if token == '[PAD]':
            break
          attention_128 = attention_128.tolist()
          attention_max = max(attention_128)
          attention_index = attention_128.index(attention_max)
          # print('===>attention_128', attention_128)
          # print('===>attention_max', token, attention_max)
          # print('===>attention_index', attention_index, tokens[attention_index])
          candidate_token = tokens[attention_index]
          if candidate_token in count_dict:
            count_dict[candidate_token] += 1
          else:
            count_dict[candidate_token] = 1
        
        # Count the times specific token is the most importance
        count_sum = 0
        for key, value in count_dict.items():
          if key == '[CLS]' or key == '[SEP]':
            continue
          count_sum += value

        for token in tokens:
          if token == '[PAD]':
            break
          if token == '[CLS]' or token == '[SEP]':
            continue
          if token in count_dict:
            weight = count_dict[token] / count_sum
          else: 
            weight = 0
          # print(token, weight)
          html.append('<span style="background-color: rgb(255,255,0,{0})">{1}</span>'.format( weight * 2, token)) 
    html_string = " ".join(html)
    return html_string
  
  def predict (self, text):
    seq, mask, token_text = self.preprocess(text)
    with torch.no_grad():
      outputs = self.model(seq, mask)
      pred_proba = outputs[0].detach().cpu().numpy()
    
    preds = np.argmax(pred_proba, axis = 1)
    result = bool(preds[0])
    print('fake predict result', result)
    
    if result == True:
      return result, ''
    
    attentions = outputs['attentions'][0]
    html = self.extract_importance(token_text['input_ids'], attentions)
    
    return result, html


fake_detector = FakeNewsEngine()

# test_text_fake = 'Alfalfa is the only cure for COVID-19.'
# test_text_real = '#IndiaFightsCorona India has one of the lowest #COVID19 mortality globally with less than 2% Case Fatality Rate. As a result of supervised home isolation &amp; effective clinical treatment many States/UTs have CFR lower than the national average. https://t.co/QLiK8YPP7E'
