import openai
import base64
import re
from text_prompts_txt import size_chart
 
openai.api_type = "azure"   
openai.api_version = "2023-05-15"       
openai.api_base = "https://bonial-openai-test-004.openai.azure.com/"
openai.api_key = "3d337d2d785d4840b9ae45ebfc4faee5"

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"  

def is_url(image_path):

    return bool(re.match(r'^(http|https)://', image_path))

def chat_with_gpt4(prompt, image_path, model="bonial-gpt-4o", max_tokens=4096):
    try: 

        if is_url(image_path):
            image_data = image_path
        else:
            image_data = convert_image_to_base64(image_path)
        
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
                                   "url": image_data
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
        print(f"URL : {image_path}")
    
        return response.choices[0].message['content'].strip()   
    except Exception as e:      
        return f"Error: {e}"    

prompt = size_chart
image_path = "https://content-media.bonial.biz/71629c21-ca73-42c6-896c-e2dbcfd4d443/main.jpg"
#image_path = "vine__.jpg"˜
response = chat_with_gpt4(prompt, image_path)                    
print(response)













        
#FR
# one_price
# one_old_and_one_new_price
# price_reduced_on_the_n_th_product_only
# one_price_with_and_one_price_without_the_card
# money_spared_on_the_card  
# offer_without_price
# offer_without_price_loyalty_card
# size_chart
# other_types

#DE
# simple_offers
# two_products_in_one_offer
# one_product_with_coupon
# several_products_with_different_prices
# price_characterization_uvp
# price_characterization_statt
# special_prise
# old_price_crossed_out
# product_number_sku
# money_rebate
# percentage_rebate
# reward
# additional_shipping
# deposit_price
# multiple_offers_with_uvp
# different_sizes
# supplemental_bid
# regular
# without_price
# additional_products
# stock_offers
# travel_booklets
# stocks
# several_products_with_different_prices




   
