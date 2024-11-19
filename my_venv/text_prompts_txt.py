prompt_models = {
    'simple_offers': 'gpt',
    'two_products_in_one_offer': 'gpt',
    'default': 'claude'
}

beverage = """
# Special rules for products:
Instructions for wine:
A "brand" and "product_brand" is usually the name of the house of wine or the region where the wine is produced (not the country). This information is on the bottle label.
If there is no product name, you should specify the wine type in "product_name" and "name" parameter: "Rotwein" or "Weißwein".
The wine name and brand cannot be repeated in the "product_description".
If the name of the winery (brand) is absent, do not record the brand name.
If the name of the drink is absent, record its type (red, white, sparkling, etc.) in the "product_name".
The place of origin of the drink should be included in the "product_description".

"""

simple_offers = """
# Your Role:
You are a useful assistant for extracting product information from a given image.              

# Output Format:
{
  "main_format":{
    "product_brand": "",
    "product_description": "",
    "product_name": "",
    "product_sku": "",
    "product_Product_category": "",
    "deal_1": [
        {
        "deal_conditions": "",
        "deal_currency": "",
        "deal_description": "",
        "deal_frequency": "",
        "deal_maxPrice": "",
        "deal_minPrice": "",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "",
        "deal_type": ""
        }
    ]
  },
  "additional_format": {
    "products": [
        {
          "product_id": "1",
          "brand": "",
          "name": "",
          "details": {
            "unit_size": "",
            "bundle_size": "",
            "deposit": "",
            "origin_country": "",
            "product_description": ""
          },
          "is_product_family": ""
        }
    ],
    "deals": [
      {
        "deal_id": "1",
        "type": "",
        "pricing": "",
        "price_type": "",
        "requirements": {
          "terms_and_conditions": "",
          "loyalty_card": "",
          "validity_period": ""
        },
        "details": {
          "price_by_base_unit": "",
          "discount": "",
          "deal_description": ""
        },
        "applied_to": "product-id",
        "is_deal_family": ""
      }
    ]
  }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
"deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

IMPORTANT!!!
If the product name contains the word (oder) or (Versch.Sorten.), split it into two separate products. Fill in the parameters for each product, including unique `product_id` and `deal_id` with their own deal_1 and deal_2

Important rule for the "main_format":
The "product_description" CANNOT contain information that is present in other json parameters.
IMPORTANT RULE: A unit price value, e.g. "1 kg = 4.28", "1 l = € 1.33", "1 kg = 11.84/ATG", "5.20/Liter", cannot be recorded in the "product_description" if the unit price value is already present in the "deal_pricebybaseunit".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES_PRICE" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

""" + beverage + """

# Rule of the highest rank for "main_format" and "additional_format":
The values and words of one of the json parameters cannot be repeated in other json parameters.
All textual information present in the image should be written to the appropriate json parameters.
Each new line ("\n".) of the "product_description" parameter should correspond to a new line ("\n".) in the text in the offer image.
Your answer should be purely json, without any additional explanation such as "```json", for example.
A product characteristic such as "Im Aufsteller", "Vegan" or "Organic" CANNOT be recorded in the "product_name", "name", "product_brand", "brand".
Rule: It is allowed to enter a value in "deal_pricebybaseunit" and "price_by_base_unit" only if the text between the unit of measurement and the price contains the symbol "=", otherwise the value will be "Null".

# General instructions for "main_format" and "additional_format":
The unit price (for example: "1 kg = 15.98", "1 l = 19.93") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

"deal_description" can only contain:
- the description of the possibility of ordering goods online (for example: "nur online", "auch online".),
- the validity period of the deal (e.g. "ab Donnerstag, 1.2")

"price_type" and "deal_type" should always be "SALES_PRICE".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
All characters (for example: "*") present in the product name or brand must be recorded.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
"product_brand" and "brand" must be written in full.
"product_name" and "name" must be written in full.
The size of the product, its quantity, or the size of the package (for example: "3er-Pack", "2 SCHALEN", "4 FLASCHEN") cannot be recorded in the "product_name" and "name".
The word "Metzgerfrisch" will always mean "product_brand", "brand".
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.

"""

# Prompts for German offers

# simple_offers = """
# # Your Role:
# You are a useful assistant for extracting product information from a given image.              

# # Output Format:
# {
#   "main_format":{
#     "product_brand": "",
#     "product_description": "",
#     "product_name": "",
#     "product_sku": "",
#     "product_Product_category": "",
#     "deal_1": [
#         {
#         "deal_conditions": "",
#         "deal_currency": "",
#         "deal_description": "",
#         "deal_frequency": "",
#         "deal_maxPrice": "",
#         "deal_minPrice": "",
#         "deal_pricebybaseunit": "",
#         "deal_loyaltycard": "",
#         "deal_type": ""
#         }
#     ]
#   },
#   "additional_format": {
#     "products": [
#         {
#           "product_id": "1",
#           "brand": "",
#           "name": "",
#           "details": {
#             "unit_size": "",
#             "bundle_size": "",
#             "deposit": "",
#             "origin_country": "",
#             "product_description": ""
#           },
#           "is_product_family": ""
#         }
#     ],
#     "deals": [
#       {
#         "deal_id": "1",
#         "type": "",
#         "pricing": "",
#         "price_type": "",
#         "requirements": {
#           "terms_and_conditions": "",
#           "loyalty_card": "",
#           "validity_period": ""
#         },
#         "details": {
#           "price_by_base_unit": "",
#           "discount": "",
#           "deal_description": ""
#         },
#         "applied_to": "product-id",
#         "is_deal_family": ""
#       }
#     ]
#   }
# }

# # Instructions for "main_format":
# If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
# "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
# "product_name" cannot contain the words from "product_description" and "product_brand".
# "product_brand" cannot contain the words from "product_name" and "product_description".
# The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
# "product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
# "product_name" always has a value.
# "deal_loyaltycard" can only have "true" or "false" values.
# "product_sku" is the serial number of the product.
# "product_sku" cannot be duplicated in the "product_description".
# For "product_product_category", define a product category like Google product category does.
# For "product_product_category", the result must be in German language.
# "deal_frequency" always has the value "ONCE".
# "deal_conditions" must contain only the terms and conditions to activate the discounted price.
# "deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
# The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
# The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Important rule for the "main_format":
# The "product_description" CANNOT contain information that is present in other json parameters.
# IMPORTANT RULE: A unit price value, e.g. "1 kg = 4.28", "1 l = € 1.33", "1 kg = 11.84/ATG", "5.20/Liter", cannot be recorded in the "product_description" if the unit price value is already present in the "deal_pricebybaseunit".

# # Instructions for "additional_format":
# If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
# "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
# "name" cannot contain the words from "product_description" and "brand".
# "brand" cannot contain the words from "name" and "product_description".
# "name" always has a value.
# "name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
# "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
# "unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
# "type" can only have "SALES" by default.
# "bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
# "deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
# "terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
# "validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
# "price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
# "discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
# An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
# - General information about the product family.
# - Specific information about the member products belonging to the product family.
# In this case:
# - Add the product family as an individual product and set "is_product_family" to true.
# - If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
#   add an individual family deal applied to only the product family and set "is_deal_family" to true.
# Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
# The "pricing" entry must always follow the format f"{value:.2f}".

# # Rule of the highest rank for "main_format" and "additional_format":
# The values and words of one of the json parameters cannot be repeated in other json parameters.
# All textual information present in the image should be written to the appropriate json parameters.
# Each new line ("\n".) of the "product_description" parameter should correspond to a new line ("\n".) in the text in the offer image.
# Your answer should be purely json, without any additional explanation such as "```json", for example.
# A product characteristic such as "Im Aufsteller", "Vegan" or "Organic" CANNOT be recorded in the "product_name", "name", "product_brand", "brand".
# Rule: It is allowed to enter a value in "deal_pricebybaseunit" and "price_by_base_unit" only if the text between the unit of measurement and the price contains the symbol "=", otherwise the value will be "Null".

# # General instructions for "main_format" and "additional_format":
# The unit price (for example: "1 kg = 15.98", "1 l = 19.93") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
# When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

# "deal_description" can only contain:
# - the description of the possibility of ordering goods online (for example: "nur online", "auch online".),
# - the validity period of the deal (e.g. "ab Donnerstag, 1.2")

# "price_type" and "deal_type" should always be "SALES_PRICE".
# The output json should contain only the text that is present in the input image in its original form, without changes or additions.
# All characters (for example: "*") present in the product name or brand must be recorded.
# If there is no data for the parameter, then indicate "Null".
# The value "Null" must always be capitalized.
# The text from the image must be clearly written into the corresponding parameter without errors.
# It is forbidden to add text to the json that is not in the image.
# "product_brand" and "brand" must be written in full.
# "product_name" and "name" must be written in full.
# The size of the product, its quantity, or the size of the package (for example: "3er-Pack", "2 SCHALEN", "4 FLASCHEN") cannot be recorded in the "product_name" and "name".
# The word "Metzgerfrisch" will always mean "product_brand", "brand".
# The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
# The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.

# """

simple_offers_client_ocr = (
    """

Input:
Vegan
2.00
KNALLER
(1 kg = 13.33)
je 150-g-Schale
Pfannengenuß
oder Grill- &
Genießerscheiben
Simply V

Output:
{
    "product_brand": "Simply V",
    "product_description": "Vegan, je 150-g-Schale",
    "product_name": "Pfannengenuß oder Grill- & Genießerscheiben",
    "product_sku": "Null",
    "product_Product_category": "Vegane Lebensmittel",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.00,
        "deal_minPrice": 2.00,
        "deal_pricebybaseunit": "1 kg = 13.33",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """
)

simple_offers_our_ocr = (
    """

Input:
Deluxe Hibiskus SANSIBAR Delipa ORANGEN SAUCE mit Rosmarin Sansibar Deluxe Fruchtsoßen Versch . Sorten . Je 235/225 g 1 kg = 12.72 / 13.29 2.99 *

Output:
{
    "product_brand": "Sansibar Deluxe",
    "product_description": "Versch. Sorten, Hibiskus Delipa ORANGEN SAUCE mit Rosmarin, Je 235/225 g",
    "product_name": "Fruchtsoßen",
    "product_sku": "Null",
    "product_Product_category": "Soßen",
    "deal": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.99,
        "deal_minPrice": 2.99,
        "deal_pricebybaseunit": "1 kg = 12.72 / 13.29",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """
)

two_products_in_one_offer = """
# Your Role:
You are a useful assistant for extracting product information from a given image.             
You will be provided with images of two products.

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },
    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_name" must contain the full names of the two products written through the conjunction "oder".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
If the offer contains information about the country of origin, this information should be included in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
If the offer contains one price, then in "deal_1" you should specify the information related to the first product, in "deal_2" - the information related to the second product.
If the offer contains two prices, then in "deal_1" you should specify the information related to the first product, in "deal_2" - the information related to the second product and two additional deals, "deal_3" and "deal_4", respectively, with deal_type: "REGULAR_PRICE" or "RECOMMENDED_RETAIL_PRICE".
"deal_maxPrice" and "deal_minPrice" cannot have the value "Null", if there is a price for "deal_1" and no price for "deal_2", then "deal_maxPrice" and "deal_minPrice" must have the same value as "deal_maxPrice" and "deal_minPrice" in "deal_1".
"deal_description" should always have the value of the product name.
"deal_description" should contain only the name of the product to which the particular "deal_1" or "deal_2" relates."
The word "oder" differentiates between two product names, for example: "Pfirsich- oder Birnenhälften". Then "Pfirsich" is "deal_1", and "Birnenhälften" is "deal_2".
The "deal_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (for example: "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (for example: "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
The "name" cannot be duplicated in the "deal_description".
"name" always has a value.
The input image always shows two products, so the output json should always contain two "product" and two "deal".
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
If the offer contains one price, then in "product_id": "1" - information related to the first product, in "product_id": "2" - information related to the second product, in "product_id": "3" - information related to the third product.
If the offer contains two prices, "product_id": "1" should contain the information relating to the first product, "product_id": "2" the information relating to the second product, and two additional transactions, "deal_3" and "deal_4", as well as "deal_5" and "deal_6" respectively, with the transaction type: "REGULAR_PRICE" or "RECOMMENDED_RETAIL_PRICE".
For offers with multiple products separated by "oder," assign each product a unique product_id with deal_type: REGULAR_PRICE; if only one price is listed, apply it to all products, and if two prices are available, assign both SALES_PRICE and REGULAR_PRICE to each product.
There may be a case where there are more than two products, e.g.:
"Seductive oder Red oder Kiss oder Noir". Then "Seductive is "product_id": "1", and "Red" is "product_id": "2", and "Noir" is "product_id": "3". 
"pricing" cannot have a value of “Null”, if there is a price for “product_id”: “1” and no price for “product_id”: “2”, and no price for “product_id”: “3”,then “pricing” must have the same value as “pricing” in “product_id”: “1”.
If each product has two prices, then two "deals" are required for each product.
The "price_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE"."
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing"" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (for example: "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "BUNDLE" by default.
"bundle_size" must contain only the size information about the bundle (for example: "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (for example: 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (for example: "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (for example: "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (for example: "Sie sparen 50%", "-50%").
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
There are always two products in an offer image.
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
The text and product description always mention two product names.
All information contained in the offer description must be written to the appropriate json parameters.
Descriptive characteristics of a product, such as geographic origin, quality, or product features, should not be confused with brand names, as they are general attributes rather than unique identifiers of a particular brand.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".



# High priority Instructions for "main_format" and "additional_format":

The "product_description" CANNOT contain information that is present in other json parameters.
IMPORTANT RULE: A unit price value, for example: "(1 kg = 13.09)", "1 kg = 4.28", "1 l = € 1.33", "1 kg = 11.84/ATG", "5.20/Liter", CANNOT be recorded in the "product_description".
json can contain at least 2 "deals".
The conjunction "oder" clearly separates the name for the first and second product, it is forbidden to enter two names with the conjunction "oder" in any of the parameters.
The number of "deal" in the "main_format" must be the same as "deals" in the "additional_format".
The main difference between "main_format" and "additional_format" is that in "additional_format" the "deal_description" field CANNOT contain the product name, but in "main_format" the "deal_description" field can contain the product name. Strictly follow this rule.
Instructions for "main_format" cannot be applied to Instructions for "additional_format".

IMOORTANT
If there are more than two products listed with the word "oder" in the image, be sure to include each of them in the product listing. Each product must provide a full description and information about the actions, in accordance with the established rules.
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description "**.
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **record in "deal_pricebybaseunit"**.

# Exception:
The values and words of one of the json parameters cannot be repeated in other json parameters, except for:
In "main_format" the "deal_description" field can contain the product name.

FINAL CHECK:
Make sure that the unit price (for example: "1 kg = 4.28", "1 l = € 1.33", "1 kg = 11.84/ATG", "5.20/Liter", "(1 kg = 11.99)") is not in the "product_description" parameter. If somehow the unit price is included in the "product_description", this information should be removed from "product_description".
Make sure that the "product_description" parameter does not contain the product price (for example: "ab 2.89", "je 24,95", "22.99", "2,34"). If somehow the price of the product got into the "product_description", it should be removed from the "product_description".

"""

two_products_in_one_offer_client_ocr = (

    """
Input:
Waterdrop
Microdrink
Sky
je 24 g Pckg.
(1 kg = 249.58)
oder Microdrink
Flair
je 26,4 g Pckg.
(1 kg = 226.89)
Aktion
5.99

Output:

{
    "product_brand": "Waterdrop",
    "product_description": "je 24 g Pckg., je 26,4 g Pckg.",
    "product_name": "Microdrink",
    "product_sku": "Null",
    "product_Product_category": "Sirup",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Sky",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 5.99,
        "deal_minPrice": 5.99,
        "deal_pricebybaseunit": "(1 kg = 249.58)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Flair",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 5.99,
        "deal_minPrice": 5.99,
        "deal_pricebybaseunit": "(1 kg = 226.89)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

  """
)

two_products_in_one_offer_our_ocr = """
Input:
x 12 FORTIONEN FLAIR 88 water MICRO GETRÄNKEWORFEL HIMBEERE HOLUNDERBLOTE Waterdrop Microdrink Sky , je 24 - g - Pckg . ( 1 kg = 249.58 ) oder Microdrink Flair , je 26,4 - g - Pckg . ( 1 kg = 226.89 ) BET OHNE ZUCKER SKY x12 ANANASERDBEERE OHNE PASSIONSFRUCHT ZUCKER waterdrop MICRODRINK GETRÄNKEWÜRFEL MIT VITAMINEN VAX Aktion 5.99

Output:

{
    "product_brand": "Waterdrop",
    "product_description": "x 12 FORTIONEN FLAIR 88 water MICRO GETRÄNKEWORFEL HIMBEERE HOLUNDERBLOTE, ANANASERDBEERE OHNE PASSIONSFRUCHT ZUCKER, GETRÄNKEWÜRFEL MIT VITAMINEN VAX, je 24 g Pckg., je 26,4 g Pckg.",
    "product_name": "Microdrink",
    "product_sku": "Null",
    "product_Product_category": "Sirup",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Sky",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 5.99,
        "deal_minPrice": 5.99,
        "deal_pricebybaseunit": "(1 kg = 249.58)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Flair",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 5.99,
        "deal_minPrice": 5.99,
        "deal_pricebybaseunit": "(1 kg = 226.89)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
BACARDÍ \n Tropical , Coconut , ** jeweils 32 % vol oder \n Carta Blanca \n 37,5 % vol , \n je 0,7 - Liter Flasche ( 1 Liter = 14.27 ) \n WHITE RUM \n 401 \n -SUPERIOR WHITE REI \n BACAR BACAR BACARDI \n COCONUT \n CARTA BLAN \n TROPICAL \n ESTABLECIDO EN EMPRESA DE \n FAMILIA \n SEX NATUREL COCOSET \n COCONUT \n BACARDI B \n F1862 1862 18628 \n EMPR \n • MADE FOR NITI \n EMPRE \n ANANDATORAL FLAVOURS \n MADE FOR NIXING \n MIX THE TROPICAL \n FOR A DESTIN \n LIDERK \n Mi , 27.12 9.99 \n UVP 13.99 \n -28 % \n

Output:
{
    "product_brand": "BACARDÍ",
    "product_description": "Tropical, Coconut, jeweils 32 % vol, 37,5 % vol, je 0,7 - Liter Flasche",
    "product_name": "BACARDÍ",
    "product_sku": "401",
    "product_Product_category": "Rum",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mi, 27.12",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 9.99,
        "deal_minPrice": 9.99,
        "deal_pricebybaseunit": "(1 Liter = 14.27)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Carta Blanca, Mi, 27.12",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 9.99,
        "deal_minPrice": 9.99,
        "deal_pricebybaseunit": "(1 Liter = 14.27)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "Null",
        "deal_maxPrice": 13.99,
        "deal_minPrice": 13.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}


    """

one_product_with_coupon = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                    "deal_id": "2",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
The "product_description" cannot contain the product name, brand or unit price.
All information present in the image should be written to the appropriate json parameters.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and this information must recorded in "deal_conditions".
"deal" with "deal_type": "SALES_PRICE" should contain the price of a sales price (for example: "ohne PENNY App") and this information must recorded in "deal_conditions".
"deal_loyaltycard" can only have "true" or "false" values.
For "deal_1", "deal_loyaltycard" can only have "true" by default.
For "deal_2", "deal_loyaltycard" can only have "false" by default.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "SPECIAL_PRICE" for "deal_2".
"deal_2" should contain information related to the coupon.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and this information must recorded in "terms_and_conditions".
"deal" with "price_type": "SALES_PRICE" should contain the price of a sales price (for example: "ohne PENNY App") and this information must recorded in "terms_and_conditions".
For "deal_id": "1", "loyalty_card" can only have "true" by default.
For "deal_id": "2", "loyalty_card" can only have "false" by default.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and "SPECIAL_PRICE" for "deal_id": "2".
"deal_id": "2" should contain information related to the coupon.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Preis mit App Coupon", "Nur mit der App").
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

"""

one_product_with_coupon_client_ocr = (

    """
Input:
Coupon
App
mit
Preis
3.49
Knaller
3.29
(1 kg = 7.83)
(1 kg = 8.31)
je 420-g-Pckg.
versch. Sorten,
Fertiggericht
Internationales
Youcook

Output:
{
    "product_brand": "Youcook",
    "product_description": "versch. Sorten, je 420-g-Pckg.",
    "product_name": "Internationales Fertiggericht",
    "product_sku": "Null",
    "product_Product_category": "Fertiggerichte",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.49,
        "deal_minPrice": 3.49,
        "deal_pricebybaseunit": "(1 kg = 8.31)",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Preis mit App Coupon",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.29,
        "deal_minPrice": 3.29,
        "deal_pricebybaseunit": "(1 kg = 7.83)",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
}

    """
)

one_product_with_coupon_our_ocr = (

    """
Input:
REWE Beste Wahl Deutschland : Weiße Champignons Kl . I , je 250 - g - Schale ( 1 kg = 5.56 ) Preis mit App Coupon Knaller 139 129 ( 1 kg = 5.16 )

Output:
{
    "product_brand": "REWE Beste Wahl",
    "product_description": "Deutschland, Kl. I, je 250-g-Schale",
    "product_name": "Weiße Champignons",
    "product_sku": "Null",
    "product_Product_category": "Gemüse",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.39,
        "deal_minPrice": 1.39,
        "deal_pricebybaseunit": "(1 kg = 5.56)",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Preis mit App Coupon",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.29,
        "deal_minPrice": 1.29,
        "deal_pricebybaseunit": "(1 kg = 5.16)",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
}

    """
)

two_products_with_coupon = """
# Your Role:
You are a useful assistant for extracting product information from a given image.             
You will be provided with images of two products with coupon.

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_3": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },
    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            },
            {
                "product_id": "2",
                "brand": "",
                "name": "",
                "details": {
                  "unit_size": "",
                  "bundle_size": "",
                  "deposit": "",
                  "origin_country": "",
                  "product_description": ""
                },
                "is_product_family": ""
              }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                    "deal_id": "2",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  },
                  {
                    "deal_id": "3",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  }
          ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
In "deal_1" you should specify the information related to the first product, in "deal_2" - the information related to the second product.
"deal_description" should contain only the name of the product to which the particular "deal_1" or "deal_2" relates."
The word "oder" differentiates between two product names, for example: "Pfirsich- oder Birnenhälften". Then "Pfirsich" is "deal_1", and "Birnenhälften" is "deal_2".
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
For "deal_1" and "deal_2", "deal_loyaltycard" can only have "true" by default.
For "deal_3", "deal_loyaltycard" can only have "false" by default.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "deal_2", "SPECIAL_PRICE" for "deal_3".
"deal_3" should contain information related to the coupon.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and this information must recorded in "deal_conditions".
"deal" with "deal_type": "SALES_PRICE" should contain the price of a sales price (for example: "ohne PENNY App") and this information must recorded in "deal_conditions".
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Preis mit App Coupon").
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
The "name" cannot be duplicated in the "deal_description".
"name" always has a value.
The input image always shows two products, so the output json should always contain two "product" and two "deal".
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
In "product" where is "product_id": "1" you should specify the information related to the first product, in "product" where is "product_id": "2" - the information related to the second product.
The word "oder" differentiates between two product names, for example: "Pfirsich- oder Birnenhälften". Then "Pfirsich" is "product_id": "1", and "Birnenhälften" is "product_id": "2".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For "deal_id": "1" and "deal_id": "2", "loyalty_card" can only have "true" by default.
For "deal_id": "3", "loyalty_card" can only have "false" by default.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and "deal_id": "2", "SPECIAL_PRICE" for "deal_id": "3".
"deal_id": "3" should contain information related to the coupon.
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and this information must recorded in "terms_and_conditions".
"deal" with "price_type": "SALES_PRICE" should contain the price of a sales price (for example: "ohne PENNY App") and this information must recorded in "terms_and_conditions".
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "BUNDLE" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Preis mit App Coupon").
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:

The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
The text and product description always mention two product names.
All information present in the image should be written to the appropriate json parameters.
Descriptive characteristics of a product, such as geographic origin, quality, or product features, should not be confused with brand names, as they are general attributes rather than unique identifiers of a particular brand.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.

# Exception:
The values and words of one of the json parameters cannot be repeated in other json parameters, except for:
In "main_format" the "deal_description" field can contain the product name.

# High priority Instructions for "main_format" and "additional_format":
The main difference between "main_format" and "additional_format" is that in "additional_format" the "deal_description" field CANNOT contain the product name, but in "main_format" the "deal_description" field can contain the product name. Strictly follow this rule.
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "deal_description".
Instructions for "main_format" cannot be applied to Instructions for "additional_format".


"""

two_product_with_coupon_client_ocr = (

    """
Input:
Jim Beam
Kentucky Straight
Bourbon Whiskey
40% Vol.
oder Honey
32,5% Vol.,
je 0,7-l-Fl.
(1 l = 15.70)
Knaller
10.99
Preis
mit
App
Coupon
10.49
(1 l = 14.99)

Output:
{
    "product_brand": "Jim Beam",
    "product_description": "je 0,7-l-Fl., je 0,7-l-Fl., 40% Vol, 32,5% Vol.",
    "product_name": "Kentucky Straight Bourbon Whiskey oder Honey",
    "product_sku": "Null",
    "product_Product_category": "Whiskey",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Kentucky Straigh Bourbon Whiskey",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 10.99,
        "deal_minPrice": 10.99,
        "deal_pricebybaseunit": "(1 l = 15.70)",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Honey",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 10.99,
        "deal_minPrice": 10.99,
        "deal_pricebybaseunit": "(1 l = 15.70)",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Preis mit App Coupon",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 10.49,
        "deal_minPrice": 10.49,
        "deal_pricebybaseunit": ""(1 l = 14.99)"",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
}

    """

)

two_product_with_coupon_our_ocr = (

    """
Input:

Coppenrath & Wiese Unsere Goldstücke 9 Weizenbrötchen \n tiefgefroren , \n je 450 - g - Btl . \n ( 1kg = 3.09 ) \n Unsen \n Goldstad \n 9 \n oder Unsere Goldstücke \n 9 Baguette - Brötchen \n tiefgefroren , \n Je 540 - g - Btl . ( 1 kg = 2.57 ) \n Ub \n Goldsti \n Broche \n Preis mit App Coupon \n Knaller \n 1.39 119 \n ( 1 kg = 2.64 / 2.20 ) \n

Output:
{
    "product_brand": "Coppenrath & Wiese",
    "product_description": "tiefgefroren, je 450-g-Btl., je 540-g-Btl.",
    "product_name": "Unsere Goldstücke 9 Weizenbrötchen",
    "product_sku": "Null",
    "product_Product_category": "Backwaren",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Unsere Goldstücke 9 Weizenbrötchen",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.39,
        "deal_minPrice": 1.39,
        "deal_pricebybaseunit": "(1 kg = 3.09)",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Unsere Goldstücke 9 Baguette-Brötchen",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.39,
        "deal_minPrice": 1.39,
        "deal_pricebybaseunit": "(1 kg = 2.57)",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Preis mit App Coupon",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.19,
        "deal_minPrice": 1.19,
        "deal_pricebybaseunit": "(1 kg = 2.64/2.20)",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
}

    """

)

several_products_with_different_prices = """
# Your Role:
You are a useful assistant for extracting product information from a given image.             
You will receive an image of the offer of several products.

# Output Format:
Not include any extra text, comments, or explanations outside of the JSON
Follow the specified JSON structure exactly:
{
    "main_format":
    {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
          "deal_1": {
        "deal_conditions": "Null",
        "deal_currency": "€",
        "deal_description": "mit Stauraum, ca. 175x145 cm, 90 cm hoch",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "499.00",
        "deal_minPrice": "499.00",
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
    },
    "deal_2": {
        "deal_conditions": "Null",
        "deal_currency": "€",
        "deal_description": "mit Stauraum, ca. 175x145 cm, 90 cm hoch",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "919.00",
        "deal_minPrice": "919.00",
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
    },
    "deal_3": {
        "deal_conditions": "Null",
        "deal_currency": "€",
        "deal_description": "mit fester Platte, ca. 80x120 cm, 75 cm hoch",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "299.00",
        "deal_minPrice": "299.00",
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
    },
    "deal_4": {
        "deal_conditions": "Null",
        "deal_currency": "€",
        "deal_description": "mit fester Platte, ca. 80x120 cm, 75 cm hoch",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "519.00",
        "deal_minPrice": "519.00",
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
    },
    "deal_5": {
        "deal_conditions": "Null",
        "deal_currency": "€",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "79.00",
        "deal_minPrice": "79.00",
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
    },
    "deal_6": {
        "deal_conditions": "Null",
        "deal_currency": "€",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "129.00",
        "deal_minPrice": "129.00",
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
    }
    },
    "additional_format": {
        "products": [
                {
                    "product_id": "1",
                    "brand": "",
                    "name": "",
                    "details": {
                    "unit_size": "",
                    "bundle_size": "",
                    "deposit": "",
                    "origin_country": "",
                    "product_description": ""
                    },
                    "is_product_family": ""
                }
            ],
            "deals": [
                {
                    "deal_id": "1",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                    },
                    "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                }
            ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Clearly define how many prices and products there are in the offer, and create a "deal" for each price and product.
Each "deal" should have its own key, for example "deal_1", "deal_2", "deal_3" and so on.
"deal_description" should contain a description of the product, excluding its name and brand.
If the text of the offer contains several brand and names, then they should be written in the "product_brand" and "product_name" using the conjunction "oder".
The description that applies to all products should be recorded in the "product_description", but the description of a specific product should be recorded in the "deal_description" of the corresponding deal. It is forbidden to write a description of a specific product in the "product_description".
If the offer has two prices for each product, such as "uvp", old strikethrough price, or "statt", then the product description is written in the "deal" where the "deal_type": "SALES_PRICE" is present.
The "product_description" cannot contain the words from "product_name", "product_brand", "deal_description" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description", "deal_description" and "product_brand".
"product_brand" cannot contain the words from "product_name", "deal_description" and "product_description".
"deal_description" cannot contain the words from "product_name", "product_description" and "product_brand".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
The "deal_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE"."
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
The "name" cannot be duplicated in the "deal_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
The "additional_format" array can contain several products and several deals.
If each product has two prices, then two "deals" are required for each product.
The "price_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE"."
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "price_type": "SALES_PRICE".
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:

The number of "deal" in the "main_format" must be the same as in the "additional_format".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
All information present in the image should be written to the appropriate json parameters.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" and "deal_description" parameters, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
If there is a price that is crossed out in the image, be sure to write it to the corresponding parameter in JSON format. The crossed-out price should be written to the corresponding 'deal', where 'deal_type': 'REGULAR_PRICE'. This ensures that all old (crossed out) prices are correctly displayed in the result.
be sure to record each offer in a separate deal


# Rule of the highest rank:
The values and words of one of the json parameters cannot be repeated in other json parameters.

# High priority Instructions for "main_format" and "additional_format":
The output json should not contain syntax errors.
Instructions for "main_format" cannot be applied to Instructions for "additional_format".

"""

several_products_with_different_prices_client_ocr = (

    """
Input:

Federkern
ohne Zierkissen
(oder ab 12.50 € mtl. RateF1)
30.70
72 × mtl. ab
Finanzkauf 3)
2049.--21 %
1599.-
999.99
1289.-
Kopfteil','0426001677
stufenlos verstellbares
Sessel*
ohne Abbildung
0426006177
ca. 303 x 245 cm,
Stoff mandel','Stellfläche
Wohnlandschaft

Output:
[
    {
        "product_brand": "Null",
        "product_description": "stufenlos verstellbares, Kopfteil, ohne Zierkissen, Federkern",
        "product_name": "Sessel",
        "product_sku": "0426001677",
        "product_Product_category": "Möbel",
        "deal_1": [
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 999.99,
                "deal_minPrice": 999.99,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "SALES_PRICE"
            }
        ],
        "deal_2": [
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 1289.0,
                "deal_minPrice": 1289.0,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "REGULAR_PRICE"
            }
        ]
    },
    {
        "product_brand": "Null",
        "product_description": "Stoff mandel, Stellfläche, ca. 303 x 245 cm, Finanzkauf 3) 72 × mtl. ab 30.70",
        "product_name": "Wohnlandschaft",
        "product_sku": "0426006177",
        "product_Product_category": "Möbel",
        "deal_1": [
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 1599.0,
                "deal_minPrice": 1599.0,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "SPECIAL_PRICE"
            }
        ],
        "deal_2": [ 
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 2049.0,
                "deal_minPrice": 2049.0,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "REGULAR_PRICE"
            }
        ]
    }
],

Input:
5052312/00 49.-
ca. 140 x 200 cm
passender Topper
ohne Topper
ohne Deko
inkl. Bonellfederkernmatratze
299.-
mtl. RateF1
€
oder ab 9 
5052311/00
schwarz','Liegefläche ca. 140 x 200 cm
Boxspringbett
111.-
5091140/00
ca. 170 x 195 x 59 cm
weiß','2-türig. B/H/T:
Schwebetürenschrank

Output:
[
  {
      "product_brand": "Null",
      "product_description": "weiß, 2-türig. B/H/T: ca. 170 x 195 x 59 cm",
      "product_name": "Schwebetürenschrank",
      "product_sku": "5091140/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 111.0,
          "deal_minPrice": 111.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "schwarz, Liegefläche ca. 140 x 200 cm, inkl. Bonellfederkernmatratze, ohne Topper, ohne Deko",
      "product_name": "Boxspringbett",
      "product_sku": "5052311/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 299.0,
          "deal_minPrice": 299.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "ca. 140 x 200 cm",
      "product_name": "passender Topper",
      "product_sku": "5052312/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 49.0,
          "deal_minPrice": 49.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  }
]

    """

)

several_products_with_different_prices_our_ocr = (

    """
Input:

ohne Abbildung Sessel * \n stufenlos verstellbares \n Kopfteil , 0426001677 1289.- 999.99 \n ohne Zierkissen \n Federkern \n RAL \n (oder ab 12.50 € mtl. RateF1) \n GÜTEZEICHEN \n M \n Möbel \n Gibt's doch gar nicht . \n DOCH BEI ROLLER ! \n Wohnlandschaft Stoff mandel , Stellfläche ca. 303 x 245 cm , 0426006177 \n -21 % \n 2049. \n 1599. \n Finanzkauf 3 ) 72 x mtl . ab 30,70 \n

Output:
[
    {
        "product_brand": "Null",
        "product_description": "stufenlos verstellbares, Kopfteil, ohne Zierkissen, Federkern",
        "product_name": "Sessel",
        "product_sku": "0426001677",
        "product_Product_category": "Möbel",
        "deal_1": [
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 999.99,
                "deal_minPrice": 999.99,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "SALES_PRICE"
            }
        ],
        "deal_2": [
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 1289.0,
                "deal_minPrice": 1289.0,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "REGULAR_PRICE"
            }
        ]
    },
    {
        "product_brand": "Null",
        "product_description": "Stoff mandel, Stellfläche, ca. 303 x 245 cm, Finanzkauf 3) 72 × mtl. ab 30.70",
        "product_name": "Wohnlandschaft",
        "product_sku": "0426006177",
        "product_Product_category": "Möbel",
        "deal_1": [
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 1599.0,
                "deal_minPrice": 1599.0,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "SPECIAL_PRICE"
            }
        ],
        "deal_2": [ 
            {
                "deal_conditions": "Null",
                "deal_currency": "EUR",
                "deal_description": "Null",
                "deal_frequency": "ONCE",
                "deal_maxPrice": 2049.0,
                "deal_minPrice": 2049.0,
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "Null",
                "deal_type": "REGULAR_PRICE"
            }
        ]
    }
],

Input:
inkl . Lattenrost inkl . 3 Schlupfsprossen Beispiel Wandpaneel B / H / T : ca. 100 x 20 x 18 cm 5093989/00 59.99 Kleiderschrank 3 - türig , B / H / T : ca. 120 x 195 x 53 cm 5093985/00 419.99 ( oder ab 12.50 € mtl . Ratef¹ ) Babyzimmer Bolto Oak / Absetzungen arktisgrau Nachbildung Babybett Liegefläche ca. 70 x 140 cm B / H / T : ca. 107 x 94-104 x 79 cm 5093988/00 299.99 ( oder ab 9.00 € mtl . RateF1 ) Wickelkommode 5093986/00 WOW ! ab Server F ohne Auflage und Deko AM LAGER ! über 10.000 Artikel sofort zum Mitnehmen ! Babybett 229.9⁹ oder ab 9 € mtl . RateF1

Output:
[
  {
      "product_brand": "Null",
      "product_description": "Babyzimmer Bolto Oak / Absetzungen arktisgrau Nachbildung, inkl. Lattenrost, inkl. 3 Schlupfsprossen, Liegefläche ca. 70 x 140 cm",
      "product_name": "Babybett",
      "product_sku": "5093986/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 229.99,
          "deal_minPrice": 229.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "B / H / T : ca. 107 x 94-104 x 79 cm, ",
      "product_name": "Wickelkommode",
      "product_sku": "5093988/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "299.99",
          "deal_minPrice": "299.99",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "3 - türig , B / H / T : ca. 120 x 195 x 53 cm",
      "product_name": "Kleiderschrank",
      "product_sku": "5093985/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 419.99,
          "deal_minPrice": 419.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "B / H / T : ca. 100 x 20 x 18 cm",
      "product_name": "Wandpaneel",
      "product_sku": "5093989/00",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 59.99,
          "deal_minPrice": 59.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  }
]

    """

)

price_characterization_uvp = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                    "deal_id": "2",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
The "product_description" cannot contain the product name, brand or unit price.
All information present in the image should be written to the appropriate json parameters.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "RECOMMENDED_RETAIL_PRICE" for "deal_2".
"deal_2" should contain information related to the UVP price.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and "RECOMMENDED_RETAIL_PRICE" for "deal_id": "2".
"deal_id": "2" should contain information related to the UVP price.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
You do not need to enter the word "UVP" in any of the parameters.
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.

"""

price_characterization_uvp_client_ocr = (

    """
Input:
Inkl. Visco-Nackenstützkissen
Je Stück. Art.-Nr. 100360077
Modell „Pro Body S 592".
7-Zonen-Kaltschaum-Matratze
H3','B 90 x L 200 cm
Punktgenaue Entlastung/Komfort
Höhe: ca. 22 cm
Bezug abnehm- und waschbar (bei 60 °C)
Gesamtbetrag Finanzierung 294.72
24 MonateB à 12.28
(1 l = 2.76)
269.-
UVP 449.-
-40%

Output:
{
    "product_brand": "Null",
    "product_description": "Modell „Pro Body S 592". Höhe: ca. 22 cm, Bezug abnehm- und waschbar (bei 60 °C), Punktgenaue Entlastung/Komfort, Inkl. Visco-Nackenstützkissen, H3, B 90 x L 200 cm, Je Stück.",
    "product_name": "7-Zonen-Kaltschaum-Matratze",
    "product_sku": "100360077",
    "product_Product_category": "Matratzen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 269.0,
        "deal_minPrice": 269.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "1 l = 2.76",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449.0,
        "deal_minPrice": 449.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """
)

price_characterization_uvp_our_ocr = (

    """
Input:
breckle Inkl . Visco - Nackenstützkissen MADE DE IN GERMANY Höhe : ca. 22 cm 60 ° Bezug abnehm- und waschbar ( bei 60 ° C ) ск Punktgenaue Entlastung / Komfort 7 - Zonen - Kaltschaum - Matratze Modell ,, Pro Body S 592 " . Weitere Größen und weiterer Härtegrad erhältlich . Je Stück . Art.-Nr. 100360077 nur online H3 , B 90 x L200 cm -40 % UVP - 449. 269. 24 Monate à 12.28 Gesamtbetrag Finanzierung 294.72

Output:
{
    "product_brand": "Null",
    "product_description": "Je Stück., Modell „Pro Body S 592". Höhe: ca. 22 cm, Bezug abnehm- und waschbar (bei 60 °C), Punktgenaue Entlastung/Komfort, Inkl. Visco-Nackenstützkissen, H3, B 90 x L 200 cm",
    "product_name": "7-Zonen-Kaltschaum-Matratze",
    "product_sku": "100360077",
    "product_Product_category": "Matratzen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 269.0,
        "deal_minPrice": 269.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449.0,
        "deal_minPrice": 449.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """
)

price_characterization_statt = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                    "deal_id": "2",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
The "product_description" cannot contain the product name, brand or unit price.
All information present in the image should be written to the appropriate json parameters.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "REGULAR_PRICE" for "deal_2".
"deal_2" should contain information related to the "statt" price.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and 
"deal_type" should always be "SALES_PRICE" for "deal_1" and "REGULAR_PRICE" for "deal_id": "2".
"deal_id": "2" should contain information related to the "statt" price.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
You do not need to enter the word "statt" in any of the parameters.
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
"""

price_characterization_statt_client_ocr = (

    """
Input:
statt 499,99 €/Stück**
Stück
399,99*
** Unverbindliche Preisempfehlung.
Art.-Nr. 2568855
halterost','mit Flavorizer-Bars®-Aromaschienen
2-Brenner mit Crossover-Zündsystem','Seitenbrenner und Warm-
GASGRILL WEBER® „SPIRIT E-220 CLASSIC"

Output:
{
    "product_brand": "WEBER®",
    "product_description": "2-Brenner mit Crossover-Zündsystem, Seitenbrenner und Warmhalterost, mit Flavorizer-Bars®-Aromaschienen",
    "product_name": "SPIRIT E-220 CLASSIC GASGRILL",
    "product_sku": "2568855",
    "product_Product_category": "Grillgeräte",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 399.99,
        "deal_minPrice": 399.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 499.99,
        "deal_minPrice": 499.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
2+1
gratis!
Share
Nussriegel
versch. Sorten,
je 3 x 35-g-Riegel
(1 kg = 27,62)
Einzelpreis 1.45 €
je 35-g-Riegel
(1 kg = 41.43)
3 für nur
2.90
statt 4.35

Output:
{
    "product_brand": "Share",
    "product_description": "versch. Sorten, Einzelpreis 1.45 €, je 35-g-Riegel, (1 kg = 41.43), je 3 x 35-g-Riegel",
    "product_name": "Nussriegel",
    "product_sku": "Null",
    "product_Product_category": "Snacks",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "2+1 gratis!",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.90,
        "deal_minPrice": 2.90,
        "deal_pricebybaseunit": "(1 kg = 27.62)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 4.35,
        "deal_minPrice": 4.35,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """
)

price_characterization_statt_our_ocr = (

    """
Input:
heyOBI VORTEIL \n 399⁹⁹ * \n Stück \n statt 499,99 € / Stück ** \n weber \n SPIRIT \n GASGRILL WEBER® ,, SPIRIT E - 220 CLASSIC \" 2 - Brenner mit Crossover - Zündsystem , Seitenbrenner und Warm halterost , mit Flavorizer - Bars® - Aromaschienen Art.-Nr. 2568855 \n ** Unverbindliche Preisempfehlung . \n

Output:
{
    "product_brand": "WEBER®",
    "product_description": "2-Brenner mit Crossover-Zündsystem, Seitenbrenner und Warmhalterost, mit Flavorizer-Bars®-Aromaschienen",
    "product_name": "SPIRIT E-220 CLASSIC GASGRILL",
    "product_sku": "2568855",
    "product_Product_category": "Grillgeräte",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 399.99,
        "deal_minPrice": 399.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 499.99,
        "deal_minPrice": 499.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
2 + 1 \n gratis ! \n BIO \n Share \n Nussriegel versch . Sorten , je 3 x 35 - g - Riegel . ( 1 kg = 27,62 ) Einzelpreis 1.45 € je 35 - g - Riegel ( 1 kg = 41.43 ) \n share \n shtres \n REPORT \n share \n 3 für nur \n 290 \n + \n statt 4.35 \n

Output:
{
    "product_brand": "Share",
    "product_description": "versch. Sorten, Einzelpreis 1.45 €, je 35-g-Riegel, (1 kg = 41.43), je 3 x 35-g-Riegel",
    "product_name": "Nussriegel",
    "product_sku": "Null",
    "product_Product_category": "Snacks",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "2+1 gratis!",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.90,
        "deal_minPrice": 2.90,
        "deal_pricebybaseunit": "(1 kg = 27.62)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 4.35,
        "deal_minPrice": 4.35,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
Jever Pilsener , Light oder Fun Alkoholfrei \n Kasten 20 x 0,5 1 \n ( 11 = € 1,50 ) \n zzgl . € 3,10 Pfand oder \n Kasten 24 x 0,331 \n ( 11 = € 1,89 ) zzgl . € 3,42 Pfand \n 14.9⁹9 \n statt 16.99 12 % \n Friesisches \n Brauna , \n EN \n DE PRIME \n JEVER \n Friesisch - herb . \n FUN \n ALKOHOLFREI PILSENER \n JEVER JEVER \n FUN \n JEVER EVER EVER \n LSENER \n

Output:
{
    "product_brand": "JEVER",
    "product_description": "Light oder Fun Alkoholfrei, Friesisch-herb, zzgl . € 3,10 Pfand, zzgl . € 3,42 Pfand",
    "product_name": "Pilsener",
    "product_sku": "Null",
    "product_Product_category": "Alkoholische Getränke",
    "deal_1": [
      {
        "deal_conditions": "Kasten 20 x 0,5",
        "deal_currency": "EUR",
        "deal_description": "Light",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 14.99,
        "deal_minPrice": 14.99,
        "deal_pricebybaseunit": "(1l = € 1,50)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
      "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Kasten 24 x 0,331",
        "deal_currency": "EUR",
        "deal_description": "Fun Alkoholfrei",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 14.99,
        "deal_minPrice": 14.99,
        "deal_pricebybaseunit": "(1l = € 1,89)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """
)

special_prise = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If there are two prices in the offer, then 2 "deals" will be provided.
If there are three prices in the offer, then 3 "deals" will be provided.
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2", "deal_3" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and this information must recorded in "deal_conditions".
"deal" with "deal_type": "SALES_PRICE" should contain the price of a sales price (for example: "ohne PENNY App") and this information must recorded in "deal_conditions".
"deal_loyaltycard" can only have "true" or "false" values.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App").
For a "deal" where "deal_type" is "SALES_PRICE", "deal_loyaltycard" can only have the value "true" by default.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" "deal" with "deal_type": "SALES_PRICE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and this information must recorded in "terms_and_conditions".
"deal" with "price_type": "SALES_PRICE" should contain the price of a sales price (for example: "ohne PENNY App") and this information must recorded in "terms_and_conditions".
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"type" and "price_type" are different parameters, they cannot have the same values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
You do not need to enter the word "UVP" and "statt" in any of the parameters.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
"""

special_prise_client_ocr = (

    """
Input:
l .
Nur gültig mit
LIDL Plus
d)
3.88*
-32%
UVP 5.79
3.99*
-31%
AKTION
2
1 l .
l
Je 0
Versch. Sorten.
Sekt
Henkell
Mo.','5.6. bis Sa.','10.6.

DEIN it
SPAR
FEST

Output:
{
    "product_brand": "Henkell",
    "product_description": "Versch. Sorten., Je 0,75 l",
    "product_name": "Sekt",
    "product_sku": "Null",
    "product_Product_category": "Alkoholische Getränke",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mo.','5.6. bis Sa.','10.6.,
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.99,
        "deal_minPrice": 3.99,
        "deal_pricebybaseunit": "1 l = 5.32",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 5.79,
        "deal_minPrice": 5.79,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Nur gültig mit LIDL Plus",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.88,
        "deal_minPrice": 3.88,
        "deal_pricebybaseunit": "1 l = 5.17",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
},

Input:
Cherry - Romatomaten Spanien , Marokko , Kl . I , je 250 - g - Schale ( 1 kg = 4.44 ) 
mit PENNY App 0.99 ( 1 kg = 3.96 ) 
1.11 
1.49¹ 
-25 % 
PENNY App Preis 
-33 % 0.99

Output:
{
    "product_brand": "Null",
    "product_description": "Spanien , Marokko , Kl . I , je 250 - g - Schale",
    "product_name": "Cherry - Romatomaten",
    "product_sku": "Null",
    "product_Product_category": "Gemüse",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.11,
        "deal_minPrice": 1.11,
        "deal_pricebybaseunit": "1 kg = 4.44",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.49,
        "deal_minPrice": 1.49,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "PENNY App Preis",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.99,
        "deal_minPrice": 0.99,
        "deal_pricebybaseunit": "1 kg = 3.96",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
},

Input:
MOHLEN SALAMI SCHINKEN SPICKER 
RÜGENWALDER MÜHLE Veganer Aufschnitt Verschiedene Sorten , je 80 - g - Packung ( 1 kg = 14.88 ) 
ohne PENNY App 1.59 je 80 - g - Packung 
( 1 kg = 19.88 ) 
Veganer 
Mortadella 
Nur mit der App 
1.19 
P.

Output:
{
    "product_brand": "RÜGENWALDER MÜHLE",
    "product_description": "Verschiedene Sorten , je 80 - g - Packung",
    "product_name": "Veganer Aufschnitt",
    "product_sku": "Null",
    "product_Product_category": "Aufschnitt",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.59,
        "deal_minPrice": 1.59,
        "deal_pricebybaseunit": "1 kg = 19.88",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Nur mit der App",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.19,
        "deal_minPrice": 1.19,
        "deal_pricebybaseunit": "1 kg = 14.88",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
}


    """

)

special_prise_our_ocr = (

    """
Input:
STARS Celebrations Je 186 g 1 kg = 10.11 CLEBRATIONS -50 % 3.79 1.88 * -51 % galia FEST Nur gültig mit LIDL Plus 1.85 * d ) 1 kg = 9.95

Output:
{
    "product_brand": "Celebrations",
    "product_description": "Je 186 g",
    "product_name": "Celebrations",
    "product_sku": "Null",
    "product_Product_category": "Süßigkeiten",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.88,
        "deal_minPrice": 1.88,
        "deal_pricebybaseunit": "1 kg = 10.11",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.79,
        "deal_minPrice": 3.79,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Nur gültig mit",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.85,
        "deal_minPrice": 1.85,
        "deal_pricebybaseunit": "1 kg = 9.95",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
},

Input:
Cherry - Romatomaten Spanien , Marokko , Kl . I , je 250 - g - Schale ( 1 kg = 4.44 ) \n mit PENNY App 0.99 ( 1 kg = 3.96 ) \n 1.11 \n 1.49¹ \n -25 % \n PENNY App Preis \n -33 % 0.99 \n % 2 \n

Output:
{
    "product_brand": "Null",
    "product_description": "Spanien , Marokko , Kl . I , je 250 - g - Schale",
    "product_name": "Cherry - Romatomaten",
    "product_sku": "Null",
    "product_Product_category": "Gemüse",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.11,
        "deal_minPrice": 1.11,
        "deal_pricebybaseunit": "1 kg = 4.44",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.49,
        "deal_minPrice": 1.49,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "PENNY App Preis",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.99,
        "deal_minPrice": 0.99,
        "deal_pricebybaseunit": "1 kg = 3.96",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
},

Input:
MOHLEN SALAMI SCHINKEN SPICKER \n RÜGENWALDER MÜHLE Veganer Aufschnitt Verschiedene Sorten , je 80 - g - Packung ( 1 kg = 14.88 ) \n ohne PENNY App 1.59 je 80 - g - Packung \n ( 1 kg = 19.88 ) \n Veganer \n Mortadella \n Nur mit der App \n 1.19 \n P. \n

Output:
{
    "product_brand": "RÜGENWALDER MÜHLE",
    "product_description": "Verschiedene Sorten , je 80 - g - Packung",
    "product_name": "Veganer Aufschnitt",
    "product_sku": "Null",
    "product_Product_category": "Aufschnitt",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.59,
        "deal_minPrice": 1.59,
        "deal_pricebybaseunit": "1 kg = 19.88",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Nur mit der App",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.19,
        "deal_minPrice": 1.19,
        "deal_pricebybaseunit": "1 kg = 14.88",
        "deal_loyaltycard": "Null",
        "deal_type": "SPECIAL_PRICE"
      }
    ]
}

    """

)

old_price_crossed_out = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                    "deal_id": "2",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
The values and words of one of the json parameters cannot be repeated in other json parameters.
It is forbidden to add text to the json that is not in the image.
If the image does not contain a product description, but only a name, set the "product_description" to "null".
The "product_description" cannot contain the product name, brand or unit price.
All information present in the image should be written to the appropriate json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "REGULAR_PRICE" for "deal_2".
"deal_2" should contain information related to the "REGULAR_PRICE" price.
"product_sku" is the serial number of the product (Art.-Nr.).
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and "REGULAR_PRICE" for "deal_id": "2".
"deal_id": "2" should contain information related to the "REGULAR_PRICE" price.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
"""

old_price_crossed_out_client_ocr = (

    """
Input:
-.29
-.22*
-24%
Je Stück
Klasse I
Griechenland
Ursprung: Italien/
Sorte: Hayward
Kiwi','lose

Output:
{
    "product_brand": "Null",
    "product_description": "Sorte: Hayward, Ursprung: Italien/Griechenland, Klasse I, Je Stück",
    "product_name": "Kiwi",
    "product_sku": "Null",
    "product_Product_category": "Obst",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.22,
        "deal_minPrice": 0.22,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.29,
        "deal_minPrice": 0.29,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """
)

old_price_crossed_out_our_ocr = (

    """
Input:
1.86 \n 149 \n 21 % gespart \n Bonbel Butterkäse \n halbfester Schnittkäse , butterzart mild und voll im Geschmack , laktosefrei , 50 % Fetti . Tr . \n 100 g \n Bonbel \n Crominer \n iger \n

Output:
{
    "product_brand": "Bonbel",
    "product_description": "halbfester Schnittkäse, butterzart mild und voll im Geschmack, laktosefrei, 50% Fetti. Tr., 100 g",
    "product_name": "Butterkäse",
    "product_sku": "Null",
    "product_Product_category": "Käse",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.49,
        "deal_minPrice": 1.49,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.86,
        "deal_minPrice": 1.86,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE
      }
    ]
}

    """
)

product_number_sku = """
# Your Role:
You are a useful assistant for extracting product information from a given image.              

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# Rule of the highest rank: The values and words of one of the json parameters cannot be repeated in other json parameters.

# General instructions:
All textual information present in the image should be written to the appropriate json parameters.
The unit price (for example: "1 kg = 15.98", "1 l = 19.93", "kg-Preis") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
"price_type" and "deal_type" should always be "SALES_PRICE".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.

"""

product_number_sku_client_ocr = (

    """
Input:
69.99
Art.-Nr. 100357896
reich: bis 20 m. Je Stück.
± 0,4 mm/m. Arbeitsbe-
(2,6 Ah/4 V). Genauigkeit:
Akku: Li-Ionen-Akku
„PKLLP 360 B3"
360 Grad
Kreuzlinienlaser
4-V-Akku-
PERFORMANCE®
PARKSIDE

Output:
{
    "product_brand": "PARKSIDE",
    "product_description": "360 Grad Kreuzlinienlaser, 4-V-Akku-, Akku: Li-Ionen-Akku (2,6 Ah/4 V). Genauigkeit: ± 0,4 mm/m. Arbeitsbe- reich: bis 20 m. Je Stück.",
    "product_name": "„PKLLP 360 B3"",
    "product_sku": "100357896",
    "product_Product_category": "Werkzeuge",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "Null",
        "deal_maxPrice": 69.99,
        "deal_minPrice": 69.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """
)

product_number_sku_our_ocr = (

    """
Input:
PARKSIDE PERFORMANCE® 4 - V - Akku Kreuzlinienlaser \n 360 Grad \n ,, PKLLP 360 B3 \" Akku : Li - Ionen - Akku ( 2,6 Ah / 4V ) . Genauigkeit : ± 0,4 mm / m . Arbeitsbe reich : bis 20 m . Je Stück . Art.-Nr. 100357896 \n nur online \n 69.99 \n

Output:
{
    "product_brand": "PARKSIDE",
    "product_description": "360 Grad Kreuzlinienlaser, 4-V-Akku-, Akku: Li-Ionen-Akku (2,6 Ah/4 V). Genauigkeit: ± 0,4 mm/m. Arbeitsbe- reich: bis 20 m. Je Stück.",
    "product_name": "„PKLLP 360 B3"",
    "product_sku": "100357896",
    "product_Product_category": "Werkzeuge",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "Null",
        "deal_maxPrice": 69.99,
        "deal_minPrice": 69.99,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """
)

date_availability = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If there are one prices in the offer, then 1 "deals" will be provided.
If two are three prices in the offer, then 2 "deals" will be provided.
If three are three prices in the offer, then 3 "deals" will be provided.
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" in the "deal" with "deal_type": "SALES_PRICE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and must recorded in the "deal" with "deal_type": "SPECIAL_PRICE".
"deal_loyaltycard" can only have "true" or "false" values.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App").
For a "deal" where "deal_type" is "SALES_PRICE", "deal_loyaltycard" can only have the value "true" by default.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

"""

date_availability_client_ocr = (

    """
Input:
Inkl. Visco-Nackenstützkissen
Je Stück. Art.-Nr. 100360077
Modell „Pro Body S 592".
7-Zonen-Kaltschaum-Matratze
H3','B 90 x L 200 cm
Punktgenaue Entlastung/Komfort
Höhe: ca. 22 cm
Bezug abnehm- und waschbar (bei 60 °C)
Gesamtbetrag Finanzierung 294.72
24 MonateB à 12.28
269.-
UVP 449.-
-40%
ab Montag','3.4.

Output:
{
    "product_brand": "Null",
    "product_description": "Modell „Pro Body S 592". Höhe: ca. 22 cm Bezug abnehm- und waschbar (bei 60 °C) Punktgenaue Entlastung/Komfort Inkl. Visco-Nackenstützkissen H3, B 90 x L 200 cm, Je Stück.",
    "product_name": "7-Zonen-Kaltschaum-Matratze",
    "product_sku": "100360077",
    "product_Product_category": "Matratzen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online, ab Montag','3.4.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 269.0,
        "deal_minPrice": 269.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449.0,
        "deal_minPrice": 449.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """

)

date_availability_our_ocr = (

    """
Input:
breckle Inkl . Visco - Nackenstützkissen MADE DE IN GERMANY Höhe : ca. 22 cm 60 ° Bezug abnehm- und waschbar ( bei 60 ° C ) ск Punktgenaue Entlastung / Komfort 7 - Zonen - Kaltschaum - Matratze Modell ,, Pro Body S 592 " . Weitere Größen und weiterer Härtegrad erhältlich . Je Stück . Art.-Nr. 100360077 nur online H3 , B 90 x L200 cm -40 % UVP - 449. 269. 24 Monate à 12.28 Gesamtbetrag Finanzierung 294.72, ab Montag','3.4.

Output:
{
    "product_brand": "Null",
    "product_description": "Je Stück., Modell „Pro Body S 592". Höhe: ca. 22 cm Bezug abnehm- und waschbar (bei 60 °C) Punktgenaue Entlastung/Komfort Inkl. Visco-Nackenstützkissen H3, B 90 x L 200 cm",
    "product_name": "7-Zonen-Kaltschaum-Matratze",
    "product_sku": "100360077",
    "product_Product_category": "Matratzen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online, ab Montag','3.4.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 269.0,
        "deal_minPrice": 269.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449.0,
        "deal_minPrice": 449.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}
    """

)

money_rebate = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If there are one prices in the offer, then 1 "deals" will be provided.
If two are three prices in the offer, then 2 "deals" will be provided.
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" in the "deal" with "deal_type": "SALES_PRICE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and must recorded in the "deal" with "deal_type": "SPECIAL_PRICE".
"deal_loyaltycard" can only have "true" or "false" values.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App").
For a "deal" where "deal_type" is "SALES_PRICE", "deal_loyaltycard" can only have the value "true" by default.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%", "-5€").
The discount can be in percentage and currency.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
"""

money_rebate_client_ocr = (

    """
Input:
Meißeln
Hammer bohren,
Bohren,
FLetzter Preis auf lidl.de zum Drucktermin
39.99*
47.99 F
-8€
bohrer
für Rundschaft-
spannbohrfutter
schlag','Schnell-
Metall-Tiefenan-
3 Bohrer (Ø 6/8/10 x 150 mm),
Zubehör: Flachmeißel (250 mm),
Inkl. Aufbewahrungskoffer
max. 19/13/24 mm. Je Stück
Beton und Stein/Metall/Holz:
0–1.650 min-1. Bohrleistung in
0–7.500 min-1. Leerlaufdrehzahl:
Schlagstärke: 1,2 J. Schlagzahl:
Frontgriff um 360° drehbar.
System) für Rundschaftbohrer.
Schnellspannbohrfutter (SDS-Plus-
Typ „PBH 800 A1". Aufsetzbares
Bohr- und Meißelhammer
PARKSIDE®
ab Montag','3.4.

Output:
{
    "product_brand": "PARKSIDE®",
    "product_description": "Typ „PBH 800 A1". Aufsetzbares Schnellspannbohrfutter (SDS-Plus- System) für Rundschaftbohrer. Frontgriff um 360° drehbar. Schlagzahl: 0–7.500 min-1. Leerlaufdrehzahl: 0–1.650 min-1. Bohrleistung in Beton und Stein/Metall/Holz: max. 19/13/24 mm. Inkl. Aufbewahrungskoffer, 3 Bohrer (Ø 6/8/10 x 150 mm), Flachmeißel (250 mm), Metall-Tiefenanschlag, Je Stück",
    "product_name": "Bohr- und Meißelhammer",
    "product_sku": "Null",
    "product_Product_category": "Werkzeuge",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ab Montag','3.4.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.99,
        "deal_minPrice": 39.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 47.99,
        "deal_minPrice": 47.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

money_rebatey_our_ocr = (

    """
Input:
Auf Seite 14 z.B. Strick fleecejacke -7 € 16.99 9.99 * auch online

Output:
{
    "product_brand": "Null",
    "product_description": "Null",
    "product_name": "Strick fleecejacke",
    "product_sku": "Null",
    "product_Product_category": "Kleidung",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "auch online",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 9.99,
        "deal_minPrice": 9.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

percentage_rebate = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If there are one prices in the offer, then 1 "deals" will be provided.
If two are three prices in the offer, then 2 "deals" will be provided.
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
The number of deals must correspond to the number of prices in the offer; it is forbidden to create a deal without a price.
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" in the "deal" with "deal_type": "SALES_PRICE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and must recorded in the "deal" with "deal_type": "SPECIAL_PRICE".
"deal_loyaltycard" can only have "true" or "false" values.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App").
For a "deal" where "deal_type" is "SALES_PRICE", "deal_loyaltycard" can only have the value "true" by default.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"discount" always has a value.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%", "-5€").
The discount can be in percentage and currency.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
"""

percentage_rebate_client_ocr = (

    """
Input:
-.29
-.22*
-24%
Je Stück
Klasse I
Griechenland
Ursprung: Italien/
Sorte: Hayward
Kiwi','lose

Output:
{
    "product_brand": "Null",
    "product_description": "Sorte: Hayward, Ursprung: Italien/Griechenland, Klasse I, Je Stück",
    "product_name": "Kiwi",
    "product_sku": "Null",
    "product_Product_category": "Obst",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.22,
        "deal_minPrice": 0.22,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.29,
        "deal_minPrice": 0.29,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
99.
1
-20%
1kg = € 4,98
400g Packung
mit Linsen-Bolognese
My Veggie Lasagne

Output:
{
    "product_brand": "My Veggie",
    "product_description": "mit Linsen-Bolognese, 400g Packung",
    "product_name": "Lasagne",
    "product_sku": "Null",
    "product_Product_category": "Fertiggerichte",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.99,
        "deal_minPrice": 1.99,
        "deal_pricebybaseunit": "1kg = € 4,98",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """

)

percentage_rebate_our_ocr = (

    """
Input:
03 LECKER Kühlung Chef Select Premium Fleischsalat Versch . Sorten . Je 200 g 1 kg = 4.40 Fleischenlat 200 -36 % 1.39 -88 * 

Output:
{
    "product_brand": "Chef Select",
    "product_description": "Versch. Sorten., Je 200 g",
    "product_name": "Premium Fleischsalat",
    "product_sku": "Null",
    "product_Product_category": "Delikatessen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.88,
        "deal_minPrice": 0.88,
        "deal_pricebybaseunit": "1 kg = 4.40",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.39
        "deal_minPrice": 1.39
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
EDEKA \n MY VEGGIE \n MY VEGGIE LASAGNE \n HIT LINENS \n My Veggie Lasagne mit Linsen - Bolognese \n 400g Packung 1kg = € 4,98 \n -20 % \n 199 \n

Output:
{
    "product_brand": "EDEKA",
    "product_description": "HIT LINENS, mit Linsen-Bolognese, 400g Packung",
    "product_name": "MY VEGGIE LASAGNE",
    "product_sku": "Null",
    "product_Product_category": "Fertiggerichte",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.99,
        "deal_minPrice": 1.99,
        "deal_pricebybaseunit": "1kg = € 4,98",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """

)

reward = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If there are two prices in the offer, then 2 "deals" will be provided.
If there are three prices in the offer, then 3 "deals" will be provided.
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2", "deal_3" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The description of the remuneration (for example: "gratis, "2+1") should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE" or "SPECIAL_PRICE".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and must recorded in the "deal" with "deal_type": "SPECIAL_PRICE".
"deal_loyaltycard" can only have "true" or "false" values.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App").
For a "deal" where "deal_type" is "SALES_PRICE", "deal_loyaltycard" can only have the value "true" by default.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" "deal" with "deal_type": "SALES_PRICE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”) **are not recorded and should be ignored when filling in "product_description"**.
"""

reward_client_ocr = (

    """
Input:
2+1
gratis!
Share
Nussriegel
versch. Sorten,
je 3 x 35-g-Riegel
(1 kg = 27,62)
Einzelpreis 1.45 €
je 35-g-Riegel
(1 kg = 41.43)
3 für nur
2.90
statt 4.35

Output:
{
    "product_brand": "Share",
    "product_description": "versch. Sorten, Einzelpreis 1.45 €, je 35-g-Riegel, (1 kg = 41.43), je 3 x 35-g-Riegel",
    "product_name": "Nussriegel",
    "product_sku": "Null",
    "product_Product_category": "Snacks",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "2+1 gratis!",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.90,
        "deal_minPrice": 2.90,
        "deal_pricebybaseunit": "(1 kg = 27.62)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 4.35,
        "deal_minPrice": 4.35,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
3.29*
15+1 Eis gratis
Tiefkühlung
1 l = 4.11
Je 16x 50 ml
Aus eigener Herstellung.
Mini Mix Eis Classic XXL
Bon Gelati

Output:
{
    "product_brand": "Bon Gelati",
    "product_description": "Tiefkühlung, Aus eigener Herstellung, Je 16x 50 ml",
    "product_name": "Mini Mix Eis Classic XXL",
    "product_sku": "Null",
    "product_Product_category": "Tiefkühlkost",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "15+1 Eis gratis",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.29,
        "deal_minPrice": 3.29,
        "deal_pricebybaseunit": "(1 l = 4.11)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}
    """
)

reward_our_ocr = (

    """
Input:
2 + 1 \n gratis ! \n BIO \n Share \n Nussriegel versch . Sorten , je 3 x 35 - g - Riegel . ( 1 kg = 27,62 ) Einzelpreis 1.45 € je 35 - g - Riegel ( 1 kg = 41.43 ) \n share \n shtres \n REPORT \n share \n 3 für nur \n 290 \n + \n statt 4.35 \n

Output:
{
    "product_brand": "Share",
    "product_description": "versch. Sorten, Einzelpreis 1.45 €, je 35-g-Riegel, (1 kg = 41.43), je 3 x 35-g-Riegel",
    "product_name": "Nussriegel",
    "product_sku": "Null",
    "product_Product_category": "Snacks",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "2+1 gratis!",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.90,
        "deal_minPrice": 2.90,
        "deal_pricebybaseunit": "(1 kg = 27.62)",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 4.35,
        "deal_minPrice": 4.35,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
4x4 \n Classic \n Aus eigener Herstellung . Je 16x 50 ml \n 11 = 4.11 \n MINI MIX CLASSIC \n BON \n Gelati \n PREMIUM EIS \n eigen \n Mandel \n * Tiefkühlung \n Bon Gelati \n Mini Mix Eis Classic XXL \n MINI MIX \n CLASSIC \n Weiß \n OHLAD \n Kakao \n Zartbitter \n NUTRI - SCORE \n XXL \n XX1 \n XXL \n XXL \n 15 + 1 Eis gratis \n 3.29 * \n

Output:
{
    "product_brand": "Bon Gelati",
    "product_description": "Aus eigener Herstellung, Je 16x 50 ml, Mini Mix Eis Classic XXL, Weiß, Kakao, Zartbitter, Tiefkühlung",
    "product_name": "Mini Mix Classic",
    "product_sku": "Null",
    "product_Product_category": "Eiscreme",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "15 + 1 Eis gratis",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.29,
        "deal_minPrice": 3.29,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}
    """
)

preliminary_promotional_price = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                    "deal_id": "2",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                      "terms_and_conditions": "",
                      "loyalty_card": "",
                      "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                  }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
The values and words of one of the json parameters cannot be repeated in other json parameters.
It is forbidden to add text to the json that is not in the image.
If the image does not contain a product description, but only a name, set the "product_description" to "null".
The "product_description" cannot contain the product name, brand or unit price.
All information present in the image should be written to the appropriate json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "REGULAR_PRICE" for "deal_2".
"deal_2" should contain information related to the "REGULAR_PRICE" price.
"product_sku" is the serial number of the product (Art.-Nr.).
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and "REGULAR_PRICE" for "deal_id": "2".
"deal_id": "2" should contain information related to the "REGULAR_PRICE" price.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "Letzter Aktionspreis" should be recorded in the "deal_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".

"""

preliminary_promotional_price_client_ocr = (

    """
Input:
Letzter Aktionspreis 1.29
1.39
-.88*
-36%
Kühlung
1 kg = 4.40
Je 200 g
Versch. Sorten.
Fleischsalat
Premium
Chef Select

Output:
{
    "product_brand": "Chef Select",
    "product_description": "Versch. Sorten., Je 200 g",
    "product_name": "Premium Fleischsalat",
    "product_sku": "Null",
    "product_Product_category": "Delikatessen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Letzter Aktionspreis 1.29",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.88,
        "deal_minPrice": 0.88,
        "deal_pricebybaseunit": "1 kg = 4.40",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.39
        "deal_minPrice": 1.39
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """
)

preliminary_promotional_price_our_ocr = (

    """
Input:
03 LECKER Kühlung Chef Select Premium Fleischsalat Versch . Sorten . Je 200 g 1 kg = 4.40 Fleischenlat 200 -36 % 1.39 -88 * Letzter Aktionspreis 1.29

Output:
{
    "product_brand": "Chef Select",
    "product_description": "Versch. Sorten., Je 200 g",
    "product_name": "Premium Fleischsalat",
    "product_sku": "Null",
    "product_Product_category": "Delikatessen",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Letzter Aktionspreis 1.29",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.88,
        "deal_minPrice": 0.88,
        "deal_pricebybaseunit": "1 kg = 4.40",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1.39
        "deal_minPrice": 1.39
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """
)

additional_shipping = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If there are one prices in the offer, then 1 "deals" will be provided.
If two are three prices in the offer, then 2 "deals" will be provided.
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" in the "deal" with "deal_type": "SALES_PRICE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
"deal_loyaltycard" can only have "true" or "false" values.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
The "deal_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%", "-5€").
The discount can be in percentage and currency.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
The "price_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the delivery option (for example: "Versandkostenzuschlag 39.95", "zzgl. Lieferzuschlag 12.95".) and the description of the installment plan (for example, "36 Monate³ à 11.81 Gesamtbetrag Finanzierung 425.16", "Monatl. Mindestrate 15.-".) must be recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

"""

additional_shipping_client_ocr = (

    """
Input:
schaltung
Inkl. Naben-
100340422
Art.-Nr.
Je Stück.
Akku (10,4 Ah/36 V).
motor. Li-Ionen-
Modell „Caravan Limited Edition". Mittel-
E-Bike Kompaktrad','20 Zoll
zzgl. Lieferzuschlag 12.95
1499.-
UVP 2299.95
-34%

Output:
{
    "product_brand": "Null",
    "product_description": "Modell „Caravan Limited Edition". Mittel- motor. Li-Ionen- Akku (10,4 Ah/36 V). Inkl. Naben- schaltung, Je Stück, zzgl. Lieferzuschlag 12.95",
    "product_name": "E-Bike Kompaktrad','20 Zoll",
    "product_sku": "100340422",
    "product_Product_category": "Fahrräder",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1499.0,
        "deal_minPrice": 1499.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2299.95,
        "deal_minPrice": 2299.95,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """
)

additional_shipping_our_ocr = (

    """
Input:
Inkl . Sitz- und Rücken kissen Siena GARDEN Hängekorb Modell ,, Salerno  . Maße : Hängekorb : ca. B 85 x H 138 x T 87 cm ; Gestell Hängekorb : ca. B 135 x H 196 x T 135 cm . Je Stück . Art.-Nr. 100313543 nur online -20 % UVP 449. 359. zzgl . Versandkostenzuschlag 39.95 36 Monate à 12.46 Gesamtbetrag Finanzierung 448.56

Output:
{
    "product_brand": "Siena GARDEN",
    "product_description": "Inkl. Sitz- und Rückenkissen, Modell ,, Salerno . Maße : ca. B 85 x H 138 x T 87 cm ; Gestell Hängekorb : ca. B 135 x H 196 x T 135 cm, Je Stück, zzgl. Versandkostenzuschlag 39.95",
    "product_name": "Hängekorb",
    "product_sku": "100313543",
    "product_Product_category": "Gartenmöbel",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 359.0,
        "deal_minPrice": 359.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449.0,
        "deal_minPrice": 449.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
},

Input:
MEHR DATEN . MEHR SPASS \n Allnet Flat S 1GB extra ! \n 3 GB \n statt 2GB / Monat \n ✔ LTE 25 inklusive \n ✔ Beste D - Netz - Qualität \n 12 € / Monat : 2 \n 5G \n I \n congstar \n 50 Mbit / s ZUBUCHBAR FÜR 5 € mtl.c7 \n Galaxy A14 \n Samsung Galaxy A14 4G 128 GB \n • 6,6 \" FHD + Infinity V - Display ( 16,72 cm Diagonale ) \n 50 MP Triplekamera mit Panorama \n und Makro - Aufnahmen \n • 2 GHz + 1,8 GHz Octacore Prozessor \n • 5.000 mAh Akku \n im Tarif Allnet Flat Sc² \n Farben \n 99 € \n

Output:
{
    "product_brand": "Samsung",
    "product_description": "4G 128 GB, 6,6 \" FHD + Infinity V - Display ( 16,72 cm Diagonale ), 50 MP Triplekamera mit Panorama und Makro - Aufnahmen, 2 GHz + 1,8 GHz Octacore Prozessor, 5.000 mAh Akku, im Tarif Allnet Flat Sc²",
    "product_name": "Galaxy A14",
    "product_sku": "Null",
    "product_Product_category": "Handys & Smartphones",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.0,
        "deal_minPrice": 99.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}
    """
)

deposit_price = """
# Your Role:
You are a useful assistant for extracting product information from a given image.              

# Output Format:
{
  "main_format":{
    "product_brand": "",
    "product_description": "",
    "product_name": "",
    "product_sku": "",
    "product_Product_category": "",
    "deal_1": [
        {
        "deal_conditions": "",
        "deal_currency": "",
        "deal_description": "",
        "deal_frequency": "",
        "deal_maxPrice": "",
        "deal_minPrice": "",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "",
        "deal_type": ""
        }
    ]
  },
  "additional_format": {
    "products": [
        {
          "product_id": "1",
          "brand": "",
          "name": "",
          "details": {
            "unit_size": "",
            "bundle_size": "",
            "deposit": "",
            "origin_country": "",
            "product_description": ""
          },
          "is_product_family": ""
        }
    ],
    "deals": [
      {
        "deal_id": "1",
        "type": "",
        "pricing": "",
        "price_type": "",
        "requirements": {
          "terms_and_conditions": "",
          "loyalty_card": "",
          "validity_period": ""
        },
        "details": {
          "price_by_base_unit": "",
          "discount": "",
          "deal_description": ""
        },
        "applied_to": "product-id",
        "is_deal_family": ""
      }
    ]
  }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
"deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

Important rule for the "main_format":
The "product_description" CANNOT contain information that is present in other json parameters.
IMPORTANT RULE: A unit price value, e.g. "1 kg = 4.28", "1 l = € 1.33", "1 kg = 11.84/ATG", "5.20/Liter", cannot be recorded in the "product_description" if the unit price value is already present in the "deal_pricebybaseunit".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# Rule of the highest rank for "main_format" and "additional_format":
The values and words of one of the json parameters cannot be repeated in other json parameters.
All textual information present in the image should be written to the appropriate json parameters.
Each new line ("\n".) of the "product_description" parameter should correspond to a new line ("\n".) in the text in the offer image.
Your answer should be purely json, without any additional explanation such as "```json", for example.
A product characteristic such as "Im Aufsteller", "Vegan" or "Organic" CANNOT be recorded in the "product_name", "name", "product_brand", "brand".
Rule: It is allowed to enter a value in "deal_pricebybaseunit" and "price_by_base_unit" only if the text between the unit of measurement and the price contains the symbol "=", otherwise the value will be "Null".

# General instructions for "main_format" and "additional_format":
The unit price (for example: "1 kg = 15.98", "1 l = 19.93") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

"deal_description" can only contain:
- the description of the possibility of ordering goods online (for example: "nur online", "auch online".),
- the validity period of the deal (e.g. "ab Donnerstag, 1.2")

"price_type" and "deal_type" should always be "SALES_PRICE".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
All characters (for example: "*") present in the product name or brand must be recorded.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
"product_brand" and "brand" must be written in full.
"product_name" and "name" must be written in full.
The size of the product, its quantity, or the size of the package (for example: "3er-Pack", "2 SCHALEN", "4 FLASCHEN") cannot be recorded in the "product_name" and "name".
The word "Metzgerfrisch" will always mean "product_brand", "brand".
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.

"""

deposit_price_client_ocr = (

    """
Input:
3.15*
8+1 gratis
1 l = -.70
zzgl. 2.25 Pfand
Je 9x 0,5 l
Gold-Pils
Perlenbacher

Output:
{
    "product_brand": "Perlenbacher",
    "product_description": "zzgl. 2.25 Pfand, Je 9x 0,5 l",
    "product_name": "Gold-Pils",
    "product_sku": "Null",
    "product_Product_category": "Bier",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "8+1 gratis",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.15,
        "deal_minPrice": 3.15,
        "deal_pricebybaseunit": "1 l = 0.70",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
(1 l = 1.10)
je 0,5 l
Pfand,
zzgl. 0.25
Premium,
Pilsener
HOLSTEN
UVP 0.85
0.55
-35%

Output:
{
    "product_brand": "HOLSTEN",
    "product_description": "Premium, je 0,5 l, Pfand, zzgl. 0.25",
    "product_name": "Pilsener",
    "product_sku": "Null",
    "product_Product_category": "Bier",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.55,
        "deal_minPrice": 0.55,
        "deal_pricebybaseunit": "1 l = 1.10",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.85,
        "deal_minPrice": 0.85,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """
)

deposit_price_our_ocr = (

    """
Input:
Perlenbacher Gold-Pils 3.15* Je 9x 0,5 l zzgl. 2.25 Pfand 1 l = -.70 8+1 gratis

Output:
{
    "product_brand": "Perlenbacher",
    "product_description": "zzgl. 2.25 Pfand, Je 9x 0,5 l",
    "product_name": "Gold-Pils",
    "product_sku": "Null",
    "product_Product_category": "Bier",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "8+1 gratis",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.15,
        "deal_minPrice": 3.15,
        "deal_pricebybaseunit": "1 l = 0.70",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
HOLSTEN \n PILSENER \n HOLSTEN Pilsener \n Premium , zzgl . 0.25 Pfand , je 0,51 \n -35 % \n 0.55 \n UVP 0.85 \n

Output:
{
    "product_brand": "HOLSTEN",
    "product_description": "Premium, je 0,5 l, Pfand, zzgl. 0.25",
    "product_name": "Pilsener",
    "product_sku": "Null",
    "product_Product_category": "Bier",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.55,
        "deal_minPrice": 0.55,
        "deal_pricebybaseunit": "1 l = 1.10",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 0.85,
        "deal_minPrice": 0.85,
        "deal_pricebybaseunit": "Null",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """
)

multiple_offers_with_uvp = """
# Your Role:
You are a useful assistant for extracting product information from a given image.             
You will receive an image of the offer of several products.

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{
    "main_format":
    {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
        "deal_3": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },
    "additional_format": {
        "products": [
                {
                    "product_id": "1",
                    "brand": "",
                    "name": "",
                    "details": {
                    "unit_size": "",
                    "bundle_size": "",
                    "deposit": "",
                    "origin_country": "",
                    "product_description": ""
                    },
                    "is_product_family": ""
                }
            ],
            "deals": [
                {
                    "deal_id": "1",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                    },
                    "details": {
                      "price_by_base_unit": "",
                      "discount": "",
                      "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                }
            ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Clearly define how many prices and products there are in the offer, and create a "deal" for each price and product.
"deal_description" should contain a description of the product, excluding its name and brand.
If the text of the offer contains several brand and names, then they should be written in the "product_brand" and "product_name" using the conjunction "oder".
The description that applies to all products should be recorded in the "product_description", but the description of a specific product should be recorded in the "deal_description" of the corresponding deal. It is forbidden to write a description of a specific product in the "product_description".
Each "deal" should have its own key, for example "deal_1", "deal_2", "deal_3" and so on.
Information about a particular product should be recorded in the "deal_description" of the relevant "deal".
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
The "deal_type" can acquire only such values: "SALES_PRICE", "RECOMMENDED_RETAIL_PRICE"."          
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".и 
"deal" with "deal_type": "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".
"product_name" always has a value.
The size of the token must be written in "product_description".
"deal_description" cannot contain a price and "product_description".
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
The "name" cannot be duplicated in the "deal_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
The "additional_format" array can contain several products and several deals.
If each product has two prices, then two "deals" are required for each product.
The "price_type" can acquire only such values: "SALES_PRICE", "RECOMMENDED_RETAIL_PRICE"."
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
"deal" with "price_type": "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "price_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "price_type": "SALES_PRICE".
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.


# General instructions:
The number of "deal" in the "main_format" must be the same as in the "additional_format".
If offer hasa discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
The text and product description always mention two product names.
All information present in the image should be written to the appropriate json parameters.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
if the old price is not crossed out, then we write the RECOMMENDED_RETAIL_PRICE type into a separate deal.

IMPORTANT 



# High priority Instructions for "main_format" and "additional_format":
The output json should not contain syntax errors.
The values and words of one of the json parameters cannot be repeated in other json parameters.
Instructions for "main_format" cannot be applied to Instructions for "additional_format".
You should always record the old price in a separate deal.


"""

multiple_offers_with_uvp_client_ocr = (

    """
Input:
SPAREN
66%
299,-
COUCHTISCH
885,- UVP
SPAREN
57%
1.999,-
WOHNLANDSCHAFT
4.664,- UVP
Stoffauswahl
XXXL
trendiger Cordstoff
**
Ø ca. 86 x 35 cm 24650013_01 885,- UVP 299,-
Couchtisch','Marmorglas weiß','Gestell Metall schwarz,
Gegen Mehrpreis: Dekokissen','Hocker sowie große Stoffauswahl
15810293_20 4.664,- UVP 1.999,-
Füße schwarz matt','ca. 296 x 207 cm
Wohnlandschaft','strapazierfähiger Bezugsstoff,
-a
-O
-3
6
0
E
LD

Output:
[
  {
      "product_brand": "XXXL",
      "product_description": "Marmorglas weiß, Gestell Metall schwarz, Ø ca. 86 x 35 cm",
      "product_name": "Couchtisch",
      "product_sku": "24650013_01",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 299.0,
          "deal_minPrice": 299.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [ 
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 885.0,
          "deal_minPrice": 885.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  },
  {
      "product_brand": "XXXL",
      "product_description": "strapazierfähiger Bezugsstoff, Füße schwarz matt, ca. 296 x 207 cm, Gegen Mehrpreis: Dekokissen, Hocker sowie große Stoffauswahl",
      "product_name": "Wohnlandschaft",
      "product_sku": "15810293_20",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1999.0,
          "deal_minPrice": 1999.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [ 
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 4664.0,
          "deal_minPrice": 4664.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  }
]

    """
)

multiple_offers_with_uvp_our_ocr = (

    """
Input:
Dieter Knoll Collection \n 5 Jahre \n GARANTIE .. Dieter Knoll Collection \n 66 % \n SPAREN \n 885 , - UVP \n 299 , \n COUCHTISCH \n H \n Wohnlandschaft , strapazierfähiger Bezugsstoff , \n Füße schwarz matt , ca. 296 x 207 cm \n 15810293 20 4.664 , - UVP 1.999 , \n Gegen Mehrpreis : Dekokissen , Hocker sowie große Stoffauswahl \n Couchtisch , Marmorglas weiß , Gestell Metall schwarz , \n Ø ca. 86 x 35 cm 24650013_01 885 , - UVP 299 , \n XXXL Stoffauswahl \n ASPENSTYLE \n trendiger Cordstoff \n WOHNLANDSCHAFT \n RAY \n 4.664 , - UVP \n 1.999 , - 57 % \n SPAREN \n MEIN MÖBELHAUS .

Output:
[
  {
      "product_brand": "XXXL",
      "product_description": "Marmorglas weiß, Gestell Metall schwarz, Ø ca. 86 x 35 cm",
      "product_name": "Couchtisch",
      "product_sku": "24650013_01",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 299.0,
          "deal_minPrice": 299.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [ 
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 885.0,
          "deal_minPrice": 885.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  },
  {
      "product_brand": "XXXL",
      "product_description": "strapazierfähiger Bezugsstoff, Füße schwarz matt, ca. 296 x 207 cm, Gegen Mehrpreis: Dekokissen, Hocker sowie große Stoffauswahl",
      "product_name": "Wohnlandschaft",
      "product_sku": "15810293_20",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1999.0,
          "deal_minPrice": 1999.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [ 
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 4664.0,
          "deal_minPrice": 4664.0,
          "deal_pricebybaseunit": "",
          "deal_rewardcurrencyname": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  }
]

    """
)

different_sizes = """
# Your Role:
You are a useful assistant for extracting product information from a given image.             
You will receive an image of the product with different sizes.

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{
    "main_format":
    {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },
    "additional_format": {
        "products": [
                {
                    "product_id": "1",
                    "brand": "",
                    "name": "",
                    "details": {
                    "unit_size": "",
                    "bundle_size": "",
                    "deposit": "",
                    "origin_country": "",
                    "product_description": ""
                    },
                    "is_product_family": ""
                }
            ],
            "deals": [
                {
                    "deal_id": "1",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                    },
                    "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                }
            ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each deal should be numbered, for example "deal_1", "deal_2", "deal_3".
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
If the text of the offer contains several brand and names, then they should be written in the "product_brand" and "product_name" using the conjunction "oder".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
The "deal_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE"."
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".
"product_name" always has a value.
The size of the token must be written in "product_description".
"deal_description" cannot contain a price and "product_description".
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
The "name" cannot be duplicated in the "deal_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
The "additional_format" array can contain several products and several deals.
If each product has two prices, then two "deals" are required for each product.
The "price_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE"."
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "price_type": "SALES_PRICE".
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The offer contains only one product that has several prices for each of the sizes of the same product. There should be a separate "deal" for each size, the description of which is written in "deal_description".
The description of size must be recorded in "deal_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
All information present in the image should be written to the appropriate json parameters.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
You do not need to enter the word "statt" in any of the parameters.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".


# High priority Instructions for "main_format" and "additional_format":
The output json should not contain syntax errors.
The values and words of one of the json parameters cannot be repeated in other json parameters.
Instructions for "main_format" cannot be applied to Instructions for "additional_format".

"""

different_sizes_client_ocr = ( 

    """
Input:
5056886/00,02-05
ca. 160 x 230 cm
je
39.99
129.99
UVP***
79.99
199.99
je
UVP***
5083744/00-04
ca. 200 x 290 cm
29.99
59.99
je
UVP***
5056885/00,02-05
ca. 120 x 170 cm
14.99
29.99
je
UVP***
5056883/00,02-05
ca. 80 x 150 cm
Langflorteppich

Output:
{
    "product_brand": "Null",
    "product_description": "Null",
    "product_name": "Langflorteppich",
    "product_sku": "5056883/00,02-05, 5056885/00,02-05, 5083744/00-04, 5056886/00,02-05",
    "product_Product_category": "Teppiche",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 80 x 150 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 14.99,
        "deal_minPrice": 14.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 120 x 170 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.99,
        "deal_minPrice": 59.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_5": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 200 x 290 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 79.99,
        "deal_minPrice": 79.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_6": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 199.99,
        "deal_minPrice": 199.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_7": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 160 x 230 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.99,
        "deal_minPrice": 39.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_8": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 129.99,
        "deal_minPrice": 129.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ]
}

    """

)

different_sizes_our_ocr = (

    """
Input:
Mission \n Fellimitat \n supersoft \n SUPER SPAR ! \n ca. 80 x 140 cm 5981911 / 00-03 UVP *** je 59.99 29.99 ca. 120 x 160 cm 5981912 / 00-03 UVP *** je 99.99 49.99 \n *** \n UVP \n 17999 \n To 99,99 \n ca. 160 x 220 cm 5981913 / 00-03 \n

Output:
{
    "product_brand": "Null",
    "product_description": "Mission supersoft SUPER SPAR !",
    "product_name": "Fellimitat",
    "product_sku": "5981911/00-03, 5981912/00-03, 5981913/00-03",
    "product_Product_category": "Teppiche",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 80 x 140 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.99,
        "deal_minPrice": 59.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 120 x 160 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 49.99,
        "deal_minPrice": 49.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.99,
        "deal_minPrice": 99.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_5": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "ca. 160 x 220 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.99,
        "deal_minPrice": 99.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_6": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 179.99,
        "deal_minPrice": 179.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
}

    """

)

regular = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
Clearly define how many prices there are in the offer, and create a "deal" for each price.
If the offer contains information about additional options, designs, etc., (e.g. "Weitere", "Versch Farben", "versch. Größen"), then this information should be written in the "deal_description" of the "deal" where "deal_type": "OTHER" and "price_type": "OTHER" are present.
"deal" with "deal_type": "OTHER" and "price_type": "OTHER" cannot have a price.
**Do not create a "deal" with "deal_type": "OTHER" and "price_type": "OTHER" if additional options are not present.**
If there are one prices in the offer, then 2 "deals" will be provided.
If two are three prices in the offer, then 3 "deals" will be provided.
"type" can only have "SALES" by default (always!).
The number of "deals" in the "main_format" must be equal to the number of "deals" in the "additional_format".
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" in the "deal" with "deal_type": "SALES_PRICE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus", "mit PENNY App") and must recorded in the "deal" with "deal_type": "SPECIAL_PRICE".
"deal_loyaltycard" can only have "true" or "false" values.
"deal" with "deal_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus", "mit PENNY App").
For a "deal" where "deal_type" is "SALES_PRICE", "deal_loyaltycard" can only have the value "true" by default.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "OTHER", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "OTHER", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
You do not need to enter the word "UVP" and "statt" in any of the parameters.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

"""

regular_client_ocr = (

    """
Input:
Weitere Farben:
Grau
Puder
Ozean
Je Set. Art.-Nr. 100324441
Waschbar bis 60 °C und trocknergeeignet.
L 200 cm). Material: 100 % Baumwolle.
(80 x 80 cm) und 1x Sommertuch (B 150 x
Set bestehend aus: 1x Kopfkissenbezug
Sommertuch mit Kissenbezug
Summer-Set
17.99
UVP 29.95
-39%
Weiß

Output:
{
    "product_brand": "Null",
    "product_description": "Summer-Set, Set bestehend aus: 1x Kopfkissenbezug (80 x 80 cm) und 1x Sommertuch (B 150 x L 200 cm). Material: 100 % Baumwolle. Waschbar bis 60 °C und trocknergeeignet.",
    "product_name": "Sommertuch mit Kissenbezug",
    "product_sku": "100324441",
    "product_Product_category": "Bettwäsche",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 17.99,
        "deal_minPrice": 17.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.95,
        "deal_minPrice": 29.95,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Weitere Farben: Grau, Puder, Ozean, Weiß",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

regular_our_ocr = (

    """
Input:
Weiß \n PRIMERA \n first spare \n nur online \n Ozean \n Summer - Set \n Sommertuch mit Kissenbezug Set bestehend aus : 1x Kopfkissenbezug ( 80 x 80 cm ) und 1x Sommertuch ( B 150 x L200 cm ) . Material : 100 % Baumwolle . Waschbar bis 60 ° C und trocknergeeignet . Je Set . Art.-Nr. 100324441 \n Puder \n Grau \n Weitere Farben : \n -39 % \n UVP 29.95 \n 17.99 \n

Output:
{
    "product_brand": "PRIMERA",
    "product_description": "Summer-Set, Set bestehend aus: 1x Kopfkissenbezug (80 x 80 cm) und 1x Sommertuch (B 150 x L 200 cm). Material: 100 % Baumwolle. Waschbar bis 60 °C und trocknergeeignet.",
    "product_name": "Sommertuch mit Kissenbezug",
    "product_sku": "100324441",
    "product_Product_category": "Bettwäsche",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 17.99,
        "deal_minPrice": 17.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.95,
        "deal_minPrice": 29.95,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "RECOMMENDED_RETAIL_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Weitere Farben: Grau, Puder, Ozean, Weiß",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

supplemental_bid = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
 
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
If there are one prices in the offer, then 2 "deals" will be provided.
If two are three prices in the offer, then 3 "deals" will be provided.
The number of "deals" in the "main_format" must be equal to the number of "deals" in the "additional_format".
All information present in the image should be written to the appropriate json parameters.
The "product_description" cannot contain the product name, brand or unit price.
The values and words of one of the json parameters cannot be repeated in other json parameters.


# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Each "deal" should have its own key, for example "deal_1", "deal_2" and so on.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
If the text of the offer contains several brand and names, then they should be written in the "product_brand" and "product_name" using the conjunction "oder".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description" in the "deal" with "deal_type": "SALES_PRICE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
"deal_loyaltycard" can only have "true" or "false" values.
For the rest of the "deal", "deal_loyaltycard" can only have a default value of "false".
"deal" where "deal_type" is "SPECIAL_PRICE" should contain information related to the special price.
The "deal_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "OTHER", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".

It is VERY IMPORTANT to ALWAYS record each price in a separate deal
write all variants for SALES_PRISE in the main in a separate deal
**do not invent your own, write down only what is in the picture**

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price (for example: "Nur gültig mit Lidl Plus") and must recorded in the "deal" with the "price_type": "SPECIAL_PRICE".
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
For a "deal" where "price_type" is "SALES_PRICE", "loyalty_card" can only have the value "true" by default.
For the rest of the "deal", "loyalty_card" can only have a default value of "false".
"deal" with "price_type": "SPECIAL_PRICE" should contain the price of a special price, such as a coupon price or a special price from a store (for example: "Nur gültig mit Lidl Plus").
The "price_type" can acquire only such values: "SALES_PRICE", "SPECIAL_PRICE", "OTHER", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (for example: crossed out, with the "statt" characteristic, "Preis ohne Treuepunkte"), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"),
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
You do not need to enter the word "UVP" and "statt" in any of the parameters.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
If there is more than one product in the image, add each of them separately in the main_format.
Only add deals of type **OTHER** if there are additional conditions (e.g., additional product for a separate price, financing, or online availability).

# Instructions for Additional offer:
All information about the Additional Offer only if there is one (for example: “LIVARNO" für 5.99”), then this information, including the price of the Additional Offer, should be written in the “deal_description” of the “deal”, where the “deal_type” is indicated: “OTHER” and ‘price_type’: “OTHER”.
Additional offer is always present.
"deal" with "deal_type": "OTHER" and "price_type": "OTHER" cannot have a values in "deal_maxPrice", "deal_minPrice" and "pricing" .
The output json must always contain "deal" with "deal_type": "OTHER" and "price_type": "OTHER".

# Exceptions:
If the offer image contains installments, this information should be ignored and not written to any of the json parameters.

"""

supplemental_bid_client_ocr = (

    """
Input:
für 39.99
Art.-Nr. 100344551
PRECISION"
Modell „PLATINUM
NBA Basketball
SPALDING
Art.-Nr. 100325601
befüllbar. Je Stück.
Sand oder Wasser
Robuster Standfuß mit
und leichten Transport.
für einen einfachen
bis 210 cm). Mit Rollen
Höhenverstellbar (170
Basketballkorb
CRIVIT®
44.99
69.99
-35%

Output:
{
    "product_brand": "CRIVIT",
    "product_description": "Höhenverstellbar (170 bis 210 cm). Mit Rollen für einen einfachen und leichten Transport. Robuster Standfuß mit Sand oder Wasser befüllbar, Je Stück",
    "product_name": "Basketballkorb",
    "product_sku": "100325601, 100344551",
    "product_Product_category": "Sport & Freizeit",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 44.99,
        "deal_minPrice": 44.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 69.99,
        "deal_minPrice": 69.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "SPALDING NBA Basketball Modell „PLATINUM PRECISION" für 39.99",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

supplemental_bid_our_ocr = (

    """
Input:
SPALDING PLATINUM SPALDING NBA Basketball Modell PLATINUM PRECISION \" Art.-Nr. 100344551 für 39.99 PRECISION Erivir ALL STAR CRIVIT® Basketballkorb Höhenverstellbar ( 170 bis 210 cm ) . Mit Rollen für einen einfachen und leichten Transport . Robuster Standfuß mit Sand oder Wasser befüllbar . Je Stück . Art.-Nr. 100325601 nur online -35 % 69.99 44.99

Output:
{
    "product_brand": "CRIVIT",
    "product_description": "Höhenverstellbar (170 bis 210 cm). Mit Rollen für einen einfachen und leichten Transport. Robuster Standfuß mit Sand oder Wasser befüllbar, Je Stück",
    "product_name": "Basketballkorb",
    "product_sku": "100325601, 100344551",
    "product_Product_category": "Sport & Freizeit",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "nur online",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 44.99,
        "deal_minPrice": 44.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 69.99,
        "deal_minPrice": 69.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "SPALDING NBA Basketball Modell „PLATINUM PRECISION" für 39.99",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

without_price = """
# Your Role:
You are a useful assistant for extracting product information from a given image.              

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.  
"product_sku" is the serial number of the product. 
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" can only have "Null" by default.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
The "pricing" can only have "Null" by default.

# Rule of the highest rank: 
The values and words of one of the json parameters cannot be repeated in other json parameters.

# General instructions:
The price description (for example: "tages-frischer Preis") must be recorded in "deal_description.
All textual information present in the image should be written to the appropriate json parameters.
The unit price (for example: "1 kg = 15.98", "1 l = 19.93", "kg-Preis") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
"price_type" and "deal_type" should always be "OTHER".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.

"""

without_price_client_ocr = (

    """
Input:
Montag','5.6. bis Dienstag','6.6.
Je 700 g
Klasse I
Südafrika/Kenia/Tansania
Ursprung: Kolumbien/Peru/
Avocado
Preis
frischer
tages-
%
AKTION

Output:
{
    "product_brand": "Null",
    "product_description": "Ursprung: Kolumbien/Peru/ Südafrika/Kenia/Tansania, Klasse I, Je 700 g",
    "product_name": "Avocado",
    "product_sku": "Null",
    "product_Product_category": "Obst",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Montag, 5.6. bis Dienstag, 6.6. Tagesfrischer Preis",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

without_price_our_ocr = (

    """
Input:
Montag','5.6. bis Dienstag','6.6.
Avocado Ursprung : Kolumbien / Peru / Südafrika / Kenia / Tansania Klasse I Je 700 g W tages frischer Preis

Output:
{
    "product_brand": "Null",
    "product_description": "Ursprung: Kolumbien/Peru/ Südafrika/Kenia/Tansania, Klasse I, Je 700 g",
    "product_name": "Avocado",
    "product_sku": "Null",
    "product_Product_category": "Obst",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Montag, 5.6. bis Dienstag, 6.6., Tagesfrischer Preis",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

additional_products = """
# Your Role:
You are a useful assistant for extracting product information from a given image.             
You will receive an image of the offer of several products.

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{
    "main_format":
    {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },
    "additional_format": {
        "products": [
                {
                    "product_id": "1",
                    "brand": "",
                    "name": "",
                    "details": {
                    "unit_size": "",
                    "bundle_size": "",
                    "deposit": "",
                    "origin_country": "",
                    "product_description": ""
                    },
                    "is_product_family": ""
                }
            ],
            "deals": [
                {
                    "deal_id": "1",
                    "type": "",
                    "pricing": "",
                    "price_type": "",
                    "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                    },
                    "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                    },
                    "applied_to": "product-id",
                    "is_deal_family": ""
                }
            ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
Clearly define how many prices and products there are in the offer, and create a "deal" for each price and product.
Each "deal" should have its own key, for example "deal_1", "deal_2", "deal_3" and so on.
Information about a particular product should be recorded in the "deal_description" of the relevant "deal".
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
The "deal_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE", "OTHER".
If the offer contains the "uvp" price characteristic, then it is "deal_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "deal_type": "REGULAR_PRICE.
"deal" with "deal_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "deal_maxPrice" and "deal_minPrice" than "deal_maxPrice" and "deal_minPrice" in "deal" with "deal_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "deal_type": "SALES_PRICE".
"product_name" always has a value.
The size of the token must be written in "product_description".
"deal_description" cannot contain a price and "product_description".
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
The "name" cannot be duplicated in the "deal_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
The "additional_format" array can contain several products and several deals.
If each product has two prices, then two "deals" are required for each product.
The "price_type" can acquire only such values: "SALES_PRICE", "REGULAR_PRICE", "RECOMMENDED_RETAIL_PRICE", "OTHER".
If the offer contains the "uvp" price characteristic, then it is "price_type": "RECOMMENDED_RETAIL_PRICE".
If the offer contains an old price (crossed out or with the "statt" characteristic), then this is the "price_type": "REGULAR_PRICE.
"deal" with "price_type": "REGULAR_PRICE" and "RECOMMENDED_RETAIL_PRICE" cannot have a lower value in "pricing" than "pricing" in "deal" with "price_type": "SALES_PRICE" of the same offer.
The description of the date should be written in the "deal_description" field of the "deal" with the "price_type": "SALES_PRICE".
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The number of "deal" in the "main_format" must be the same as in the "additional_format".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
All information present in the image should be written to the appropriate json parameters.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".

# High priority Instructions for "main_format" and "additional_format":
The output json should not contain syntax errors.
The values and words of one of the json parameters cannot be repeated in other json parameters.
Instructions for "main_format" cannot be applied to Instructions for "additional_format".

# Instructions for Additional offer:
All information about Additional offer (for example: "Gegen Mehrpreis: Sitz- und Rückenheizung 356,-, motor. Kopfteilverstellung 221,-, außenliegender Akku mit Ladestation 403,-, Überzug für Akku in Leder 100,-, sowie große Stoff- und Lederauswahl") then this information including the price of the Additional offer should be written in the "deal_description" of the "deal" where the "deal_type": "OTHER" and "price_type": "OTHER" is present.
Additional offer is always present.
"deal" with "deal_type": "OTHER" and "price_type": "OTHER" cannot have a values in "deal_maxPrice", "deal_minPrice" and "pricing" .
The output json must always contain "deal" with "deal_type": "OTHER" and "price_type": "OTHER".

"""

additional_products_client_ocr = (

    """
Input:
30.05.2023
ab Dienstag,
nach Umbau,
Ludwigsburg
XXXLutz in
NEU!
Leder-Sofa 2,5-sitzig 3.797,-
Gesamtpreis für abgebildetes
SPAREN
63%
1.999,-
LEDER-SOFA 2,5-SITZIG
5.526,- UVP
Leder
echtes
inkl. Armteilverstellung
inkl. Armteilverstellung
Überzug für Akku in Leder
Gegen Mehrpreis:
außenliegender Akku
Gegen Mehrpreis:
manuelle Kopfteilverstellung
Gegen Mehrpreis:
Kopfteilverstellung
Wallfree-Funktion mit motor.
Gegen Mehrpreis: motor.
Akku mit Ladestation 330,-','Überzug für Akku in Leder 82,-','Dekokissen sowie große Stoff- und Lederauswahl
Gegen Mehrpreis: motor. Wallfree-Funktion mit motor. Kopfteilverstellung 1.798,- ','Herz-Waage-Funktion 152,-,
ca. 194 x 94 x 95 cm 02970559_04 5.526,- UVP 1.999,-
Leder-Sofa 2,5-sitzig','echtes Leder','mit Armteilverstellung','Füße anthrazit pulverbeschichtet,
mit Ladestation 403,-','Überzug für Akku in Leder 100,-','sowie große Stoff- und Lederauswahl
Gegen Mehrpreis: Sitz- und Rückenheizung 356,-','motor. Kopfteilverstellung 221,-','außenliegender Akku
Sternfuß anthrazit pulverbeschichtet','ca. 71 x 114 x 84 cm 02970555_15 4.465,- UVP 1.499,-
Leder-Relaxsessel','echtes Leder','mit 2-motor. Relaxfunktion','mit manueller Kopfteilverstellung,
Couchtisch','Tischplatte Keramik','Gestell Metall anthrazit matt','ca. 83 cm Ø x 35 cm 15100338_02 1.553,- UVP 649,-
Couchtisch','Tischplatte Eiche furniert','Gestell Metall anthrazit matt','ca. 83 cm Ø x 42 cm 15100338_03 1.071,- UVP 449,-
Gegen Mehrpreis: manuelle Kopfteilverstellung 393,-','Dekokissen sowie große Stoff- und Lederauswahl
Leder-Sofa 3-sitzig','echtes Leder','mit Armteilverstellung','Füße anthrazit pulverbeschichtet','ca. 224 x 94 x 95 cm 02970559_03 6.085,- UVP 2.199,-

Output:
[
  {
      "product_brand": "Null",
      "product_description": "echtes Leder, mit Armteilverstellung, Füße anthrazit pulverbeschichtet, 194 x 94 x 95 cm",
      "product_name": "Leder-Sofa 2,5-sitzig",
      "product_sku": "02970559_04",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "ab Dienstagca, 30.05.2023",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1999.0,
          "deal_minPrice": 1999.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 5526.0,
          "deal_minPrice": 5526.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: motor. Wallfree-Funktion mit motor. Kopfteilverstellung 1.798,-, Herz-Waage-Funktion 152,-, Akku mit Ladestation 330,-, Überzug für Akku in Leder 82,-, Dekokissen sowie große Stoff- und Lederauswahl",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "echtes Leder, mit 2-motor. Relaxfunktion, mit manueller Kopfteilverstellung, Sternfuß anthrazit pulverbeschichtet, ca. 71 x 114 x 84 cm",
      "product_name": "Leder-Relaxsessel",
      "product_sku": "02970555_15",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "ab Dienstagca, 30.05.2023",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1499.0,
          "deal_minPrice": 1499.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 4465.0,
          "deal_minPrice": 4465.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: Sitz- und Rückenheizung 356,-, motor. Kopfteilverstellung 221,-, außenliegender Akku mit Ladestation 403,-, Überzug für Akku in Leder 100,-, sowie große Stoff- und Lederauswahl",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "Tischplatte Keramik, Gestell Metall anthrazit matt, ca. 83 cm Ø x 35 cm",
      "product_name": "Couchtisch",
      "product_sku": "15100338_02",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "ab Dienstagca, 30.05.2023",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 649.0,
          "deal_minPrice": 649.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1553.0,
          "deal_minPrice": 1553.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "Tischplatte Eiche furniert, Gestell Metall anthrazit matt, ca. 83 cm Ø x 42 cm",
      "product_name": "Couchtisch",
      "product_sku": "15100338_03",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "ab Dienstagca, 30.05.2023",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 449.0,
          "deal_minPrice": 449.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1071.0,
          "deal_minPrice": 1071.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  },
  {
      "product_brand": "Null",
      "product_description": "echtes Leder, mit Armteilverstellung, Füße anthrazit pulverbeschichtet, ca. 224 x 94 x 95 cm",
      "product_name": "Leder-Sofa 3-sitzig",
      "product_sku": "02970559_03",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "ab Dienstagca, 30.05.2023",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 2199.0,
          "deal_minPrice": 2199.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 6085.0,
          "deal_minPrice": 6085.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: manuelle Kopfteilverstellung 393,-, Dekokissen sowie große Stoff- und Lederauswahl",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  }
]

    """

)

additional_products_our_ocr = (

    """
Input:
AB \n 63 % \n SPAREN \n 275 , - UVP \n * 9990 \n ROTER PREIS \n ARMLEHNSTUHL \n ROTER PREIS \n 1.782 , - UVP \n 699 , \n 60 % \n SPAREN \n ESSTISCH \n Wildeiche teilmassiv \n LINEA NATURA \n XXXL Farbauswahl \n 28150046_27 1.782 , - UVP 275 , - UVP 99,90 \n Esstisch , Wildeiche massiv , Sockelplatte und Applikation in Metall schwarz , ca. 160 x 90 cm Armlehnstuhl , strapazierfähiger Bezugsstoff , Gestell Eiche massiv natur geölt 23150001_02 Gegen Mehrpreis : Armlehnstuhl mit Drehfunktion erhältlich 23150001_03 320 , - UVP 119 , Polsterbank , strapazierfähiger Bezugsstoff , Gestell Eiche massiv natur geölt , ca. 159 cm 23150001_01 650 , - UVP 279 , Highboard , Front Wildeiche massiv , Korpus Wildeiche furniert , Rahmen Metall schwarz , ca. 155 x 136 x 38 cm 28150046_26 2.679 , - UVP 999 , - Gegen Mehrpreis : 2er - Set Glaskantenbeleuchtung für Highboard 78 , Vitrine , Front Wildeiche massiv , Korpus Wildeiche furniert , Rahmen Metall schwarz , ca. 89 x 200 x 38 cm 28150046_23 2.156 , - UVP 799 , - Gegen Mehrpreis : 2er - Set Glaskantenbeleuchtung für Vitrine 77 , Sideboard , Front Wildeiche massiv , Korpus Wildeiche furniert , Rahmen Metall schwarz , ca. 180 x 85 x 42 cm 28150046_24 2.184 , - UVP 799 , - Gegen Mehrpreis : LED - Spot - Beleuchtung für Sideboard 197 , \n 699 , \n

Output:
[
  {
      "product_brand": "LINEA NATURA",
      "product_description": "Front Wildeiche massiv, Korpus Wildeiche furniert, Rahmen Metall schwarz, ca. 180 x 85 x 42 cm",
      "product_name": "Sideboard",
      "product_sku": "28150046_24",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 799.0,
          "deal_minPrice": 799.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 2184.0,
          "deal_minPrice": 2184.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: LED-Spot-Beleuchtung für Sideboard 197,-",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  },
  {
      "product_brand": "LINEA NATURA",
      "product_description": "Front Wildeiche massiv, Korpus Wildeiche furniert, Rahmen Metall schwarz, ca. 89 x 200 x 38 cm",
      "product_name": "Vitrine",
      "product_sku": "28150046_23",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 799.0,
          "deal_minPrice": 799.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 2156.0,
          "deal_minPrice": 2156.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: 2er-Set Glaskantenbeleuchtung für Vitrine 77,-",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  },
  {
      "product_brand": "LINEA NATURA",
      "product_description": "Front Wildeiche massiv, Korpus Wildeiche furniert, Rahmen Metall schwarz, ca. 155 x 136 x 38 cm",
      "product_name": "Highboard",
      "product_sku": "28150046_26",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 999.0,
          "deal_minPrice": 999.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 2679.0,
          "deal_minPrice": 2679.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: 2er-Set Glaskantenbeleuchtung für Highboard 78,-",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  },
  {
      "product_brand": "LINEA NATURA",
      "product_description": "strapazierfähiger Bezugsstoff, Gestell Eiche massiv natur geölt, ca. 159 cm",
      "product_name": "Polsterbank",
      "product_sku": "23150001_01",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 279.0,
          "deal_minPrice": 279.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 650.0,
          "deal_minPrice": 650.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  },
  {
      "product_brand": "LINEA NATURA",
      "product_description": "strapazierfähiger Bezugsstoff, Gestell Eiche massiv natur geölt",
      "product_name": "Armlehnstuhl",
      "product_sku": "23150001_02",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 99.90,
          "deal_minPrice": 99.90,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 275.0,
          "deal_minPrice": 275.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ],
      "deal_3": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Gegen Mehrpreis: Armlehnstuhl mit Drehfunktion erhältlich 23150001_03 320,- UVP 119,-",
          "deal_frequency": "ONCE",
          "deal_maxPrice": "Null",
          "deal_minPrice": "Null",
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "OTHER"
        }
      ]
  },
  {
      "product_brand": "LINEA NATURA",
      "product_description": "Wildeiche massiv, Sockelplatte und Applikation in Metall schwarz, ca. 160 x 90 cm",
      "product_name": "Esstisch",
      "product_sku": "28150046_27",
      "product_Product_category": "Möbel",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 699.0,
          "deal_minPrice": 699.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ],
      "deal_2": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 1782.0,
          "deal_minPrice": 1782.0,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "RECOMMENDED_RETAIL_PRICE"
        }
      ]
  }
]

    """

)

stock_offers = """
# Your Role:
You are a useful assistant for extracting product information from a given image.              

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" can only have "Null" by default.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
The "pricing" can only have "Null" by default.

# Rule of the highest rank: 
The values and words of one of the json parameters cannot be repeated in other json parameters.

# General instructions:
The price description (for example: "tages-frischer Preis") must be recorded in "deal_description.
All textual information present in the image should be written to the appropriate json parameters.
The unit price (for example: "1 kg = 15.98", "1 l = 19.93", "kg-Preis") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
"price_type" and "deal_type" should always be "OTHER".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.

"""

stock_offers_client_ocr = (

    """
Input:
5€
Rabatt
lidl-fotos.de
Code FU3345 auf
Digitaldruck mit dem
buch A4 Hardcover im
5€ Rabatt auf ein Foto-
Lidl FotosJ

Output:
{
    "product_brand": "Null",
    "product_description": "auf ein Fotobuch A4 Hardcover im Digitaldruck mit dem Code FU3345 auf lidl-fotos.de",
    "product_name": "5 € Rabatt",
    "product_sku": "Null",
    "product_Product_category": "Fotografie",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Montag, 29.5. bis Sonntag, 4.6.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

stock_offers_our_ocr = (

    """
Input:
5€
Rabatt
lidl-fotos.de
Code FU3345 auf
Digitaldruck mit dem
buch A4 Hardcover im
5€ Rabatt auf ein Foto-
Lidl FotosJ

Output:
{
    "product_brand": "Null",
    "product_description": "auf ein Fotobuch A4 Hardcover im Digitaldruck mit dem Code FU3345 auf lidl-fotos.de",
    "product_name": "5 € Rabatt",
    "product_sku": "Null",
    "product_Product_category": "Fotografie",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Montag, 29.5. bis Sonntag, 4.6.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

travel_booklets = """
# Your Role:
You are a useful assistant for extracting product information from a given image.                

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
Strictly follow this format:
{   
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                },
                {
                  "deal_id": "2",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# High priority Instructions for "main_format" and "additional_format":
The values and words of one of the json parameters cannot be repeated in other json parameters.
It is forbidden to add text to the json that is not in the image.
If the image does not contain a product description, but only a name, set the "product_description" to "null".
The "product_description" cannot contain the product name, brand or unit price.
All information present in the image should be written to the appropriate json parameters.

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
Description of the product discount (for example: “-47%”, "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26% gespart","Aktionspreis 6.99") be sure to ignore and do not write “main_format” in any of the parameters.
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"deal_type" should always be "SALES_PRICE" for "deal_1" and "REGULAR_PRICE" for "deal_2".
"deal_2" should contain information related to the "REGULAR_PRICE" price if crosed out price is present.
The offer may contain only "deal_1" with "deal_type": "SALES_PRICE".
"product_sku" is the serial number of the product (Art.-Nr.).
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"price_type" should always be "SALES_PRICE" for "deal_id": "1" and "REGULAR_PRICE" for "deal_id": "2".
"deal_id": "2" should contain information related to the "REGULAR_PRICE" price if crosed out price is present.
The offer may contain only "deal" with "price_type": "SALES_PRICE".
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain only the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
An offer can include a product family (e.g. a furniture collection, a product sold in different variations of sizes, colors, etc.) and may contain:
- General information about the product family.
- Specific information about the member products belonging to the product family.
In this case:
- Add the product family as an individual product and set "is_product_family" to true.
- If there is a price applied to the entire product family (e.g. collection "ab 99.99"), 
  add an individual family deal applied to only the product family and set "is_deal_family" to true.
Ensure that when there is a product family with N member products, the "products" array contains 1 family item and N member items.
The "pricing" entry must always follow the format f"{value:.2f}".
If offer has a discount (for example: "-47%", "-5€", "67% SPAREN", "AKTION -27%", "Sie sparen 55%", "26 gespart", "Aktionspreis 6.99"), be sure to include it in additional_format in discount.

# General instructions:
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
The text from the image must be clearly written into the corresponding parameter without errors.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The "price_by_base_unit" and "deal_pricebybaseunit" (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter") cannot be duplicated, recorded in the "product_description".

"""

travel_booklets_client_ocr = (

    """
Input:
Buchungscode: C2FA01
stimmungen für deutsche Staatsangehörige: ein gültiger Reisepass.
[1] Route A. [2] Route B','Details online. Sonstiges: Routenänderungen vorbehalten. Einreisebe-
Reiseveranstalter: Select Holidays c/o New2go GmbH • Infos S. 2
Balkonkabine Premium 1599.- 1599.- 1799.- 1899.-
Balkonkabine Classic 1499.- 1499.- 1699.- 1799.-
Außenkabine Premium 1299.- 1399.- 1499.- 1599.-
Außenkabine Classic 1199.- 1249.- 1349.- 1449.-
Innenkabine Premium 999.- 1049.- 1149.- 1249.-
Innenkabine Classic 888.- 949.- 999.- 1099.-
Termine 27.06.[1] 29.08.[2] 18.07.[2] 08.08.[2]
Preise & Termine 2023 in €/Person in der 2-Bett-Kabine
Spa','Thalassotherapie-Pool','Sauna,
Whirlpools','Wasserrutsche','Samsara
Restaurants','13 Bars','4 Pools','5
Costa Fascinosa: Ausstattung: 5
','inkl. Vollpension
Costa Fascinos
10-tägige Reise','Premiumklasse-Schiff
Ostsee Kreuzfahrt
Costa Fascinosa
Visby
Route A
LITAUEN
LETTLAND
Riga
Helsinki
Tallinn
Stockholm
FINNLAND
ESTLAND
DEUTSCHLAND
SCHWEDEN
Kiel
C2FA01
Buchungscode:
979.- 10 Tage p.P. ab
888.- a)
-91 €
• Deutsch sprechender
• Trinkgeld an Bord
Vollpension
• 9 ÜN an Bord','inkl.
Inklusivleistungen
C2FA01
Buchungscode:
979.- 10 Tage p.P. ab
888.- a)
-91 €
• Deutsch sprechender
• Trinkgeld an Bord
Vollpension
• 9 ÜN an Bord','inkl.
Inklusivleistungen
i. W. v. € 117.-!
Inkl. Getränkepaket
Buchungscode: C2FA01
stimmungen für deutsche Staatsangehörige: ein gültiger Reisepass.
[1] Route A. [2] Route B','Details online. Sonstiges: Routenänderungen vorbehalten. Einreisebe-
Reiseveranstalter: Select Holidays c/o New2go GmbH • Infos S. 2
Balkonkabine Premium 1599.- 1599.- 1799.- 1899.-
Balkonkabine Classic 1499.- 1499.- 1699.- 1799.-
Außenkabine Premium 1299.- 1399.- 1499.- 1599.-
Außenkabine Classic 1199.- 1249.- 1349.- 1449.-
Innenkabine Premium 999.- 1049.- 1149.- 1249.-
Innenkabine Classic 888.- 949.- 999.- 1099.-
Termine 27.06.[1] 29.08.[2] 18.07.[2] 08.08.[2]
Preise & Termine 2023 in €/Person in der 2-Bett-Kabine
no','Kinderclub.
Diskothek','Shopping-Center','4D-Ki-
Joggingparcours','Theater','Kasino,
türkisches Dampfbad','Fitnesscenter,
,
Spa','Thalassotherapie-Pool','Saun
Whirlpools','Wasserrutsche','Samsara
Restaurants','13 Bars','4 Pools','5
Costa Fascinosa: Ausstattung: 5
Costa Fascinosa','inkl. Vollpension
10-tägige Reise','Premiumklasse-Schiff
Ostsee Kreuzfahrt
C2FA01
Buchungscode:
979.- 10 Tage p.P. ab
888.- a)
-91 €
• Deutsch sprechender
• Trinkgeld an Bord
Vollpension
• 9 ÜN an Bord','inkl.
Inklusivleistungen
C2FA01
Buchungscode:
979.- 10 Tage p.P. ab
888.- a)
-91 €
Kreuzfahrt
für die Dauer der
• Parkplatz inkl. Transfers
Gästeservice an Bord
• Deutsch sprechender
• Trinkgeld an Bord
Vollpension
• 9 ÜN an Bord','inkl.
Inklusivleistungen
C2FA01
Buchungscode:
979.- 10 Tage p.P. ab
888.- a)
-91 €
Kreuzfahrt
für die Dauer der
• Parkplatz inkl. Transfers
Gästeservice an Bord
• Deutsch sprechender
• Trinkgeld an Bord
Vollpension
• 9 ÜN an Bord','inkl.
Inklusivleistungen
Buchungscode:

Output:
{
    "product_brand": "Null",
    "product_description": "Costa Fascinosa: Ausstattung: 5 Restaurants, 13 Bars, 4 Pools, 5 Whirlpools, Wasserrutsche, Samsara Spa, Thalassotherapie-Pool, Sauna, türkisches Dampfbad, Fitnesscenter, Joggingparcours, Theater, Kasino, Diskothek, Shopping-Center, 4D-Kino, Kinderclub. 10-tägige Reise auf dem Premiumklasse-Schiff Costa Fascinosa, Route A: Kiel, LITAUEN, LETTLAND, Riga, ESTLAND, Tallinn, FINNLAND, Helsinki, SCHWEDEN, Stockholm, DEUTSCHLAND. Termine: 27.06.[1], 29.08.[2], 18.07.[2], 08.08.[2]. Preise & Termine 2023 in €/Person in der 2-Bett-Kabine: Balkonkabine Premium 1599.- 1799.- 1899.-, Balkonkabine Classic 1499.- 1699.- 1799.-, Außenkabine Premium 1299.- 1399.- 1599.-, Außenkabine Classic 1199.- 1249.- 1449.-, Innenkabine Premium 999.- 1149.- 1249.-, Innenkabine Classic 888.- 949.- 1099.-. Buchungscode: C2FA01. Preis ab 979.-, -91 €. Inklusivleistungen: Deutsch sprechender Gästeservice an Bord, Trinkgeld an Bord, Vollpension, 9 Übernachtungen an Bord, Parkplatz inkl. Transfers für die Dauer der Kreuzfahrt. Details online unter Route B. Sonstiges: Routenänderungen vorbehalten. Einreisebestimmungen für deutsche Staatsangehörige: ein gültiger Reisepass. Reiseveranstalter: Select Holidays c/o New2go GmbH • Infos S. 2.",
    "product_name": "Ostsee Kreuzfahrt",
    "product_sku": "Null",
    "product_Product_category": "Reisen",
    "deal_1": [
      {
        "deal_conditions": "10 Tage p.P. ab",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 888.0,
        "deal_minPrice": 888.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 979.0,
        "deal_minPrice": 979.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

travel_booklets_our_ocr = (

    """
Input:
03.09 . \n Mittelmeer Kreuzfahrt \n 8 - tägige Reise inkl . Flug , Luxus - Schiff \n Explorer of the Seas , inkl . Vollpension an Bord \n 888. \n 999. \n 1399. \n 1699. \n 11.06 . \n 1049. \n 1149. \n 1499 . \n 1699. \n Buchungscode : C19201 \n Reiseverlauf 1. Tag : Anreise . Flug chenland ) . 5. Tag : Mykonos ( Grie nach Bologna , Transfer zum Hafen chenland ) . 6. Tag : Argostoli ( Grie ( Ab : 19.00 Uhr ) . 2. Tag : Kotor ( Mon- chenland ) . 7. Tag : Erholung auf See . tenegro ) . 3. Tag : Korfu ( Griechen- 8. Tag : Ravenna ( Italien ) ( An : 6.00 land ) . 4. Tag : Piräus / Athen ( Grie- Uhr ) , Transfer , Rückflug . \n Preise & Termine 2023 in € / Person in der 2 - Bett - Kabine Abflughafen \n Frankfurt \n Termine \n Innenkabine Standard \n Innenkabine Superior \n Außenkabine \n Balkonkabine \n Sonstiges : Routenänderungen vorbehalten . \n Reiseveranstalter : Select Holidays c / o New2go GmbH \n Inkl . Hin- & \n Rückflug ! \n 23.07 . , \n 20.08 . \n 1249. \n 1299. \n 1549. \n 1949. \n 25.06 . , \n 17.09 . \n 1349. \n 1399. \n 1549. \n 1999. \n Montenegro , Kotor \n ITALIEN \n Bologna \n Ravenna \n Mittelmeer \n Adria \n MONTENEGRO Kotor \n GRIECHENLAND \n Korfu Mykonos Piräus / Athen \n Agostoli \n -311 € \n 8 Tage p.P. ab 1199 .- \n 888.- ) \n Buchungscode : \n C19201 \n Inklusivleistungen \n • Flug ab / bis Frankfurt nach Bologna \n • Transfers laut Reiseverlauf \n Rail & Fly UNOSCO \n inclusive \n • 7 Übernachtungen an Bord , inkl . Vollpension \n ✰✰✰ Best Preis \n Garantie \n

Output:
{
    "product_brand": "Null",
    "product_description": "8-tägige Reise inkl. Flug auf dem Luxus-Schiff Explorer of the Seas, inkl. Vollpension an Bord. Route: Anreise. Flug nach Bologna, Transfer zum Hafen, Kotor (Montenegro), Korfu (Griechenland), Piräus/Athen (Griechenland), Mykonos (Griechenland), Argostoli (Griechenland), Erholung auf See, Ravenna (Italien) (An: 6.00 Uhr),Transfer, Rückflug. Termine: 03.09., 11.06., 23.07., 20.08., 25.06., 17.09. Preise & Termine 2023 in €/Person in der 2-Bett-Kabine: Balkonkabine 1699.- 1949.- 1999.-, Außenkabine 1399.- 1499.- 1549.-, Innenkabine Superior 999.- 1149.- 1399.-, Innenkabine Standard 888.- 1049.- 1349.-. Buchungscode: C19201. Preis ab 1199.-, -311 €. Inklusivleistungen: 7 Übernachtungen an Bord, Transfers laut Reiseverlauf, Flug ab/bis Frankfurt nach Bologna. Sonstiges: Routenänderungen vorbehalten. Reiseveranstalter: Select Holidays c/o New2go GmbH • Infos S.2.",
    "product_name": "Mittelmeer Kreuzfahrt",
    "product_sku": "Null",
    "product_Product_category": "Reisen",
    "deal_1": [
      {
        "deal_conditions": "8 Tage p.P. ab",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 888.0,
        "deal_minPrice": 888.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 1199.0,
        "deal_minPrice": 1199.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

stocks = """
# Your Role:
You are a useful assistant for extracting product information from a given image.              

# Output Format:
Your answer should be purely json, without any additional explanation such as "```json", for example.
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

# Instructions for "main_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
"product_name" cannot contain the words from "product_description" and "product_brand".
"product_brand" cannot contain the words from "product_name" and "product_description".
The unit size (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm") should be written in the "product_description".
"product_name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"product_name" always has a value.
"deal_loyaltycard" can only have "true" or "false" values.
"product_sku" is the serial number of the product.
"product_sku" cannot be duplicated in the "product_description".
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in German language.
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
If the image contains the validity period of the deal the validity period of the deal (e.g. "ab Donnerstag, 1.2"), it should be written in the "deal_description".
"deal_pricebybaseunit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
The "deal_maxPrice" and "deal_minPrice" can only have "Null" by default.

# Instructions for "additional_format":
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
The "product_description" cannot contain the words from "name", "brand" and "price_by_base_unit".
"name" cannot contain the words from "product_description" and "brand".
"brand" cannot contain the words from "name" and "product_description".
"name" always has a value.
"name" can be taken only from the description on the image, not from the packaging or photo of the product itself.
"is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
"unit_size" must contain only the size information (volume, weight, lenghts, etc.) of a single unit (e.g. "1L Packung", "je 100 g", "ca 20 x 20 cm").
"type" can only have "SALES" by default.
"bundle_size" must contain only the size information about the bundle (e.g. "Kasten = 12 x 1L").
"deposit" must include only the deposit costs (e.g. 'zzgl. 4.50 Pfand').
"terms_and_conditions" must contain only the terms and conditions to activate the discounted price.
"validity_period" must contain only the validity period of the deal (e.g. "ab Donnerstag, 1.2").
"price_by_base_unit" must contain the price by base unit (e.g. "1 l = € 1,33", "(1 kg = 11,84/ATG)", "5,20/Liter").
"discount" must contain only the description of the discount or remuneration (e.g. "Sie sparen 50%", "-50%").
The "pricing" can only have "Null" by default.

# Rule of the highest rank: 
The values and words of one of the json parameters cannot be repeated in other json parameters.

# General instructions:
The price description (for example: "tages-frischer Preis") must be recorded in "deal_description.
All textual information present in the image should be written to the appropriate json parameters.
The unit price (for example: "1 kg = 15.98", "1 l = 19.93", "kg-Preis") should always be recorded in the "deal_pricebybaseunit" and "price_by_base_unit" and cannot be duplicated in the "product_description".
When writing information to the "product_description" parameter, each new line must be shifted in accordance with the information in the image, the shift should be marked with the symbol "\n".
The description of the possibility of ordering goods online (for example: "nur online", "auch online".) should be recorded in the "deal_description".
"price_type" and "deal_type" should always be "OTHER".
The output json should contain only the text that is present in the input image in its original form, without changes or additions.
If there is no data for the parameter, then indicate "Null".
The value "Null" must always be capitalized.
The text from the image must be clearly written into the corresponding parameter without errors.
It is forbidden to add text to the json that is not in the image.
The word "Aktion" and "KNALLER" do not refer to any parameter and should be ignored.
The input text should be written grammatically correct in German, even if there are errors in the input text. Pay particular attention to broken words and hyphens.
"""

stocks_client_ocr = (

    """
Input:
Buchungscode: LBYPR2303
Zusatzkosten pro Tag: Kurtaxe: ca. € 1.50/Person','ca. € 1.-Kind ( 6 - 15 J.).
Sonstiges:
Reiseveranstalter: HTH Hanse Touristik Hamburg GmbH • Infos S.2
07.07.-08.09.
30.03.-06.04.','17.05.-06.07.
18.03.-29.03.','15.04.-16.05.','09.09.-03.11.
04.11.-19.11.
Anreise täglich
€ /Person im Studio/Familienstudio
Termine 2023 i
Preise &
Familienstudio: mit Stockbett
Kind.
+ 1
2 Erw.
Belegung: max.
Terrasse.
WLAN und Balkon/
TV,
sche/ WC,
bahn und Minigolf. Studio: mit Du-
Kegel-
Bar,
Restaurant,
Lift,
zeption,
Ausstattung: Re-
gelegen.
Englmar
in St.
Lage:
Predigtstuhl Resort:
Ultra All Inclusive
Predigtstuhl Resort,
Eigenanreise','3','5 bzw. 7 Nächte,
Bayerischer Wald St. Englmar
Predigtstuhl Resort
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
129.-
-30 €
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
a)
129.-
-30 €
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
Ultra All
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
2 Kinder bis 11 Jahre frei!
Buchungscode: LBYPR2303
Sonstiges: Zusatzkosten pro Tag: Kurtaxe: ca. € 1.50/Person','ca. € 1.-Kind ( 6 - 15 J.).
Reiseveranstalter: HTH Hanse Touristik Hamburg GmbH
07.07.-08.09. 229.- 349.- 469.-
30.03.-06.04.','17.05.-06.07. 199.- 289.- 379.-
18.03.-29.03.','15.04.-16.05.','09.09.-03.11. 169.- 239.- 329.-
04.11.-19.11. 129.- 199.- 269.-
Anreise täglich 3 Nächte 5 Nächte 7 Nächte
Preise & Termine 2023 in € /Person im Studio/Familienstudio
• Zuschlag App.: ab € 40.-
Wunschleistung pro Person:
Kinder.
räumen. Belegung: max. 2 Erw. + 3
Kinder. App.: größer','mit 2 Schlaf-
für Kinder. Belegung max. 2 Erw. + 2
Kind. Familienstudio: mit Stockbett
Terrasse. Belegung: max. 2 Erw. + 1
sche/ WC','TV','WLAN und Balkon/
bahn und Minigolf. Studio: mit Du-
zeption','Lift','Restaurant','Bar','Kegel-
Englmar gelegen. Ausstattung: Re-
Predigtstuhl Resort: Lage: in St.
Ultra All Inclusive
Predigtstuhl Resort,
Eigenanreise','3','5 bzw. 7 Nächte,
Bayerischer Wald St. Englmar
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
a)
129.-
-30 €
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
Ultra All
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
129.- a)
-30 €
zertifizierte Soccer- Halle
• Eintritt in die FIFA-
Saunalandschaft
• Bade- und
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
• 3','5 bzw. 7 ÜN','Ultra All
Inklusivleistungen
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
a)
129.-
-30 €
zertifizierte Soccer- Halle
• Eintritt in die FIFA-
Saunalandschaft
• Bade- und
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
Ultra All
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
Buchungscode:
-30 €
lidl- reisen.de
reisen
Eigen an-
lidl- reisen.de
reisen

Output:
{
    "product_brand": "Lidl Reisen",
    "product_description": "Eigenanreise, 3, 5 bzw. 7 Nächte, Predigtstuhl Resort, Ultra All Inclusive. Predigtstuhl Resort: Lage: in St. Englmar gelegen. Ausstattung: Rezeption, Lift, Restaurant, Bar, Kegelbahn und Minigolf. Studio: mit Dusche/ WC, TV, WLAN und Balkon/ Terrasse. Belegung: max. 2 Erw. + 1 Kind. Familienstudio: mit Stockbett für Kinder. Belegung max. 2 Erw. + 2 Kinder. App.: größer, mit 2 Schlafräumen. Belegung: max. 2 Erw. + 3 Kinder. Inkl. Eintritt ins Biermuseum! Buchungscode: LBYPR2303",
    "product_name": "Bayerischer Wald St. Englmar",
    "product_sku": "Null",
    "product_Product_category": "Reisen",
    "deal_1": [
      {
        "deal_conditions": "3 Nächte p.P. ab",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 129.0,
        "deal_minPrice": 129.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 159.0,
        "deal_minPrice": 159.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Wunschleistung pro Person: Zuschlag App.: ab € 40.-",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
},

Input:
5€
Rabatt
lidl-fotos.de
Code FU3345 auf
Digitaldruck mit dem
buch A4 Hardcover im
5€ Rabatt auf ein Foto-
Lidl FotosJ

Output:
{
    "product_brand": "Null",
    "product_description": "auf ein Fotobuch A4 Hardcover im Digitaldruck mit dem Code FU3345 auf lidl-fotos.de",
    "product_name": "5 € Rabatt",
    "product_sku": "Null",
    "product_Product_category": "Fotografie",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Montag, 29.5. bis Sonntag, 4.6.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

stocks_our_ocr = (

    """
Input:
Buchungscode: LBYPR2303
Zusatzkosten pro Tag: Kurtaxe: ca. € 1.50/Person','ca. € 1.-Kind ( 6 - 15 J.).
Sonstiges:
Reiseveranstalter: HTH Hanse Touristik Hamburg GmbH • Infos S.2
07.07.-08.09.
30.03.-06.04.','17.05.-06.07.
18.03.-29.03.','15.04.-16.05.','09.09.-03.11.
04.11.-19.11.
Anreise täglich
€ /Person im Studio/Familienstudio
Termine 2023 i
Preise &
Familienstudio: mit Stockbett
Kind.
+ 1
2 Erw.
Belegung: max.
Terrasse.
WLAN und Balkon/
TV,
sche/ WC,
bahn und Minigolf. Studio: mit Du-
Kegel-
Bar,
Restaurant,
Lift,
zeption,
Ausstattung: Re-
gelegen.
Englmar
in St.
Lage:
Predigtstuhl Resort:
Ultra All Inclusive
Predigtstuhl Resort,
Eigenanreise','3','5 bzw. 7 Nächte,
Bayerischer Wald St. Englmar
Predigtstuhl Resort
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
129.-
-30 €
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
a)
129.-
-30 €
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
Ultra All
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
2 Kinder bis 11 Jahre frei!
Buchungscode: LBYPR2303
Sonstiges: Zusatzkosten pro Tag: Kurtaxe: ca. € 1.50/Person','ca. € 1.-Kind ( 6 - 15 J.).
Reiseveranstalter: HTH Hanse Touristik Hamburg GmbH
07.07.-08.09. 229.- 349.- 469.-
30.03.-06.04.','17.05.-06.07. 199.- 289.- 379.-
18.03.-29.03.','15.04.-16.05.','09.09.-03.11. 169.- 239.- 329.-
04.11.-19.11. 129.- 199.- 269.-
Anreise täglich 3 Nächte 5 Nächte 7 Nächte
Preise & Termine 2023 in € /Person im Studio/Familienstudio
• Zuschlag App.: ab € 40.-
Wunschleistung pro Person:
Kinder.
räumen. Belegung: max. 2 Erw. + 3
Kinder. App.: größer','mit 2 Schlaf-
für Kinder. Belegung max. 2 Erw. + 2
Kind. Familienstudio: mit Stockbett
Terrasse. Belegung: max. 2 Erw. + 1
sche/ WC','TV','WLAN und Balkon/
bahn und Minigolf. Studio: mit Du-
zeption','Lift','Restaurant','Bar','Kegel-
Englmar gelegen. Ausstattung: Re-
Predigtstuhl Resort: Lage: in St.
Ultra All Inclusive
Predigtstuhl Resort,
Eigenanreise','3','5 bzw. 7 Nächte,
Bayerischer Wald St. Englmar
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
a)
129.-
-30 €
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
Ultra All
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
129.- a)
-30 €
zertifizierte Soccer- Halle
• Eintritt in die FIFA-
Saunalandschaft
• Bade- und
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
• 3','5 bzw. 7 ÜN','Ultra All
Inklusivleistungen
LBYPR2303
Buchungscode:
159.- 3 Nächte p.P. ab
a)
129.-
-30 €
zertifizierte Soccer- Halle
• Eintritt in die FIFA-
Saunalandschaft
• Bade- und
• Kinderbetreuung
• Indoor-Spielhalle
Inclusive bis 22.00 Uhr
Ultra All
• 3','5 bzw. 7 ÜN,
Inklusivleistungen
Buchungscode:
-30 €
lidl- reisen.de
reisen
Eigen an-
lidl- reisen.de
reisen

Output:
{
    "product_brand": "Lidl Reisen",
    "product_description": "Eigenanreise, 3, 5 bzw. 7 Nächte, Predigtstuhl Resort, Ultra All Inclusive. Predigtstuhl Resort: Lage: in St. Englmar gelegen. Ausstattung: Rezeption, Lift, Restaurant, Bar, Kegelbahn und Minigolf. Studio: mit Dusche/ WC, TV, WLAN und Balkon/ Terrasse. Belegung: max. 2 Erw. + 1 Kind. Familienstudio: mit Stockbett für Kinder. Belegung max. 2 Erw. + 2 Kinder. App.: größer, mit 2 Schlafräumen. Belegung: max. 2 Erw. + 3 Kinder. Inkl. Eintritt ins Biermuseum! Buchungscode: LBYPR2303",
    "product_name": "Bayerischer Wald St. Englmar",
    "product_sku": "Null",
    "product_Product_category": "Reisen",
    "deal_1": [
      {
        "deal_conditions": "3 Nächte p.P. ab",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 129.0,
        "deal_minPrice": 129.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 159.0,
        "deal_minPrice": 159.0,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Wunschleistung pro Person: Zuschlag App.: ab € 40.-",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

# Prompts for French offers


one_price = """
#Your Role:
You will be provided with text relating to offer from the promotional brochure.

#Output Format:
Your answer should be purely json, without any additional explanation such as ```json, for example. Your extracted data should be presented in JSON format as follows: Always follow the structure given in the Output Format when formulating your response.
```json
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": "REGULAR_PRICE"
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

input text

# Instructions :
"product_name" always has a value.
If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
In the "product_name" parameter, the product name must be written in full.
Extract "deal_pricebybaseunit" from text segments containing only the price by base unit in the format <base-unit> = <price> or similar (for example, 1 l = € 1.50, Le kg : 5,20 €, 9,95 € le kg).
Rule: "deal_pricebybaseunit" can have a value only if the word "Soit" is specified before the unit price (should be complete, for example: "Soit 23,34 € le kg, Soit le L : 10,35 €"), if this word is missing, specify the value "Null".
The quantity of the product, such as weight or volume (ml, l, g, kg), is always recorded in the "product_description".
The input text should be written grammatically correct in French, even if there are errors in the input text.
Pay particular attention to broken words and hyphens.
If the input text has not been assigned to any of the parameters, it should be written in "product_description".
It is forbidden to write "deal" without numbering, always follow the numbering, for example deal_1, deal_2, deal_3 and so on.
If there is no data for the category, then indicate Null.
For "product_product_category", define a product category like Google product category does.
For "product_product_category", the result must be in French language.
"is_product_family", "loyalty_card", "is_deal_family" can only be a value "True" or "False"."
If the offer mentions any loyalty program compte, cagnoté, prix déduit, Prix payé en caisse, Prix carte, Sans carte, then "deal_loyaltycard" should be set to True.
The value of one json parameter cannot be repeated in another json parameter.
In additional_format the  "type" can acquire only such values: SALES.
 **Filter for Discount Percentages**: Any values with a discount in percentage (e.g., "-20%", "50% de réduction") or a specific amount (e.g., "-5€") **must be ignored and excluded** from all JSON parameters, especially from "deal_conditions" and "deal_description".
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
To "deal_description", certain terms of the deal are attributed, such as "Le moins cher".  This information should be recorded in "deal_conditions":
If there is an entry in product_name, it is in no case allowed to duplicate the same value in product_description.
Always write "Null" with a capital letter
"deal_frequency" always has the value "ONCE".
"deal_conditions" must contain only the terms and conditions to activate the discounted price.
"deal_description" can only contain:
- the description of the possibility of ordering goods online (for example: "nur online", "auch online".),
- the validity period of the deal (e.g. "ab Donnerstag, 1.2")

# general conditions :
- The product name cannot be included in the product description.
- To “deal_description” certain deal terms are attributed, such as “Le moins cher”. This information should be recorded in “deal_conditions”.
- Sometimes the deal description is cut out: ie. For “-50% sur le 2e” Al puts “sur le 2e” in “deal_conditions”, whereas the full offer should be in “deal_description”.
- Age grades (including toys) should be placed in “product_description”, ie. “à partir de 3 ans” .
- All offers where there is only one price will have deal_type: regular.
- the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only null
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"


#main_format:
- deal with minPrice and maxPrice should always be the same
- Data such as litsre and grams (e.g. 1 litre = € 1,50, Le kg : 5,20 €, 9,95 € le kg). must not be in product_description
- In no case should the name of the product be recorded in the "product_Description" it is better to write down only Null
- IMPORTANT in "product_brand", "product_description" , "product_name" cannot have the same values
- "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
- "product_name" cannot contain the words from "product_description" and "product_brand".
- "product_brand" cannot contain the words from "product_name" and "product_description".
- deal_description cannot contain a price
- at the very end, when everything is generated, check yourself again and remove the product name from the description IMPORTANT
The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.

# Check at the end:
1. At the very end, cross-check that no words or phrases from "product_name" appear in "product_description". This is critical for accuracy.
2. IMPORTANT remove any words from "product_description" if they are repeated in "product_description". Make sure they do not appear even if they partially match .
3. Check if the description cannot contains words from the product name



""" 


one_price_client_ocr = (

    """
Input:
Soit le kg : 15€90
5% MG
500 g
BOEUF AUCHAN(1)
VIANDE HACHÉE PUR
95
7€
La barquette
FRANCE OR

Output:
{
    "product_brand": "AUCHAN",
    "product_description": "5% MG, FRANCE OR, , 500 g",
    "product_name": "VIANDE HACHÉE PUR BOEUF",
    "product_sku": "Null",
    "product_Product_category": "Viande",
    "deal_1": [
      {
        "deal_conditions": "La barquette",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 7.95,
        "deal_minPrice": 7.95,
        "deal_pricebybaseunit": "Soit le kg : 15€90",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """

)

one_price_our_ocr = (
  

    """
Input:
FRANCE € 2.9⁹9 63 BON " Catégorie 1 Calibre 28+ NOIX SÈCHE FILIÈRE AUCHAN " CULTIVONS LE Le sachet de 650 g Soit le kg : 4 € 60 FRUITS & LEGUMES DE FRANCE Auchan CULTIVONS LEBON

Output:
{
    "product_brand": "AUCHAN",
    "product_description": "FRUITS & LEGUMES DE FRANCE, CULTIVONS LE BON, 650 g",
    "product_name": "NOIX SÈCHE",
    "product_sku": "Null",
    "product_Product_category": "Noix",
    "deal_1": [
      {
        "deal_conditions": "Le sachet",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 2.99,
        "deal_minPrice": 2.99,
        "deal_pricebybaseunit": "Soit le kg : 4€60",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
}

    """

)


one_old_and_one_new_price = """
# Your Role:
You will be provided with text relating to offers from a promotional brochure.

# Output Format:
Provide your answer in pure JSON format, without any additional explanation such as ```json. Structure the data in JSON exactly as follows:

{
    "main_format": {
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
                "deal_conditions": "",
                "deal_currency": "",
                "deal_description": "",
                "deal_frequency": "",
                "deal_maxPrice": "",
                "deal_minPrice": "",
                "deal_pricebybaseunit": "",
                "deal_loyaltycard": "",
                "deal_type": ""
            }
        ],
    },

    "additional_format": {
        "products": [
            {
                "product_id": "1",
                "brand": "",
                "name": "",
                "details": {
                    "unit_size": "",
                    "bundle_size": "",
                    "deposit": "",
                    "origin_country": "",
                    "product_description": ""
                },
                "is_product_family": ""
            }
        ],
        "deals": [
            {
                "deal_id": "1",
                "type": "",
                "pricing": "",
                "price_type": "",
                "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                },
                "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                },
                "applied_to": "product-id",
                "is_deal_family": ""
            }
        ]
    }
}

### Instructions 1:
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- "product_name" always has a value and cannot appear in "product_description".
- "product_description" cannot contain information related to "product_name" or "deal_pricebybaseunit".
- Avoid repeating words from "product_name" in "product_description."
- Always write "product_name" in full in the parameter.
- Extract "deal_pricebybaseunit" in the format <base-unit> = <price> (e.g., 1 l = €1.50).
- Include product quantities (ml, l, g, kg) in "product_description".
- Ignore discounts (e.g., -13%, -5€, 2ème à -50%).
- Correct any grammatical errors in French input, especially broken words.
- Unassigned input text should go into "product_description".
- Deals should always be numbered (e.g., deal_1, deal_2).
- Use "Null" if no data is available for a category.
- Use French for "product_Product_category" (Google category style).
- "deal_loyaltycard" can only be "False" or "True".
- Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
- deal_description cannot contain a price with tax "1.91€ TTC"
- always write "Null" with a capital letter
- dont record sku number in "product_description" and always write this in "product_sku" (for example:"485189/485146/485138/485170/485162.") 
= if there is a TTC in the description, it should be written in deal_description, but if there is no TTC dont write this
- if text has "Dont éco. contribution : 0,12€TTC" you want to be ignored and record Null
- ALWAYS discount in "-200€" or rescente "-50%" must be ignored 
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- IMPORTAN  in deals "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- IMPORTAN “price_type" need record "SALES_PRICE" or "REGULAR_PRICE”.
- deal_frequency always "ONCE"
- deal_pricebybaseunit always must contain base unit (for example: "le kg : 7,33 €")
- in "deal_conditions" canot contain information about contribution (for example: ""Dont éco. contribution : 0,07€TTC") record Null

# Important Points:
- If loyalty terms (e.g., "compte", "cagnoté", "prix déduit") are mentioned, set "deal_loyaltycard" to "True".
- Ensure unique values for each JSON parameter.
- **"deal_type" can only be "REGULAR_PRICE" and "SALES_PRICE**.

### Important Notes:
1. **Prices without Tax (HT)**:
   - Prices without tax (HT) should **never** be included in any deal or separate entry IMPORTANT.
   - If the HT price is crossed out, **it must be completely ignored** and should **not** be recorded anywhere in the data, including in the `deal_conditions`, `product_description`, or any other fields.
   - **Do not create a separate deal for the HT price**, even if it is crossed out.

2. **Prices with Tax (TTC)**:
   - Prices with tax (TTC) should always be recorded in the deal as the **main price** under the `SALES_PRICE` deal type.
   


# general conditions :
1. **Very important**: The product name cannot be included in the product description.
2. To “deal_description” certain deal terms are attributed, such as “Le moins cher”. This information should be recorded in “deal_conditions”.
3. Sometimes the deal description is cut out: ie. For “-50% sur le 2e” Al puts “sur le 2e” in “deal_conditions”, whereas the full offer should be in “deal_description”.
4. Age grades (including toys) should be placed in “product_description”, ie. “à partir de 3 ans” .
5. All offers where there is only one price will have deal_type: regular.
6. If there is a crossed-out price, it must be recorded in a separate deal with the REGULAR type 
7. The main price is always a separate deal with the REGULAR_PRICE type
8. IMPORTANT ALWAYS The price without tax (HT) must be written in the product_description at the end of the description add (example: "Ouverture frontale. Structure rigide. Compartiment renforcé. <"old crossed out price without tax"99€HT>, <price without tax88€HT> Taille IATA. 452356 ")
11.  just the crossed out price is recorded in a separate deal_type REGULAR_PRICE
    -the price that is not crossed out should go to SALES_PRICE 
12. The "deal_description" describes the terms of the deal, e.g. "Offre valable sur le moins cher" if any.  This information must be complete and recorded in the "deal_description" field.
13. the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only Null
14 in Deal conditions cannot contain information about the price without tax (43.29 €HT)
15. in deal_description if price with tax or not tax  (for example:"1.91€ TTC","3.00€HT") need to record only "TTC" or "HT" without number
16. DONT CREATE DEAL WITH PRICE HT
17. If in "product_description" has same information in "product_name" should be in "product_description" Null


#main_format:
1. deal with minPrice and maxPrice should always be the same
2. Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description "**.
3. Never record in deal price HT 
4. Record in deal only TTC price 


### Instructions 2:
-always check whether the price without TTC tax is correct
-always check that the price without tax is indicated in the product_description(for example: "Inner and outer polypropylene. metal fittings. 8 cm diameter.   <"price excluding tax" 1.59€HT>, <“crossed out price” 43.29€HT">) and always indicate the price with HT in triangular brackets
-Never record two different prices in one deal 
-If you have a price with TTC tax, you should only write it to REGULAR_PRICE and ignore all references to the HT price.
- **Deal numbering**: Each deal should be numbered in the format `deal_1`, `deal_2`, etc., when applicable.
- **Price with tax (TTC)**: If the price includes tax (TTC), it should always be recorded as a `REGULAR_PRICE` deal.
- **Household price without tax (HT)**: 
  - If the price without tax is crossed out, it must be completely ignored and not recorded.
  - If the price without tax contains the letters HT, then this price should not be recorded in the deal
  - Always indicate the price, the crossed-out price excluding tax and the price excluding tax in the product description (for example: "Inner and outer polypropylene. metal fittings. 8 cm diameter.   <"price excluding tax" 1.59€HT>, <“crossed out price” 43.29€HT>") and always indicate the price with HT in brackets 
- **Product Description**:
  - Never repeat the product name in the `product_description`.
- **Deal Conditions**: 
  - If there’s an age rating (e.g., "à partir de 3 ans"), it should be placed in `product_description`.


### Check yourself
- Never make up data yourself
- check it is true  product_brand
- check in "deals" in "type" field should contain only the value  "SALES"
- check in  "deals" in "type" cannot contain "REGULAR"
- check if offer cannot contain TTC dont record in deal_description
- "deal_type" in "main_format" must be "SALES_PRICE" AND "REGULAR_PRICE"
- crossed out prise always "REGULAR_PRICE"
- values such as "1€ de remise immédiate" must be record in "deal_condition" 
- check whether it is really recorded values about taxes in "product_description" (for example:"<28€99HT>","<4€15HT>) and check whether the price with tax corresponds exactly to what is shown
- IMPORTANTAlways check that the euro cents are correct
"""


one_old_and_one_new_price_client_ocr = (

    """
Input:
Garantie 2 ans
Réf. 429181
thermostat réglable de 80 à 200 °c','puissance 1400 w
symboles LED','départ différé','minuterie jusqu'à 60 min,
poisson','panneau de commande numérique tactile avec
- bacon - poulet - crevettes - steak - gâteau - légumes -
Cuve de 3 l soit environ 400 g','8 programmes : frites
FRITEUSE KITCHENCOOK AIRMED
d’éco-participation
Dont 0,50€
99
49€
99
79€
de remise immédiate
30€

Output:
{
    "product_brand": "KITCHENCOOK",
    "product_description": "Cuve de 3 l soit environ 400 g, 8 programmes : frites - bacon - poulet - crevettes - steak - gâteau - légumes - poisson, panneau de commande numérique tactile avec symboles LED, départ différé, minuterie jusqu'à 60 min, thermostat réglable de 80 à 200 °c, puissance 1400 w, Garantie 2 ans, Dont 0,50€ d'éco - participation",
    "product_name": "FRITEUSE AIRMED",
    "product_sku": "429181",
    "product_Product_category": "Appareils de cuisine",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 49.99,
        "deal_minPrice": 49.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 79.99,
        "deal_minPrice": 79.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

one_old_and_one_new_price_our_ocr = (

    """
Input:
KITCHENCOOK 7999 € 4999⁹9 Dont 0,50 € d'éco - participation FRITEUSE KITCHENCOOK AIRMED Cuve de 3 l soit environ 400 g , 8 programmes : frites - bacon - poulet - crevettes - steak - gâteau - légumes - poisson , panneau de commande numérique tactile avec symboles LED , départ différé , minuterie jusqu'à 60 min , thermostat réglable de 80 à 200 ° c , puissance 1400 w Réf . 429181 Garantie 2 ans 30 € de remise immédiate

Output:
{
    "product_brand": "KITCHENCOOK",
    "product_description": "Cuve de 3 l soit environ 400 g, 8 programmes : frites - bacon - poulet - crevettes - steak - gâteau - légumes - poisson, panneau de commande numérique tactile avec symboles LED, départ différé, minuterie jusqu'à 60 min, thermostat réglable de 80 à 200 °c, puissance 1400 w, Garantie 2 ans, Dont 0,50€ d'éco - participation",
    "product_name": "FRITEUSE AIRMED",
    "product_sku": "429181",
    "product_Product_category": "Appareils de cuisine",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 49.99,
        "deal_minPrice": 49.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 79.99,
        "deal_minPrice": 79.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)


price_reduced_on_the_n_th_product_only = """
Your Role:
You will be provided with text relating to an offer from the promotional brochure.

Output Format:
Your answer should be purely in JSON, without any additional explanation or code formatting such as "```json". The extracted data should follow this JSON structure exactly:
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

### Instructions 1:


"product_name" must always have a value.
Ensure "product_name" has the complete product name.
Extract "deal_pricebybaseunit" only from segments containing the base unit price in the format <base-unit> = <price>, like "1 l = € 1.50," "Le kg : 5,20 €," or "9,95 € le kg."
Data such price as litre and grams (e.g. 1 litre = € 1,50, Le kg : 5,20 €, 9,95 € le kg). must not be in product_description
Avoid repeating words from "product_name" in "product_description."
"product_description" cannot contain information related to "product_name" or "deal_pricebybaseunit".
"product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
Any unassigned input data should go in "product_description."
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
in main_format product_description should be has full descriptions about all price
All available prices on the page should be displayed in the product_description. This will provide complete information, exclude only those prices if these prices are already in the deal_minPrice or deal_maxPrice fields. Include all prices in the product_description for a detailed description of each product.
Ignore discounts (e.g., -13%, -5€, 2ème à - 50%) for all JSON parameters.
Ensure French language accuracy, correcting broken or hyphenated words.
record each individual "deal" sequentially (for example: "deal_1", "deal_2", "deal_3").
If the category is unknown, use "Null" for "product_product_category."
Set "product_product_category" as a French-language Google product category.
The "deal_loyaltycard" can only be "True" or "False."
The price for one item should be recorded in a separate transaction (deal_1) with the "REGULAR_PRICE" type, and the price for several items should be recorded in a separate transaction (deal_2) with the "SALES_PRICE" type.
The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
write the unit price (for example: "soit l'unite") in regular and the discounted price (for example: "les 2") in sales
record baseunit (for example:"soit le kg:10.77") in deal_pricebybaseunit
in deal_conditions record only condition not full text and full text should be record in deal_description
for each deal, the conditions should be recorded in separate deals (for example: "deal_1_conditions: les 2", "deal_2_conditions: soit l'unite")
if deal_conditions and deal_description are duplicated, then write "Null" in deal_description 
if product_brand is (for example:"PAIC","kinder") then "product_name": (for example:"Exel","bueno") and so on

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "True" or "False" values.
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- IMPORTANT in product_description cannot feed values (for example: "Soit le kg : 14,68 €" ) from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- ALWAYS discount in "-200€" or rescente "-50%" must be ignored 
- price with type "SALES_PRICE" always less than "REGULAR_PRICE"
- IMPORTANT exclude all price data from the "product_description"
- IMPORTANT  in deals "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- IMPORTANT “price_type" need record "SALES_PRICE" or "REGULAR_PRICE”.
- IMPORTANT exclude all price data from the product description
- IMPORTANT deal_description cannot contain information about price and base unit
- IMPORTANT "deal_type" in "main_format" can only be "SALES_PRICE" or "REGULAR_PRICE."

> if price has three price (crossed out, regular and discount) then we record only crossed out in "SALES_PRICE" and regular in "REGULAR_PRICE"
> if "deal_conditions" contain text "Les 2 : 17,98 € au lieu de 23,98 €", "soit l'unité 8,99" need to record only "les 2", "soit l'unité"
> ALWAYS exclude in "deal_conditions" and "deal_description" anything about price and base unit include in "deal_pricebybaseunit"
### Instructions 2:
p
If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "True."
Values in one JSON parameter should not duplicate in another.
Adhere strictly to the example structure.
the discounted price will always be SALES_PRICE 
min and max price must always be specified and must be the same for each deal
Unit prices (for example: "Le kg : 24.94 €", "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description" **.
it is important to write the price for for two unit (for example:"soit l'unite") in the SALES deal and one unit (for example:"Les 2 : 17,98 € au lieu de 23,98 €"  in deal_conditions) in REGULAR
Be sure to record the price for one item and the price for multiple items in a separate deal
indicate only the price for one product and the price of the product that will cost at a discount
if the deal_conditions contains the condition in a complete phrase , only in this case you need to write null in the deal_description
each individual deal must be recorded in a separate deal_1 and deal_2


### Check yourself
- if in "deal_conditions" nothing to indicate, then write null
- value of discaunt always ignored
- check it is true  product_brand
- check in "deals" in "type" field should contain only the value  "SALES" 
- check that the "deal_description" does not contain a price for the product (for example: “Soit les 2 produits : 3,50 €”)
- simple "type" must be only "SALES" not "SALES_PRICE" not "REGULAR_PRICE" not "REGULAR"
- check that the data about price and base unit always exlude from "deal_description" IF NOT DESCRIPTION RECORD NULL
- "deal_type" in "main_format" must be "SALES_PRICE" AND "REGULAR_PRICE"
""" 
# do not indicate the price that is the total price for two products if it is deal_3, just ignore it and do not write deal_3
#indicate only the price for one product and the price of the product that will cost at a discount  

# The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
# To "deal_description", certain terms of the deal are attributed, such as "Le moins cher".  This information should be recorded in "deal_conditions":
price_reduced_on_the_n_th_product_only_client_ocr = (

    """
Input:
Vendu seul : 2€35
Soit le kg : 4€41
4 x 100 g
Nature
SKYR DANONE
77
1€
Soit l’unité
au lieu de 4€70
53
3€
Les 2
sur le 2ème
50%
France
Transformé en

Output:
{
    "product_brand": "DANONE",
    "product_description": "Nature, Transformé en France, 4 x 100 g",
    "product_name": "SKYR",
    "product_sku": "Null",
    "product_Product_category": "Produits laitiers",
    "deal_1": [
      {
        "deal_conditions": "Les 2",
        "deal_currency": "EUR",
        "deal_description": "Soit l’unité 1€77, Vendu seul : 2€35",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.53,
        "deal_minPrice": 3.53,
        "deal_pricebybaseunit": "Soit le kg : 4€41",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Soit l’unité",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 4.70,
        "deal_minPrice": 4.70,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

price_reduced_on_the_n_th_product_only_our_ocr = (

    """
Input:
Transformé en France SKYR 50% sur le 2ème www Les 2 3 au lieu de 4 € 70 Dwww SKYR T AMAA SP SKYR 53 Soit l'unité € 19/17 77 Skyp SKYR Dobrino Ma DPOW SKYR SKYR DANONE Nature 4x100 g Soit le kg : 4 € 41 Vendu seul : 2 € 35

Output:
{
    "product_brand": "DANONE",
    "product_description": "Nature, Transformé en France, Dobrino Ma DPOW, 4 x 100 g",
    "product_name": "SKYR",
    "product_sku": "Null",
    "product_Product_category": "Produits laitiers",
    "deal_1": [
      {
        "deal_conditions": "Les 2",
        "deal_currency": "EUR",
        "deal_description": "Soit l’unité 1€77, Vendu seul : 2€35",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 3.53,
        "deal_minPrice": 3.53,
        "deal_pricebybaseunit": "Soit le kg : 4€41",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 4.70,
        "deal_minPrice": 4.70,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)


one_price_with_and_one_price_without_the_card =  """
Your Role:
You will be provided with text relating to an offer from the promotional brochure.

Output Format:
Your answer should be purely in JSON, without any additional explanation or code formatting such as "```json". The extracted data should follow this JSON structure exactly:
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}
Instructions 1:

"product_name" must always have a value.
Avoid repeating words from "product_name" in "product_description."
"product_description" should not include data related to "product_name" or "deal_pricebybaseunit."
Ensure "product_name" has the complete product name.
Extract "deal_pricebybaseunit" from text segments containing only the price by base unit in the format <base-unit> = <price> or similar (for example, 1 l = € 1.50, Le kg : 5,20 €, 9,95 € le kg).
it is important not to write the base price per unit in the product_description (e.g. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg).
"product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
Ignore discounts (e.g., -13%, -5€, 2ème à - 50%) for all JSON parameters.
Ensure French language accuracy, correcting broken or hyphenated words.
Any unassigned input data should go in "product_description."
Number each "deal" sequentially (e.g., deal_1, deal_2, deal_3).
If the category is unknown, use "Null" for "product_product_category."
Set "product_product_category" as a French-language Google product category.
 The "deal_loyaltycard" can only be "True" or "False."
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only Null

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycadr is always False
- if the condition always record in "deal_conditions"
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- ALWAYS discount in "-200€" or rescente "-50%" must be ignored 

Instructions 2:

If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "Yes."
Values in one JSON parameter should not duplicate in another.
Adhere strictly to the example structure.
"deal_type" can only be "SALES_PRICE" or "REGULAR_PRICE."
make a separate deal for each price
min and max price must always be specified and must be the same for each deal
Unit prices (for example: "Le kg : 24.94 €", "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description "**.
check whether there are any base units in the product_description (for example. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg), if so, remove them from there
Always check if you have a loyalty card 
The price without a loyalty card is recorded in a transaction of the REGULAR type, and the price with a loyalty card is recorded in a separate transaction of the SALE type.
Each deal moust be in separate deal_n
in deals in additional_format type must be SALES_PRICE
text like be Carte U déduits and so on must be in deal_condition
always indicate the unit (for example: "Le kg : 24.94 €") price in the deal_pricebybaseunit 
the deal_description cannot contain the price for the product (for example:"2€73 le lot"), put it in Null 


### check yourself 
always check that the value without the card is recorded correctly and the value with the card is recorded correctly IMPORTANT
always check is correctly record description in each deal, remember that you cannot have the same description in two deals  IMPORTANT
""" 


one_price_with_and_one_price_without_the_card_client_ocr = (

    """
Input:
avec porte-ustensiles
2 tablettes latérales rabattables
COUVERTS
12
449 !
Sans carte :
Plancha gaz
389!
carte
Prix
Prix sans la carte : 449 !
Garantie 2 ans(3). Chariot roulant en acier. Réf. 3138522114398.
Avec récupérateur des graisses. Allumage piezo électronique.
fonte émaillée l. 60 x P. 40 cm. Dim. totales l. 134 x P. 52 x H. 98 cm.
2 brûleurs 6 kW. Châssis et chariot en acier. Surf. de cuisson en
Plancha gaz EXLD

Output:
{
    "product_brand": "EXLD",
    "product_description": "avec porte-ustensiles, 2 tablettes latérales rabattables, Garantie 2 ans(3). Chariot roulant en acier. Avec récupérateur des graisses. Allumage piezo électronique. 2 brûleurs 6 kW. Châssis et chariot en acier. Surf. de cuisson en fonte émaillée l. 60 x P. 40 cm. Dim. totales l. 134 x P. 52 x H. 98 cm.",
    "product_name": "Plancha gaz",
    "product_sku": "3138522114398",
    "product_Product_category": "Appareils de cuisson",
    "deal_1": [
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 389,
        "deal_minPrice": 389,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Prix sans la carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449,
        "deal_minPrice": 449,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

one_price_with_and_one_price_without_the_card_our_ocr = (

    """
Input:
Prix carte \n castorama \n 389 € \n Plancha gaz \n Sans carte : \n 449 € \n CAMPINGAZ \n O \n + \n tablettes latérales rabattables \n avec porte - ustensiles \n CAMPINGAZ \n 41 12 \n COUVERTS \n Plancha gaz EXLD \n 2 brûleurs 6 kW . Châssis et chariot en acier . Surf . de cuisson en fonte émaillée I. 60 x P. 40 cm . Dim . totales I. 134 x P. 52 x H. 98 cm . Avec récupérateur des graisses . Allumage piezo électronique . Garantie 2 ans ( 3 ) . Chariot roulant en acier . Réf . 3138522114398 . Prix sans la carte : 449 € \n

Output:
{
    "product_brand": "CAMPINGAZ",
    "product_description": "EXLD 2 brûleurs 6 kW. Châssis et chariot en acier. Surf. de cuisson en fonte émaillée I. 60 x P. 40 cm. Dim. totales I. 134 x P. 52 x H. 98 cm. Avec récupérateur des graisses. Allumage piezo électronique. Garantie 2 ans (3). Chariot roulant en acier. tablettes latérales rabattables avec porte-ustensiles.",
    "product_name": "Plancha gaz",
    "product_sku": "3138522114398",
    "product_Product_category": "Appareils de cuisson extérieure",
    "deal_1": [
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 389,
        "deal_minPrice": 389,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Prix sans la carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 449,
        "deal_minPrice": 449,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """
)


money_spared_on_the_card=  """
Your Role:
You will be provided with text related to an offer from the promotional brochure.

Output Format:
Your answer should be purely in JSON, without any additional explanation or code formatting such as "```json". The extracted data should follow this JSON structure exactly:
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ],
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}


Instructions 1:

"product_name" must always have a value.
Avoid repeating words from "product_name" in "product_description."
"product_description" should not include data related to "product_name" or "deal_pricebybaseunit."
Ensure "product_name" has the complete product name.
Extract "deal_pricebybaseunit" only from segments containing the base unit price in the format <base-unit> = <price>, like "1 l = € 1.50," "Le kg : 5,20 €," or "9,95 € le kg."
do not write the base price per unit (e.g. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg) in the product_description.
"product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
Ignore discounts (e.g., -13%, -5€, 2ème à - 50%) for all JSON parameters.
Ensure French language accuracy, correcting broken or hyphenated words.
Any unassigned input data should go in "product_description."
Number each "deal" sequentially (for example: "deal_1", "deal_2", "deal_3").
If the category is unknown, use "Null" for "product_product_category."
Set "product_product_category" as a French-language Google product category.
 The "deal_loyaltycard" can only be "True" or "False."
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
the price with the loyalty card should be recorded in the deal_n with deal_type SALE, and the price without the loyalty card should be recorded in a separate deal_n with deal_type REGULAR
 The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only null

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycadr is always False
- if the condition always record in "deal_conditions"
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- ALWAYS discount in "-200€" or rescente "-50%" must be ignored 

Instructions 2:

If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "Yes."
Values in one JSON parameter should not duplicate in another.
Adhere strictly to the example structure.
"deal_type" can only be "REGULAR_PRICE" or "SALES_PRICE".
check whether there are any base units in the product_description (for example. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg), if there are, then remove them from there
check before generating json, check if all prices are really written in a separate deal.
min and max price should always be the same

### check yourself 
always check that the value without the card is recorded correctly and the value with the card is recorded correctly IMPORTANT
""" 


money_spared_on_the_card_client_ocr = (

    """
Input:
coloris Bleu ou Rose à 18,90 €
Existe aussi le smartphone Paw patrol
Soit 5,98 € sur la Carte Carrefour.
Dès 3 ans. #d
les héros de la Pat' Patrouille.
6 activités pour apprendre et s'amuser avec
repliable et tablette avec touches sensitives.
2 en 1 : ordinateur avec écran LCD','clavier
Paw Patrol
Mon ordinateur tablette éducatif
D’ÉCONOMIES(2)
20%
Prix payé en caisse
d'éco-participation
dont 0,07 €
90
29€
Remise Fidélité déduite
92
23€
Soit

Output:
{
    "product_brand": "Paw Patrol",
    "product_description": "2 en 1 : ordinateur avec écran LCD, clavier repliable et tablette avec touches sensitives. 6 activités pour apprendre et s'amuser avec les héros de la Pat' Patrouille. Dès 3 ans. #d, Existe aussi le smartphone Paw patrol coloris Bleu ou Rose à 18,90 €, dont 0,07 € d'éco-participation",
    "product_name": "Mon ordinateur tablette éducatif",
    "product_sku": "Null",
    "product_Product_category": "Jouets",
    "deal_1": [
      {
        "deal_conditions": "Remise Fidélité déduite",
        "deal_currency": "EUR",
        "deal_description": "Soit 5,98 € sur la Carte Carrefour.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 23.92,
        "deal_minPrice": 23.92,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Prix payé en caisse",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.90,
        "deal_minPrice": 29.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
Soit le kg : 35€75
600 g
MMM!
SURGELÉES
SAUVAGES
GÉANTES
GAMBAS
cagnotte déduite*
16
17€
prix payé en caisse
45
21€
WA
compte
sur votre
soit 4€29
20%

Output:
{
    "product_brand": "MMM!",
    "product_description": "SURGELÉES, SAUVAGES, GÉANTES, 600 g",
    "product_name": "GAMBAS",
    "product_sku": "Null",
    "product_Product_category": "Fruits de mer",
    "deal_1": [
      {
        "deal_conditions": "cagnotte déduite*",
        "deal_currency": "EUR",
        "deal_description": "4€29 sur votre compte",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 17.16,
        "deal_minPrice": 17.16,
        "deal_pricebybaseunit": "Soit le kg : 35€75",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "prix payé en caisse",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 21.45,
        "deal_minPrice": 21.45,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)

money_spared_on_the_card_our_ocr = (

    """
Input:
20 % D'ÉCONOMIES ( 2 ) BERAYS 299⁰ dont 0,07 € d'éco - participation Prix payé en caisse Soit VERKEE 2392 Soit 5,98 € sur la Carte Carrefour . Existe aussi le smartphone Paw patrol Remise Fidélité déduite coloris Bleu ou Rose à 18,90 € Mon ordinateur tablette éducatif Paw Patrol 2 en 1 : ordinateur avec écran LCD , clavier repliable et tablette avec touches sensitives . 6 activités pour apprendre et s'amuser avec les héros de la Pat ' Patrouille . Dès 3 ans .

Output:
{
    "product_brand": "Paw Patrol",
    "product_description": "2 en 1 : ordinateur avec écran LCD, clavier repliable et tablette avec touches sensitives. 6 activités pour apprendre et s'amuser avec les héros de la Pat' Patrouille. Dès 3 ans. #d, Existe aussi le smartphone Paw patrol coloris Bleu ou Rose à 18,90 €, dont 0,07 € d'éco-participation",
    "product_name": "Mon ordinateur tablette éducatif",
    "product_sku": "Null",
    "product_Product_category": "Jouets",
    "deal_1": [
      {
        "deal_conditions": "Remise Fidélité déduite",
        "deal_currency": "EUR",
        "deal_description": "Soit 5,98 € sur la Carte Carrefour.",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 23.92,
        "deal_minPrice": 23.92,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Prix payé en caisse",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.90,
        "deal_minPrice": 29.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
soit 4 € 29 sur votre compte WAACH 20 % 21 % prix payé en caisse € 17.⁹6 cagnotte déduite * Auchan Collection SURGELÉ Mmm ! Gambas géantes sauvages surgelées réchées en océan Indien 11 600 Auchan GAMBAS GÉANTES SAUVAGES SURGELÉES MMM ! 600 g Soit le kg : 35 € 75 Tendres et Savoureuses

Output:
{
    "product_brand": "MMM!",
    "product_description": "SURGELÉES, SAUVAGES, GÉANTES, 600 g, Auchan Collection, réchées en océan Indien, Tendres et Savoureuses",
    "product_name": "GAMBAS",
    "product_sku": "Null",
    "product_Product_category": "Fruits de mer",
    "deal_1": [
      {
        "deal_conditions": "cagnotte déduite*",
        "deal_currency": "EUR",
        "deal_description": "4€29 sur votre compte",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 17.16,
        "deal_minPrice": 17.16,
        "deal_pricebybaseunit": "Soit le kg : 35€75",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "prix payé en caisse",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 21.45,
        "deal_minPrice": 21.45,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
}

    """

)


offer_without_price = """
Your Role:
You will be provided with text related to an offer from the promotional brochure.

Output Format:
Your answer should be purely in JSON, without any additional explanation or code formatting such as "```json". The extracted data should follow this JSON structure exactly:
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}
### Instructions 1:

"product_name" must always have a value.
"product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
Ensure French language accuracy, correcting broken or hyphenated words.
Any unassigned input text should go in "product_description."
If the category is unknown, use "Null" for "product_product_category."
Set "product_product_category" as a French-language Google product category.
 The "deal_loyaltycard" can only be "True" or "False."
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only null

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycadr is always False
- if the condition always record in "deal_conditions"
- cyrrency always € not EUR
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- ALWAYS discount in "-200€" or rescente "-50%" must be ignored 
- ALWAYS if "product_name" = "product_brand" you must exclude value with product_brand  and change null
- ALWAYS if "product_name" !="product_description" record Null 


> IMPORTANT "price_type" and "deal_type" should always be "OTHER".
> "type" should always be "SALES".
> if “product_brand” and “product_description” have the same value as “product_name”, then this value should be excluded from “product_brand” and “product_description”
### Instructions 2:

If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "True".
Adhere strictly to the example structure.
The "deal_type" can only have the value "OTHER."
"deal" entries with "deal_type": "OTHER" cannot include values for "deal_maxPrice" or "deal_minPrice."



### Check yourself
- Check if you have filled in deal_conditions correctly
- Check what "product_brand" , "product_name" the data is not repeated
- IMPORTANT Check what "product_description" , "product_name" the data is not repeated


""" 
# INSTRUCTION 1:  

offer_without_price_client_ocr = (

    """
Input:
des glaces
la gamme
sur
Hors promotions en cours et formats promo
Offre valable sur le moins cher
au choix
sur le 2ème
de remise immédiate
60%

Output:
{
    "product_brand": "Null",
    "product_description": "Null",
    "product_name": "60% de remise immédiate sur le 2ème au choix sur la gamme des glaces",
    "product_sku": "Null",
    "product_Product_category": "Glaces",
    "deal_1": [
      {
        "deal_conditions": "Offre valable sur le moins cher\nHors promotions en cours et formats promo",
        "deal_currency": "Null",
        "deal_description": "60% de remise immédiate",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

offer_without_price_our_ocr = (

    """
Input:
ASHADEMAS \n BEN & JERRY'S \n the \n COOKIE DOUGH cool - lection \n WORG GERATOMI \n Cookie \n new ! \n BAR \n new ! \n new ! \n BEN & J Sun \n 4x \n 100ml \n Choco - 1 \n Cheeseca \n de Cheesecake Ice Cream with \n baby Coed with \n Green , Chocolatey Sains & Ch \n new ! \n nou \n BEN & JERRY'S Cookie Dough \n Vanilla Ice Cream with Chunks of \n Chocolate Chip Cookie Doug \n Offre valable sur le moins cher \n Hors promotions en cours et formats promo \n 60 % \n de remise immédiate sur le 2ème au choix \n sur \n la gamme des glaces \n BEN & JERRY'S \n SURGELÉ \n +2 \n vignettes \n à collectionner \n * Le meilleur des promos \n

Output:
{
    "product_brand": "BEN & JERRY'S",
    "product_description": "Null",
    "product_name": "60% de remise immédiate sur le 2ème au choix sur la gamme des glaces, COOKIE DOUGH cool - lection, de Cheesecake Ice Cream with baby Coed with Green , Chocolatey Sains & Ch, Vanilla Ice Cream with Chunks of Chocolate Chip Cookie Doug",
    "product_sku": "Null",
    "product_Product_category": "Glaces",
    "deal_1": [
      {
        "deal_conditions": "Offre valable sur le moins cher\nHors promotions en cours et formats promo",
        "deal_currency": "Null",
        "deal_description": "60% de remise immédiate, +2 vignettes à collectionner",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "OTHER"
      }
    ]
}

    """

)


offer_without_price_loyalty_card = """
Your Role:
You will be provided with text related to an offer from the promotional brochure.

Output Format:
Your answer should be purely in JSON, without any additional explanation or formatting such as "```json". The extracted data should follow this JSON structure exactly:
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}

Instructions 1:

The "product_name" field must always have a value.
Always include product quantity (e.g., ml, l, g, kg) in "product_description."
Ensure all French text is grammatically correct, fixing any broken words or hyphens.
Any unassigned text from the input should be written in "product_description."
Avoid repeating words from "product_name" in "product_description."
Use "Null" for "product_product_category" if category data is unavailable.
Define "product_product_category" following the structure of a Google product category, and ensure the result is in French.
"deal_loyaltycard" should only be "TRUE" or "False"

the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only null

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycadr is always False
- if the condition always record in "deal_conditions"
- IMPORTANT in "product_brand", "product_description" , "product_name" cannot have the same values
- cyrrency always € not EUR
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- ALWAYS discount in "-200€" or rescente "-50%" must be ignored 

> "loyalty_card" always need have value "True" 
Instructions 2:

Set "deal_loyaltycard" to "True" if there’s any mention of loyalty terms such as "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte."
Follow the exact example structure strictly.
"deal_type" may only have the value "OTHER."
"deal" entries with "deal_type": "OTHER" cannot include values for "deal_maxPrice" or "deal_minPrice."
always check that the product name is not in the product description
Always check if you have a loyalty card
Check if you have filled in deal_conditions correctly


### check yourself 
always check that the value without the card is recorded correctly and the value with the card is recorded correctly IMPORTANT
""" 


offer_without_price_loyalty_card_client_ocr = (

    """
Input:
DÉMAQUILLER
ET DISQUES À
DES COTONS
SUR LA GAMME
PRODUIT AU CHOIX
SUR LE 2ÈME
SUR VOTRE COMPTE*
D’ÉCONOMIE
50%
Offre valable sur le moins cher Offre valable sur le moins cher

Output:
{
    "product_brand": "Null",
    "product_description": "Null",
    "product_name": "50% D’ÉCONOMIE SUR VOTRE COMPTE. SUR LE 2ÈME PRODUIT AU CHOIX SUR LA GAMME DES COTONS ET DISQUES À DÉMAQUILLER",
    "product_sku": "Null",
    "product_Product_category": "Produits de beauté",
    "deal_1": [
      {
        "deal_conditions": "Offre valable sur le moins cher",
        "deal_currency": "Null",
        "deal_description": "50% SUR VOTRE COMPTE*",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ]
}

    """

)

offer_without_price_loyalty_card_our_ocr = (

    """
Input:
Nestle \n LES RECETTES DE \n L'ATELIER . \n AU CHOIX SUR \n LA GAMME \n 68 % D'ÉCONOMIE \n SUR VOTRE COMPTE * \n SUR LE 2ÈME \n Nestle \n LES RECETTES DE \n L'ATELIER . \n hyrtiles Amendes \n & Poisettes BA & \n 70 % \n CACAO \n Nestle \n LES RECETTES DE \n L'ATELIER . BIO \n Nestle \n LES RECETTES DE \n L'ATELIER . \n Raising Amandes & settes RA & H \n Offre valable sur le moins cher Hors promotions en cours et formats promo \n

Output:
{
    "product_brand": "Nestle",
    "product_description": "LES RECETTES DE L'ATELIER, hyrtiles Amendes & Poisettes BA & 70% CACAO, LES RECETTES DE L'ATELIER. BIO, LES RECETTES DE L'ATELIER. Raising Amandes & settes RA & H",
    "product_name": "68% D'ÉCONOMIE SUR VOTRE COMPTE. SUR LE 2ÈME AU CHOIX SUR LA GAMME",
    "product_sku": "Null",
    "product_Product_category": "Chocolat",
    "deal_1": [
      {
        "deal_conditions": "Offre valable sur le moins cher Hors promotions en cours et formats promo",
        "deal_currency": "Null",
        "deal_description": "68% SUR VOTRE COMPTE*",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ]
}

    """

)


size_chart = """
Your Role:
You will be provided with text relating to an offer from the promotional brochure.

Output Format:
Your answer should be in JSON only "```json":
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]
        "deal_2": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}
### Instructions 1:

The "product_name" must always have a value.
Avoid duplicating words from "product_name" in "product_description."
"product_description" should not contain details related to "product_name" or "deal_pricebybaseunit."
Record "deal_pricebybaseunit" based only on exact formats like "<base-unit> = <price>" (e.g., "1 l = € 1.50").
Include quantity (e.g., ml, l, g, kg) in "product_description."
Do not record discounts (like -13%, -5€, 2ème à -50%) in any JSON parameter.
Correct any French grammar errors in the text, even if the original has mistakes.
Text not assigned to specific parameters should go in "product_description."
Use "Null" if there’s no data for "product_product_category."
The "product_product_category" should follow Google product category style and be in French.
"deal_loyaltycard" should be either "True" or "False"
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only Null
When there are two price types, one crossed out and one not crossed out, add the crossed out price to the "REGULAR_PRICE" transaction type of the crossed out price in a separate deal , and the not crossed out price to the "SALES_PRICE" type in a separate deal. 
When there is only one type in the offer, this type is always REGULAR but all prices must be in separate deals
IMPORTANT to stock all prices even if they are repeated in separate deals.
always each price must be in a separate deal with its own number (for example: "deal_1", "deal_2" , "deal_3" ).
min and max prices are always the same

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- The "deal_maxPrice" and "deal_minPrice" must be recorded as a price per unit 

- in "deal_pricebybaseunit" cannot contain value in the "deal_maxPrice" and "deal_minPrice"
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycard is always False
- if the condition always record in "deal_conditions"
- IMPORTANT in "product_brand", "product_description" , "product_name" cannot have the same values
- cyrrency always € not EUR
- deal_description (from exmaple: "-30% de remise immédiate") with discount record only in deal_type "SALES_PRICE"
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
    

> that there can be more than 10 prices and you MUST write them all down in separate deal
> in "deal_pricebybaseunit" need to record "58,93 € le m²"
> in deal_conditions cannot contain price number only "l'unité" and so on
> in deal_description need to record size "220 x 12 cm. Ep. 19mm" and so on
### Instructions 2:

always for each price it is necessary to create a new deal_1 deal_2 and so on
If the text includes different prices for varying product sizes, create multiple "deal" entries for each size and price. Ensure each is in the complete JSON format.
Set "deal_loyaltycard" to "True" if loyalty terms like "compte," "cagnoté," "prix déduit," or "Prix payé en caisse" appear.
No JSON parameter value should repeat in another parameter.
Follow the structure and details exactly as shown in the examples.
"deal_type" should only be "REGULAR_PRICE" and "SALES_PRICE".
If there are more than thirteen sizes, you need to check yourself and verify the exact number of sizes that are recorded in each deal
There are cases when there is just a price (PRIX) and a price with a promo code (PRIX PROMO), then it is necessary to add PRIX to "REGULAR" and PRIX PROMO to "SALES".
check if each size corresponds to each price and only when you are sure only then generate json
Determine the total number of products in the image before you start processing, and make sure all products are included in the JSON, with separate deal_Ns for each."
After processing all the products, check that all items are numbered from 1 to the total number of products in the image, without gaps.
Ensure all items are individually recorded, even if they share similar or identical prices. Each item must be treated as a separate deal, with unique entries for each size or price, to account for every item individually.
"Record only the prices explicitly stated in the text. Do not generate or estimate any prices not present in the source material. If a price is missing, set the value to 'Null' instead of creating a new price."

### Check yourself 
- IMPORTANT Always check all the prices on the offer and always put each price in a separate deal 


""" 

size_chart_client_ocr = (

    """
Input:
VOUS
LIVRÉ CHEZ
VOUS
LIVRÉ CHEZ
S
E
R
I
A
L
U
B
U
T
dont éco-part. 0,30€(2)
ø 3,66 x H 1,22 m à 299 €
Modèle présenté :
le bon fonctionnement de la filtration.
Hydroaération : permet de contrôler
tubulaires Prism INTEX
du montage des bassins
Pour visionner le film
FLASHEZ-MOI
2
PERSONNES
MIN.
45/60
ET NETTOYÉ
SOL PLAT
PISCINE TUBULAIRE PRISM FRAME Garantie légale 2 ans(1)
avec marches amovibles et plateforme. Épaisseur vinyle 0,64 mm.
inclus : bâche de protection','tapis de sol','échelle de sécurité
inclus : cartouche de filtration A','échelle de sécurité avec marches amovibles et plateforme. Épaisseur vinyle : 0,58 mm.
Accessoires
dont éco-part. 0,50€(2)
759€
dont éco-part. 0,50€(2)
649€
dont éco-part. 0,25€(2)
349€
dont éco-part. 0,30€(2)
299€
dont éco-part. 0,25€(2)
259€
Prix
Ø 6,10 x H 1,17 m
Ø 5,49 x H 1,07 m
Ø 4,57 x H 0,91 m
Ø 3,66 x H 1,07 m
Ø 3,66 x H 0,84 m
de nage
Dimensions surface
4,4 m3/h
4,4 m3/h
2,7 m3/h
2,7 m3/h
1,7 m3/h
Filtre à cartouche
32,7 m3
24,3 m3
14,6 m3
10,6 m3
8,6 m3
Capacité du bassin
Ø 6,10 m
Ø 5,49 m
Ø 4,57 m
Ø 3,66 m
Ø 3,66 m
Espace nécessaire
Ø 6,10 x H 1,32 m
Ø 5,49 x H 1,22 m
Ø 4,57 x H 1,07 m
Ø 3,66 x H 1,22 m
Ø 3,66 m x H 99 cm
Dimensions
RONDES
à partir de
dont éco-part. 0,25€(2)
259€
*selon modèle
équipement * :
renforcées
Jambes
PVC
Liner
fournie
Echelle
filtration
Système
dont vous disposez !
nous vous proposons les formes adaptées à l’espace
et économiques. Rondes','ovales ou rectangulaires...
Faciles à monter et à démonter','elles sont à la fois solides
Les piscines tubulaires sont en kit.
SIMPLICITÉ & SOLIDITÉ

Output:
{
    "product_brand": "INTEX",
    "product_description": "Garantie légale 2 ans(1), Les piscines tubulaires sont en kit. Faciles à monter et à démonter, elles sont à la fois solides et économiques. Rondes, ovales ou rectangulaires... nous vous proposons les formes adaptées à l’espace dont vous disposez !, Système filtration, Echelle fournie, Liner PVC, Jambes renforcées, équipement * : à partir de dont éco-part. 0,25€(2) 259€ *selon modèle, Pour visionner le film du montage des bassins FLASHEZ-MOI, 2 PERSONNES MIN. 45/60 ET NETTOYÉ SOL PLAT, Hydroaération : permet de contrôler le bon fonctionnement de la filtration. Modèle présenté : ø 3,66 x H 1,22 m à 299 € dont éco-part. 0,30€(2)",
    "product_name": "PISCINE TUBULAIRE PRISM FRAME",
    "product_sku": "Null",
    "product_Product_category": "Piscines",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,25€(2), Dimensions surface de nage: Ø 3,66 x H 0,84 m, Filtre à cartouche: 1,7 m3/h, Capacité du bassin: 8,6 m3, Espace nécessaire: Ø 3,66 m, Dimensions: Ø 3,66 m x H 99 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 259.00,
        "deal_minPrice": 259.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,30€(2), Dimensions surface de nage: Ø 3,66 x H 1,07 m, Filtre à cartouche: 2,7 m3/h, Capacité du bassin: 10,6 m3, Espace nécessaire: Ø 3,66 m, Dimensions: Ø 3,66 x H 1,22 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 299.00,
        "deal_minPrice": 299.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,25€(2), Dimensions surface de nage: Ø 4,57 x H 0,91 m, Filtre à cartouche: 2,7 m3/h, Capacité du bassin: 14,6 m3, Espace nécessaire: Ø 4,57 m, Dimensions: Ø 4,57 x H 1,07 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 349.00,
        "deal_minPrice": 349.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,50€(2), Dimensions surface de nage: Ø 5,49 x H 1,07 m, Filtre à cartouche: 4,4 m3/h, Capacité du bassin: 24,3 m3, Espace nécessaire: Ø 5,49 m, Dimensions: Ø 5,49 x H 1,22 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 649.00,
        "deal_minPrice": 649.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_5": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,50€(2), Dimensions surface de nage: Ø 6,10 x H 1,17 m, Filtre à cartouche: 4,4 m3/h, Capacité du bassin: 32,7 m3, Espace nécessaire: Ø 6,10 m, Dimensions: Ø 6,10 x H 1,32 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 759.00,
        "deal_minPrice": 759.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
39,99 €
69,99 €x
29,99 €
59,99 €x
19,99 €
39,99 €x
Prix
70 cm
60 cm
46 cm
Tailles
Disponible en différents coloris
Cadenas à code intégré.
Canne télescopique intégrée,
En ABS','4 roues multidirectionnelles,
SHERRER
Valise Jean Louis
La valise cabine* 46 cm
99
19€
99x
39€
À partir de

Output:
{
    "product_brand": "Jean Louis SHERRER",
    "product_description": "Disponible en différents coloris, Cadenas à code intégré, Canne télescopique intégrée, En ABS, 4 roues multidirectionnelles, La valise cabine",
    "product_name": "Valise",
    "product_sku": "Null",
    "product_Product_category": "Bagages",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Taille: 46 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 19.99,
        "deal_minPrice": 19.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.99,
        "deal_minPrice": 39.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Taille: 60 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.99,
        "deal_minPrice": 59.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_5": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Taille: 70 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.99,
        "deal_minPrice": 39.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_6": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 69.99,
        "deal_minPrice": 69.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SREGULAR_PRICE"
      }
    ]
}
    """

)

size_chart_our_ocr = (

    """
Input:
à partir de \n 259 € \n dont éco - part . 0,25 € ( ² ) \n Dimensions Espace nécessaire Capacité du bassin Filtre à cartouche \n Dimensions surface \n de nage \n Prix \n PISCINE TUBULAIRE PRISM FRAME INTEX Garantie légale 2 ans ( ¹ ) \n RONDES \n Ø 4,57 x H 1,07 m \n Ø 4,57 m \n 14,6 m³ \n 2,7 m³ / h \n 0 4,57 x H 0,91 m \n 349 € \n dont éco - part . 0,25 € \n # \n 0 3,66 m x H 99 cm \n Ø 3,66 m \n 8,6 m³ \n 1,7 m³ / h \n Ø 3,66 x H 0,84 m \n 259 € \n dont éco - part . 0,25 € \n Ø 3,66 x H 1,22 m \n 0 3,66 m \n 10,6 m³ \n 2,7 m³ / h \n 0 3,66 x H 1,07 m \n 299 € \n dont éco - part . 0,30 € \n Hydroaération : permet de contrôler le bon fonctionnement de la filtration . \n Modèle présenté : \n Ø 3,66 x H 1,22 m à 299 € \n dont éco - part . 0,30 € ( 2² ) \n INTEX \n Ø 5,49 x H 1,22 m \n Ø 5,49 m \n 24,3 m³ \n 4,4 m³ / h \n Ø 5,49 x H 1,07 m \n 649 € \n dont éco - part . 0,50 € ) \n LIVRE CHEZ VOUS \n SIMPLICITÉ & SOLIDITÉ \n Les piscines tubulaires sont en kit . \n Faciles à monter et à démonter , elles sont à la fois solides et économiques . Rondes , ovales ou rectangulaires ... nous vous proposons les formes adaptées à l'espace dont vous disposez ! \n équipement * : \n PERSONNES \n * selon modèle \n TUBULAIRES \n 2 *** \n 45/60 \n MIN . \n 759 € \n dont éco - part . 0,50 € \n Jambes renforcées \n Ø 6,10 x H 1,32 m \n 0 6,10 m \n 32,7 m³ \n 4,4 m³ / h \n 0 6,10 x H 1,17 m \n Liner PVC \n inclus : bâche de protection , tapis de sol , échelle de sécurité SOL PLAT \n ET NETTOYÉ \n LIVRE CHEZ VOUS \n Echelle fournie \n Système filtration \n FLASHEZ - MOI Pour visionner le film du montage des bassins tubulaires Prism INTEX \n

Output:
{
    "product_brand": "INTEX",
    "product_description": "Garantie légale 2 ans (¹), Hydroaération : permet de contrôler le bon fonctionnement de la filtration, Les piscines tubulaires sont en kit. Faciles à monter et à démonter, elles sont à la fois solides et économiques. Rondes, ovales ou rectangulaires... nous vous proposons les formes adaptées à l'espace dont vous disposez! Jambes renforcées, Liner PVC, inclus : bâche de protection, tapis de sol, échelle de sécurité SOL PLAT ET NETTOYÉ, Echelle fournie, Système filtration",
    "product_name": "PISCINE TUBULAIRE PRISM FRAME",
    "product_sku": "Null",
    "product_Product_category": "Piscines",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,25€(2), Dimensions surface de nage: Ø 3,66 x H 0,84 m, Filtre à cartouche: 1,7 m3/h, Capacité du bassin: 8,6 m3, Espace nécessaire: Ø 3,66 m, Dimensions: Ø 3,66 m x H 99 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 259.00,
        "deal_minPrice": 259.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,30€(2), Dimensions surface de nage: Ø 3,66 x H 1,07 m, Filtre à cartouche: 2,7 m3/h, Capacité du bassin: 10,6 m3, Espace nécessaire: Ø 3,66 m, Dimensions: Ø 3,66 x H 1,22 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 299.00,
        "deal_minPrice": 299.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,25€(2), Dimensions surface de nage: Ø 4,57 x H 0,91 m, Filtre à cartouche: 2,7 m3/h, Capacité du bassin: 14,6 m3, Espace nécessaire: Ø 4,57 m, Dimensions: Ø 4,57 x H 1,07 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 349.00,
        "deal_minPrice": 349.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,50€(2), Dimensions surface de nage: Ø 5,49 x H 1,07 m, Filtre à cartouche: 4,4 m3/h, Capacité du bassin: 24,3 m3, Espace nécessaire: Ø 5,49 m, Dimensions: Ø 5,49 x H 1,22 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 649.00,
        "deal_minPrice": 649.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_5": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "dont éco-part. 0,50€(2), Dimensions surface de nage: Ø 6,10 x H 1,17 m, Filtre à cartouche: 4,4 m3/h, Capacité du bassin: 32,7 m3, Espace nécessaire: Ø 6,10 m, Dimensions: Ø 6,10 x H 1,32 m",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 759.00,
        "deal_minPrice": 759.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
À partir de \n 3999 \n 199 \n À SAISIR \n QUANTITÉ LIMITÉE \n La valise cabine * 46 cm \n Valise Jean Louis \n SHERRER \n En ABS , 4 roues multidirectionnelles , \n \" \n Canne télescopique intégrée , \n Cadenas à code intégré . \n Disponible en différents coloris \n 2 \n QAS \n Tailles \n 46 cm \n 60 cm \n 70 cm \n Prix \n 3.9,99 € 19,99 € \n 59,99 € 29,99 € \n 69,99 € 39,99 € \n

Output:
{
    "product_brand": "Jean Louis SHERRER",
    "product_description": "En ABS, 4 roues multidirectionnelles, Canne télescopique intégrée, Cadenas à code intégré. Disponible en différents coloris, QUANTITÉ LIMITÉE",
    "product_name": "Valise",
    "product_sku": "Null",
    "product_Product_category": "Bagages",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Taille: 46 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 19.99,
        "deal_minPrice": 19.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.99,
        "deal_minPrice": 39.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Taille: 60 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.99,
        "deal_minPrice": 59.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_5": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Taille: 70 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.99,
        "deal_minPrice": 39.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_6": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 69.99,
        "deal_minPrice": 69.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SREGULAR_PRICE"
      }
    ]
}

    """

)


other_types = """
Your Role:
You will be provided with text relating to an offer from a promotional brochure.

Output Format:
Your answer should be strictly in JSON format, with no additional annotations. Adhere to the following structure:
{
    "main_format":{
        "product_brand": "",
        "product_description": "",
        "product_name": "",
        "product_sku": "",
        "product_Product_category": "",
        "deal_1": [
            {
            "deal_conditions": "",
            "deal_currency": "",
            "deal_description": "",
            "deal_frequency": "",
            "deal_maxPrice": "",
            "deal_minPrice": "",
            "deal_pricebybaseunit": "",
            "deal_loyaltycard": "",
            "deal_type": ""
            }
        ]

    },

    "additional_format": {
        "products": [
            {
              "product_id": "1",
              "brand": "",
              "name": "",
              "details": {
                "unit_size": "",
                "bundle_size": "",
                "deposit": "",
                "origin_country": "",
                "product_description": ""
              },
              "is_product_family": ""
            }
          ],
          "deals": [
                {
                  "deal_id": "1",
                  "type": "",
                  "pricing": "",
                  "price_type": "",
                  "requirements": {
                    "terms_and_conditions": "",
                    "loyalty_card": "",
                    "validity_period": ""
                  },
                  "details": {
                    "price_by_base_unit": "",
                    "discount": "",
                    "deal_description": ""
                  },
                  "applied_to": "product-id",
                  "is_deal_family": ""
                }
          ]
    }
}
### Instructions for "main_format".
"product_name" must always have a value.
Avoid including "product_name" words in "product_description."
"product_description" should not contain details that relate to "product_name" or "deal_pricebybaseunit."
Record "deal_pricebybaseunit" only from text segments that follow the format <base-unit> = <price> (e.g., "1 l = € 1.50").
Always include product quantity (ml, l, g, kg) in "product_description."
Do not record discounts (e.g., -13%, -5€) unless "deal_type" is "OTHER."
Correct any French grammar errors, even if they appear in the source text.
Assign any unallocated text to "product_description."
If there’s no category data, use "Null" for "product_product_category."
"product_product_category" should follow Google product category guidelines and be in French.
"deal_loyaltycard" should be "Null" or "Yes."
Age ratings (including toys) should be placed in "product_description", EXAMPLE ("à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois")
The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
Record only the prices explicitly stated in the text. Do not generate or estimate any prices not present in the source material.
min and max price always should be identical
each deal_id should be always record in separate deal in main_forman (for example:"deal_1",deal_2" and so on)
Each deal should always display all prices available on the text.
If multiple prices or sizes appear in the text, each should have a separate "deal" entry within a single JSON response.
Set "deal_loyaltycard" to "Yes" if loyalty terms like "compte," "cagnoté," "prix déduit" appear.
Ensure each parameter value is unique to its assigned field.
Follow the structure and details in the examples without deviation.
"deal_type" should only be "REGULAR_PRICE","SALES_PRICE" or "OTHER."
"deal_type" "OTHER" must not contain "deal_maxPrice" or "deal_minPrice."
For prices referring to the same product (different sizes, adult/junior), combine them within one JSON. Do not split into separate JSONs.
check if all the available prices from the page have been fixed accurately.


# instructions for offer with several products and with loyalty card **:
price with a card is always written to the SALES_PRICE type price without a card is always in REGULAR 
write in the condition "Prix Carte" if there is a loyalty card, and "Sans carte" if there is not, BUT only if there was at least one card in the total offerer.
always write down each deal in a separate deal IMPORTANT
always check whether you have used all possible prices on the page and recorded them in a separate deal IMPORTANT
deal_conditions and deal_description must be filled in only TTC price
# instructions for loyalty program: with a discount from the store **: 
1. **Prices without Tax (HT)**:
   - Prices without tax (HT) should **never** be included in any deal or separate entry.
   - If the HT price is crossed out, **it must be completely ignored** and should **not** be recorded anywhere in the data, including in the `deal_conditions`, `product_description`, or any other fields.
   - **Do not create a separate deal for the HT price**, even if it is crossed out.

2. **Prices with Tax (TTC)**:
   - Prices with tax (TTC) should always be recorded in the deal as the **main price** under the `SALES_PRICE` deal type.
   - The price with tax (TTC) must be displayed in the `deal_description` field as the main price.

-always check whether the price without TTC tax is correct
-always check that the price without tax is indicated in the product_description(for example: "Inner and outer polypropylene. metal fittings. 8 cm diameter.   ("price excluding tax" 1.59€HT), (“crossed out price” 43.29€HT)") and always indicate the price with HT in brackets
-Never record two different prices in one deal 
-If you have a price with TTC tax, you should only write it to REGULAR_PRICE and ignore all references to the HT price.
- **Deal numbering**: Each deal should be numbered in the format `deal_1`, `deal_2`, etc., when applicable.
- **Price with tax (TTC)**: If the price includes tax (TTC), it should always be recorded as a `REGULAR_PRICE` deal.
- **Household price without tax (HT)**: 
  - If the price without tax is crossed out, it must be completely ignored and not recorded.
  - Always indicate the price, the crossed-out price excluding tax and the price excluding tax in the product description (for example: "Inner and outer polypropylene. metal fittings. 8 cm diameter.   ("price excluding tax" 1.59€HT), (“crossed out price” 43.29€HT)") and always indicate the price with HT in brackets 
   IMPORTANT ALWAYS The price without tax (HT) must be written in the product_description at the end of the description add (example: "Ouverture frontale. Structure rigide. Compartiment renforcé. ("old crossed out price without tax"99€HT), (price without tax88€HT) Taille IATA. 452356 ")
- **Product Description**:
  - Never repeat the product name in the `product_description`.
- **Deal Conditions**: 
  - Complete offers should be recorded in `deal_description`.
  - If there’s an age rating (e.g., "à partir de 3 ans"), it should be placed in `product_description`.s
the discounted price from the store will be SALES_PRICE and the old price will be REGULAR_PRICE
the deal_description and deal_conditions fields in the deal must always be filled in
""" 




other_types_client_ocr = (

    """
Input:
manche en acier réglable de 109 à 140 cm
balai avec franges et tête articulée 360°,
contient : manche + seau 6 L + panier d’essorage,
LEIFHEIT
Set Clean Twist Mop Ergo
en5€
34,90
29,90*
déduit
!urocora
prix

Output:
{
    "product_brand": "LEIFHEIT",
    "product_description": "contient : manche + seau 6 L + panier d’essorage, balai avec franges et tête articulée 360°, manche en acier réglable de 109 à 140 cm",
    "product_name": "Set Clean Twist Mop Ergo",
    "product_sku": "Null",
    "product_Product_category": "Produits de nettoyage",
    "deal_1": [
      {
        "deal_conditions": "Prix €urocora déduit",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.90,
        "deal_minPrice": 29.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "L'unité",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 34.90,
        "deal_minPrice": 34.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
2,4L
Garantie légale 2 ans
• Parois transparentes #d
• Utilisable avec de l'huile/beurre
• Cuisson à l'air chaud
mélanger
• Panier anti-adhésif avec cuillère à
Réf. : ARI-2953-XL
iMachine à pop corn XL
D’ÉCONOMIES(2)
30€
REMISE FIDÉLITÉ DÉDUITE
99
29€
Soit
d'éco-participation
dont 0,30 €
99
59€
99x
99€
Prix payé en caisse

Output:
{
    "product_brand": "Null",
    "product_description": "2,4L, Garantie légale 2 ans, Parois transparentes #d, Utilisable avec de l'huile/beurre, Cuisson à l'air chaud, Panier anti-adhésif avec cuillère à mélanger, dont 0,30 € d'éco-participation",
    "product_name": "Machine à pop corn XL",
    "product_sku": "ARI-2953-XL",
    "product_Product_category": "Appareils de cuisine",
    "deal_1": [
      {
        "deal_conditions": "Prix payé en caisse",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.99,
        "deal_minPrice": 59.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "REMISE FIDÉLITÉ DÉDUITE",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.99,
        "deal_minPrice": 99.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
DÈS 500 € D’ACHATS
-5%(a)
DÈS 1000 € D’ACHATS
OU COMPOSITE
DALLES EN BOIS
DE TERRASSE ET
SUR LES LAMES
-10%(a)
CARTE
EXCLU

Output:
{
    "product_brand": "Null",
    "product_description": "EXCLU CARTE",
    "product_name": "-10% SUR LES LAMES DE TERRASSE ET DALLES EN BOIS OU COMPOSITE DÈS 1000 € D’ACHATS",
    "product_sku": "Null",
    "product_Product_category": "Matériaux de construction",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "Null",
        "deal_description": "-10% DÈS 1000 € D’ACHATS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "Null",
        "deal_description": "-5% DÈS 500 € D’ACHATS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ]
},

Input:
Lavabo XL
intégré
Porte-savon
Douche
Bain-douche
Économie d’eau : débit réduit de 6 L/min
Mitigeur lavabo
90
89€
industriel
Design
Réf. 5059340583136.
Mitigeur thermostatique bain-douche 119 €
Réf. 5059340582757.
Mitigeur thermostatique douche 109 €
Mitigeur lavabo XL 129 € Réf. 5059340582658.
Mitigeur lavabo 89,90 € Réf. 5059340582573.
En laiton et zinc. Noir.
Série mitigeurs Selenga

Output:
{
    "product_brand": "Null",
    "product_description": "Lavabo XL, Porte-savon intégré, Douche, Bain-douche, Économie d’eau : débit réduit de 6 L/min, Design industriel, En laiton et zinc. Noir.",
    "product_name": "Série mitigeurs Selenga",
    "product_sku": "5059340582573, 5059340582658, 5059340582757, 5059340583136",
    "product_Product_category": "Plomberie",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur lavabo",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 89.90,
        "deal_minPrice": 89.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur lavabo XL",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 129.00,
        "deal_minPrice": 129.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur thermostatique douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 109.00,
        "deal_minPrice": 109.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur thermostatique bain-douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 119.00,
        "deal_minPrice": 119.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
120 x 170 cm
Rectangle
Rond Ø 80 cm
le tapis
90
39€
À partir de
jute et coton
Tressage
jute naturel(1) :
Existe en version
Grand 59,90 € l. 120 x L. 170 cm. Réf. 5059340473956.
Moyen 39,90 € l. 80 x L. 150 cm. Réf. 5059340474151.
En jute et coton. Coloris noir.
Tapis

Output:
{
    "product_brand": "Null",
    "product_description": "Tressage jute et coton, Existe en version jute naturel(1). Moyen l. 80 x L. 150 cm. En jute et coton. Coloris noir. Rond Ø 80 cm",
    "product_name": "Tapis",
    "product_sku": "5059340473956, 5059340474151",
    "product_Product_category": "Tapis",
    "deal_1": [
      {
        "deal_conditions": "À partir de le tapis",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.90,
        "deal_minPrice": 39.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Grand l. 120 x L. 170 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.90,
        "deal_minPrice": 59.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
Douche
ANS
5
Bain-douche
84,90 €
Sans carte :
Mitigeur lavabo
90
69€
carte
Prix
Bain-douche 99 € Réf. 4059625168882. Prix sans la carte : 119 €
Douche 89,90 € Réf. 4011097753508. Prix sans la carte : 109 €
Réf. 4059625168813. Prix sans la carte : 84,90 €
Lavabo M 69,90 € À installer sur vasque avec cuve profonde.
En laiton chromé.
Série mitigeurs Mysport

Output:
{
    "product_brand": "Null",
    "product_description": "Mitigeur lavabo. À installer sur vasque avec cuve profonde. En laiton chromé.",
    "product_name": "Série mitigeurs Mysport",
    "product_sku": "4059625168813, 4011097753508, 4059625168882",
    "product_Product_category": "Plomberie",
    "deal_1": [
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 69.90,
        "deal_minPrice": 69.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Sans carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 84.90,
        "deal_minPrice": 84.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 89.90,
        "deal_minPrice": 89.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Sans carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 109.00,
        "deal_minPrice": 109.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_5": [ 
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Bain-douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.00,
        "deal_minPrice": 99.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_6": [ 
      {
        "deal_conditions": "Sans carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 119.00,
        "deal_minPrice": 119.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
ZOOM BRODERIE
d'OEKO-TEX®
Label STANDARD 100
Divers coloris selon les magasins
Du 38 au 54
100% coton
INEXTENSO
BERMUDA HOMME
99
9€
d'OEKO-TEX®
Label STANDARD 100
Du S au XXL
100% coton
INEXTENSO
TEE-SHIRT HOMME
99
5€

Output:
[
  {
      "product_brand": "INEXTENSO",
      "product_description": "ZOOM BRODERIE, Label STANDARD 100 d'OEKO-TEX®, Divers coloris selon les magasins, 100% coton, Du 38 au 54",
      "product_name": "BERMUDA HOMME",
      "product_sku": "Null",
      "product_Product_category": "Vêtements pour hommes",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 9.99,
          "deal_minPrice": 9.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "INEXTENSO",
      "product_description": "Label STANDARD 100 d'OEKO-TEX®, 100% coton, Du S au XXL",
      "product_name": "TEE-SHIRT HOMME",
      "product_sku": "Null",
      "product_Product_category": "Vêtements pour hommes",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 5.99,
          "deal_minPrice": 5.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  }
],

Input:
JUNIOR
T-SHIRT ANTI-UV
-43%
29,99€
16,99€
du 2 au 7 ans. Taille junior : du 8 au 16 ans.
Taille bébé : du 6 au 18 mois. Taille cadet :
86% polyester recyclé','14% élasthanne.
Indice de protection solaire UPF 50.
CADET/BÉBÉ
T-SHIRT ANTI-UV
-32%
24,99€
16,99€
texturisée
antidérapante
supérieure
Semelle

Output:
{
    "product_brand": "Null",
    "product_description": "Indice de protection solaire UPF 50.\n86% polyester recyclé, 14% élasthanne.\nTaille bébé : du 6 au 18 mois. \nTaille cadet : du 2 au 7 ans. \nTaille junior : du 8 au 16 ans.",
    "product_name": "T-SHIRT ANTI-UV",
    "product_sku": "Null",
    "product_Product_category": "Vêtements pour enfants",
    "deal_1": [
      {
        "deal_conditions": "CADET/BÉBÉ",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "CADET/BÉBÉ",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 24.99,
        "deal_minPrice": 24.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "JUNIOR",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "JUNIOR",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

    """

)

other_types_our_ocr = (

    """
Input:
prix Eurocora déduit \n 5 € \n 34 € 90 \n en \n Euro cora \n 29 € 90 * \n Set Clean Twist Mop Ergo LEIFHEIT \n contient : manche + seau 6 L + panier d'essorage , balai avec franges et tête articulée 360 ° , manche en acier réglable de 109 à 140 cm \n

Output:
{
    "product_brand": "LEIFHEIT",
    "product_description": "contient : manche + seau 6 L + panier d’essorage, balai avec franges et tête articulée 360°, manche en acier réglable de 109 à 140 cm",
    "product_name": "Set Clean Twist Mop Ergo",
    "product_sku": "Null",
    "product_Product_category": "Produits de nettoyage",
    "deal_1": [
      {
        "deal_conditions": "Prix €urocora déduit",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.90,
        "deal_minPrice": 29.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "L'unité",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 34.90,
        "deal_minPrice": 34.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
Capacité \n 2,4L \n Prix payé en caisse \n 9999 5999 \n € \n dont 0,30 € d'éco - participation \n 30 \n D'ÉCONOMIES ( 2 ) \n Soit \n 2999 \n REMISE FIDÉLITÉ DÉDUITE \n Popcern \n i Machine à pop corn XL \n Réf . : ARI - 2953 - XL \n • Panier anti - adhésif avec cuillère à mélanger \n • Cuisson à l'air chaud \n • Utilisable avec de l'huile / beurre \n • Parois transparentes Garantie légale 2 ans -Ariete \n

Output:
{
    "product_brand": "Ariete",
    "product_description": "Machine à pop corn XL, Panier anti-adhésif avec cuillère à mélanger, Cuisson à l'air chaud, Utilisable avec de l'huile/beurre, Parois transparentes, Garantie légale 2 ans, dont 0,30 € d'éco-participation",
    "product_name": "Machine à pop corn XL",
    "product_sku": "ARI-2953-XL",
    "product_Product_category": "Appareils de cuisine",
    "deal_1": [
      {
        "deal_conditions": "Prix payé en caisse",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.99,
        "deal_minPrice": 59.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "REMISE FIDÉLITÉ DÉDUITE",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.99,
        "deal_minPrice": 99.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
EXCLU castorama CARTE \n la \n -10 % \n SUR LES LAMES DE TERRASSE ET DALLES EN BOIS OU COMPOSITE DÈS 1000 € D'ACHATS \n -5 % \n DÈS 500 € D'ACHATS \n

Output:
{
    "product_brand": "Null",
    "product_description": "EXCLU castorama CARTE",
    "product_name": "-10% SUR LES LAMES DE TERRASSE ET DALLES EN BOIS OU COMPOSITE DÈS 1000 € D’ACHATS",
    "product_sku": "Null",
    "product_Product_category": "Matériaux de construction",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "Null",
        "deal_description": "-10% DÈS 1000 € D’ACHATS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "Null",
        "deal_description": "-5% DÈS 500 € D’ACHATS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ]
},

Input:
SUR \n LE \n L'UNITÉ : \n 15€90 \n SUR LE \n E O \n 3⁰ \n Queues de Homard Crues surgelées CASINO \n 2 x 100 g ( 200 g ) \n Autres variétés ou poids disponibles à des prix différents Le kg : 79 € 50 \n + \n Casino \n AVANTAGE carte \n -20 % -30 % -40 % \n CAGNOTTÉS + \n CAGNOTTÉS \n E O \n CAGNOTTÉS \n 45 \n FLOBN \n SUR LE \n QUEUES \n de Homard \n Atlantique Nord Quest SURGELÉES \n 200 g \n

Output:
{
    "product_brand": "CASINO",
    "product_description": "Queues de Homard Crues surgelées, 2 x 100 g (200 g), Autres variétés ou poids disponibles à des prix différents",
    "product_name": "Queues de Homard Crues surgelées",
    "product_sku": "Null",
    "product_Product_category": "Fruits de mer",
    "deal_1": [
      {
        "deal_conditions": "L'UNITÉ",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 15.90,
        "deal_minPrice": 15.90,
        "deal_pricebybaseunit": "Le kg : 79€50",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "-20% CAGNOTTÉS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "-30% CAGNOTTÉS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "-40% CAGNOTTÉS",
        "deal_frequency": "ONCE",
        "deal_maxPrice": "Null",
        "deal_minPrice": "Null",
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "OTHER"
      }
    ]
},

Input:
BON BON \n 8990 \n Mitigeur lavabo \n + Design industriel \n Mitigeur thermostatique bain - douche 119 € \n Réf . 5059340583136 . \n Série mitigeurs Selenga \n En laiton et zinc . Noir . \n Mitigeur lavabo 89,90 € Réf . 5059340582573 . \n Mitigeur lavabo XL 129 € Réf . 5059340582658 . \n Mitigeur thermostatique douche 109 € \n Réf . 5059340582757 . \n Économie d'eau : débit réduit de 6 L / min \n OF \n Lavabo XL \n Douche \n + \n Porte - savon intégré \n Bain - douche \n 大 \n

Output:
{
    "product_brand": "BON BON",
    "product_description": "Lavabo XL, Porte-savon intégré, Douche, Bain-douche, Économie d’eau : débit réduit de 6 L/min, Design industriel, En laiton et zinc. Noir.",
    "product_name": "Série mitigeurs Selenga",
    "product_sku": "5059340582573, 5059340582658, 5059340582757, 5059340583136",
    "product_Product_category": "Plomberie",
    "deal_1": [
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur lavabo",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 89.90,
        "deal_minPrice": 89.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur lavabo XL",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 129.00,
        "deal_minPrice": 129.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur thermostatique douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 109.00,
        "deal_minPrice": 109.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Mitigeur thermostatique bain-douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 119.00,
        "deal_minPrice": 119.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
À partir de \n € \n 3990 \n le tapis \n Moyen 39,90 € 1.80 x L. 150 cm . Réf . 5059340474151 . Grand 59,90 € I. 120 x L. 170 cm . Réf . 5059340473956 . \n Tapis \n En jute et coton . Coloris noir . \n Tressage jute et coton \n Existe en jute 120 x Rond Ø

Output:
{
    "product_brand": "Null",
    "product_description": "Tressage jute et coton, Existe en jute. Moyen l. 80 x L. 150 cm. En jute et coton. Coloris noir. Rond Ø",
    "product_name": "Tapis",
    "product_sku": "5059340473956, 5059340474151",
    "product_Product_category": "Tapis",
    "deal_1": [
      {
        "deal_conditions": "À partir de le tapis",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 39.90,
        "deal_minPrice": 39.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Null",
        "deal_currency": "EUR",
        "deal_description": "Grand l. 120 x L. 170 cm",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 59.90,
        "deal_minPrice": 59.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ]
},

Input:
Prix carte \n castorama \n 69 % \n Mitigeur lavabo Sans carte : \n 84,90 € \n hansgrohe \n GARANTIE \n LO \n 5 \n ANS \n Bain - douche \n Série mitigeurs Mysport \n En laiton chromé . \n Lavabo M 69,90 € À installer sur vasque avec cuve profonde . Réf . 4059625168813. Prix sans la carte : 84,90 € \n Douche \n Douche 89,90 € Réf . 4011097753508. Prix sans la carte : 109 € Bain - douche 99 € Réf . 4059625168882. Prix sans la carte : 119 € \n

Output:
{
    "product_brand": "Null",
    "product_description": "Mitigeur lavabo. À installer sur vasque avec cuve profonde. En laiton chromé.hansgrohe, GARANTIE 5 ANS",
    "product_name": "Série mitigeurs Mysport",
    "product_sku": "4059625168813, 4011097753508, 4059625168882",
    "product_Product_category": "Plomberie",
    "deal_1": [
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 69.90,
        "deal_minPrice": 69.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "Sans carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 84.90,
        "deal_minPrice": 84.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [ 
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 89.90,
        "deal_minPrice": 89.90,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "Sans carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 109.00,
        "deal_minPrice": 109.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_5": [ 
      {
        "deal_conditions": "Prix carte",
        "deal_currency": "EUR",
        "deal_description": "Bain-douche",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 99.00,
        "deal_minPrice": 99.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Yes",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_6": [ 
      {
        "deal_conditions": "Sans carte",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 119.00,
        "deal_minPrice": 119.00,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

Input:
ZOOM BRODERIE \n OEKO - TEX® CONFIDENCE IN TEXTILES ge STANDARD 100 CQ 1203/6 IFTH \n Tasted for harmful substances www.oko-tx.com/and \n € \n 5 , ⁹⁹9 \n 99 \n OEKO - TEX® \n CONFIDENCE IN TEXTILES \n STANDARD 100 CQ 1203/6 IFTH Tested for harmful substances www.eko-tex.com/standard 00 \n € \n 99⁹⁹9 \n EXISTE \n JUSQU'AU \n 54 \n Inextenso \n TEE - SHIRT HOMME INEXTENSO 100 % coton \n Du S au XXL Label STANDARD 100 d'OEKO - TEX® \n **** \n BERMUDA HOMME \n INEXTENSO \n 100 % coton \n Du 38 au 54 \n Divers coloris selon les magasins Label STANDARD 100 d'OEKO - TEX® \n

Output:
[
  {
      "product_brand": "INEXTENSO",
      "product_description": "ZOOM BRODERIE, Label STANDARD 100 d'OEKO-TEX®, Divers coloris selon les magasins, 100% coton, Du 38 au 54, CONFIDENCE IN TEXTILES IN TEXTILES ge STANDARD 100 CQ 1203/6 IFTH, Tasted for harmful substances www.oko-tx.com",
      "product_name": "BERMUDA HOMME",
      "product_sku": "Null",
      "product_Product_category": "Vêtements pour hommes",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 9.99,
          "deal_minPrice": 9.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  },
  {
      "product_brand": "INEXTENSO",
      "product_description": "Label STANDARD 100 d'OEKO-TEX®, 100% coton, Du S au XXL, CONFIDENCE IN TEXTILES IN TEXTILES ge STANDARD 100 CQ 1203/6 IFTH, Tasted for harmful substances www.oko-tx.com",
      "product_name": "TEE-SHIRT HOMME",
      "product_sku": "Null",
      "product_Product_category": "Vêtements pour hommes",
      "deal_1": [
        {
          "deal_conditions": "Null",
          "deal_currency": "EUR",
          "deal_description": "Null",
          "deal_frequency": "ONCE",
          "deal_maxPrice": 5.99,
          "deal_minPrice": 5.99,
          "deal_pricebybaseunit": "",
          "deal_loyaltycard": "Null",
          "deal_type": "SALES_PRICE"
        }
      ]
  }
],

Input:
Semelle + \n BORN \n 16.99 € 16.990 \n , 99 € \n 29,99 € -43 % \n T - SHIRT ANTI - UV JUNIOR \n 24,99 € -32 % \n T - SHIRT ANTI - UV CADET / BÉBÉ \n Indice de protection solaire UPF 50 . 86 % polyester recyclé , 14 % élasthanne . Taille bébé : du 6 au 18 mois . Taille cadet : du 2 au 7 ans . Taille junior : du 8 au 16 ans . \n

Output:
{
    "product_brand": "Null",
    "product_description": "Indice de protection solaire UPF 50.\n86% polyester recyclé, 14% élasthanne.\nTaille bébé : du 6 au 18 mois. \nTaille cadet : du 2 au 7 ans. \nTaille junior : du 8 au 16 ans.",
    "product_name": "T-SHIRT ANTI-UV",
    "product_sku": "Null",
    "product_Product_category": "Vêtements pour enfants",
    "deal_1": [
      {
        "deal_conditions": "CADET/BÉBÉ",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_2": [ 
      {
        "deal_conditions": "CADET/BÉBÉ",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 24.99,
        "deal_minPrice": 24.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ],
    "deal_3": [
      {
        "deal_conditions": "JUNIOR",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 16.99,
        "deal_minPrice": 16.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "SALES_PRICE"
      }
    ],
    "deal_4": [ 
      {
        "deal_conditions": "JUNIOR",
        "deal_currency": "EUR",
        "deal_description": "Null",
        "deal_frequency": "ONCE",
        "deal_maxPrice": 29.99,
        "deal_minPrice": 29.99,
        "deal_pricebybaseunit": "",
        "deal_loyaltycard": "Null",
        "deal_type": "REGULAR_PRICE"
      }
    ]
},

    """

)


def get_prompt_for_golden_example(gold_type):
    match gold_type:
        case "simple-offers":
            return simple_offers, 'simple_offers'
        case "2-products-in-one-offer":
            return two_products_in_one_offer, 'two_products_in_one_offer'
        case "an-offer-with-a-coupon":
            return one_product_with_coupon, 'one_product_with_coupon'
        case "2-products-in-one-offer-+-coupon":
            return two_products_with_coupon, 'two_products_with_coupon'
        case "several-products-in-one-offer-with-different-prices":
            return several_products_with_different_prices, 'several_products_with_different_prices'
        case "offers-with-price-characterization-(uvp)":
            return price_characterization_uvp, 'price_characterization_uvp'
        case "offers-with-price-characteristic-(statt)":
            return price_characterization_statt, 'price_characterization_statt'
        case "offers-with-dealtype-special_price":
            return special_prise, 'special_prise'
        case "offers-with-the-old-price-crossed-out":
            return old_price_crossed_out, 'old_price_crossed_out'
        case "offers-with-product-number-(sku)":
            return product_number_sku, 'product_number_sku'
        case "offers-with-the-condition_-available-from-such-and-such-a-number":
            return date_availability, 'date_availability'
        case "offers-with-the-condition:-available-from-such-and-such-a-number":
            return date_availability, 'date_availability'
        case "offers-with-money_rebate":
            return money_rebate, 'money_rebate'
        case "offers-with-percentage_rebate":
            return percentage_rebate, 'percentage_rebate'
        case "offers-with-reward":
            return reward, 'reward'
        case "offers-with-an-additional-shipping":
            return additional_shipping, 'additional_shipping'
        case "offers-with-an-additional-deposit-price":
            return deposit_price, 'deposit_price'
        case "scene-with-multiple-offers-+-uvp-price-for-each-offers":
            return multiple_offers_with_uvp, 'multiple_offers_with_uvp'
        case "offers-with-different-sizes":
            return different_sizes, 'different_sizes'
        case "regular":
            return regular, 'regular'
        case "with-the-price-of-the-supplemental-bid":
            return supplemental_bid, 'supplemental_bid'
        case "with-a-product-without-a-price":
            return without_price, 'without_price'
        case "availability-of-additional-products":
            return additional_products, 'additional_products'
        case "stock-offers":
            return stock_offers, 'stock_offers'
        case "travel-booklets":
            return travel_booklets, 'travel_booklets'
        case "stocks":
            return stocks, 'stocks'

    return False
