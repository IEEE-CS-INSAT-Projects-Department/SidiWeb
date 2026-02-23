# SidiWeb AI - Week 2 Implementation

## ✅ Completed Tasks (Semaine 2)

### 1. Implémentation Chaîne

#### Created `chains/recommendation_chain.py` ✅

- **RecommendationChain** class implementing the full LangChain pipeline
- Uses `ChatPromptTemplate` to structure the prompt
- Integrates OpenAI GPT-3.5-turbo LLM
- Supports both synchronous (`invoke`) and asynchronous (`ainvoke`) execution
- Loads design system from JSON
- Validates API key from environment variables

**Key Features:**

- Dynamic prompt injection with user inputs (sector, style, preferences)
- Design system integration via JSON loading
- Error handling and validation
- Factory function `create_recommendation_chain()` for easy instantiation

### 2. Schéma de Sortie

#### Created `models/output_models.py` ✅

**Pydantic Models Defined:**

1. **`RecommendationOutput`** (as specified in PDF):

   ```python
   class RecommendationOutput(BaseModel):
       templates: List[str]  # IDs
       colors: List[str]     # HEX
       fonts: Dict[str, str] # heading/body
   ```

2. **`DetailedRecommendationOutput`** (extended version with reasoning):
   - `recommended_templates`: List of templates with explanations
   - `recommended_palette`: Palette with reasoning
   - `recommended_fonts`: Font pairing with reasoning

3. Supporting models:
   - `TemplateRecommendation`
   - `PaletteRecommendation`
   - `FontRecommendation`

#### JsonOutputParser Integration ✅

- Used `JsonOutputParser(pydantic_object=DetailedRecommendationOutput)`
- Ensures structured JSON output from LLM
- Automatic validation against Pydantic schema

### 3. Testing avec Inputs Simulés

#### Created `test_recommendation_chain.py` ✅

**Test Scenarios:**

1. Education + Modern (simple, professional, accessible)
2. Business + Corporate (professional, trustworthy, clean)
3. Portfolio + Creative (bold, artistic, unique)
4. E-commerce + Modern (user-friendly, conversion-focused)
5. Portfolio + Minimal (no specific preferences)

**Features:**

- Formatted output display
- Error handling
- API key validation check
- Multiple test scenarios as specified

### 4. Design System

#### Created `data/design_system.json` ✅

**Content:**

- **9 Templates** covering education, business, portfolio, ecommerce, saas, healthcare
- **9 Color Palettes** with HEX codes mapped to sectors
- **6 Font Pairings** for different styles (modern, minimal, classic, corporate, creative)

Each entry includes:

- Unique ID
- Sector/style mapping
- Description
- Relevant metadata

## 📦 Project Structure

```
sidiweb-workspace/
├── .env                          # OpenAI API key configuration
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── data/
│   ├── design_system.json        # ✅ Design system data
│   ├── backend_templates/
│   └── design_notes/
├── prompts/
│   ├── initial_prompt.txt        # Base LLM prompt
│   └── variables.py              # Input variable definitions
└── src/
    ├── __init__.py
    ├── chains/
    │   ├── __init__.py
    │   └── recommendation_chain.py  # ✅ Main chain implementation
    ├── models/
    │   ├── __init__.py
    │   └── output_models.py         # ✅ Pydantic models
    └── test_recommendation_chain.py # ✅ Test script
```

## 🚀 How to Run

### 1. Configure API Key

Edit `.env` file:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

```bash
cd src
python test_recommendation_chain.py
```

## 📝 Usage Example

```python
from chains.recommendation_chain import create_recommendation_chain

# Create the chain
chain = create_recommendation_chain()

# Get recommendations
result = chain.invoke(
    sector="education",
    style="modern",
    preferences="simple, professional, accessible"
)

# Result contains:
# - recommended_templates: List of template objects with IDs and reasons
# - recommended_palette: Palette object with ID and reason
# - recommended_fonts: Font object with heading, body, and reason
```

## 🔧 Technical Stack

- **LangChain 0.1.0** - Framework for LLM applications
- **OpenAI GPT-3.5-turbo** - Language model
- **Pydantic 2.5.3** - Data validation and schema definition
- **Python 3.11+** - Programming language

## ✨ Key Features Implemented

✅ ChatPromptTemplate integration  
✅ OpenAI LLM (GPT-3.5-turbo) integration  
✅ Pydantic models for structured output  
✅ JsonOutputParser for JSON validation  
✅ Design system JSON loading  
✅ Comprehensive error handling  
✅ Multiple test scenarios  
✅ Async support (ainvoke method)

## 📋 Next Steps (Semaine 3+)

- Integrate with backend API
- Add more sophisticated template matching logic
- Implement caching for improved performance
- Add user feedback loop
- Create web interface
- Add logging and monitoring

## 🤝 Integration Points

The recommendation chain can be easily integrated into:

- Flask/FastAPI backend endpoints
- Streamlit dashboard
- CLI tool
- Jupyter notebooks for experimentation

## 📖 Reference

Based on project specifications from SidiWeb.pdf (Semaine 2):

- ✅ Créer chains/recommendation_chain.py
- ✅ Utiliser ChatPromptTemplate
- ✅ Intégrer LLM (OpenAI GPT-3.5-turbo)
- ✅ Tester avec inputs simulés
- ✅ Définir Pydantic model (RecommendationOutput)
- ✅ Utiliser JsonOutputParser
