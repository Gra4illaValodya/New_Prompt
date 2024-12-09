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

image_path = "https://content-media.bonial.biz/63b20a99-2bff-477d-9d0d-a1568e633f72/main.jpg"

response = chat_with_gpt4(prompt, image_path) 
 
print(response)     

# loyalty program: with a discount from the store
# 1. https://content-media.bonial.biz/ecd523ca-e31b-445b-9f9e-f62de6252130/main.jpg
# 1. https://content-media.bonial.biz/b72f94a7-1002-479f-ae75-993b3724a865/main.jpg
# 2. https://content-media.bonial.biz/65b8e869-865e-4c9b-ad5b-aa0e8406e3ec/main.jpg
# 3. https://content-media.bonial.biz/892beb4c-0bcd-44bb-86f9-b0c762186df4/main.jpg
# 4. https://content-media.bonial.biz/1238de9e-5a23-4d8f-990d-1f1a96b74d51/main.jpg

# scene with different product and price :
# 1. https://content-media.bonial.biz/1017da95-fa90-4e8f-985e-48856f7e7f17/main.jpg
# 2. https://content-media.bonial.biz/3c664db8-011b-4d9d-81c6-0d516527467c/main.jpg
# 3. https://content-media.bonial.biz/90fec59f-2015-4e40-b5c9-44896b87e288/main.jpg
# 4. https://content-media.bonial.biz/6b3cc57e-fcfb-42c7-bced-74bc2fc80e64/main.jpg
# 5. https://content-media.bonial.biz/63b20a99-2bff-477d-9d0d-a1568e633f72/main.jpg

# offer with several products and with loyalty card :
# 1. https://content-media.bonial.biz/571cdfca-9cad-4c6c-a1d8-e9ca6753aa19/main.jpg 
# 2. https://content-media.bonial.biz/0bd2e999-a540-4067-95ad-33abc5b1fb8c/main.jpg
# 3. https://content-media.bonial.biz/ae8a8c75-3e3a-48e5-93f9-dfd56387f329/main.jpg 
# 4. https://content-media.bonial.biz/c6552e4b-a73d-4684-af7e-c00cee0f918f/main.jpg
# 5. https://content-media.bonial.biz/c7b603da-16f4-42db-acf1-44914d7b0b7c/main.jpg

# offer with two sales price and one regular price
# 1. https://content-media.bonial.biz/2feba6c4-7d40-4e91-b975-e50b96774d91/main.jpg
# 2. https://content-media.bonial.biz/3aa7f9ba-1ad8-4942-8dbe-53d2db2aaf44/main.jpg
# 3. https://content-media.bonial.biz/b0dd23f9-1cb3-4d60-9308-5d70d1fc8687/main.jpg
# 4. https://content-media.bonial.biz/5809b76c-3070-48c6-9ce2-fc46fcc8e7cb/main.jpg
# 5. https://content-media.bonial.biz/9428911a-f6b4-4eb0-aa7e-8e2da71c419d/main.jpg

# offer with several products
# 1. https://content-media.bonial.biz/2f282406-e82a-48fa-a6cc-9b8b1f59cc0a/main.jpg
# 2. https://content-media.bonial.biz/03fb1ed5-e99f-466a-a770-6ff88d432887/main.jpg
# 3. https://content-media.bonial.biz/b17d7fb6-44a0-4089-aa24-d2dd63178d0f/main.jpg
# 4. https://content-media.bonial.biz/b7cef865-6196-4046-9524-ce0af558bb67/main.jpg
# 5. https://content-media.bonial.biz/306bab6e-496c-44a9-8bb9-a42479e97d79/main.jpg

# offer with two sales price and one regular price
# 1. https://content-media.bonial.biz/2feba6c4-7d40-4e91-b975-e50b96774d91/main.jpg
# 2. https://content-media.bonial.biz/3aa7f9ba-1ad8-4942-8dbe-53d2db2aaf44/main.jpg
# 3. https://content-media.bonial.biz/b0dd23f9-1cb3-4d60-9308-5d70d1fc8687/main.jpg
# 4. https://content-media.bonial.biz/5809b76c-3070-48c6-9ce2-fc46fcc8e7cb/main.jpg
# 5. https://content-media.bonial.biz/9428911a-f6b4-4eb0-aa7e-8e2da71c419d/main.jpg



# offer with several products and with loyalty card :
# 1. https://content-media.bonial.biz/571cdfca-9cad-4c6c-a1d8-e9ca6753aa19/main.jpg 
# 2. https://content-media.bonial.biz/0bd2e999-a540-4067-95ad-33abc5b1fb8c/main.jpg - цей шось лагає
# 3. https://content-media.bonial.biz/ae8a8c75-3e3a-48e5-93f9-dfd56387f329/main.jpg 
# 4. https://content-media.bonial.biz/c6552e4b-a73d-4684-af7e-c00cee0f918f/main.jpg
# 5. https://content-media.bonial.biz/c7b603da-16f4-42db-acf1-44914d7b0b7c/main.jpg

