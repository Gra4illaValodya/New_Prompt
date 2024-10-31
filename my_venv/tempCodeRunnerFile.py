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
The description of the product discount (for example: "-47%", "-5€".) should be ignored and not written to any of the "main_format" parameters.
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

# Instructions for Additional offer:
All information about Additional offer (for example: "SPALDING NBA Basketball Modell „PLATINUM PRECISION" für 39.99") then this information including the price of the Additional offer should be written in the "deal_description" of the "deal" where the "deal_type": "OTHER" and "price_type": "OTHER" is present.
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
