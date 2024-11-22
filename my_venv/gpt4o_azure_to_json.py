import openai
import base64
import re
from text_prompts_txt import one_price
 
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


prompt = one_price
image_path = "https://content-media.bonial.biz/102aa539-8c6e-4cc0-a4b8-1b613a399485/main.jpg"
#image_path = "vine__.jpg"
response = chat_with_gpt4(prompt, image_path)                    
print(response)

# 1. https://content-media.bonial.biz/59f93948-c450-4add-a053-d48a3d76e824/main.jpg
# 2. https://content-media.bonial.biz/60a64f1c-6d09-4375-87d9-0f7d9c7ac11d/main.jpg
# 3. https://content-media.bonial.biz/14231501-a580-47ab-b4fe-cf3e42507013/main.jpg
# 4. https://content-media.bonial.biz/bfb7ed95-50af-4ed4-8647-85a6421572e0/main.jpg
# 5. https://content-media.bonial.biz/8d458ab6-c0b7-4f87-b36e-855a5a770bf0/main.jpg
# 6. https://content-media.bonial.biz/03976572-4ad7-43c1-8e33-a57a1f4687ec/main.jpg
# 7. https://content-media.bonial.biz/8384861d-6a36-42bd-9578-6548c3000a3e/main.jpg
# 8. https://content-media.bonial.biz/0fc755ed-c3ea-46da-8bd3-df0cd8c0aa27/main.jpg
# 9. https://content-media.bonial.biz/102aa539-8c6e-4cc0-a4b8-1b613a399485/main.jpg
# 10. https://content-media.bonial.biz/b798d917-49ea-4b2c-bbc8-4639147e446f/main.jpg
# 11. https://content-media.bonial.biz/09552598-8138-4bed-bfa2-08c7d623ef26/main.jpg
# 12. https://content-media.bonial.biz/474d1f67-7ee8-4a0b-8dca-f745c56f1f17/main.jpg
# 13. https://content-media.bonial.biz/df50a8ae-07f6-4c7d-bdcb-b5d5cb6e7e67/main.jpg


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




   
