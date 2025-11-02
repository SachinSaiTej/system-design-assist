# System Design Assistant

AI-powered System Design Assistant that generates comprehensive, structured system design documents from user requirements.

## 🚀 Phase 1 MVP

This is the MVP implementation featuring:
- ✅ User input via Next.js frontend
- ✅ FastAPI backend with structured prompt building
- ✅ AI-powered design generation (OpenAI GPT-4)
- ✅ Beautiful Markdown rendering
- ✅ Modular, iteration-ready architecture

## 📁 Project Structure

```
system-design-assistant/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   │   └── design.py       # Design generation endpoint
│   ├── core/               # Core business logic
│   │   ├── prompt_builder.py  # Markdown prompt builder
│   │   └── ai_client.py     # AI client abstraction
│   ├── schemas/            # Pydantic models
│   │   └── design_schema.py
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt    # Python dependencies
│
└── system-design-web/      # Next.js frontend
    ├── src/
    │   ├── app/            # Next.js App Router
    │   │   ├── page.tsx    # Input page
    │   │   └── result/     # Result page
    │   └── components/      # React components
    │       ├── MarkdownRenderer.tsx
    │       └── LoadingSpinner.tsx
    └── package.json
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_MODEL=gpt-4
```

6. Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd system-design-web
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🎯 Usage

1. **Start both servers** (backend on port 8000, frontend on port 3000)

2. **Open the frontend** in your browser: `http://localhost:3000`

3. **Enter your system design requirement** in the textarea:
   - Example: "Design a URL shortener service like bit.ly that can handle 100 million URLs per day"

4. **Click "Generate System Design"**

5. **View the result** - A comprehensive system design document with:
   - Functional Requirements
   - Non-Functional Requirements
   - High-Level Architecture
   - Component Descriptions
   - Data Flow
   - Technology Stack Recommendations
   - Scalability & Trade-offs
   - Future Enhancements

## 🔧 API Endpoints

### POST `/api/design/generate`

Generate a system design document.

**Request:**
```json
{
  "user_input": "Design a distributed cache system"
}
```

**Response:**
```json
{
  "design_markdown": "# System Design: Distributed Cache\n\n## Functional Requirements\n..."
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "System Design Assistant API is running!"
}
```

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `OPENAI_MODEL` | OpenAI model to use | No | `gpt-4` |

## 🏗️ Architecture

### Backend

- **FastAPI**: Modern, fast web framework
- **Modular Structure**: Separated into API routes, core logic, and schemas
- **Prompt Builder**: Structured markdown prompt generation
- **AI Client**: Abstraction layer for LLM interactions

### Frontend

- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe development
- **TailwindCSS**: Modern styling
- **React Markdown**: Markdown rendering with syntax highlighting

## 🔄 Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend Development

```bash
cd system-design-web
npm run dev
```

## 📦 Dependencies

### Backend
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openai` - OpenAI API client
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

### Frontend
- `next` - React framework
- `react-markdown` - Markdown rendering
- `tailwindcss` - Styling
- `typescript` - Type safety

## 🚧 Future Enhancements (Phase 2+)

- [ ] RAG pipeline integration for context-aware responses
- [ ] Diagram generation (Mermaid/PlantUML)
- [ ] Design iteration and refinement
- [ ] Save/load design documents
- [ ] Export to PDF/Word
- [ ] Collaborative editing

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

