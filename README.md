# LinkedIn Post Generator

A Streamlit-based application that generates LinkedIn posts in multiple languages and styles using LLM few-shot learning. The app uses the Groq API to generate posts based on user-selected parameters like topic, length, and language.

## Features

- **Multiple Language Support**: Generate posts in English and Hinglish (Hindi-English mix)
- **Flexible Post Length**: Choose between Short (1-5 lines), Medium (6-10 lines), or Long (11-15 lines) posts
- **Topic Selection**: Select from a variety of topics automatically extracted from your data
- **Few-Shot Learning**: Uses example posts to maintain consistent writing style
- **Automated Data Preprocessing**: Cleans and enriches raw post data with metadata
- **Tag Unification**: Automatically unifies similar tags for consistency

## Project Structure

```
├── main.py              # Streamlit web application interface
├── post_generator.py    # Core post generation logic
├── few_shot.py          # Few-shot example management
├── preprocess.py        # Data preprocessing and cleaning
├── llm_helper.py        # LLM configuration and initialization
├── requirements.txt     # Python dependencies
└── data/
    ├── raw_posts.json       # Raw input data (create this)
    └── processed_posts.json # Processed data (auto-generated)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key

### Setup Steps

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd linkedin-post-generator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   Alternatively, for Streamlit, add your API key to `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

5. **Prepare your data**
   
   Create a `data` directory with `raw_posts.json` containing your LinkedIn posts:
   ```json
   [
     {
       "text": "Your LinkedIn post text here...",
       "tags": ["Career", "Tech"]
     },
     {
       "text": "Another post...",
       "tags": ["Job Search"]
     }
   ]
   ```

## Usage

### Step 1: Preprocess Your Data

Run the preprocessing script to clean and enrich your raw post data:

```bash
python preprocess.py
```

This will:
- Clean and validate all post text
- Extract metadata (line count, language, tags)
- Unify similar tags
- Generate `data/processed_posts.json`

### Step 2: Run the Web Application

Launch the Streamlit app:

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Step 3: Generate Posts

1. Select a **Topic** from the dropdown
2. Choose a **Length** (Short, Medium, or Long)
3. Pick a **Language** (English or Hinglish)
4. Click **Generate** to create a new LinkedIn post

## How It Works

### Data Pipeline

1. **Preprocessing** (`preprocess.py`):
   - Cleans corrupted text and Unicode errors
   - Extracts metadata using LLM (line count, language, tags)
   - Unifies similar tags for consistency

2. **Few-Shot Management** (`few_shot.py`):
   - Loads processed posts from JSON
   - Filters posts by length, language, and topic
   - Provides examples to the LLM for style consistency

3. **Post Generation** (`post_generator.py`):
   - Creates a prompt with user parameters
   - Includes 1-2 example posts for few-shot learning
   - Calls the Groq LLM to generate the post

4. **Web Interface** (`main.py`):
   - Provides user-friendly dropdown selectors
   - Handles errors gracefully
   - Displays generated posts

## Configuration

### Models

The app uses the **Llama 3.3 70B Versatile** model from Groq:
- High performance for content generation
- Good instruction following
- Supports multiple languages

To change the model, edit `llm_helper.py`:
```python
llm = ChatGroq(
    groq_api_key=st.secrets["GROQ_API_KEY"],
    model_name="your_model_name"  # Change here
)
```

### Post Length Categories

Edit the thresholds in `few_shot.py`:
```python
def categorize_length(self, line_count):
    if line_count < 5:
        return "Short"
    elif 5 <= line_count <= 10:
        return "Medium"
    else:
        return "Long"
```

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **python-dotenv**: Environment variable management
- **langchain**: LLM orchestration
- **langchain-groq**: Groq integration for LangChain
- **langchain-core**: Core LangChain utilities
- **groq**: Groq API client

## Troubleshooting

### Issue: "No posts found matching filters"
- **Solution**: Check that your `processed_posts.json` contains posts with the selected combination of length, language, and topic. Run preprocessing again.

### Issue: "GROQ_API_KEY not found"
- **Solution**: Ensure your API key is set in `.env` file or `.streamlit/secrets.toml`

### Issue: JSON parsing errors in preprocessing
- **Solution**: Verify your `raw_posts.json` is valid JSON. Use a JSON validator to check.

### Issue: Tag extraction gives unexpected results
- **Solution**: Ensure your raw posts have a `tags` field in the JSON structure

## API Requirements

You need a Groq API key to use this application:
1. Sign up at https://console.groq.com
2. Generate an API key
3. Add it to your `.env` or `.streamlit/secrets.toml` file

## Performance Tips

- **Caching**: Streamlit automatically caches the `FewShotPosts` initialization
- **Batch Processing**: For large datasets, preprocess in batches
- **API Rate Limits**: Groq has rate limits; add delays if processing many posts

## Future Enhancements

- [ ] Support for additional languages (Spanish, French, etc.)
- [ ] Custom post templates
- [ ] Post history and export functionality
- [ ] A/B testing different styles
- [ ] Integration with LinkedIn API for direct posting
- [ ] Advanced filtering by multiple topics
- [ ] User authentication and post management

## Notes

- The app requires internet connectivity for LLM API calls
- Generated posts are not automatically posted to LinkedIn; they're for review and manual posting

