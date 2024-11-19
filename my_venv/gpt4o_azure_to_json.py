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

image_path = "https://content-media.bonial.biz/5a65acdb-308f-465b-b647-a8ac5c59fdd2/main.jpg"
#image_path = "vine__.jpg"
response = chat_with_gpt4(prompt, image_path)           
print(response)         

# 1. https://content-media.bonial.biz/f925444b-e918-46e5-9b38-c7cfb17bce0c/main.jpg
#     1. https://content-media.bonial.biz/803f40b6-5c80-47af-8240-3fdd329b3138/main.jpg

# 2. https://content-media.bonial.biz/4f233637-fa7a-4422-94e6-088e0f87fce4/main.jpg

# 3. https://content-media.bonial.biz/5a65acdb-308f-465b-b647-a8ac5c59fdd2/main.jpg
  
# 4. https://content-media.bonial.biz/5d53ca31-70d8-4915-bc02-3ddc2bca9210/main.jpg

# 5. https://content-media.bonial.biz/1737d220-528f-4103-8b39-47dcfc753019/main.jpg

# 6. https://content-media.bonial.biz/e2f80ea4-efe4-48ff-b8d9-9d18b025c532/main.jpg

# 7. https://content-media.bonial.biz/b135847e-224e-4d5a-990c-1269dc40de55/main.jpg

# 8. https://content-media.bonial.biz/e36faeec-3e78-4e94-8aff-75149aaf0dfd/main.jpg

# 9. https://content-media.bonial.biz/0e24b535-05e8-4c03-8170-6ec0f368739a/main.jpg
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




   
