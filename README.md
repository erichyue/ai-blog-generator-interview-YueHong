# AI-Powered Blog Post Generator with Daily Automation

This project is a Flask application that, given a keyword, performs mock "SEO research" and then calls the OpenAI API to generate a draft blog post. It also includes a daily scheduler to automatically generate a new post for a predefined keyword once per day.

## Features

- **REST API**: A Flask endpoint to generate blog posts on demand.
- **AI Content Generation**: Integrates with OpenAI's `gpt-3.5-turbo` model to create unique, SEO-informed content.
- **Mock SEO Metrics**: A built-in module simulates fetching SEO data like `search volume`, `keyword difficulty`, and `average CPC` .
- **Structured Output**: The generated content is parsed into a structured JSON format, including a title, an outline, and the full content with placeholder affiliate links replaced.
- **Daily Automation**: Uses APScheduler to automatically run a job each day to generate a post for a predefined keyword and save it to a local file.

## Technologies Used

The project uses the following technologies and libraries:

- Flask
- OpenAI API
- APScheduler
- python-dotenv

## Project Structure

```
.
├── daily_posts/        # Directory where scheduled posts are saved
├── app.py              # Main Flask application, API endpoint, and scheduler setup
├── ai_generator.py     # Module for calling OpenAI and processing the response
├── seo_fetcher.py      # Module for mocking SEO metrics
├── requirements.txt    # Project dependencies
└── .env                # Environment variables (you must create this)
```

## Setup and Installation

### 1. Clone the Repository


```bash
git clone  https://github.com/erichyue/ai-blog-generator-interview-YueHong.git
cd ai-blog-generator-interview-YueHong
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.


```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all required packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Configuration

The application requires environment variables for configuration. Create a file named `.env` in the root of the project directory and add the following variables.

### 1. Create the `.env` file

```bash
touch .env
```

### 2. Add Environment Variables

Add your OpenAI API key to the `.env` file. You can optionally override the default settings for the daily scheduled job.

```txt
# OPENAI API KEY
OPENAI_API_KEY="sk-YourSecretOpenAIKey"

# the daily scheduler
DAILY_KEYWORD="wireless earbuds"
DAILY_HOUR=9
DAILY_MINUTE=30
```

- `OPENAI_API_KEY`: Secret API key from OpenAI.
- `DAILY_KEYWORD`: The default keyword for the daily automated post.
- `DAILY_HOUR`: The hour (0-23) when the daily job should run.
- `DAILY_MINUTE`: The minute (0-59) when the daily job should run.

## Running the Application

To start the Flask server and the background scheduler, run the `app.py` script:

```bash
python app.py
```

The application will start on `http://0.0.0.0:5001`. You will see a confirmation message that the APScheduler has also started.

```
APScheduler started: daily job at 09:30 for 'wireless earbuds'
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5001
Press CTRL+C to quit
```

## Usage

### API Endpoint

To generate a blog post, send a `GET` request to the `/generate` endpoint with a `keyword` query parameter.

#### Example Request with `curl`:

Bash

```bash
curl "http://localhost:5001/generate?keyword=blog+generate"
```

#### Example Success Response:

If successful, the API will return a `200 OK` status with a JSON object containing the keyword, SEO metrics, generated blog post, and a timestamp.

```JSON
{
  "avg_cpc": 2.43,
  "content": "# The Power of Blog Generation in SEO\n\nIn the world of SEO, understanding key metrics is crucial for achieving success. With a search volume of 17,103, a keyword difficulty of 78.12, and an average CPC of $2.43, optimizing your content for search engines is more important than ever.\n\n## Leveraging Blog Generation Tools\n\nCreating high-quality and relevant content is essential for improving your website's search engine rankings. One way to streamline this process is by using blog generation tools like {[Affiliate Link](https://example.com/affiliate1)}. These tools can help you generate blog posts quickly and efficiently, saving you time and effort while ensuring that your content is optimized for SEO.\n\nAnother benefit of using blog generation tools is the ability to generate a large volume of content on a consistent basis. By regularly publishing fresh and engaging blog posts, you can attract more traffic to your website and improve your search engine visibility over time.\n\n## Enhancing SEO Performance with Automated Content\n\nAutomated content generation tools like {[Affiliate Link](https://example.com/affiliate2)} can also help boost your SEO performance. These tools use advanced algorithms to create unique and relevant content based on your specified keywords and topics. By incorporating this content into your website, you can increase your chances of ranking higher in search engine results pages and driving more organic traffic to your site.\n\nFurthermore, automated content generation can help you target long-tail keywords and specific niches that may be difficult to address manually. By diversifying your content strategy with the help of these tools, you can reach a wider audience and improve your overall SEO performance.\n\n## Maximizing Results Through Content Optimization\n\nTo maximize the benefits of blog generation in SEO, it is essential to optimize the generated content for search engines. Tools like {[Affiliate Link](https://example.com/affiliate3)} can help you analyze and improve the SEO-friendliness of your blog posts, including keyword density, meta tags, and readability. By fine-tuning these elements, you can enhance your content's visibility and relevance to search engines, ultimately driving more organic traffic to your website.\n\nIn conclusion, leveraging blog generation tools and automated content creation can significantly enhance your SEO efforts. By consistently producing high-quality, optimized content, you can improve your search engine rankings, attract more organic traffic, and ultimately achieve your digital marketing goals.",
  "generated_at": "2025-06-07T05:59:54.168408Z",
  "keyword": "blog generate",
  "keyword_difficulty": 78.12,
  "outline": [
    "Leveraging Blog Generation Tools",
    "Enhancing SEO Performance with Automated Content",
    "Maximizing Results Through Content Optimization"
  ],
  "search_volume": 17103,
  "title": "The Power of Blog Generation in SEO"
}
```

## Daily Automation

The application includes a background scheduler that automatically generates one blog post per day.

- **Trigger**: The job runs at the time specified by `DAILY_HOUR` and `DAILY_MINUTE` in `.env` file.
- **Keyword**: It uses the keyword specified by `DAILY_KEYWORD`.
- **Output**: The generated JSON payload is saved to a file in the `daily_posts/` directory. The filename is formatted as `<keyword>_YYYYMMDD.json` (e.g., `wireless_earbuds_20250606.json`).
