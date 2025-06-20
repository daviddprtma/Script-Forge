
<br/>
<div align="center">

<h3 align="center">(WINNER #3 for Hack Another Day - Quira Agents🎉🎉)Script Forge™️</h3>

<p align="center">
A multiple AI agents to research, create, and get summary for the video scripts from social media📱

</p>
</div>

## If you want to check the announcement for the list of the winner, go check it out in here [Hack Another Day - Quira Agents](https://quira.sh/quests/creator/submissions?questId=25)

## About The Project

Script Forge is the multi agent video content planner to research, create, and polish video scripts from social media. The system primary employs on evaluation to ensure high quality and engaging content.

## Features
- **Multi-Agent Architecture**
  - ResearchAgent: Plans and conducts topic research
  - ScriptWriterAgent: Creates initial video scripts
  - PolishingAgent: Enhances scripts for engagement
  - EvaluatorAgent: Assesses quality and provides feedback

- **Advanced Content Research**
  - Dynamic search query generation
  - Web content extraction and processing
  - ChromaDB-based vector storage for semantic search
  - URL deduplication and content filtering

- **Intelligent Script Generation**
  - Platform-specific formatting (TikTok, YouTube Shorts, Instagram Reels)
  - Automatic timestamp generation
  - Engaging transitions and hooks
  - Visual suggestions and hashtag generation

- **Quality Assurance**
  - Automated evaluation of research quality
  - Script engagement scoring
  - Improvement suggestions
  - Multiple retry attempts for low-scoring outputs

### Built With

- [Python](https://www.python.org/)
- [Deepseek ](https://www.deepseek.com/)
- [SerpApi](https://serpapi.com/)
### Installation

1. Get the API Key from Deepseek API [DeepSeek API](https://api-docs.deepseek.com/) & SerpAPI [SerpAPI](https://serpapi.com/)
2. Clone this repo
   ```sh
   git clone https://github.com/daviddprtma/Script-Forge.git 
   ```
 ```sh
cd Script-Forge
   ```
3. Create & activate a virtual env:
   ```sh
   python -m venv venv 
   ```
```sh
source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependecies
   ```sh
   pip install -r requirements.txt
   ```
5. Create .env file with your API Keys: 
   ```sh
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

```sh
   SERPAPI_KEY=your_serpapi_key

   ```
## Usage

1. Run the script: 
   ```sh
   python deepseek_agent.py
   ```

2. Follow the interactive prompts to specify:
   - Video format (TikTok, YouTube Short, Instagram Reel)
   - Video length
   - Number of questions/items
   - Topic
   - Number of URLs per search query
   - Number of search terms


3. The system will generate:
   - Research data
   - Initial script
   - Polished script
   - Evaluation reports
   - Human-readable output


## Output Structure

```
output/
├── [Topic]_[Timestamp]/
│   ├── debug/
│   │   └── (Debug logs and raw API responses)
│   ├── research/
│   │   └── (Research data and evaluations)
│   ├── script/
│   │   └── (Initial and polished scripts)
│   ├── evaluation/
│   │   └── (Evaluation reports)
│   ├── final_script.json
│   └── final_script.txt
```

## Video Presentation
For the video presentation, see it in below⬇️
<br>
<br>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/149zpF3VLHE/0.jpg)](https://www.youtube.com/watch?v=149zpF3VLHE)
