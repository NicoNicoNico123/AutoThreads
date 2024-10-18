# Automate Threads

Automate Threads is a Python project that fetches trending topics from Google, generates tweets based on those topics, and automatically posts them to Threads, a social media platform. This project was built as a mini project for my portfolio and for fun, showcasing my skills in AI-powered content generation and integration with the Threads API for posting.

## Features

- AI-powered content generation based on trending topics
- Automatic posting to Threads
- Scheduled content generation and posting using Prefect
- Integration with SerpAPI for trending topics and news

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/automate-threads.git
   cd automate-threads
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   THREADS_ID=your_threads_id
   THREADS_ACCESS_TOKEN=your_threads_access_token
   SERPAPI_KEY=your_serpapi_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

### Threads API

To have access to the Threads API, please review this guide: https://developers.facebook.com/docs/threads

### Running the main script

To generate content and post it to Threads:

```
poetry run python threads/main.py
```

### Running the scheduled flow

To set up the scheduled flow using Prefect:

```
poetry run python threads/prefect/dailyflow.py
```

This will create a deployment that runs every 12 hours.

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
