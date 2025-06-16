import csv
import os
from time import monotonic

from openai import OpenAI
import anthropic
import google.generativeai as genai

from personal_key import my_key_openai, my_key_anthropic, my_key_google


openai_client = OpenAI(api_key=my_key_openai)
anthropic_client = anthropic.Anthropic(api_key=my_key_anthropic)
genai.configure(api_key=my_key_google)


def make_gpt_call(prompt, model):
    return openai_client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

def make_anthropic_call(prompt, model):
    return anthropic_client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ).content[0].text

def make_google_call(prompt, model):
    model = genai.GenerativeModel(model)
    return model.generate_content(prompt).text

def make_llm_call(prompt, model='dummy'):
    if 'gemini' in model.lower(): return make_google_call(prompt, model)
    if 'claude' in model.lower(): return make_anthropic_call(prompt, model)
    if 'gpt' in model.lower() or 'o1-preview' in model.lower(): return make_gpt_call(prompt, model)
    if model == 'dummy': return '"Answer: no"'#'dummy output'
    return None

def make_multiple_calls(prompt_list, model):
    return pd.DataFrame([{'model':model, 'Prompt': prompt, 'full_response': make_gpt_call(prompt, model)} 
            for prompt in prompt_list]) 

def process_answer(result):
    result = result.lower()
    answer = result.split('answer')[-1]
    if 'yes' in answer:
        return 1
    if 'not' in answer: 
        return None
    if 'no' in answer:
        return 0
    return None

def write_csv(filename, instance):
    if os.path.isfile(filename):
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = list(instance.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(instance)
            return
    else:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = list(instance.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(instance)

def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours*3600) // 60
    remaining_seconds = seconds - hours*3600 - minutes*60
    return int(hours), int(minutes), int(remaining_seconds)


def print_status(idx, len_df, start_id, start_time):
    remaining = len_df-idx
    num_prompts_processed = 1 + (idx - start_id)
    elapsed_time = monotonic() - start_time
    time_per_prompt = elapsed_time / num_prompts_processed
    eta = convert_seconds((len_df - idx) * time_per_prompt)
    print(
        '('+str(idx) + '/' + str(len_df)+') '+str(round(100*idx/len_df,2))+'%'
        +' ETA:' + str(eta[0])+':'+str(eta[1])+':'+str(eta[2]), 
          end="\r")