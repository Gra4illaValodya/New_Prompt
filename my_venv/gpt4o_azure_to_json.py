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
    
        return response.choices[0].message['content'].strip()   
    except Exception as e:      
        return f"Error: {e}"    


prompt = size_chart
image_path = "https://content-media.bonial.biz/ec808ec8-191a-44c0-8dbe-f793fc96e80f/main.jpg"
#image_path = "vine__.jpg"
response = chat_with_gpt4(prompt, image_path)                    
print(response)

    # 1. https://content-media.bonial.biz/ec808ec8-191a-44c0-8dbe-f793fc96e80f/main.jpg
    # 2. https://content-media.bonial.biz/b2580888-4eb3-403e-b543-be1400b11588/main.jpg
    # 3. https://content-media.bonial.biz/38190d46-b241-4017-85f2-0b2b43173b94/main.jpg
    # 4. https://content-media.bonial.biz/b889484d-7dcd-41d2-ae8b-973db1646bd6/main.jpg
    # 5. https://content-media.bonial.biz/8ac819fe-2aac-46bb-9092-d39625525563/main.jpg  тут що б не робив 1 діл не дораховує 
    # 6. https://content-media.bonial.biz/fedbced9-b555-4d7a-bb4c-a84c5daexc4c4/main.jpg
    # 7. https://content-media.bonial.biz/69c53b29-6087-4194-8884-d2dda11f1889/main.jpg
    # 8. https://content-media.bonial.biz/8985d082-baa2-4ed7-8899-dee33a56fdc7/main.jpg
    # 9. https://content-media.bonial.biz/8dd07775-9721-442e-9eb0-8abeca92d055/main.jpg
    # 10. https://content-media.bonial.biz/0609ba05-52d1-4fd4-819f-67a0051a7267/main.jpg.      
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




   
