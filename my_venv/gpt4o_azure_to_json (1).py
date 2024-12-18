import openai
# from text_prompts_txt import offer_without_price
# from text_prompts_txt import deposit_price    
# from text_prompts_txt3 import one_old_and_one_new_price
from old_text_prompts_txt import two_products_with_coupon
openai.api_type = "azure"   
openai.api_version = "2023-05-15"
openai.api_base = "https://bonial-openai-test-004.openai.azure.com/"
openai.api_key = "3d337d2d785d4840b9ae45ebfc4faee5"



def chat_with_gpt4(prompt, image_path,  model="bonial-gpt-4o", max_tokens=4096):
    try:
        response = openai.ChatCompletion.create(
            engine=model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user",
                       "content": [
                           {
                               "type": "text",
                               "text": prompt
                           },
                           {
                               "type": "image_url",
                               "image_url": {
                                   "url": image_path
                               }
                           }
                       ]
                       }
                      ],
            max_tokens=max_tokens,
            temperature=0.1
        )
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        print(f"Prompt tokens: {prompt_tokens}")       
        print(f"Completion tokens: {completion_tokens}")
        print(f"Total tokens: {total_tokens}")

        return response.choices[0].message['content'].strip()   
    except Exception as e:  
            return f"Error: {e}"    
        

prompt = two_products_with_coupon

image_path = "https://content-media.bonial.biz/9d074b5c-285b-41fa-975a-fcdef9fdf3eb/main.jpg"

response = chat_with_gpt4(prompt, image_path) 

print(response) 
 
#  GERMAN 
#  1. https://content-media.bonial.biz/eb7285b0-6ae6-4a20-8e6d-8045ab10e467/main.jpg
#  2. https://content-media.bonial.biz/9d074b5c-285b-41fa-975a-fcdef9fdf3eb/main.jpg
#  3. https://content-media.bonial.biz/812cea6b-21cb-44b4-a5f0-e69d503c7293/main.jpg" --- записується Preis mit App Coupon в опис

