import openai
import base64
# from text_prompts_txt import simple_offers
# from product_prompts import simple_offers
from text_prompts_txt import simple_offers

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_base = "https://bonial-openai-test-004.openai.azure.com/"
openai.api_key = "3d337d2d785d4840b9ae45ebfc4faee5"

 
def chat_with_gpt4(prompt, image_path,  model="bonial-gpt-4o", max_tokens=4096):
    try:
        with open(image_path, 'rb') as image_file:
            image_path = base64.b64encode(image_file.read()).decode('utf-8')

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
                               "type": "image",
                               "image": image_path
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

prompt = simple_offers

image_path = "/Users/admin/Desktop/claud_sonet/Архів (1)/shampan_.jpg"

response = chat_with_gpt4(prompt, image_path)
print(response)
