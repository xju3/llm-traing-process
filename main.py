from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Check if MPS is available
device = "mps" if torch.backends.mps.is_available() else "cpu"
# Initialize the model and tokenizer
model_name = "xju3/learning-wikitext-2-raw-1"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, token="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", device=0 if device == "mps" else -1)

app = FastAPI()

# Define request and response models
class GenerateRequest(BaseModel):
    prompt: str
    max_length: int = 100

class GenerateResponse(BaseModel):
    generated_text: str
    
@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    try:
        # Use pipeline to generate text
        output = generator(request.prompt, max_length=request.max_length, num_return_sequences=1)
        return GenerateResponse(generated_text=output[0]["generated_text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with: uvicorn main:app --reload
