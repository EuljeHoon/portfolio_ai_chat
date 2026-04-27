# Jehoon Portfolio AI Backend
![Chatbot demo](README_image/chat_bot_image.png)

This project is Chatbot backend for my portfolio website.  
This AI system works without **vector DB/embedding**, chooses JSON chunks based on the rules and deliver it to Gemini API(`Gemini 2.5 flash lite`).

## API endpoint

- `POST /api/chat/`
- example prompt:

```json
{
  "message": "What are the Jehoon's experiences?"
}
```

- exmaple response:

```json
{
  "answer": "Jehoon has experience in software engineering, data analysis, and network administration.

- Developed and enhanced AI-driven platforms for complex scientific analysis, including protein structure prediction and data processing.
- Managed and optimized web application development, focusing on state management, API integration, and secure authentication.
- Gained practical experience in network operations, including configuration, security, and maintenance of tactical communication systems.
- Contributed to improving system performance and data throughput through efficient coding practices and parallel processing."
}
```
![Chatbot demo](README_image/response.png)

## How this AI works?

1. Client send `message`to `POST /api/chat/`
2. `chat()` in `chat/views.py` evaluates the input and call `ask_ai(message)`
3. Load `portfolio_chunks.json` from `chat/services.py`
4. Classify the question into 5+ categories (`about`, `experience`, `projects`, `skills`, `general`, ...)
5. Select chunk(/chat/data/portfolio_chunks.json):
   - If question includes some message like `title`/`company`choose that chunk first
   - If not choose the chunk that match the `section`
   - If the category result turned out`general`, use all th chunks
6. Combined selected chunks into `context` string and create Gemini prompt
7. Call Gemini(`gemini-2.5-flash-lite`) and create response
8. Work on the formatting(Remove useless markdown, bullets) and return the response

## Important Point

- This is not **semantic vector search**
- The logic is:
  - String category matching(`title`, `company`, ...)
  - Filtering based on the category(`section`)
- I chose this way because since dataset is small, it will be easier to operate.

## Cache/Performance Strategy

- Caching category classification results: 1 hour (`ai_class_<hash>`)
- Caching final response: 1 hour (`ai_answer_<hash>`)
- Try exponential backoff on Gemini 429(maximum 3 times)
- Apply user throttle for too many requests  (`30/min` default)

## Data Sources

- Chunk file: `chat/data/portfolio_chunks.json`
- Key fields(expect): `section`, `title`, `company`, `content`

## Environment Variables

- `GEMINI_API_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CORS_ALLOWED_ORIGINS`
- `DRF_ANON_THROTTLE_RATE`

## Deployment

The application is deployed on Render.

🔗 Live URL: https://portfolio-ai-chat.onrender.com
### Notes on Performance

The application is currently hosted on Render’s free tier. As a result, the first request may experience slower response times due to cold-start latency when the service has been idle.

Additionally, the system uses a RAG (Retrieval-Augmented Generation) pipeline, which involves external API calls (e.g., LLM and retrieval services), contributing further to overall response time.

## Future development idea

- `Embedding + Vector` Search(managed vector DB)
- Integrate `Redis` to implement more efficient caching.

## Link to frontend repository
Link: https://github.com/EuljeHoon/jehoon_website
