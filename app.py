from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__)

# Load the model and tokenizer
model_name = "xju3/learning-wikitext-2-raw-1"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route("/generate", methods=["POST"])
def generate_response():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    response = generator(user_input, max_length=100, num_return_sequences=1)
    answer = response[0]["generated_text"]
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(port=5000, debug=True)