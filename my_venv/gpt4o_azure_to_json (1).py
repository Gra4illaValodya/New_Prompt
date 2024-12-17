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
 
#  HT TTC
# 1. https://content-media.bonial.biz/0fb5d70e-2e49-48cb-bbe5-507342e020d8/main.jpg     +5
# 2. https://content-media.bonial.biz/0e24b535-05e8-4c03-8170-6ec0f368739a/main.jpg     +5
# 3. https://content-media.bonial.biz/197f2fb5-315f-44a0-9e63-7b73c10dfb66/main.jpg     +5  
# 4. https://content-media.bonial.biz/2fe533e9-af97-465d-9f52-e3fbc66a5a94/main.jpg     +5
# 5. https://content-media.bonial.biz/4913cf4d-0d96-41b0-8a9b-6d6ff9859494/main.jpg     +5
# 6. https://content-media.bonial.biz/12c967dc-8239-4782-b075-8db6468c4ae4/main.jpg     +5
# 7. https://content-media.bonial.biz/6ed04250-f828-4e50-931b-0cc0bec29ca2/main.jpg     +5
# 8. https://content-media.bonial.biz/402d4520-b160-4a7a-bc86-6dd371e67f9f/main.jpg     +5
# 9. https://content-media.bonial.biz/9beffa7c-adcc-4c82-bee9-1b224e0b64ae/main.jpg     +5
# 10. https://content-media.bonial.biz/9eb6ca2f-3121-466f-bfb2-7bb2d429df09/main.jpg    +5
# 11. https://content-media.bonial.biz/315d4afe-f5a2-46c0-b304-fb9d7333e76d/main.jpg    +5
# 12. https://content-media.bonial.biz/ea501635-1980-4f3d-a363-24e110c41bf6/main.jpg    +5
# 13. https://content-media.bonial.biz/a8ed94ae-e133-4bfe-9fda-d9129ba9ba02/main.jpg
# 14. https://content-media.bonial.biz/8500d82f-fb27-4a3c-b7bd-b2e9adfe96c8/main.jpg
# 15. https://content-media.bonial.biz/72cc0ba5-4fdf-49d7-b17f-451cb87a161d/main.jpg

 
#  One price
# 1. https://content-media.bonial.biz/e01a98c5-d8ab-4e89-86b4-5fa35a6b8999/main.jpg     +5
# 2. https://content-media.bonial.biz/20575810-8313-4332-924b-8ce95fb5128e/main.jpg     +5
# 3. https://content-media.bonial.biz/0ca99942-cc94-4da7-9585-0e8104646281/main.jpg     +5
# 4. https://content-media.bonial.biz/aca96f38-359f-4af9-8616-35908e03ecfd/main.jpg     +5
# 5. https://content-media.bonial.biz/83d89bd1-6e06-49aa-b41b-44219aae42ab/main.jpg     +5
# 6. https://content-media.bonial.biz/b152839e-5c35-4c2d-a4a0-2389678109b7/main.jpg     +5
# 7. https://content-media.bonial.biz/ca198ed6-28fb-42f7-be01-76cf8137be36/main.jpg     +5 
# 8. https://content-media.bonial.biz/e8e91ae9-24cc-475f-b7e3-0472d93d7e87/main.jpg     +5
# 9. https://content-media.bonial.biz/2ac93ac0-7293-4a4c-8220-86b03b7a7116/main.jpg     +5
# 10. https://content-media.bonial.biz/32d4b3a5-9718-4f90-b2a9-29db9b103d9f/main.jpg    +5

 
#  ВОЗРАСТ  игрушки для детей
# 1. https://content-media.bonial.biz/9fb9ab33-cfcb-4d4a-a9af-68f39b8ccede/main.jpg
# 2. https://content-media.bonial.biz/5f9e94bf-039d-43b7-9084-b73be4a5a4fa/main.jpg
# 3. https://content-media.bonial.biz/d4408e66-4bf1-4c9a-8180-565b1bf48d86/main.jpg
# 4. https://content-media.bonial.biz/14a50b9f-13ca-4457-bb77-ca7a83c78886/main.jpg
# 5. https://content-media.bonial.biz/13724033-c214-4775-97ff-61c6e887b553/main.jpg
 
# Le moins cher

# 1. https://content-media.bonial.biz/4c394d43-7927-4735-b48e-89110faafcea/main.jpg     +5
# 2. https://content-media.bonial.biz/dd8a97b8-ee9d-4a22-a8cd-79458f7a39b5/main.jpg     +5
# 3. https://content-media.bonial.biz/d0b45383-5f0a-4a98-a952-420c2d46fff6/main.jpg     +5
# 4. https://content-media.bonial.biz/cc8693e9-2092-40c9-89d2-399537fbefe6/main.jpg     +5
# 5. https://content-media.bonial.biz/497b8b5e-3c1b-43ce-969b-037b6a46486b/main.jpg — ТУТ НЕ ВПЕВНЕНИЙ ЧИ ВІРНО
# 6. https://content-media.bonial.biz/32d19aa5-a420-4db5-bdf5-5fc9e2670d33/main.jpg     +5
# 7. https://content-media.bonial.biz/e0345284-17a4-4364-aef0-1df6418a4a30/main.jpg     +5
# 8. https://content-media.bonial.biz/e6eb8d69-68ea-4094-aa26-165fca26db74/main.jpg     +5
# 9. https://content-media.bonial.biz/d5980f9f-77f8-4f82-be50-99039250feb7/main.jpg     +5


# sur le

# 1. https://content-media.bonial.biz/c296626f-fadd-43ab-9f61-5a9938517d39/main.jpg     +5     price_reduced_on_the_n_th_product_only
# 2. https://content-media.bonial.biz/4dc09e7c-a70e-4f54-8740-a521fb1b9c03/main.jpg     +5
# 3. https://content-media.bonial.biz/4da71451-275d-4c5e-bc1e-bcb5483f742f/main.jpg     +5
# 4. https://content-media.bonial.biz/f1d593b0-f220-480b-b49f-7e40e234ee70/main.jpg     +5     offer_without_price
# 5. https://content-media.bonial.biz/fb5c04e9-cbd1-47e8-b37b-156ebcb8ec19/main.jpg     +5
# 7. https://content-media.bonial.biz/e06ade2c-834d-4585-be0f-cdd0d9f05ef7/main.jpg     +5
# 8. https://content-media.bonial.biz/601a48e6-7006-41c0-85ce-bdd66d498a8e/main.jpg     +5
# 9. https://content-media.bonial.biz/c1029db8-39f6-4f18-8b10-d6f64164d640/main.jpg     +5      offer_without_price 
# 10. https://content-media.bonial.biz/f84ddba7-67d3-47ac-8426-bbe49138f0ca/main.jpg    +5      offer_without_price
# 11. https://content-media.bonial.biz/57bda371-038d-4265-abfe-1f952325bd67/main.jpg
# 12. https://content-media.bonial.biz/e63d0a84-6de2-466e-9a22-3843c1c46854/main.jpg
# 13. https://content-media.bonial.biz/15862297-092d-4c65-9df9-e45ac0e5e923/main.jpg