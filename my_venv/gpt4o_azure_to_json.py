import openai
import base64
import re
from text_prompts_txt import offer_without_price
 
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
    
        return response.choices[0].message['content'].strip()   
    except Exception as e:      
        return f"Error: {e}"    


prompt = offer_without_price
image_path = "https://content-media.bonial.biz/0e3ab1e9-ee76-4f4e-9633-71b6e68929e3/main.jpg"
#image_path = "vine__.jpg"
response = chat_with_gpt4(prompt, image_path)                    
print(response)

# 1. https://content-media.bonial.biz/985ec85e-0c15-43a6-a99b-acd118acb711/main.jpg
# 2. https://content-media.bonial.biz/9eeece72-a98f-416e-acb9-bc9752d49679/main.jpg
# 3. https://content-media.bonial.biz/4fde78af-7974-4cf2-ba2b-614fc4d8da53/main.jpg
# 4. https://content-media.bonial.biz/884938b5-d236-4e1e-b484-5d55851b6d1f/main.jpg
# 5. https://content-media.bonial.biz/f3ed4bba-f6be-4a62-aac8-3a517c87c110/main.jpg
# 6. https://content-media.bonial.biz/9c251ae2-83eb-459c-a1a2-637f78c0ff65/main.jpg
# 7. https://content-media.bonial.biz/fedd7564-245a-4c73-b335-5abb36689a19/main.jpg
# 8. https://content-media.bonial.biz/b555dc79-bcb6-4d54-ac4a-03a54c14a74e/main.jpg  ——
# 9. https://content-media.bonial.biz/bdcaa722-35ad-4e57-8d3d-b395fcdd436b/main.jpg
# 10. https://content-media.bonial.biz/f0eb8fae-02bc-4fd2-bb5e-2fe0debfa928/main.jpg


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




   
