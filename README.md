# System Design Assistant

AI-powered System Design Assistant that generates comprehensive, structured system design documents from user requirements.

## 🚀 Phase 1 MVP

This is the MVP implementation featuring:
- ✅ User input via Next.js frontend
- ✅ FastAPI backend with structured prompt building
- ✅ AI-powered design generation (OpenAI GPT-4)
- ✅ Beautiful Markdown rendering
- ✅ Modular, iteration-ready architecture

## 🎯 Phase 2 - Interactive Refinement

Phase 2 adds powerful interactive features:
- ✅ **Interactive Chat Refinement** - Refine designs with natural language instructions
- ✅ **Section-Level Regeneration** - Regenerate individual sections with custom instructions
- ✅ **Mermaid Diagram Rendering** - Automatic rendering of Mermaid diagrams in markdown
- ✅ **Local Session Persistence** - Designs and history persist in localStorage
- ✅ **Design History** - View and restore previous versions of your design
- ✅ **Enhanced Markdown Support** - Full GFM support with syntax highlighting

## 📁 Project Structure

```
system-design-assistant/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   │   ├── design.py       # Design generation endpoint
│   │   ├── refine.py       # Design refinement endpoint (Phase 2)
│   │   └── section.py      # Section regeneration endpoint (Phase 2)
│   ├── core/               # Core business logic
│   │   ├── prompt_builder.py  # Markdown prompt builder
│   │   ├── ai_client.py     # AI client abstraction
│   │   └── context_manager.py # Session context management (Phase 2)
│   ├── schemas/            # Pydantic models
│   │   ├── design_schema.py
│   │   ├── refine_schema.py  # Phase 2
│   │   └── section_schema.py # Phase 2
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt    # Python dependencies
│
└── system-design-web/      # Next.js frontend
    ├── src/
    │   ├── app/            # Next.js App Router
    │   │   ├── page.tsx    # Input page
    │   │   └── result/     # Result page (Phase 2 enhanced)
    │   ├── components/     # React components
    │   │   ├── MarkdownRenderer.tsx  # Enhanced with Mermaid (Phase 2)
    │   │   ├── LoadingSpinner.tsx
    │   │   ├── ChatPanel.tsx        # Phase 2
    │   │   ├── SectionViewer.tsx    # Phase 2
    │   │   ├── HistoryPanel.tsx     # Phase 2
    │   │   └── MermaidRenderer.tsx   # Phase 2
    │   └── store/          # State management
    │       └── designStore.ts       # Zustand store with persistence (Phase 2)
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

### Phase 2: Interactive Refinement Mode

After generating a design, you can:

1. **Refine the Design** (Chat Tab):
   - Enter natural language instructions to improve or modify the design
   - Examples: "Add caching layer", "Improve scalability section", "Add more details to architecture"
   - The AI will update relevant sections while maintaining document structure

2. **Regenerate Sections** (Sections Tab):
   - View all document sections (H1 and H2 headings)
   - Click "Regenerate" on any section with optional custom instructions
   - Individual sections are updated independently

3. **View History** (History Tab):
   - See all previous versions of your design
   - Restore any previous version with one click
   - Track what changes were made with instruction history

4. **Mermaid Diagrams**:
   - Design documents can include Mermaid diagrams
   - Diagrams are automatically rendered when marked with ```mermaid code blocks
   - Supports flowcharts, sequence diagrams, and more

5. **Local Persistence**:
   - Your current design and history are saved to localStorage
   - Refresh the page without losing your work
   - Works across browser sessions

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

### POST `/api/refine` (Phase 2)

Refine an existing design document.

**Request:**
```json
{
  "previous_design": "# System Design...",
  "instruction": "Add caching layer with Redis",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "refined_design": "# System Design...",
  "session_id": "session-uuid"
}
```

### POST `/api/section` (Phase 2)

Regenerate a specific section of a design.

**Request:**
```json
{
  "previous_design": "# System Design...",
  "section_name": "High-Level Architecture",
  "instruction": "Add more details about load balancing",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "updated_design": "# System Design...",
  "regenerated_section": "## High-Level Architecture\n...",
  "session_id": "session-uuid"
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
- `remark-gfm` - GitHub Flavored Markdown support (Phase 2)
- `mermaid` - Diagram rendering (Phase 2)
- `zustand` - State management with persistence (Phase 2)
- `tailwindcss` - Styling
- `typescript` - Type safety

## ✅ Phase 2 Completed Features

- [x] Interactive chat-based refinement
- [x] Section-level regeneration
- [x] Mermaid diagram rendering
- [x] Local session persistence
- [x] Design history tracking
- [x] Enhanced markdown support (GFM)

## 🚧 Future Enhancements (Phase 3+)

- [ ] RAG pipeline integration for context-aware responses
- [ ] Export to PDF/Word
- [ ] Collaborative editing
- [ ] Version comparison/diff view
- [ ] Template library
- [ ] Multi-language support

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

