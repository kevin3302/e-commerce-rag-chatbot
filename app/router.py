from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name="faq",
    utterances=[
        "What is your return policy?",
        "Can I return a product after purchase?",
        "How many days do I have to return an item?",
        "What should I do if I receive a defective product?",
        "Can I get a replacement for a damaged item?",
        "How long does a refund take?",
        "When will I receive my refund?",
        "How can I track my order?",
        "Where is my order?",
        "What payment methods do you accept?",
        "Can I pay using a credit card?",
        "Do you offer discounts on HDFC credit cards?",
        "Is cash on delivery available?",
        "Can I cancel my order after placing it?",
        "What is your shipping policy?"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "Show me Nike shoes with 50 percent discount",
        "I want Nike shoes on sale",
        "Find shoes under Rs. 3000",
        "Show me products between Rs. 2000 and Rs. 5000",
        "Do you have formal shoes in size 9?",
        "Show me Puma shoes in size 10",
        "Are there any Puma shoes on sale?",
        "What is the price of Puma running shoes?",
        "Show me black Adidas shoes",
        "Find running shoes under Rs. 4000",
        "Show me men's casual shoes",
        "Do you have women's sports shoes?",
        "Find discounted sneakers",
        "Show me the cheapest Nike shoes",
        "Which Puma shoes are available?"
    ]
)

router = SemanticRouter(routes=[faq, sql], encoder=encoder, auto_sync="local")
router.set_threshold(0.3)

if __name__ == "__main__":
    print(router("What is your policy on damaged products, any idea?").name)
    # print(router("Pink Puma shoes in price range 5000 to 1000").name)
    print(router("Show top 3 shoes in descending order of rating").name)