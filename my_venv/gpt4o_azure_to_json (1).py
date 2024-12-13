import openai
# from text_prompts_txt import offer_without_price
# from text_prompts_txt import deposit_price    
from text_prompts_txt import other_types
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


prompt = other_types

image_path = "https://content-media.bonial.biz/c7b603da-16f4-42db-acf1-44914d7b0b7c/main.jpg"

response = chat_with_gpt4(prompt, image_path) 

print(response)

# offer with several products and with loyalty card :
# 1. https://content-media.bonial.biz/571cdfca-9cad-4c6c-a1d8-e9ca6753aa19/main.jpg 
# 2. https://content-media.bonial.biz/0bd2e999-a540-4067-95ad-33abc5b1fb8c/main.jpg 
# 3. https://content-media.bonial.biz/ae8a8c75-3e3a-48e5-93f9-dfd56387f329/main.jpg 
# 4. https://content-media.bonial.biz/c6552e4b-a73d-4684-af7e-c00cee0f918f/main.jpg
# 5. https://content-media.bonial.biz/c7b603da-16f4-42db-acf1-44914d7b0b7c/main.jpg

# scene with different product and price :
# 1. https://content-media.bonial.biz/1017da95-fa90-4e8f-985e-48856f7e7f17/main.jpg -відсотки
# 2. https://content-media.bonial.biz/3c664db8-011b-4d9d-81c6-0d516527467c/main.jpg
# 3. https://content-media.bonial.biz/90fec59f-2015-4e40-b5c9-44896b87e288/main.jpg
# 4. https://content-media.bonial.biz/386b3e86-ddcd-41a8-b5a2-96d3705a16ee/main.jpg
# 5. https://content-media.bonial.biz/341d65ed-fd3d-494f-a115-c18bd2b57bcf/main.jpg

# loyalty program: with a discount from the store
#    1. https://content-media.bonial.biz/ecd523ca-e31b-445b-9f9e-f62de6252130/main.jpg
# 2. https://content-media.bonial.biz/65b8e869-865e-4c9b-ad5b-aa0e8406e3ec/main.jpg 
# 3. https://content-media.bonial.biz/892beb4c-0bcd-44bb-86f9-b0c762186df4/main.jpg --- тут не забирається Le produit de 426 g
# 4. https://content-media.bonial.biz/2d185e05-bfca-485b-b781-bf261bae55e5/main.jpg 
# 5. https://content-media.bonial.biz/d20216d3-1e36-464a-b11b-87a4075d795d/main.jpg


# 7. https://content-media.bonial.biz/78e5f43f-7084-4760-8dae-229772543ded/main.jpg
# 8. https://content-media.bonial.biz/ea6056d4-b570-49be-b6d5-8c299707e56b/main.jpg

# offer with two sales price and one regular price
# 1. https://content-media.bonial.biz/2feba6c4-7d40-4e91-b975-e50b96774d91/main.jpg
# 2. https://content-media.bonial.biz/3aa7f9ba-1ad8-4942-8dbe-53d2db2aaf44/main.jpg
# 3. https://content-media.bonial.biz/b0dd23f9-1cb3-4d60-9308-5d70d1fc8687/main.jpg
# 4. https://content-media.bonial.biz/5809b76c-3070-48c6-9ce2-fc46fcc8e7cb/main.jpg
# 5. https://content-media.bonial.biz/f126c210-399f-475c-b68e-00115a6f9b96/main.jpg

# offer with several products
# 1. https://content-media.bonial.biz/2f282406-e82a-48fa-a6cc-9b8b1f59cc0a/main.jpg --- тут проблема 
# 2. https://content-media.bonial.biz/03fb1ed5-e99f-466a-a770-6ff88d432887/main.jpg --- тут проблема 
# 3. https://content-media.bonial.biz/b17d7fb6-44a0-4089-aa24-d2dd63178d0f/main.jpg
# 4. https://content-media.bonial.biz/0082a858-712c-42f8-b09a-6a8780a98c4a/main.jpg
# 5. https://content-media.bonial.biz/306bab6e-496c-44a9-8bb9-a42479e97d79/main.jpg

#offer with several transactions without a price
# 1. https://content-media.bonial.biz/ad73e320-48e5-477a-9b74-301cc7848fd1/main.jpg
# 2. https://content-media.bonial.biz/9ca0b951-e344-4075-9702-c901cd288680/main.jpg
# 3. https://content-media.bonial.biz/9770d5fe-15f4-4d3e-b03c-32399b6a4b4d/main.jpg
# 4. https://content-media.bonial.biz/df318ed8-20a7-4b37-8633-a2c398dabcc9/main.jpg
# 5. https://content-media.bonial.biz/7d90ab8d-5fad-4059-9983-1717fe5b40ca/main.jpg
