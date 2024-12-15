prompt_models = {
    'simple_offers': 'gpt',
    'two_products_in_one_offer': 'gpt',
    'default': 'claude'
}




other_types = """
Your Role:
You will be provided with text relating to an offer from a promotional brochure.

Output Format:
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



### Instructions for "main_format".
- if the offer has a price with a tax (“HT“, ‘TTC’) then you must write the general description in ‘main_format’ in ‘product_description’ in the format (full description <1.25 € HT>, <1.99 € HT>, <2.39 € HT>, <20.90 € HT>, <1.25 € HT>”)
- in the “main_format” in “deal” in “deal_description” it turns out to write all the information that is needed for the description then “main_format” “product_description” can be written as Null
- If duplicates appear in both "deal_type":"REGULAR_PRICE" and "deal_type":"SALES_PRICE" for the same group, retain the "deal_description" in "REGULAR_PRICE" and replace it with Null in "SALES_PRICE".
- "product_name" must always have a value.
- IMPORTANT: Assign "deal_type":"SPECIAL_PRICE" only if the loyalty program explicitly indicates a discount from a specific store in deal_conditions (for example: "Lidl plus"). If the loyalty program mentions a loyalty card without specifying a store or discount, do not assign "deal_type":"SPECIAL_PRICE".
- IMPORTANT when there is a loyalty program with a clearly specified discount from the store, you need to write the store's discount in the “main_format” in the “deal” in the “deal_conditions” (for example: “Prix Lidl plus deduit”) and write in «deal_type":»SPECIAL_PRICE"
- Avoid applying SPECIAL_PRICE to general loyalty programs without reference to a store.
- Avoid including "product_name" words in "product_description."
- "product_description" should not contain details that relate to "product_name" or "deal_pricebybaseunit."
- if in «main_format» in «product_description» value("Mitigeur lavabo Ecos L, Mitigeur thermostatique douche Ecostat 1001, Mitigeur thermostatique bain-douche Ecostat 1001»), and in «main_format» in «deal_1» in «deal_description»:value ("Mitigeur lavabo Ecos L»),in «deal_2» in «deal_description»:value("Mitigeur thermostatique douche Ecostat 1001»), in «deal_3» in «deal_description»:value(" Mitigeur thermostatique bain-douche Ecostat 1001») then write Null in «product_description» 
- If the deal_pricebybaseunit field contains a value (for example, “1 kg = 8.58 €”), then this value should be removed from the deal_description.
- The deal_description field should not contain details that duplicate or relate to information from deal_pricebybaseunit.
- Record "deal_pricebybaseunit" only from text segments that follow the format <base-unit> = <price> (e.g., "1 l = € 1.50").
- Always include product quantity (ml, l, g, kg) in "product_description."
- Correct any French grammar errors, even if they appear in the source text.
- in product_description cannot contain information about price(for example:"Existe aussi en ton pierre à 59,95 €")
- if the product description clearly indicates an additional price (for example, “a ton of Pierre A”), then it should be written in the “main_format” in “deal” “deal_description” but it cannot be repeated in different deals, we replace it with Null in “main_format” in “deal” with "deal_type":"SALES_PRICE"
- If there’s no category data, use "Null" for "product_product_category."
- "product_product_category" should follow Google product category guidelines and be in French.
- "deal_loyaltycard" should be "True" or "False"
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- Record only the prices explicitly stated in the text. Do not generate or estimate any prices not present in the source material.
- min and max price always should be identical
- IMPORTANT ALWASY Each deal should be recorded in the format deal_1, deal_2, deal_3, and so on, even if they belong to the same product.
- Each deal must be recorded in a separate array under a unique key, for example, “deal_1”, “deal_2”, with one deal object in the array.
- Each deal should always display all prices available on the text.
- If multiple prices or sizes appear in the text, each should have a separate "deal" entry within a single JSON response.
- Set "deal_loyaltycard" to "True" if loyalty terms like "compte," "cagnoté," "prix déduit" appear.
- Ensure each parameter value is unique to its assigned field.
- Follow the structure and details in the examples without deviation.
- "deal_type" should only be "REGULAR_PRICE","SALES_PRICE", "SPECIAL_PRICE" or "OTHER"
- If the deal contains prices (maxPrice or minPrice), the deal type must be “SALES_PRICE” ,“REGULAR_PRICE” ,"SALES_PRICE", definitely not “OTHER”.
- Do not record discounts (e.g., -13%, -5€) unless "deal_type" is "OTHER."
- For prices referring to the same product (different sizes, adult/junior), combine them within one JSON. Do not split into separate JSONs.
- check if all the available prices from the page have been fixed accurately.
- if some field is empty you must record Null
- Always write "Null" with a capital letter
- ALWAYS check yourself, all possible prices should be written down in separate deal
- price cannot contain in deal_description 
- if in description contain text ("Uni 31,37 € le carton de 1,31 m²") you need record only ("le carton de 1,31 m²")
- if the price is indicated by mm, m2, m3, kg, L then it should be written in deal_pricebybaseunit (for example: “le m² = 29.95”) but if the price is not indicated by unit (for example “le carton de 1.31 m² = 31.37”) then you should write Null
- the price specified per unit of measurement must be recorded in deal_pricebybaseunit price per 
- cannot duplicate deal_pricebybaseunit (for exmaple:"1 kg = 8,58 €") and deal_description (for exmaple:"1 kg = 8,58 €") in such cases always write null in deal_description
- quantity of goods for different weights (for example, “le carton de 1.31 m²”) should be recorded in deal_description and the minPrice and maxPrice should be recorded based on (1.31 m² * per unit price) but the price can be calculated and it is important to write exactly what is written on the offer
- write only the data that is on the offer, do not make up your own 
- deal_frequency always "ONCE"
- IMPORTANT all deal must have unique numeric (for example:"deal_1","deal_2")
- cannot be repeated in "deals" "deal_pricebybaseunit" 
- exclude discount (for example:"20%*" ,"23%", "-20%" ,"40€","-10€") from "main_format" in "deals" in "deal_deascription"
- if the product description is repeated in the "main_format" in "deals" in "deal_description" with "deal_type":"SALES_PRICE" and "deal_type":"REGULAR_PRICE" then you need to write Null in "deal_type":"SALES_PRICE".
- if the product description is repeated in the "main_format" in "deals" in "deal_pricebybaseunit" with "deal_type":"SALES_PRICE" and "deal_type":"REGULAR_PRICE" then you need to write Null in "deal_type":"SALES_PRICE".
- if the deal has a clearly defined custom description, then it must be written in the “main_format” in “deals” in “deal_description” but only “deal_type: “SALES_PRICE” and exclude from ”deal_type: “REGULAR_PRICE”.
- if product_name and product_sku are the same, then you need to write null in product_sku
- IMPORTANT the art number (for example: "Art. 8207849", "Art. 8207594", "Ref. 3663602991601.", " Réf. 3188000776648."), should always be written in the "main_format" in "product_sku"
- IMPORTANT if the description says “Ref. 3188000776648” (e.g. ‘1 tête, L. 10 x P. 14 x H. 13 cm. Réf. 3188000776648’). If so, remove it from the description and add it to “main_format” in “product_sku”. 
- IMPORTANT If “main_format” in “deal” contains all the necessary information for the description in “deal_description”, then “main_format” in “product_description” should be set to Null.
- Ensure that all duplicates in 'deal_description' are removed. Keep only one instance of each description
- **THESE RULES ARE SUITABLE FOR BOTH ONE PRODUCT AND SEVERAL** 
(
  - IMPORTANT In the product_description, only add the price in the format <799.99€HT> if it is clearly marked as HT on the page. If there is no “HT” marking, the price must be ALWAYS is excluded <799.99€HT> in product_description.
  - in TTC, deal_conditions will always be Null
  - Check each field (“product_description”, “deal_conditions”, “deal_description”) for the words “Dont éco. contribution”,"éco-contribution", "TTC".
  - Remove all references to contributions from these fields.
  - if the offer contains a price without tax (“HT”), you should ignore it and not create a separate deal for it
  - create deal only TTC price and exclude all information about HT
  - Price TTC always SALES_PRICE 
  - if the text contains “Dont éco. contribution : 0,42 €HT, 0,50 €TTC”, it should be ignored in the product_descriptions
  - Always record in product_description prices  without tax (HT) in a format that includes cents.
  - IMPORTANT If the price is crossed out or not crossed out, enter it in triangular brackets in the following format: <whole.cents€HT>. Examples: <27.23€HT>, <43.46€HT>, <19.31€HT>.
      Be sure:
      Make sure that all prices without tax, even crossed out prices, are stored exclusively in the product_description field.
      Never record prices without tax (HT) in any other field.
      If there is only one price without tax, be sure to write only one price and do not invent others that do not exist
      whether the cents after the decimal point are correct, the product_description should be <4.23€HT> or <4.15€HT>. 
)

- IMPORTANT: make sure that the product_description contains all prices without HT tax, if there are such prices (“<1.59 €HT>”, “<43.29 €HT>”) immediately add them to the  "main_format" in "product_description" and only then generate JSON 
- IMPORTANT: always check whether you need to write information about “<1.59 €HT>”, “<43.29 €HT>” in the product_description sometimes you do not add a correctly crossed out HT price or add it where there are no HT prices at all
- if text has "Dont éco. contribution : 0,12€TTC" you want to be ignored and record Null



### Instructions for "additional_format".
- in "additional_format" must product_id must always match the deal quantity (for example: "deal_1","deal_2").
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value only "SALES" not "SALES_PRICE" and "REGULAR".
- check in "price_type" must be only value "SALES_PRICE" or "REGULAR_PRICE" not "REGULAR".
- "type" should always be "SALES".
- discount ("50€","-20€","-25%","34%") must be in "additional_format" in "discount" field.


### GENERAL INSTRUCTIONS**:
- if in "main_format" in  "deal_1" with "deal_type": "REGULAR_PRICE" has the value (for example:"L. 1,98 x H. 1,53 m. En acier galvanisé plastifié. Fil 0 4 mm.Maille 200 x 55 mm. Anthracite.") and in "deal_2" in "deal_type": "SALES_PRICE" has the same value ("L. 1,98 x H. 1,53 m. En acier galvanisé plastifié. Fil 0 4 mm.Maille 200 x 55 mm. Anthracite.") then you need to "deal_type": "SALES_PRICE" should be set to Null
- you need to scan the entire text and write out all possible prices that are written even in the smallest print in the descriptions of a separate agreement.
- if duplicates appear in the same REGULA_PRICE and SALES_PRICE group at the same time, then leave one duplicate in REGULAR_PRICE and replace the other in SALES_PRICE with Null
- If there is no clearly spelled out text, then do not come up with something of your own and replace it with Null
- if there is a scene with different products and prices, then you need to write all the names of the products in"main_format" in the "product_name" separated by a comma (for example: “MAILLOT DE BAIN” oder “CHAPEAU DE PAILLE”)
- if there is a scene with different products and prices, there are cases when the price per unit is specified in text (for example: "L`unite", "   la pièce"), then you need to write it in “main_format” in “deals”: “deal_description”  
- if the price contains the text “Prix avant remise”, then it must be written in the “main_format” in “deals”: “deal_conditions” with "deals": “REGULAR_PRICE”
- when there is a loyalty program: with a discount from the store, and there is a clearly written description, then you need to write a full description (for example:"Offre cumulable dans la limite d'un remboursement de 100 €, Voir conditions en magasin","Offre cumulable dans la limite d'un remboursement de 80 €, Voir conditions en magasin")  in the "deal_type":"SALES_PRICE"
- when there is a loyalty program: with a discount from the store, then you need to write in the "main_format" in the "deals" in the "deal_conditions" write full condition (for example:"Offre de remboursement 60€","Offre de remboursement 40€","Offre de remboursement 30€") only in the "deal_type":"SALES_PRICE"
- in the "main_format" in "deals" in "SALES_PRICE" and "REGULAR_PRICE" there must be a price if it is not there then do not create a deal. 
- Price with refund (for example:"Don't eco-participation 10.00€","Don't eco-participation 30.00€","Don't eco-participation 40.00€",) should be written in “main_format” in “deals” in "deal_type":"SPECIAL_PRICE".
- this condition applies if the offer contains two sale prices and one regular price
- if there is no discount with a loyalty card, then it will be REGULAR_PRICE  
- IMPORTANT if there is a loyalty card in the offer, then in the "main_format" in "deals" in "deal_conditions" you need to write ("Prix carte", "Sans carte","Prix sans la carte" and so on)
- if the sku number is clearly indicated on the offer, then write it in the "main_format" in "product_sku"
- if the offer clearly indicates the price without tax (HT), write it in the "main_format" in the "product_description"
- if there is a loyalty program: with a discount from the store, then there can only be "REGULAR_PRICE" , "SALES_PRICE" "SPECIAL_PRICE" without "OTHER"
- IMPORTANT sif the price is crossed out, it refers to the "main_format" in "deals" with the "deal_type": "REGULAR_PRICE".
- IMPORTANT if you found a condition ("remise immediate","REMISE IMMEDIATE","REMIS IMMEDIATE"), write it in the "main_format" in "deal" in "deal_conditions" and it refers to the "main_format" in "deals" of the "deal_type": "SALES_PRICE".
- if there is a loyalty program: with a discount from the store, the discounted price will  be "main_format" in "deals" of "deal_type":"SPECIAL_PRICE"
- IMPORTANT: if the offer has a condition (“de remise différée”, “DE REMISE DIFFÉRÉE”), write it in the “main_format” in “deal” in “deal_conditions” and it will always be “SPECIAL_PRICE”.
- the discounted price from the store (for example:"lidl plus") must be written in "main_format" in "deals" in "deal_type": "SPECIAL_PRICE"
- if the offer has several deals without a price, then the deal with a price will be "REGULAR_PRICE" and without a price will be "OTHER"
- In "OTHER" cannot be price
- if there is no explicit text (“Prix avant remise”,"prix avant remise), then in the “main_format” in “deals” where “deal_type”: “REGULAR_PRICE” in “deal_conditions” you need to write Nulls
- If in the "main_format" in "product_name" there is information about the size for each deal, then you need to exclude it from "product_name" and add it to "deal_description"
- IMPORTANT ALWAYS If the description (deal_description) is repeated in one group of deals, then this description is written to the deal from “main_format” in “deal” in “deal_description” with “deal_type” type: “REGULAR_PRICE”, and in the deal from "main_format" in "deal" in "deal_description" with the type "deal_type": “SALES_PRICE”, the deal_description field is filled with NULL.
- IMPORTANT always remove duplicate descriptions in "main_format" in "deal" in "deal_type":"SALES_PRICE"
- if the offer with two sale prices and one regular price has a size description ("T. XS à XL", "T. XS à XXL"), you need  always to write it in “main_format” in “deals” in “deal_description”.
- IMPORTANT if the offer with several products In the product_description, only add the price in the format <799.99€HT> if it is clearly marked as HT on the page. If there is no “HT” marking, the price must be ALWAYS is excluded <799.99€HT> in product_description.
- IMPORTANTif an offer with several transactions without a price, then we will always have 1 price recorded in REGULAR_PRICE and everything else must be recorded in OTHER and exclude the price  
- if there are several prices in the offer, then we write the lower price in the main_format in the deal in deal_type: SALES_PRICE and write the higher one in the main_format in the deal in deal_type:REGULAR_PRICE 
- enter “main_format” in “deal” in “deal_description” from “deal_type”: “REGULAR_PRICE” all the full information about the dimensions (for example, context: “1 т. D. 33 x W. 15 x H. 14 cm.”, ”2 tons. L. 40 x W. 20 x H. 16 cm.”, "160x180", "1200x2000", "16 x 23 x 4 cm", "H. 180 cm")



### CHECK YOURSELF 
- Check if all duplicates are excluded from the "main_format" in "deal" in "deal_description" when "deal_type":"SALES_PRICE".
- Check if the information in deal_description contains all necessary details; if so, write Null in product_description.
- make sure that the condition “Prix Lidl plus deduit” is always SPECIAL_PRICE
- make sure that the price without tax (“HT”) is always ignored everywhere except main_format in the product_description in the format (“<27.23€HT>”, “<43.46€HT>”, “<19.31€HT”)
- if text has ("Dont éco. contribution : 0,50€TTC","Dont éco. contribution : 0,42€HT, 0,50€TTC" and so on) you should to be ignored and record Null
- if the offer clearly indicates the price without tax HT 799.99 €HT, it must be written in the product_description in the format (Fabriquée avec des granulats issus de matières plastiques recyclées. <799.99 €HT>)
- It is IMPORTANT to check whether the contract has clearly stated dimensions (e.g: “L. 1.98 x H. 1.53 m. En acier galvanisé plastifié. Fil 0 4 mm.Maille 200 x 55 mm. Anthracite.”, ”Existe aussi en haut. 1,73 m ou haut. 1.93 m et en vert”, ‘2 têtes, L. 33 x P. 15 x H. 14 cm.’, ‘L. 33 x P. 15 x H. 14 cm.’) at the appropriate price, then this size with the accompanying text should be written main_format in the deal in the deal_description with ‘deal_type’: “REGULAR_PRICE” 
- ALWAYS check in the offer with several products and with a loyalty card that in the main_format in the deal there are no repetitions in the deal_description, if there are such repetitions, then in the "main_format" in the "deal" with "deal_type":"SALES_PRICE" you need to write Null and in the “main_format” in the "deal" with “deal_type”: “REGULAR_PRICE” you need to leave unchanged 
- check offer with several products and with a loyalty card should only type "REGULAR_PRICE" and "SALES_PRICE" without "SPECIAL_PRICE" and "OTHER"
- if we have the following condition (“-20% of the cagnotés sur le 2e (i)”, “-30% of the cagnotés sur le 3e (i)”, “-40% of the cagnotés sur le 4e (i)”) then it will always be of type “OTHER”
- check that the information in deal_pricebybaseunit remains only in deal_pricebybaseunit and is removed from all remaining ones
- Check if we have an offer with two sales prices and one regular price, then we will have the following types “REGULAR_PRICE” “SALES_PRICE” “SPECIAL_PRICE” without “OTHER”
- Check if it is always and everywhere ignored (“Dont éco-participation 10,00 €”, “Dont éco-participation 20,00 €”)
- check if the HT price is clearly indicated on the offer then it should be written in the product_description
- check that there is an equal number of "deals" in which the price with tax ("TTC") is recorded to the price without tax ("HT") recorded in the "main_format" in the "product_description"
- check if the sku number is explicitly indicated on the offer then it should be written in “main_format” in “product_sku”
Check that the description says “Ref. 3188000776648” (e.g. ‘1 tête, L. 10 x P. 14 x H. 13 cm. Réf. 3188000776648’). If so, remove it from the description and add it to “main_format” in “product_sku”.
- Check if the text contains “Dont éco. contribution : 0,50 €TTC”, ignore it and write Null.
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


one_price = """
#Your Role:
You will be provided with image relating to offer from the promotional brochure.

#Output Format:
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

### INSTRUCTION GENERAL:
- "product_name" always has a full value.
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- In the "product_name" parameter, the product name must be written in full.
- The input text should be written grammatically correct in French, even if there are errors in the input text.
- Pay particular attention to broken words and hyphens.
- It is forbidden to write "deal" without numbering, always follow the numbering, for example deal_1, deal_2, deal_3 and so on.
- If there is no data for the category, then indicate Null.
- For "product_product_category", define a product category like Google product category does.
- For "product_product_category", the result must be in French language.
- "is_product_family", "loyalty_card", "is_deal_family" can only be a value "True" or "False".
- In additional_format the  "type" can acquire only such values: SALES.
- IMPORTANT The value of one json parameter cannot be repeated in another json parameter.
-  **Filter for Discount Percentages**: Any values with a discount in percentage (e.g., "-20%", "50% de réduction") or a specific amount (e.g., "-5€") **must be ignored and excluded** from all JSON parameters, especially from "deal_conditions" and "deal_description".
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- Always write "Null" with a capital letter
- "deal_frequency" always has the value "ONCE".
- All offers where there is only one price will have deal_type: REGULAR_PRICE.
- Record the main brand name along with additional information (for example, “EARL LES LIETS a branges”) in one product_brand field.

### main_format:
- deal with minPrice and maxPrice should always be the same
- "product_description" cannot contain the words from "product_name", "product_brand" and "deal_pricebybaseunit".
- "product_name" cannot contain the words from "product_description" and "product_brand".
- "product_brand" cannot contain the words from "product_name" and "product_description".
- at the very end, when everything is generated, check yourself again and remove the product name from the description IMPORTANT
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- "product_sku" is the serial number of the product.
- "product_sku" cannot be duplicated in the "product_description".
- information about gram and liter (for example: “Soit 135 € le kg.”) should be excluded from the product_description


### INSTRUCTIONS FOR product_name:
- If there is an entry in product_name, it is in no case allowed to duplicate the same value in product_description.
- The product name cannot be included in the product description.
- if "product_name" and "product_brand" identical  you need record in "product_brand" value "Null"

### INSTRUCTIONS FOR product_description:
- The quantity of the product, such as weight or volume (ml, l, g, kg), is always recorded in the "product_description".
- If the input text has not been assigned to   any of the parameters, it should be written in "product_description"
- In no case should the name of the product be recorded in the "product_Description" it is better to write down only Null
- IMPORTANT if in offer specified information about base unit without price ("le m2","le kilo") you need to write in product_description

### INSTRUCTIONS FOR deal_description:
- To "deal_description", certain terms of the deal are attributed, such as "Le moins cher".  This information should be recorded in "deal_conditions":
- Data such as litsre and grams (e.g. 1 litre = € 1,50, Le kg : 5,20 €, 9,95 € le kg). must not be in product_description
- "deal_description" can only contain:
  - the description of the possibility of ordering goods online (for example: "nur online", "auch online".),
  - the validity period of the deal (e.g. "ab Donnerstag, 1.2")
- Sometimes the deal description is cut out: ie. For “-50% sur le 2e” Al puts “sur le 2e” in “deal_conditions”, whereas the full offer should be in “deal_description”.
- the full offer should be in the “deal_description” field (for example: “-50% sur le 2e:”), but then you do not need to duplicate it in deal_conditions and you need to write only null
- IMPORTANT in product_description cannot feed values from deal_pricebybaseunit
- deal_description cannot contain a price
- if in description exist text about price (for example:"5.90€ l`unite") for one unit you need to write in deal_description

### INSTRUCTIONS FOR deal_pricebybaseunit:
- always add the value of the base unit to deal_price (for example, 1 liter = 1.50 €, Le kg : 5.20 €, 9.95 € le kg,Le L : 18.95 €), but if the price per kilogram (for example, 1 liter = 1.50 €, Le kg : 5.20 €, 9.95 € le kg, 29.99 € le kg,Le L : 18.95 €)is the same as maxPrice and minPrice (1.50 ,5.20 ,9.95, 29.99,18.95), then write Null in deal_pricebybaseunit.
- In the absence of a clear indication, check the full text of the offer, where the information may be hidden (for example, in the small print or in the product description).

### INSTRUCTIONS FOR deal_loyaltycard:
- If the offer mentions any loyalty program compte, cagnoté, prix déduit, Prix payé en caisse, Prix carte, Sans carte, then "deal_loyaltycard" should be set to True.

### INSTRUCTIONS FOR deal_conditions:
- "deal_conditions" must contain only the terms and conditions to activate the discounted price.
- To “deal_description” certain deal terms are attributed, such as “Le moins cher”. This information should be recorded in “deal_conditions”.
- IMPORTANT Write words such as (“les 2”,“Les 2 pour”,“soit la bouteile”,"la barquette","la barquette 6 pièces ","le prodidut",“les 3 pour” ,"le kilo","le kg" ,"le produit" and so on) in deal_conditions

### INSTRUCTIONS FOR additional_format:
- Text uniqueness:Before adding data to the product_description, check if this text contains values that are already present in the details fields (unit_size, origin_country, etc.). 
If it does, remove it from the product_description.
Leave in the product_description only the information that is not present in the other fields.
- Category priority:Always leave the category (Catégorie 1) in the product_description, even if other data is duplicated.
Field clarity:

All information must be in its respective fields:Size: Record only in unit_size.
  Country of origin: Record only in origin_country.
  Additional information: Unique data not included in other fields should remain in        product_description.
- Duplication and deletion:If data is duplicated between the fields (unit_size, origin_country) and product_description, leave this data only in the main field (for example, unit_size) and remove it from product_description.

-Formatting:The product_description should be concise and clear. Avoid duplicating data from other fields. For example, if the size is 750/975g in unit_size, it should not be in product_description.


### Check at the end:
- IMPORTANT in "product_brand", "product_description" , "product_name" cannot have the same values
- IMPORTANT check and record "deal_pricebybaseunit" if there exist in offe
- At the very end, cross-check that no words or phrases from "product_name" appear in "product_description". This is critical for accuracy.
- IMPORTANT remove any words from "product_description" if they are repeated in "product_description". Make sure they do not appear even if they partially match .
- Check if the description and brand cannot contains words from the product name
- Always write down the age category if it is in the "deal_description" not "product_description"
- Always write an accurate product description

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
You will be provided with image relating to offers from a promotional brochure.

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

### INSTRUCTION GENERAL:
- Always divide transactions into separate deals for example: deal_1, deal_2
- If there are REGULAR_PRICE and SALES_PRICE, they must be divided into deal_1, deal_2
- The result should always be stable IMPORTANT
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- Always write "product_name" in full in the parameter.
- Correct any grammatical errors in French input, especially broken words.
- Use "Null" if no data is available for a category.
- Always write "Null" with a capital letter
- Use French for "product_Product_category" (Google category style).
- "deal_loyaltycard" can only be "False" or "True".
- if text has "Dont éco. contribution : 0,12€TTC" you want to be ignored and record Null
- IMPORTANT  in deals "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- IMPORTANT “price_type" need record "SALES_PRICE" or "REGULAR_PRICE”.
- deal_frequency always "ONCE"
- If loyalty terms (e.g., "compte", "cagnoté", "prix déduit") are mentioned, set "deal_loyaltycard" to "True".
- Ensure unique values for each JSON parameter.
- "deal_type" can only be "REGULAR_PRICE" and "SALES_PRICE.
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- If there is a crossed-out price, it must be recorded in a separate deal with the REGULAR_PRICE type 
- The main price is always a separate deal with the REGULAR_PRICE type
- Just the crossed out price is recorded in a separate deal_type REGULAR_PRICE
- The price that is not crossed out should go to SALES_PRICE 
- VERY IMPORTANT Dont create a separate deal with price (HT) 
- In any case, do not write down the deal for the price without tax (HT)
- Note that prices without tax (HT) should be ignored and not recorded at all.
- The "deal" structure is always unique:
- IMPORTANT Each "deal" must have its own unique number, even if it belongs to one product and remember to clear deals that belong to "HT"
- IMPORTANT to write TTC for deal_description if it is available on the offer
- REMEMBER there can be only one price REGULAR_PRICE or two prices second SALES_PRICE
- NEVER record several deals in one deal
- IMPORTANT:
    Always record in product_description prices  without tax (HT) in a format that includes cents.
    If the price is crossed out or not crossed out, enter it in triangular brackets in the following format: <whole.cents€HT>.
    Examples: <27.23€HT>, <43.46€HT>, <19.31€HT>.
    Be sure:
    Make sure that all prices without tax, even crossed out prices, are stored exclusively in the product_description field.
    Never record prices without tax (HT) in any other field.
    If there is only one price without tax, be sure to write only one price and do not invent others that do not exist
    whether the cents after the decimal point are correct, the product_description should be <4.23€HT> or <4.15€HT>. 
- The price must be stored and displayed without modification or rounding (For example: If the input value is 4.154, you need to display 4.15, not 4.00).
- TTC record only if this exist in image if not exclude from deal_description
- ALWAYS to clear deals that belong to "HT"
- You cannot write TTC if it does not exist 
- Deal with minPrice and maxPrice should always be the same
- Unit prices (e.g: "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description "**.
- Never record in deal price HT 
- Only the TTC price is recorded in the deal, the "HT" price is always ignored
- Prices without tax (HT) should **never** be included in any deal or separate entry IMPORTANT.
- If the HT price is crossed out, **it must be completely ignored** and should **not** be recorded anywhere in the data, including in the `deal_conditions`, `product_description`, or any other fields.
- **Do not create a separate deal for the HT price**, even if it is crossed out.
- IMPORTANT dont create deal if her dont have max and min price
- Note that prices without tax (HT) should be ignored and not recorded at all.
- Always number the deal and NEVER record several deals in one
- If there is a price with TTC tax then it is forbidden to create other deals
- Exclude all information about price without tax HT from deal
- All references to the price without tax (HT) should be excluded from the data. If the text contains information about the price without tax (for example, “43.29 €HT”), it should be ignored and not recorded in any field.
- Always write all HT information in product_description
- IMMEDIATELY dont not create deal with HT price
- Always divide transactions into separate deals for example: deal_1, deal_2
- NEVER record several deals in one deal

### INSTRUCTIONS FOR additional_format:
- Text uniqueness:Before adding data to the product_description, check if this text contains values that are already present in the details fields (unit_size, origin_country, etc.). 
If it does, remove it from the product_description.
Leave in the product_description only the information that is not present in the other fields.
- Category priority: always leave the category (Catégorie 1) in the product_description, even if other data is duplicated if there is no data then write Null
Field clarity:

All information must be in its respective fields:Size: Record only in unit_size.
  Country of origin: Record only in origin_country.
  Additional information: Unique data not included in other fields should remain in  product_description.
- Duplication and deletion:If data is duplicated between the fields (unit_size, origin_country) and product_description, leave this data only in the main field (for example, unit_size) and remove it from product_description.
-Formatting:The product_description should be concise and clear. Avoid duplicating data from other fields. For example, if the size is 750/975g in unit_size, it should not be in product_description.

### INSTRUCTION FOR product_name:
- "product_name" always has a value and cannot appear in "product_description".
- Never repeat the product name in the `product_description`.
- if "product_name" and "product_brand" identical  you need record in "product_brand" value "Null"

### INSTRUCTION FOR product_description:
- "product_description" cannot contain information related to "product_name" or "deal_pricebybaseunit".
- Avoid repeating words from "product_name" in "product_description."
- Include product quantities (ml, l, g, kg) in "product_description".
- Unassigned input text should go into "product_description".
- deal_description cannot contain a price with tax "1.91€ TTC"
- dont record sku number in "product_description" and always write this in "product_sku" (for example:"485189/485146/485138/485170/485162.") 
- IMPORTANT in product_description cannot feed values from deal_pricebybaseunit
- Always indicate the price, the crossed-out price excluding tax and the price excluding tax in the product description (for example: "Inner and outer polypropylene. metal fittings. 8 cm diameter. <3.00€HT>  <1.59€HT>, <43.29€HT>") and always indicate the price with HT in brackets 
- If in "product_description" has same information in "product_name" should be in "product_description" Null
- if there are no HT letters in < > then do not write anything
- IMPORTANT: In the product_description, only add the price in the format <799.99€HT> if it is clearly marked as HT on the page. If there is no “HT” marking, the price must be ALWAYS is excluded <799.99€HT> in product_description.
- IMPORTANT if there is no HT price then be sure to exclude data from the product_description
- Always indicate the entire price with HT in the product description, regardless of whether the price is crossed out or not

### INSTRUCTION FOR deal_description:
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- if the description contains TTC, then you need to write “TTC” in the deal_description, but if there is no TTC, then do not write it in the deal_description
- Sometimes the deal description is cut out: ie. For “-50% sur le 2e” Al puts “sur le 2e” in “deal_conditions”, whereas the full offer should be in “deal_description”.
- The "deal_description" describes the terms of the deal, e.g. "Offre valable sur le moins cher" if any.  This information must be complete and recorded in the "deal_description" field.
- The full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only Null
- In deal_description if price with tax or not tax  (for example:"1.91€ TTC","3.00€HT") need to record only "TTC" or "HT" without number
- If there’s an age rating (e.g., "à partir de 3 ans"), it should be placed in `product_description`.
- ALWAYS exclude  TTC value from the "deal_description" if it is nowhere IMPORTANT
- always ignore the discount in the deal_description section if it is present: “4€ de remise immédiate”, "1€ de remise immédiate", "34% de remise immédiate" and write the discount in the discount field
- if TTC cannot contain in page immediately exclude from deal_description

### INSTRUCTION FOR deal_pricebybaseunit:
- IMPORTANT When the unit price (liter or kilogram) is listed directly below the main price: Check whether the base unit information (e.g. “Le L : 18.95€”) is located directly next to the main price If this is the case, only write the base unit in deal_conditions, for example: “deal_conditions": “Le L”. Do not add anything to the deal_pricebybaseunit field.
- IMPORTANT When the base unit price is far from the main price: If the base unit information is located in the text or description (for example, “Le kg : 27.91€”), then it needs to be moved to deal_pricebybaseunit. For example: “deal_pricebybaseunit": “Le kg : 27,91€”. Do not add this information to deal_conditions.
- Extract "deal_pricebybaseunit" in the format <base-unit> = <price> (fror example=  1 l = €1.50, Le kg : 5.20 €, 9.95 € le kg).
- In the absence of a clear indication, check the full text of the offer, where the information may be hidden (for example, in the small print or in the product description).
- Duplication check: Before writing a value to deal_pricebybaseunit, check if this value is already used in other deals.
- Uniqueness: Each deal must have a unique value in deal_pricebybaseunit or be left blank if the base price is duplicated.
- Priority: If there is a duplicate value, only record deal_pricebybaseunit for a deal with a REGULAR_PRICE type. For a deal with the SALES_PRICE type, deal_pricebybaseunit must be Null if there is no separate price per base unit for this deal.
- Duplicate action: In case of duplication, leave the deal_pricebybaseunit for one deal and set it to “Null” for the other deals.
- Adding a base price is mandatory:Always add a base unit value (for example: "1 liter = 1.50 €","Le kg : 5.20 €", "le kg : 27.91 €") to the deal_pricebybaseunit.
- IMPORTANT always add the value of the base unit to deal_pricebybaseunit (for example, "1 liter = 1.50 €", "Le kg : 5.20 €", "9.95 € le kg" ,"le kg : 27,91€"), but if the price per kilogram (for example, 1 liter = 1.50 €, Le kg : 5.20 €, 9.95 € le kg, 29.99 € le kg , le L : 18,95€ )is the same as maxPrice and minPrice (1.50 ,5.20 ,9.95, 29.99, 18.95), then write Null in deal_pricebybaseunit.
- if in page exist information about base unit always add in deal_pricebybaseunit
- IMPORTANT In the deal_pricebybaseunit, you cannot specify a price for the entire product, only for the base unit.
- If the information about the base unit of measurement (for example, “Le kg : 27.91 €”) is located in the text far from the main price, then it must be specified only in deal_pricebybaseunit, and leave the value “Null” in deal_conditions.
- It is not allowed to duplicate information in both fields at the same time.
- If the base unit information (for example, “Le L : 18.95 €”) is located below the base price, it is displayed only in deal_conditions, and the deal_pricebybaseunit field remains “Null”.
- If a value in the deal_pricebybaseunit duplicates information that can be understood from the deal_conditions (e.g. “Le L : 18.95 €” and “Le L”), the deal_pricebybaseunit is deleted.
- No value in deal_conditions and deal_pricebybaseunit can duplicate information about displacement, weight, or minPrice and maxPrice.
- if the deal_pricebybaseunit contains the total weight for the product, then it should first be in REGULAR_PRICE
- If both fields contain the same information (for example, “Le L” in deal_conditions and “Le L : 18.95 €” in deal_pricebybaseunit), only one field remains: deal_conditions with a unit of measure (for example:“Le L”) only in one group of conditions and **IMPORTANT ALWAYS Null in the other.**
- IMPORTANT If only one base unit (for example:"Le kg : 27.91 €") in offer she must to write only in  deal_pricebybaseunit in "REGULAR_PRICE"

### INSTRUCTION FOR discount:
- Ignore discounts in all parameters except “discount” (for example: "-13%", "-5€", "from 2 to -50%").
- ALWAYS write the discount in euros "-200€" or percentage, "34%", "-13%", "-5€", "from 2 to -50%" in the "discount" field
- if contain text (for example:"1€ de remise immédiate","3€ de remise immédiate","5€ de remise immédiate") record to discount "1€","3€","5€"

### INSTRUCTION FOR deal_conditions:
- in "deal_conditions" canot contain information about contribution (for example: "Dont éco. contribution : 0,07€TTC") record Null
- To “deal_description” certain deal terms are attributed, such as “Le moins cher”. This information should be recorded in “deal_conditions”.
- in "deal_conditions" cannot contain information about the price without tax (43.29 €HT)
- IMPORTANT Write words such as (“les 2”, “Les 2 pour”, “soit la bouteile”, “la barquette”, “le product”, “les 3 pour”, “Vendu seul” and so on) in deal_conditions but it is important that there is only one deal_condition in one deal_condition instead of repetitions write Null
- If the condition (for example: “le product”) appears in SALES_PRICE, remove it from REGULAR_PRICE (by setting it to “Null”), but keep it in SALES_PRICE if it is present on the offer.
- Exclude (le produit) from REGULAR_PRICE
- there cannot be a duplicate deal (for example: “Le L”,"Le produit") in “deal_conditions” (there can be only one, then it must be included immediately before generating JSON)
- if there is such text under the price in SALES_PRICE (for example: “Le lot au choix”, "Le L" and so on), then it should be written only in the condition to SALES_PRICE  and IMPORTANT write Null in REGULAR_PRICE!
- For each deal, if the condition is a SALES_PRICE and contains specific text (e.g., 'Le lot au choix'), write it in deal_conditions for SALES_PRICE, and set deal_conditions to Null for REGULAR_PRICE in the same set of deals."
- You can implement this by ensuring that for each pair of deal_1 and deal_2, if deal_conditions for SALES_PRICE contains "Le lot au choix", you remove it from deal_conditions for the REGULAR_PRICE.
- if in  deal_pricebybaseunit is exist (for example:"9.90 € le kg","6.53 € le kg") you must exclude all information about base unit from "deal_conditions" (for example:"Le kg") and write Null

### HIGHT PRIORITY INSTRUCTIONS:
- Leave only deals with “deal_description”: “TTC”.
- IMPORTANT Delete all deal "HT"
- if there is information about kilograms or liters on the page, then be sure to write them in the appropriate fields
- Each deal is allocated to a separate key: “deal_1”, "deal_2" on so on
- there can be no identical conditions in two deals 
- If “deal_conditions” and “deal_pricebybaseunit” occur simultaneously in one deal: “Le L” and "deal_pricebybaseunit": “Le L : 18.95 €”, then you need to leave only deal_conditions
- ALWAYS, if the offer does not contain prices with TTC tax, immediately exclude them from the deal_description
- IMPORTANT Write words such as (“les 2”, “Les 2 pour”, “soit la bouteile”, “la barquette”, “le product”, “les 3 pour”, “Vendu seul”, “le lot","Le produit" and so on) in deal_conditions but it is important that there is only one deal_condition  in one deal_condition in SALES_PRICE  instead of repetitions write Null


### Check yourself:
- IMPORTANT delete extra deal with information about price or crossed out price (HT) and leave only TTC
- ALWAYS if the offer has more than 2 prices (regular_price and sales_price), they also need to be recorded
- always check the correctness of the discount in euros, especially in the following cases (1€ de remise immédiate )
- IMPORTANT: always check whether you need to write information about “<1.59 €HT>”, “<43.29 €HT>” in the product_description sometimes you do not add a correctly crossed out HT price or add it where there are no HT prices at all
- IMPORTANT: check if the offer contains information about taxes, if not, immediately remove all references to information from the product_description “<1.59 €HT>”, “<43.29 €HT>” 
- IMPORTANT if there is a discount, be sure to record it in the sales price discount
- IMPORTANT: if there is no HT price, exclude data from product_description 
- IMPORTANT never create another deal if be in the offer price taxes TTC!
- IMPORTANT never specify a price with “TTC” tax in the deal_description, it will immediately exclude it from the listing if it does not exist 
- never write to the TTC if there is no tax on the offer price, instead write Null
- always only write in deal_deascription if there is a TTC price 
- IMPORTANT Always add a base unit if it is available and does not interfere with other rules
- If the price per unit "deal_pricebybaseunit" is explicitly specified as additional information and does not duplicate the value from deal_maxPrice or deal_minPrice, it must be recorded.
- Be sure to check the entire page for the base unit of measurement (for example, “Le kg : 27.91 €”,“Le kq : 27.91 €”,"Le kg : 4.59 €" and so on) and write it in deal_pricebybaseunit
- check that there is no duplication of information about the displacement and kilograms in both fields (deal_pricebybaseunit and deal_conditions) for example (“deal_pricebybaseunit”: “Le L : 18.95 €”, “deal_conditions”: “Le L”,)
- check that there is no deal that has a price without tax (HT), if there is one, then you need to remove it immediately before generating JSON
- Make sure that the unit price is indicated if it is under the price or in the text, and only then generate JSON with all the unit data inserted
- Always avoid duplicating the same phrases from a separate agreement in deal_conditions
- IMPORTANT: make sure that the product_description contains all prices without HT tax, if there are such prices (“<1.59 €HT>”, “<43.29 €HT>”) immediately add them to the product_description and only then generate JSON 
- if not TTC in the page you need to exclude all information from deal_description about TTC
- if in page exist base unit (“Le kg : 27.91 €”) immediately write information about base unit in "deal_pricebybaseunit" field
- if  SALES_PRICE "deal_conditions" has value ("Le L","Le lot au choix","Le produit") you need ALWAYS IMMEDIATELY delete ("Le L","Le lot au choix","Le produit") in REGULAR_PRICE deal_condition
- if there are several base units for each deal on the page, you must write each to its own type in SALES_PRICE and REGULAR PRICE in deal_pricebybaseunit and exclude them from deal_conditions

 


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
You will be provided with a image of the offer from the brochure.

Output Format:
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

### INCTRUCTIONS FOR GENERAL:
- "product_name" must always have a value.
- Ensure "product_name" has the complete product name.
- Data such price as litre and grams (e.g. 1 litre = € 1,50, Le kg : 5,20 €, 9,95 € le kg). must not be in product_description
- Avoid repeating words from "product_name" in "product_description."
- "product_description" cannot contain information related to "product_name" or "deal_pricebybaseunit".
- "product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
- Any unassigned input data should go in "product_description."
- IMPORTANT there are situations where there are three different prices” crossed out price, regular price and price with a discount on the loyalty card, then you need to write them in three different transactions in which the discount with the loyalty card will be of type SALES_PRICE, and all the rest - REGULAR_PRICE
- In main_format product_description should be has full descriptions about all price
- All available prices on the page should be displayed in the product_description. This will provide complete information, exclude only those prices if these prices are already in the deal_minPrice or deal_maxPrice fields. Include all prices in the product_description for a detailed description of each product.
- Ensure French language accuracy, correcting broken or hyphenated words.
- record each individual "deal" sequentially (for example: "deal_1", "deal_2").
- If the category is unknown, use "Null" for "product_product_category."
- Set "product_product_category" as a French-language Google product category.
- The "deal_loyaltycard" can only be "True" or "False."
- Crossed out price ALWAYS include in new sepatate  with unique number  "deal" and  deal_type "REGULAG_PRICE"
- Write the unit price (for example: "soit l'unite") in regular and the discounted price (for example: "les 2") in sales
- If product_brand is (for example:"PAIC","kinder") then "product_name": (for example:"Exel","bueno") and so on
- Exclude from product_description all information about (for example, 1 l = € 1.50, Le kg : 5,20 €, 9,95 € le kg, Prix vendu seul : 1,75 €-)
- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- All parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "True" or "False" values.
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- IMPORTANT in product_description cannot feed values (for example: "Soit le kg : 14,68 €" ) from deal_pricebybaseunit
- If "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- Price with type "SALES_PRICE" always less than "REGULAR_PRICE"
- IMPORTANT  in deals "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- IMPORTANT “price_type" need record "SALES_PRICE" or "REGULAR_PRICE”.
- IMPORTANT exclude all price data from the product description
- IMPORTANT exclude all price data from the "product_description"
- IMPORTANT "deal_type" in "main_format" can only be "SALES_PRICE" or "REGULAR_PRICE."
- IMPORTANT If price has three price (crossed out, regular and discount) then we record only discount in "SALES_PRICE" and regular in "REGULAR_PRICE"
- If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "True."
- Adhere strictly to the example structure.
- Unit prices (for example: "Le kg : 24.94 €", "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description" **.
- Values in one JSON parameter should not duplicate in another.
- Min and max price must always be specified and must be the same for each deal
- It is important to write the price for for two unit (for example:"soit l'unite") in the SALES_PRICE deal and one unit (for example:"Les 2 : 17,98 € au lieu de 23,98 €"  in deal_conditions) in REGULAR_PRICE
- Be sure to record the price for one item and the price for multiple items in a separate deal
- Indicate only the price for one product and the price of the product that will cost at a discount
- Each individual deal must be recorded in a separate deal_1 and deal_2
- You always missing data about crossed out price
- Remember that if there is a discount on the offer (“-34%”, “60%”, “2€”, “-1€”), it must be written in additional_format in “discount”
- The percentage discount and its description should be ignored and not recorded in any of the parameters
- if the information about deal_pricebybaseunit is not accurate, then it is desirable that the price per unit in REGULAR_PRICE is higher and in SALES_PRICE is lower
- IMPORTANT data cannot be repeated in product_brand product_description product_name 
- IMPORTANT The percentage discount and its description ("30% soit 6,90 € versés sur ma Carte U") should be ignored and not recorded in any of the parameters except additional_format in the “discount” field
- must be only two deal
- Uniqueness of deal_pricebybaseunit: The value of deal_pricebybaseunit should be recorded in only one deal for each product. If this value is already used in one deal, other deals for this product must contain “Null” in the deal_pricebybaseunit field.
- Uniqueness of product_description and product_name: the product_description and product_name fields cannot contain the same values. If the values in both fields are the same, you need to update one of them to make it completely unique without duplication, and if the words are repeated, then write Null in product_description.

### INSTRUCTIONS FOR additional_format:
- Text uniqueness:Before adding data to the product_description, check if this text contains values that are already present in the details fields (unit_size, origin_country, etc.). 
If it does, remove it from the product_description.
Leave in the product_description only the information that is not present in the other fields.
- Category priority: always leave the category (Catégorie 1) in the product_description, even if other data is duplicated if there is no data then write Null
Field clarity:

All information must be in its respective fields:Size: Record only in unit_size.
  Country of origin: Record only in origin_country.
  Additional information: Unique data not included in other fields should remain in  product_description.
- Duplication and deletion:If data is duplicated between the fields (unit_size, origin_country) and product_description, leave this data only in the main field (for example, unit_size) and remove it from product_description.
-Formatting:The product_description should be concise and clear. Avoid duplicating data from other fields. For example, if the size is 750/975g in unit_size, it should not be in product_description.


### INCTRUCTIONS FOR deal_pricebybaseunit:
- Extract "deal_pricebybaseunit" only from segments containing the base unit price in the format <base-unit> = <price>, like "1 l = € 1.50," "Le kg : 5,20 €," or "9,95 € le kg."
- Always add the value of the base unit to deal_pricebybaseunit (for example, 1 liter = 1.50 €, Le kg : 5.20 €, 9.95 € le kg), but if the price per kilogram (for example, 1 liter = 1.50 €, Le kg : 5.20 €, 9.95 € le kg, 29.99 € le kg)is the same as maxPrice and minPrice (1.50 ,5.20 ,9.95, 29.99), then write Null in deal_pricebybaseunit.


### INCTRUCTIONS FOR discounts:
- Ignore discounts (for example: "-13%", "-5€", "2ème à - 50%") for all JSON parameters except the discount parameter
- IMPORTANT discount (for example:"-68% sur le 2ème" ,"60% sur le 2ème") need to record "-68%","60%"
- The discounted price will always be SALES_PRICE 
- ALWAYS add a discount in the "discount" field 


### INCTRUCTIONS FOR deal_description:
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
- If deal_conditions and deal_description are duplicated, then write "Null" in deal_description 
- Always record descriptions in  deal_description if it exist otherwise null
- IMPORTANT deal_description cannot contain information about price and base unit
- Write down the information that is under the description (for example: “au lieu de 18€55”) in deal_description
- The price in the description cannot be the same as the max and min price (“Les 2 : 6,97 € au lieu de 9,30 €”), you need to exclude “Les 2 : 6,97 €”
- The text from deal_conditions, if it contains additional information (for example, “Vendu seul : 2€35”,"Soit les 2 produits: 4.99€ - Soit le kg : 13.79€"), should always be transferred to deal_conditions for the SALES_PRICE type, avoiding duplication in deal_conditions and leaving deal_description empty for the REGULAR_PRICE type.
- If the offer text contains the condition “Vendu seul”, it must be recorded in the deal_description along with the associated price (for example, “Soit l'unité 1 €77, Vendu seul : 2 €35”,"Le lot vendu seul: 8.30€") and the base unit must be specified in deal_pricebybaseunit only in SALES_PRICE and leaving deal_description empty for the REGULAR_PRICE type..
- In deal_conditions, write only general conditions, such as “Les 2” or “Soit l'unité”, without specifying prices or details of the sale separately.
- Terms like “Vendu seul” should be completely excluded from deal_conditions and included in deal_description.
- Always follow the format: short terms in deal_conditions, and extended terms (with a price like “Vendu seul”) in deal_description.
- extended text (for example, “Vendu seul : 2€35”,"Soit les 2 produits: 4.99€ - Soit le kg : 13.79€") can only be in SALES_PRICE and always excluded from REGULAR_PRICE

### INCTRUCTIONS FOR deal_conditions: 
- If the text of the offer contains short terms (for example, “les 2”, “Les 2 pour”, “soit la bouteile”, “l'unite”), write them down without changing them.
- IMPORTANT Write words such as (“les 2”, “Les 2 pour”, “soit la bouteile”, “la barquette”, “le product”, “les 3 pour”, “Vendu seul” ,“l'unite” and so on) in deal_conditions but it is important that there is only one deal_condition in one deal_condition instead of repetitions write Null
- If the offer text contains an extended description of the terms and conditions (e.g., “Soit les 2 produits: 4.99€ - Soit le kg: 13.79€”, ‘soit apres remise l'unite’), write the entire text in deal_conditions.
- It is forbidden to include minimum/maximum prices or prices with units of measurement in the deal_conditions.
- Always choose the full text if the offer text contains both short and long terms.
- Adapt the deal_conditions to the offer text: write short terms briefly, and full terms in full.
- Exclude prices and units of measurement from deal_conditions (for example, “3€89 L'UNITÉ” → “L'UNITÉ”, “SOIT APRÈS REMISE 2€73 L'UNITÉ” → “SOIT APRÈS REMISE”)**write lowercase**.
- Search for keywords in the text (for example, “L'UNITÉ”, “APRÈS REMISE”) and ignore numbers and units of measurement **write lowercase**.
- Add only conditions without numbers and units of measurement to deal_conditions.

### Check yourself
- Always write down the discount("-68%" ,"-2€","20%" in the "discount"
- If in "deal_conditions" nothing to indicate, then write null
- Value of discaunt always ignored
- Check it is true  product_brand
- Check in "deals" in "type" field should contain only the value  "SALES" 
- Check that the "deal_description" does not contain a price for the product (for example: “Soit les 2 produits : 3,50 €”)
- Simple "type" must be only "SALES" not "SALES_PRICE" not "REGULAR_PRICE" not "REGULAR"
- Check that the data about price and base unit always exlude from "deal_description" IF NOT DESCRIPTION RECORD NULL
- "deal_type" in "main_format" must be "SALES_PRICE" AND "REGULAR_PRICE"
- In field "deal_description" connot contain data about "deal_pricebybaseunit"
- In field "deal_description" connot contain data about discount instead record Null
- Always write down the age category if it is in the "deal_description" not "product_description"
- Make sure that the price "vendu seul" per unit is necessarily recorded in the  separate deal
- Make sure that the price per unit of goods ("le kg: 13€63", "Soit le kg: 4,97€") is necessarily recorded in “deal_pricebybaseunit”
- check that the discount is necessarily recorded in the "discount" field
- check product_description and product_name cannot be repeat word

""" 

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
### INSTRICTIONS FOR GENERAL:
- "product_name" must always have a value.
- Avoid repeating words from "product_name" in "product_description."
- "product_description" should not include data related to "product_name" or "deal_pricebybaseunit."
- Ensure "product_name" has the complete product name.
- Extract "deal_pricebybaseunit" from text segments containing only the price by base unit in the format <base-unit> = <price> or similar (for example, 1 l = € 1.50, Le kg : 5,20 €, 9,95 € le kg).
- It is important not to write the base price per unit in the product_description (e.g. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg).
- "product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
- Ensure French language accuracy, correcting broken or hyphenated words.
- Any unassigned input data should go in "product_description."
- Number each "deal" sequentially (e.g., deal_1, deal_2).
- If the category is unknown, use "Null" for "product_product_category."
- Set "product_product_category" as a French-language Google product category.
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
- The full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only Null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- All parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "True" or "False" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- If there is no loyalty card for the price, then deal_loyaltycadr is always False
- If the condition always record in "deal_conditions"
- If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "True."
- Values in one JSON parameter should not duplicate in another.
- Adhere strictly to the example structure.
- "deal_type" can only be "SALES_PRICE" or "REGULAR_PRICE."
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- If "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- IMPORTANT exclude all information about price in "deal_description"
- The discount field cannot be empty if the offer has a discount
- IMPORTANT Discount and discount ("40% sur le 2ème produit au choix soit 1,20 € versé sur ma Carte U") text always must be ignored in JSON
- The following text (“4.78€ 2 products of choice € Carte U deducted”) must be added to the “deal_description” in SALES_PRICE
- The price for two products should be recorded in SALES_PRICE and the card discount in the description of the same deal
- REGULAR_PRICE will be the price without a discount with the description in deal_description (for example:“le produit au choix”).
- SALES_PRICE is the price co discounted and with a description in deal_description (for example: “Les 2 produits au choix € Carte U déduits”).
- The price in the deal_description cannot be the same as minPrice and maxPrice, so write the deal_description in this format (“4,78 € les 2 produits au choix payés en caisse”) and the minPrice and maxPrice “5.98”
- The price in deal_description must be different from both minPrice and maxPrice. 
- IMPORTANT The percentage discount and its description ("30% soit 6,90 € versés sur ma Carte U") should be ignored and not recorded in any of the parameters except additional_format in the “discount” field
- prices with date restrictions should be written down separate deal
- Uniqueness of deal_pricebybaseunit: The value of deal_pricebybaseunit should be recorded in only one deal for each product. If this value is already used in one deal, other deals for this product must contain “Null” in the deal_pricebybaseunit field.
- Uniqueness of product_description and product_name: the product_description and product_name fields cannot contain the same values. If the values in both fields are the same, you need to update one of them to make it completely unique without duplication, and if the words are repeated, then write Null in product_description.
- Write "Prix payé en caisse" in deal_conditions, ensure there are only two deals, with the first deal being REGULAR_PRICE. For SALES_PRICE deals with a discount, write "49.99 remise fidélité déduite" in deal_description.
- must be only two deal
- deal one is REGULAR_PRICE
- if deal with type SALES_PRICE have discout you need write (49.99 remise fidelite deduite) in deal_description
- Exclude all information about discount 

### INSTRUCTIONS FOR main_format:
- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- NEVER record several deals in one deal

### INSTRUCTIONS FOR “deal_description”:
- Write full information about description (for example:"La barquette" ,"le produit" )  in the deal_description field
- Always write only the description that applies to a specific deal
- Exclude text  (for example:"Les 2 produits au choix" , "Les 2 produits au choix € Carte U déduits") from deal_description
- Always record descriptions in  deal_description if it exist otherwise null
- Search for the price for two products (for example:“5.95€ les 2 produits au choix payes en caisse”) and write only this price in the SALES_PRICE deal and add the description (for example:“4.78€ les 2 produits au choix € carte u deduits”) to it in the deal_description in main_format
- IMPORTANT ALWAYS make sure that the price for example (4.78 €) in the deal_description is always less than the maximum and minimum price for example (5.98 €), because it is a discount
- IMPORTANT ALWAYS add all information about  additional credits (“5 € supplementaires verses sur”) should be recorded in the deal_description
- Add a description to a price that is limited in time

### INSTRUCTIONS FOR deal_conditions:
- If there is such a text (“La boîte”, “La boîte € Carte U déduits”), then you need to write “La boîte” in REGULAR_PRICE and “La boîte € Carte U déduits” in SALEC_PRICE in deal_conditions
- If there is such a text (“Le produit au choix”, “Le produit au choix Carte U déduits”), then you need to write “Le produit au choix” in REGULAR_PRICE and “e produit au choix  Carte U déduits” in SALEC_PRICE in deal_conditions
- Do not repeat the conditions in deals 
- Condition must be in price with discount deal_2
- Always write only the condition that applies to a specific deal
- Text (for example:"Les 2 produits au choix" , "Les 2 produits au choix € Carte U déduits") must be in deal_conditions and exclude from deal_description
- IMPORTANT Write words such as (“les 2”,“Les 2 pour”,“soit la bouteile”,"le prodidut",“les 3 pour” and so on) in deal_conditions

### INSTRUCTION FOR discount:
- Ignore discounts in all parameters except “discount” (for example: "-13%", "-5€", "from 2 to -50%").
- ALWAYS write the discount in euros "-200€" or percentage, "34%", "-13%", "-5€", "from 2 to -50%" in the "discount" field
- if contain text (for example:"1€ de remise immédiate","3€ de remise immédiate","5€ de remise immédiate") record to discount "1€","3€","5€"



### 

- Condition and description values cannot be repeated in separate deal
- ALWAYS record discount
- Always write a similar text (20%, i.e. 1.50 € verse sur ma Carte U) only in the deals "SALES_PRICE"

Instructions 2:
IMPORT Ensure that all mentions of discounts (for example:percentages like "20%", fixed amounts like "-10€") are accurately extracted and recorded in the "discount" field under "deals".

min and max price must always be specified and must be the same for each deal
Unit prices (for example: "Le kg : 24.94 €", "(1 kg = 13.09)", “1 kg = 4.28”, “1 l = € 1.33”, “1 kg = 11.84/ATG”, “5.20/Liter”, “(1 kg = 11.99)”,"1 Liter = 25.98") **are not recorded and should be ignored when filling in "product_description "**.
check whether there are any base units in the product_description (for example. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg), if so, remove them from there
Always check if you have a loyalty card 
The price without a loyalty card is recorded in a transaction of the REGULAR type, and the price with a loyalty card is recorded in a separate transaction of the SALE type.
Each deal moust be in separate deal_n
in deals in additional_format type must be SALES_PRICE
text like be Carte U déduits and so on must be in deal_condition
always indicate the unit (for example: "Le kg : 24.94 €",   ) price in the deal_pricebybaseunit 
the deal_description cannot contain the price for the product (for example:"2€73 le lot"), put it in Null 

### check yourself 
- Always check that the value without the card is recorded correctly and the value with the card is recorded correctly IMPORTANT
- Always check is correctly record description in each deal, remember that you cannot have the same description in two deals  IMPORTANT
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "SALES_PRICE"
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "REGULAR_PRICE"
- Check in "price_type" must be only value "SALES_PRICE" or "REGULAR_PRICE" not "REGULAR"
- In field "deal_description" connot contain data about "deal_pricebybaseunit"
- In field "deal_description" connot contain data about discount instead record Null
- ALWAYS check whether you have a loyalty card or not 
- Your often record in "deal_loyaltycard" True when should be False
- Add this information ("-10€ DE REMISE IMMÉDIATE AVEC") in "deal_condition" only if "deal_loyaltycard" True
- Always make sure that the discount should be recorded in the “discount” field in any case.
- Always write down the age category if it is in the "deal_description" not "product_description"
- IMPORTANT all deal must have unique numeric (for example:"deal_1","deal_2")
- Always write down the discount("-68%" ,"-2€","20%","4€" in the "discount"
- NEVER record several deals in one deal
- Always write down the discount("-68%" ,"-2€","20%","4€" with loyalty card ) in the "discount"
- Check if right record minPrice and MaxPrice  and deal_description
- Check if the information about additional credits (“3 € supplementaires verses sur” ,"20% supplementaires verses sur") is added to the deal_description
- Check if the information about description(“la produit d`eco-participation”,"la produit avec ma carte u") is added to the deal_description
- 
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


money_spared_on_the_card =  """
Your Role:
You will be provided with image related to an offer from the promotional brochure.

Output Format:
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


### INSTRUCTION FOR GENERAL:
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- All parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- Extract "deal_pricebybaseunit" only from segments containing the base unit price in the format <base-unit> = <price>, like "1 l = € 1.50," "Le kg : 5,20 €," or "9,95 € le kg."
- do not write the base price per unit (e.g. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg, ∏le kg : 33€31) in the product_description.
- "product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
- Ensure French language accuracy, correcting broken or hyphenated words.
- Any unassigned input data should go in "product_description."
- Number each "deal" sequentially (for example: "deal_1", "deal_2")
- If the category is unknown, use "Null" for "product_product_category."
- Set "product_product_category" as a French-language Google product category.
- The "deal_loyaltycard" can only be "True" or "False."
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- The price with the loyalty card should be recorded in the deal_n with deal_type "SALES_PRICE", and the price without the loyalty card should be recorded in a separate deal_n with deal_type "REGULAR_PRICE"
- The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
- The full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only null
- "deal_frequency" always has the value "ONCE".
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyal`tycadr is always False
- If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "True."
- Values in one JSON parameter should not duplicate in another.
- Adhere strictly to the example structure.
- "deal_type" can only be "REGULAR_PRICE" or "SALES_PRICE".
- Check whether there are any base units in the product_description (for example. 1 litre = 1.50 €, Le kg : 5.20 €, 9.95 € le kg), if there are, then remove them from there
- Before generating the json, check if all the prices are really written in a separate agreement, if they are really present
- Min and max price should always be the same
- Exclude from product_description all information about (for example, 1 l = € 1.50, Le kg : 5,20 €, 9,95 € le kg)
- Crossed-out prices should not contain a description and condition 
- If there are only two prices, then the smaller one will be SALES_PRICE and the larger one will be REGULAR_PRICE
- IMPORTANT do not add a deal if the price is in the product_description
- Use only the data provided in the source file, image, or other source.
- If there is no data for a particular field, leave the value of that field as Null or empty, according to the format.
- Do not repeat values in the following fields:deal_conditions,deal_description,deal_maxPrice,deal_minPrice
- Before adding a record to the structure, perform a check to determine if the field value already exists in another record.
- If the value is duplicated, the field should be set to Null or changed according to other conditions.
- Always divide transactions into separate deals for example: deal_1, deal_2
- NEVER record several deals in one deal

### INSTRUCTIONS FOR additional_format:
- discount ("50€","-20€","-10%","34%") must be in "additional_format" in "discount" field
- Text uniqueness:Before adding data to the product_description, check if this text contains values that are already present in the details fields (unit_size, origin_country, etc.). 
If it does, remove it from the product_description.
Leave in the product_description only the information that is not present in the other fields.
- Category priority: always leave the category (Catégorie 1) in the product_description, even if other data is duplicated if there is no data then write Null
Field clarity:

All information must be in its respective fields:Size: Record only in unit_size.
  Country of origin: Record only in origin_country.
  Additional information: Unique data not included in other fields should remain in  product_description.
- Duplication and deletion:If data is duplicated between the fields (unit_size, origin_country) and product_description, leave this data only in the main field (for example, unit_size) and remove it from product_description.
-Formatting:The product_description should be concise and clear. Avoid duplicating data from other fields. For example, if the size is 750/975g in unit_size, it should not be in product_description.


### INSTRUCTION FOR product_name:
- "product_name" must always have a value.
- Avoid repeating words from "product_name" in "product_description."
- "product_description" should not include data related to "product_name" or "deal_pricebybaseunit."
- Ensure "product_name" has the complete product name.
- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored

### INSTRUCTION FOR deal_description:
- Always record descriptions in  deal_description if it exist otherwise null
- If "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- IMPOTRANT include similar text (for example:"2.89 € sur la Carte Carrefour") in deal_description 
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- IMPORTANT in deal_description must be ignored and excluded information about discount (30% D'ÉCONOMIES) should to record Null
- IMPORTANT in deal_description must be ignored and excluded information about price number(7,79) should to record Null
- ALWAYS exclude price with deal_description
- ALWAYS add descriptions if they are available (for example:"Prix paye en caisse") in offer if not add Null 
- Exclude text  (for example:"Les 2 produits au choix" , "Les 2 produits au choix € Carte U déduits") from deal_description
- IMPORTANT ignore prices that are not in a specially designated block
- Added to product description SALES_PRICE ("soit 5.55 € sur la carte carrefour" and so on) in deal_description
- IMPORTANT IMMEDIATELY exclude  all information about discount (for example:"30% à cagnotter") from deal_description

### INSTRUCTION FOR deal_pricebybaseunit:
- IMPOTRANT exclude similar text (for example:"2.89 € sur la Carte Carrefour") and write Null
- Record in "deal_pricebybaseunit" (for example, 1 l = € 1.50, Le kg : 5,20 €, 9,95 € le kg).
- Duplication check: Before writing a value to deal_pricebybaseunit, check if this value is already used in other deals.
- Uniqueness: Each deal must have a unique value in deal_pricebybaseunit or be left blank if the base price is duplicated.
- Priority: If there is a duplicate value, only record deal_pricebybaseunit for a deal with a REGULAR_PRICE type. For a deal with the SALES_PRICE type, deal_pricebybaseunit must be Null if there is no separate price per base unit for this deal.
- Duplicate action: In case of duplication, leave the deal_pricebybaseunit for one deal and set it to “Null” for the other deals.

### INSTRUCTION FOR deal_conditions:
- IMPORTANT If offer has some text about "Prix payé en caisse" and "Remise Fidélité déduite" you should always write it in "deal_conditions"
- ALWAYS Exclude "Prix payé en caisse" and "Remise Fidélité déduite" in deal_description and include in deal_conditions
- If the condition always record in "deal_conditions"
- if exist text  ("prix payé en caisse") must be in REGULAR_PRICE in deal_conditions
- IMPORTANT Write words such as (“les 2”, “Les 2 pour”, “soit la bouteile”, “la barquette”, “le product”, “les 3 pour”, “Vendu seul”,"cagnotte déduite", "prix payé en caisse"and so on) in deal_conditions but it is important that there is only one deal_condition in one deal_condition instead of repetitions write Null
- in deal_conditions cannot contain price information

### INSTRUCTION FOR discount:
- IMPORTANT ALWAYS if "deal_description" include discount then exclude discount from "deal_description" (for example:"20% D'ÉCONOMIES","30% à cagnotter")
- ALWAYS if "deal_description" include price then exclude price from "deal_description" (for example:"7,79")
- In "deal_deacription" cannot contain information about price (for example:"8,90 PRIX PAYÉ EN CAISSE ","30% à cagnotter","4,45 TICKET E.Leclerc COMPRIS*" ,"302,66 € dont 0,62 € d'éco-participation THE SWITCH + THE GAME Prix payé à la caisse") recond only text ("PRIX PAYÉ EN CAISSE","TICKET E.Leclerc COMPRIS","d'éco-participation THE SWITCH + THE GAME Prix payé à la caisse")
- IMPORTANT always record discount in  "deals" in field "discount" (for example:"20%","-60%",""-30€","20€")
- IMPORTANT: always write the discount in “discount” (for example: “20%”, “-60%”, “-30€”, “20€”)

### HIGHT PRIORITY INSTRUCTIONS:
- never create a separate deal for such cases when there is a discounted price where “deal_maxPrice”: “54.99”, “deal_minPrice": “54.99” which should have a “deal_description”: “Soit 49.99€ Remise Fidélité déduite”,"Je cagnotte : 4,64 €", immediately add this to the deal_description to the price that is under the strikethrough
- It is IMPORTANT to immediately write phrases such as (“les 2”, “Les 2 pour”, “soit la bouteile”, “la barquette”, “le product”, “les 3 pour”, “Vendu seul”, “le lot”, “Le product”, etc.) in deal_conditions, but it is important that there is only one deal_condition in one deal_condition, in SALES_PRICE write Null instead of repetitions.
- if such text (for example: “Soit 5,55 € sur la Carte Carrefour” and so on) is written in deal_description but there is a condition (for example:"Prix payé en caisse" ,"cagnotte déduite" ), then the condition must be written in deal_conditions
- If deal_description contains a number that is already present in deal_maxPrice or deal_minPrice: Remove it from deal_description.
- If the number is already present in any other field (for example, deal_conditions or deal_pricebybaseunit): Set this field to Null.
- IMPORTANT if there is no data on the page, you can't make up your own data!!!
- IMPORTANT If the conditions and description of the discount (for example, “Soit 4€64 sur la carte Casino”) are duplicated between REGULAR_PRICE and SALES_PRICE: Leave only the record with deal_type: “REGULAR_PRICE”.Delete the record with deal_type: “SALES_PRICE”.


### check yourself 
- Text (for example:"Les 2 produits au choix" , "Les 2 produits au choix € Carte U déduits") must be in deal_conditions and exclude from deal_description
- Always check if there is data that can be added to the deal_description  
- Always check that the value without the card is recorded correctly and the value with the card is recorded correctly IMPORTANT
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "SALES_PRICE"
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "REGULAR_PRICE"
- Check in "price_type" must be only value "SALES_PRICE" or "REGULAR_PRICE" not "REGULAR"
- IMPORTANT check that there is no information about discount and price number in field "deal_description" record Null
- If there is no something on the offer, you do not need to come up with your own WRITE ONLY WHAT IS ON THE OFFER
- Always write down the age category if it is in the "deal_description" not "product_description"
- ALWAYS if there is a description of the goods or a condition, it must be written in the appropriate fields
- ALWAYS if there is a discount, it must be written in the appropriate field with a discount and not in all deals
- IMPORTAT check price must be always exclude from deal_description
- IMPORTANT if exist values ("Prix payé en caisse" ,"cagnotte déduite") immediatly need write in deal_conditions
- ALWAYS exclude discout (30% à cagnotter) from all deal_description

- Do not create new deal records for discounts. All information should be added only to the deal_description in the corresponding SALES_PRICE record.
- before generating JSON, check if all keywords are really written in deal_conditions such as (“les 2”, “Les 2 pour”, “soit la bouteile”, “La barquette”, “le productidut”, “les 3 pour”  and so on)
- The deal_conditions, deal_description, and deal_pricebybaseunit fields must not contain values that are already in the numeric fields.nn
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
### INSTRUCTION GENERALS:

"product_name" must always have a value.
"product_description" should always include product quantity, like weight or volume (e.g., ml, l, g, kg).
Ensure French language accuracy, correcting broken or hyphenated words.
Any unassigned input text should go in "product_description."
If the category is unknown, use "Null" for "product_product_category."
Set "product_product_category" as a French-language Google product category.
 The "deal_loyaltycard" can only be "True" or "False."

"deal_frequency" always has the value "ONCE".
IMPORTANT "price_type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.

Ignore discounts (for example: "-13%", "-5€", "2ème à - 50%" ,"4€ de réduction immédiate") for all JSON parameters except the discount parameter, write only ("- 50%","4€","-5€","20%") ”

### INSTRUCTIONS FOR main_format
- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l) cannot be in product_descriptions
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycadr is always False
- cyrrency always € not EUR
- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- ALWAYS if "product_name" = "product_brand" you must exclude value with product_brand  and change null
- ALWAYS if "product_name" !="product_description" record Null 


- ALWAYS all information about discount (for example:"-24%", "-2€" , "30%" ,"4€") add in discount
- If JSON parametr has empty string you must to record "Null"
> IMPORTANT "price_type" and "deal_type" should always be "OTHER".
> "type" should always be "SALES".
> if “product_brand” and “product_description” have the same value as “product_name”, then this value should be excluded from “product_brand” and “product_description”
### Instructions 2:

If the offer includes terms related to loyalty programs like "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte," set "deal_loyaltycard" to "True".
Adhere strictly to the example structure.
The "deal_type" can only have the value "OTHER."
"deal" entries with "deal_type": "OTHER" cannot include values for "deal_maxPrice" or "deal_minPrice."

### INSTRUCTIONS FOR deal_conditions:


### INSTRUCTIONS FOR deal_description:
- ALWAYS add similar text ("sur la gamme chocolat bio Ethiquable" , "-34% de remise immédiate") in deal_description
- always record descriptions in  deal_description if it exist otherwise null
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
- all information about description must to record in deal_description


### Check yourself
- Check if you have filled in deal_conditions correctly
- IMPORTANT Check what "product_description" , "product_name" the data is not repeated
- IMPORTANT Check what "“product_brand”" , "product_name" the data is not repeated
- always write down the age category if it is in the "deal_description" not "product_description"
- NEVER write the same values for product_brand and product_name



""" 


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

Instructions 1:

The "product_name" field must always have a value.
Always include product quantity (e.g., ml, l, g, kg) in "product_description."
Ensure all French text is grammatically correct, fixing any broken words or hyphens.
Any unassigned text from the input should be written in "product_description."
Avoid repeating words from "product_name", "product_brand" and "product_description."
Use "Null" for "product_product_category" if category data is unavailable.
Define "product_product_category" following the structure of a Google product category, and ensure the result is in French.
"deal_loyaltycard" should only be "True" or "False"
"deal_type" can only be "OTHER"

the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only null

- MAIN_FORMAT only the text below the product_name is written to the product_description, other text is ignored
- always record descriptions in  deal_description if it exist otherwise null
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
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
- "loyalty_card" always need have value "True" 
- Cannot duplicate words in product_brand i product_name
- IMPORTANT The percentage discount and its description ("30% soit 6,90 € versés sur ma Carte U") should be ignored and not recorded in any of the parameters except additional_format in the “discount” field only % or €
- in the additional_format in the product field there should be only one product_id with the product that is specified in the product_description
- if the product_description contains the value “GREENcolors ARTY 24, STABILOaquacolor ARTY 24, Pen 68 ARTY 18” then write only in “additional_format” in “products” in name only the product that is written in the description and immediately exclude all others
- IMPORTANT always write in the product_description only the information that is on the page and do not shorten or add anything of your own
- if there are several products on the page, then write only the first one in product_description


Instructions 2:

Set "deal_loyaltycard" to "True" if there’s any mention of loyalty terms such as "compte," "cagnoté," "prix déduit," "Prix payé en caisse," "Prix carte," or "Sans carte."
Follow the exact example structure strictly.
"deal_type" may only have the value "OTHER."
"deal" entries with "deal_type": "OTHER" cannot include values for "deal_maxPrice" or "deal_minPrice."
always check that the product name is not in the product description
Always check if you have a loyalty card
Check if you have filled in deal_conditions correctly


### check yourself 
- always check that the value without the card is recorded correctly and the value with the card is recorded correctly IMPORTANT
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "SALES_PRICE"
- IMPORTANT check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "REGULAR_PRICE"
- check in "price_type" must be only value "OTHER"
- "deal_type" in "main_format" must be "SALES_PRICE" AND "REGULAR_PRICE"
- crossed out prise always "REGULAR_PRICE"
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
### INCTRUCTIONS FOR GENERAL:

= The "product_name" must always have a value.
- Record "deal_pricebybaseunit" based only on exact formats like "<base-unit> = <price>" (e.g., "1 l = € 1.50").
- Include quantity (e.g., ml, l, g, kg) in "product_description."
- Correct any French grammar errors in the text, even if the original has mistakes.
- Use "Null" if there’s no data for "product_product_category."
- The "product_product_category" should follow Google product category style and be in French.
- "deal_loyaltycard" should be either "True" or "False"
- IMPORTANT if the offer contains a description of the age category (for example:"à partir de 3 ans", "Dès 3 ans" , "Dès 6 mois"), it must be written in deal_description 
- The "deal_description" is used to describe the terms of the deal, for example, "Offre valable sur le moins cher".  This information must be complete and recorded in the "deal_conditions"
- the full offer should be in the "deal_description" field (for example: "-50% sur le 2e:"), but then you do not need to duplicate it in deal_conditions and write only Null
- When there are two price types, one crossed out and one not crossed out, add the crossed out price to the "REGULAR_PRICE" transaction type of the crossed out price in a separate deal , and the not crossed out price to the "SALES_PRICE" type in a separate deal. 
- When there is only one type in the offer, this type is always REGULAR_PRICE but all prices must be in separate deals
- IMPORTANT to stock all prices even if they are repeated in deals.
- always each price must be in a separate deal with its own number (for example: "deal_1", "deal_2" , "deal_3" ).
- min and max prices are always the same
- IMPORTANT Only the text below the product_name is written to the product_description, other text is ignored
- "deal_frequency" always has the value "ONCE".
- If the text of the offer contains any type of quotation marks (for example: '„ “'), then they should be replaced with '\\\"'.
- IMPORTANT "type" can only have "SALES" or "BUNDLE". "BUNDLE" - only if there are two or more products in the offer at the same price.
- all parameters that are empty or "" should always be written as Null
- "is_product_family", "loyalty_card", "is_deal_family" can only have "true" or "false" values.
- IMPORTANT always write down the card availability value accurately
- The "deal_maxPrice" and "deal_minPrice" entry must always follow the format f"{value:.2f}".
- The "deal_maxPrice" and "deal_minPrice" prices should be the same in a particular deal.
- The "deal_maxPrice" and "deal_minPrice" must be recorded as a price per unit 
- "type" in additional_format can only have "SALES" by default.
- in "deal_pricebybaseunit" cannot contain value in the "deal_maxPrice" and "deal_minPrice"
- if "deal_description" and "deal_conditions" repead then you need record null in "deal_conditions"
- All null must be Null with capitalize first later
- if there is no loyalty card for the price, then deal_loyaltycard is always False
- IMPORTANT in "product_brand", "product_description" , "product_name" cannot have the same values
- currency always € not EUR
- deal_description (from exmaple: "-30% de remise immédiate") with discount record only in deal_type "SALES_PRICE"
- if "product_brand" and "product_name" identical  you need record in "product_brand" value "Null"
- always for each price it is necessary to create a new deal_1 deal_2 and so on
- If the text includes different prices for varying product sizes, create multiple "deal" entries for each size and price. Ensure each is in the complete JSON format.
- Set "deal_loyaltycard" to "True" if loyalty terms like "compte," "cagnoté," "prix déduit," or "Prix payé en caisse" appear.
- No JSON parameter value should repeat in another parameter.
- Follow the structure and details exactly as shown in the examples.
- "deal_type" should only be "REGULAR_PRICE" and "SALES_PRICE".
- If there are more than thirteen sizes, you need to check yourself and verify the exact number of sizes that are recorded in each deal
- There are cases when there is just a price (PRIX) and a price with a promo code (PRIX PROMO), then it is necessary to add PRIX to "REGULAR" and PRIX PROMO to "SALES".
- check if each size corresponds to each price and only when you are sure only then generate json
- Determine the total number of products in the image before you start processing, and make sure all products are included in the JSON, with separate deal_Ns for each."
- After processing all the products, check that all items are numbered from 1 to the total number of products in the image, without gaps.
- Ensure all items are individually recorded, even if they share similar or identical prices. Each item must be treated as a separate deal, with unique entries for each size or price, to account for every item individually.
- "Record only the prices explicitly stated in the text. Do not generate or estimate any prices not present in the source material. If a price is missing, set the value to 'Null' instead of creating a new price."
- that there can be more than 10 prices and you MUST write them all down in separate deal
- Specify the price per roll, set, or bag in the maxPrice and minPrice fields ( for example:"39€50","39€92") Record the price per square meter, cubic meter, or kilogram in the deal_pricebybaseunit field ( for example:"le m² 6€58","le m² 13€86").. Ensure each field contains the correct price information.
- Do not create separate deals for the price per kg, m² or m³. These prices should be recorded in the deal_pricebybaseunit field, not in separate transactions. Make sure that these prices are only listed in the deal_pricebybaseunit field and not duplicated in other fields or deals.
- If there are several deals with the deal_pricebybaseunit field filled in, create only those deals. If a deal has a Null deal_pricebybaseunit field, exclude it from the general list of deals if there are other deals with these fields filled in. However, if all deals have a Null deal_pricebybaseunit field, create all deals without exception.
- IMPORTANT: Never write the deal_pricebybaseunit value into maxPrice or minPrice. These fields are for the total product price, while deal_pricebybaseunit is strictly for unit-based pricing.
- Always count the exact number of prices, sizes and write everything in a separate deal
- Add sku number in product_sku with a slash /“sku”/“sku”/“sku”/ if there are any on the offer

### INCTRUCTIONS FOR discount:
- Do not record discounts (like -13%, -5€, 2ème à -50%) in any JSON parameter except the discount field.


### INCTRUCTIONS FOR product_description:

- IMPORTAN in product_description cannot feed values from deal_pricebybaseunit
- Avoid duplicating words from "product_name" in "product_description."
- "product_description" should not contain details related to "product_name" or "deal_pricebybaseunit."
- Text not assigned to specific parameters should go in "product_description."
- IMPORTANT price per unit of measurement (for example: Le kg : 6,67 €, l, 87 40mm) cannot be in product_description
- remove information about the diameter and degrees from product_description

### INCTRUCTIONS FOR deal_description:
- always record descriptions in  deal_description if it exist otherwise null
- this information ("Réduction excentrée 100-40","Coude male 87° 40","é égal femelle 87° 40") must be in deal_description
- in "deal_description" cannot contain price
- always ignored price in deal_description
- in deal_description need to record size "220 x 12 cm. Ep. 19mm" and so on
- always write the dimensions in the deal_description
- text must be same dimensions different (but not always)
- if not information write Null
- It is IMPORTANT to write only dimensions without unnecessary text
- exclude text "La valise 75 cm" in deal_description,  leave only 75 cm
- if there is a capacity (3 L, 10 L, 30 L) and a diameter (Ø 60x47 cm, Ø 80x66 cm, Ø 44x53 cm), then the capacity should be written and the diameter should be written in deal_deascription , output must be (3 L, Ø 60x47 cm)
- always if there are dimensions, specify them in each deal in deal_description


### INCTRUCTIONS FOR deal_conditions:
- if the condition always record in "deal_conditions" 
- in deal_conditions cannot contain price number only "l'unité" and so on
- information dont repeat in deal_description
- if not information write Null
- exclude text "le kg" shoud be write Null
- IMPORTANT, if there is no explicit condition, we do not write the text (“l'unité”) in deal_conditions, but write Null, we write it only when the text (“l'unité”) is explicitly specified, we write it in deal_conditions


### INCTRUCTIONS FOR deal_pricebybaseunit:
- In the deal_pricebybaseunit field, record the value 58,93 € le m. Ensure that this value is properly stored and displayed in the specified field.
- IMPORTANT ALWAYS if there is an offer with a filled deal_pricebybaseunit, then other deals that do not have a deal_pricebybaseunit should be excluded 

### Check yourself 
- IMPORTANT Always check all the prices on the offer and always put each price in a separate deal, except for prices per kilogram m2 m3
- Check if you accidentally wrote the price in a separate deal that should be in deal_pricebybaseunit
- check only in "deals" froms "additional_format" in "type" field should contain only the value  "SALES" not "SALES_PRICE"
- check in "price_type" must be only value "SALES_PRICE" or "REGULAR_PRICE" not "REGULAR"
- if there are many sizes, then you need to look at each of them carefully and write down each one and do not need to generate anything yourself
- spend a little more time, but check all the dimensions again and write them down carefully in separate deal
- you often miss some deals 
- always write down the age category if it is in the "deal_description" not "product_description"
- check that the price  (À partir de 35€) is excluded from the deal_description
- check that the full text record in  deal_description
- Check that the number of deals in the array is correct. Remember:
  A deal is defined as a unique combination of price and size.
  The price can repeat, but each size must be unique for that price.
  If the price is the same but the sizes are different, they should be counted as separate deals.
  Return the exact number of unique deals by checking both parameters: price and size.
- Check if text information is missing about (l'unité,le kg) then write  Null in deal_conditions
- Please note that if the prices are the same but have different sizes, they all need to be recorded in separate deals
- please note to whether there is a text ("l'unité") on the offer, if so, write it down in deal_conditionst
- always please note to whether you have recorded all possible options for recording in separate deals
- IMPORTANT: never miss offers with the same prices
- please make sure that the product_name and product_description are not repeated

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
