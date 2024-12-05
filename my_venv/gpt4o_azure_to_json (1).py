import openai
# from text_prompts_txt import offer_without_price
# from text_prompts_txt import deposit_price
from text_prompts_txt import one_old_and_one_new_price
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


prompt = one_old_and_one_new_price

image_path = "https://content-media.bonial.biz/6d48e46c-7e2c-4a3c-951a-e9c376d2e722/main.jpg"

response = chat_with_gpt4(prompt, image_path)

print(response) 



# one_old_and_one_new_price
#     1. https://content-media.bonial.biz/0e24b535-05e8-4c03-8170-6ec0f368739a/main.jpg
# 1. https://content-media.bonial.biz/4913cf4d-0d96-41b0-8a9b-6d6ff9859494/main.jpg
# 2. https://content-media.bonial.biz/12c967dc-8239-4782-b075-8db6468c4ae4/main.jpg
# 3. https://content-media.bonial.biz/6d48e46c-7e2c-4a3c-951a-e9c376d2e722/main.jpg — бутилка
# 4. https://content-media.bonial.biz/07049ca0-0a50-4725-ba5b-6cdd466c708a/main.jpg
# 5. https://content-media.bonial.biz/cf785f31-0068-48e8-a821-260f54d3f0f5/main.jpg
# 6. https://content-media.bonial.biz/567fff20-3557-420b-8dde-dd96749ec7fe/main.jpg
# 7. https://content-media.bonial.biz/3e6cc52b-e8c7-4620-8c1a-21a14953d7d5/main.jpg
# 8. https://content-media.bonial.biz/63cf5b7a-d495-4338-96bf-bacf203f57f9/main.jpg
# 9. https://content-media.bonial.biz/00797340-4897-47da-bace-3bcc114ca2ae/main.jpg


