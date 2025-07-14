from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai import LLMConfig, LLMExtractionStrategy # from crawl4ai.extraction_strategy import , LLMConfig
import asyncio
import json

# 1. Define your schema
class CVEntry(BaseModel):
    job_title: str = Field(..., description="Job Title")
    company: str = Field(..., description="Company Name")
    start_date: str = Field(..., description="Start Date")
    end_date: str = Field(..., description="End Date")
    description: str = Field(..., description="Job Description")

# 2. LLM Extraction Strategy
llm_config = LLMConfig(
    provider="openai",  # For OpenAI-compatible endpoints like llma
    base_url="http://localhost:8000/v1",
    api_token="sk-no-auth-needed"
)

extraction_strategy = LLMExtractionStrategy(
    llm_config=llm_config,
    schema=CVEntry.schema(),
    extraction_type="schema",
    instruction="Extract professional experience details for a CV."
)

# 3. Browser and crawler config
browser_cfg = BrowserConfig(headless=True)
run_config = CrawlerRunConfig(
    extraction_strategy=extraction_strategy
    # Do not include max_depth or concurrency here!
)

seed_urls = [
    "https://www.linkedin.com/in/target-person",
    "https://twitter.com/target_person",
    "https://meshackkinyua.com/target_person",
    "https://medium.com/@target_person"
]

# 4. Format function
def format_cv(entries):
    cv_md = "# Professional CV\n\n"
    for e in entries:
        if hasattr(e, "dict"):
            e = e.dict()
        cv_md += f"## {e['job_title']} at {e['company']}\n"
        cv_md += f"- **Duration:** {e['start_date']} – {e['end_date']}\n"
        cv_md += f"- **Description:** {e['description']}\n\n"
    return cv_md

# 5. Main async routine
async def main():
    results = []
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        for url in seed_urls:
            result = await crawler.arun(url=url, config=run_config)
            if result and result.success and result.extracted_content:
                try:
                    entries = json.loads(result.extracted_content)
                    if isinstance(entries, dict):
                        entries = [entries]
                    results.extend(entries)
                except Exception as e:
                    print(f"Error parsing extracted content from {url}: {e}")
            else:
                print(f"Crawl failed for {url}: {getattr(result, 'error_message', 'Unknown error')}")
    if results:
        cv_markdown = format_cv(results)
        with open("cv.md", "w") as f:
            f.write(cv_markdown)
        print("CV written to cv.md")
    else:
        print("No CV entries extracted.")

if __name__ == "__main__":
    asyncio.run(main())
