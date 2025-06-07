# ai_generator.py

import openai

def generate_blog(keyword: str, seo_metrics: dict) -> dict:
    """
    1) Build the prompt string (as you already do).
    2) Call openai.chat.completions.create(...) with the prompt as a USER message.
    3) Extract the returned Markdown.
    4) Parse title / outline / content.
    5) Replace the {{AFF_LINK_n}} placeholders with dummy URLs.
    6) Return a dict containing title, outline, and final content.
    """
    # Build the prompt string
    prompt = build_prompt(keyword, seo_metrics)

    # Call OpenAI's chat completion endpoint (model gpt-3.5-turbo)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an experienced SEO blog writer."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )

    # Extract the raw Markdown text from the response
    raw = response.choices[0].message.content.strip()

    # Split the text into lines
    lines = raw.split("\n")

    # Assume the first line is "# Title", so strip off the "# "
    title_line = lines[0].strip()
    title = title_line.lstrip("# ").strip()

    # Reassemble the entire Markdown content
    content = "\n".join(lines)

    # Build an outline list by collecting every "## " heading
    outline = [line.lstrip("## ").strip() for line in lines if line.startswith("## ")]

    # Replace {{AFF_LINK_n}} placeholders with dummy URLs
    # (Assume GPT inserted at least 3 placeholders: AFF_LINK_1, AFF_LINK_2, AFF_LINK_3)
    dummy_urls = [
        "https://example.com/affiliate1",
        "https://example.com/affiliate2",
        "https://example.com/affiliate3"
    ]
    
    # Iterate placeholder indices 1..len(dummy_urls)
    content_with_links = content
    for i, url in enumerate(dummy_urls, start=1):
        placeholder = f"{{AFF_LINK_{i}}}"
        markdown_link = f"[Affiliate Link]({url})"      
        content_with_links = content_with_links.replace(placeholder, markdown_link)

    # Return a dictionary that your Flask route can jsonify
    return {
        "title": title,
        "outline": outline,
        "content": content_with_links
    }


def build_prompt(keyword: str, seo: dict) -> str:
    """
    Construct an English prompt that instructs the model to:
     1. Write a catchy Markdown-level-1 title (prefixed by "# ").
     2. Mention the SEO metrics (search volume, keyword difficulty, average CPC).
     3. Include at least three second-level headings ("## "), each with 2–3 paragraphs.
     4. Insert placeholders {{AFF_LINK_1}}, {{AFF_LINK_2}}, etc., at least three total.
     5. Conclude with a final paragraph.
     6. Output only the Markdown content (no extra commentary).
    """
    return f"""
Please act as an experienced SEO blog writer. Generate a draft blog post in Markdown about "{keyword}". Requirements:
1. The first line should be a catchy title, prefixed by "# ".
2. In the introduction paragraph, briefly mention these SEO metrics:
   - Search Volume: {seo['search_volume']}
   - Keyword Difficulty: {seo['keyword_difficulty']}
   - Average CPC: ${seo['avg_cpc']}
3. The body must include at least three second-level headings ("## "), each heading followed by 2–3 paragraphs of content.
4. Within each "## " section, insert at least one placeholder {{{{AFF_LINK_n}}}}. Total placeholders should be at least three, numbered consecutively ({{AFF_LINK_1}}, {{AFF_LINK_2}}, {{AFF_LINK_3}}, etc.).
5. Conclude with a final paragraph after all headings.
6. Output ONLY the blog post content in Markdown format. Do not include any explanation or commentary outside the post itself.
""".strip()
