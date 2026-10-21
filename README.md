# Research Paper Summarizer

An AI-powered command-line tool that reads a research paper in PDF format and turns it into a clear, structured summary. It extracts the text **and** the figures from the paper, summarizes each part with OpenAI models, and combines everything into one final report.

Tested on the classic paper [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762).

## Features

- **PDF text extraction** with PyMuPDF
- **Figure extraction**: embedded images are pulled out of the PDF automatically
- **Chunked summarization**: long papers are split into overlapping chunks so nothing is cut off
- **Figure analysis**: a vision-capable model explains what each figure shows
- **Structured final report** with four sections: Overview, Methods, Key Findings, and Visual Insights

## How it works

```
PDF
 ├─► Extract text ──► Split into chunks ──► Summarize each chunk ─┐
 │                                                                ├─► Final structured report
 └─► Extract images ──► Analyze each image with a vision model ───┘
```

1. `extract_pdf_content` reads every page, collects the text, and saves embedded images as `image_page_<page>_<index>.png`.
2. `chunk_text` splits the text into chunks of 3,000 characters with a 300-character overlap.
3. `summarize_chunk` summarizes each chunk into key insights, methods, and conclusions.
4. `analyze_image` sends each extracted figure to the model and asks what insights it provides.
5. `generate_final_report` merges the text summaries and image insights into one report.

## Tech stack

- Python 3.9+
- [OpenAI API](https://platform.openai.com/) (`gpt-4o-mini`)
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF parsing
- [python-dotenv](https://pypi.org/project/python-dotenv/) for loading the API key

## Project structure

```
Research Paper Summarization/
├── research_paper_summarizer.py   # Main script
├── requirements.txt               # Python dependencies
├── .env                           # Your API key (never commit this file)
├── .gitignore
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/research-paper-summarizer.git
cd research-paper-summarizer
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:

```
openai
pymupdf
python-dotenv
```

### 4. Add your OpenAI API key

Create a file named `.env` in the project folder:

```
OPENAI_API_KEY=your_api_key_here
```

> **Warning:** Never upload your `.env` file to GitHub. Make sure `.env` is listed in `.gitignore`.

### 5. Add a PDF and run

Place your PDF in the project folder, then set its name in the last lines of `research_paper_summarizer.py`:

```python
pdf_path = "attention_is_all_you_need.pdf"
```

Run the script:

```bash
python research_paper_summarizer.py
```

## Example output

The script prints a report like this:

```
Splitting text into chunks...
Summarizing text...
Analyzing images...

Final Report:

Overview
...
Methods
...
Key Findings
...
Visual Insights
...
```

## Configuration

You can tune the behavior by editing these values in the script:

| Setting | Where | Default | Description |
| --- | --- | --- | --- |
| `chunk_size` | `chunk_text()` | `3000` | Characters per text chunk |
| `overlap` | `chunk_text()` | `300` | Characters shared between chunks |
| `model` | API calls | `gpt-4o-mini` | OpenAI model used for text and image analysis |
| `temperature` | `summarize_chunk()` | `0.3` | Lower values give more focused summaries |

## Notes and limitations

- Every text chunk and every extracted image is a separate API call, so **longer papers cost more** and take more time.
- Extracted images are saved in the project folder. Delete them after a run if you don't need them.
- Very small images, such as logos and icons, are also extracted and analyzed.
- Results depend on the quality of the PDF. Scanned PDFs without selectable text are not supported.

## Roadmap

- [ ] Accept the PDF path as a command-line argument
- [ ] Save the final report to a Markdown or PDF file
- [ ] Skip tiny images and save figures into a separate folder
- [ ] Add retry and error handling for API calls
- [ ] Simple web interface with Streamlit

## License

Add a license of your choice (for example, MIT) by creating a `LICENSE` file.

## Author

Built by **Nuth**, a Bachelor of FinTech student at ACLEDA University of Business, as a hands-on project in AI and data science.
