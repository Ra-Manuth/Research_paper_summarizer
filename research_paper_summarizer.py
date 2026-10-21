import os
import base64
from dotenv import load_dotenv
import fitz
from openai import OpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    images = []
    
    for page_num, page in enumerate(doc):
        text += page.get_text()
        
        for image_index, image in enumerate(page.get_images(full=True)):
            xref = image[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            image_filename = f"image_page_{page_num}_{image_index}.png"
            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            images.append(image_filename)
            
    return text, images

def chunk_text(text, chunk_size=3000, overlap=300):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def summarize_chunk(chunk):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "You summarize research papers into key insights, methods, and conclusions."
            },
            {
                "role": "user",
                "content": f"Summarize this research content:\n\n{chunk}"
            }
        ]
    )
    return response.choices[0].message.content

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this research figure and explain what insights it provides."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content

def process_paper(pdf_path):
    text, images = extract_pdf_content(pdf_path)
    
    print("Splitting text into chunks...")
    chunks = chunk_text(text)
    
    print("Summarizing text...")
    summaries = [summarize_chunk(chunk) for chunk in chunks]
    
    print("Analyzing images...")
    image_insights = [analyze_image(image) for image in images]
    
    final_summary = "\n\n".join(summaries)
    
    return {
        "text_summary": final_summary,
        "image_insights": image_insights
    }

def generate_final_report(results):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Create a structured research summary with sections: Overview, Methods, Key Findings, and Visual Insights."
            },
            {
                "role": "user",
                "content": f"Text Summary:\n{results['text_summary']}\n\nImage Insights:\n{results['image_insights']}"
            }
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    pdf_path = "attention_is_all_you_need.pdf"
    results = process_paper(pdf_path)
    report = generate_final_report(results)
    print("\nFinal Report:\n")
    print(report)
