from openai import OpenAI
from termcolor import colored
import os
import re
import json
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
from smolagents import Tool, CodeAgent, DuckDuckGoSearchTool
import chromadb
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sentence_transformers import SentenceTransformer
import uuid
import time

def print_step(message: str) -> None:
    """Print a step in the process with color."""
    print(colored(f"[STEP] {message}", "cyan"))

def print_error(message: str, error: Exception = None) -> None:
    """Print an error message with color."""
    error_msg = f"[ERROR] {message}"
    if error:
        error_msg += f": {str(error)}"
    print(colored(error_msg, "red"))

def print_success(message: str) -> None:
    """Print a success message with color."""
    print(colored(f"[SUCCESS] {message}", "green"))

def create_output_folder(topic: str) -> str:
    """Create a timestamped output folder for the topic."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"output/{topic.replace(' ', '_')}_{timestamp}"
    
    # Create main output folder
    os.makedirs(folder_name, exist_ok=True)
    
    # Create subdirectories for different types of output
    os.makedirs(os.path.join(folder_name, "debug"), exist_ok=True)
    os.makedirs(os.path.join(folder_name, "research"), exist_ok=True)
    os.makedirs(os.path.join(folder_name, "script"), exist_ok=True)
    os.makedirs(os.path.join(folder_name, "evaluation"), exist_ok=True)
    
    print_step(f"Created output folder structure: {folder_name}")
    return folder_name

def save_debug_file(output_folder: str, content: str, filename: str) -> None:
    """Safely save debug content to a file."""
    try:
        debug_path = os.path.join(output_folder, "debug", filename)
        os.makedirs(os.path.dirname(debug_path), exist_ok=True)
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print_error(f"Failed to save debug file {filename}: {e}")

# Load environment variables
try:
    load_dotenv()
    print_step("Loaded environment variables from .env file")
except Exception as e:
    print_error("Failed to load .env file", e)

# Constants
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class ContentRetrieverTool:
    """Tool for retrieving and managing content."""
    def __init__(self, output_folder: str = None, urls_per_query: int = 3):
        self.output_folder = output_folder
        self.urls_per_query = urls_per_query
        self.search_results = []
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        if not SERPAPI_KEY:
            raise ValueError("SERPAPI_KEY not found in environment variables")
        
        # Initialize ChromaDB
        if output_folder:
            chroma_path = os.path.join(output_folder, "chroma_db")
            self.client = chromadb.PersistentClient(path=chroma_path)
        else:
            self.client = chromadb.Client()
            
        self.collection = self.client.create_collection(
            name="content_store",
            metadata={"hnsw:space": "cosine"}
        )

    def search_with_retry(self, query: str, max_retries: int = 3, delay: int = 2) -> List[Dict]:
        """Execute search with retries using SerpAPI."""
        from serpapi import GoogleSearch
        import time
        
        for attempt in range(max_retries):
            try:
                search = GoogleSearch({
                    "q": query,
                    "api_key": SERPAPI_KEY,
                    "num": self.urls_per_query * 2  # Get extra results in case some URLs fail
                })
                results = search.get_dict()
                
                if "organic_results" not in results:
                    raise ValueError("No organic results found in SerpAPI response")
                    
                return results["organic_results"]
                
            except Exception as e:
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    print_error(f"Search attempt {attempt + 1} failed: {e}")
                    print_step(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    raise  # Re-raise the last exception

    def gather_content_with_queries(self, search_queries: List[str]):
        """Execute multiple search queries and gather content."""
        print_step(f"Gathering content using {len(search_queries)} search queries...")
        
        # Track processed URLs to avoid duplicates
        processed_urls = set()
        
        for query in search_queries:
            print_step(f"Searching: {query}")
            try:
                # Remove quotes from query
                clean_query = query.strip('"').strip("'")
                
                # Use SerpAPI to search with retries
                search_results = self.search_with_retry(clean_query)
                print_step(f"Got {len(search_results)} search results")
                
                # Process each result
                processed_count = 0
                for result in search_results:
                    if processed_count >= self.urls_per_query:
                        break
                        
                    url = result.get("link")
                    if not url or url in processed_urls:  # Skip if URL already processed
                        continue
                        
                    try:
                        print_step(f"Fetching content from: {url}")
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        response = requests.get(url, headers=headers, timeout=10)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Remove script and style elements
                        for element in soup(["script", "style"]):
                            element.decompose()
                        
                        # Extract text content from paragraphs and headers
                        paragraphs = []
                        for elem in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                            text = elem.get_text().strip()
                            if text and len(text) > 20:  # Only keep substantial paragraphs
                                paragraphs.append(text)
                        
                        if not paragraphs:
                            print_error(f"No substantial content found at {url}")
                            continue
                            
                        text = '\n\n'.join(paragraphs)
                        print_step(f"Extracted {len(text)} characters of content")
                        
                        if text:  # Only add if we got some content
                            # Add to ChromaDB
                            embedding = self.encoder.encode(text).tolist()
                            self.collection.add(
                                documents=[text],
                                embeddings=[embedding],
                                metadatas=[{
                                    "source": url,
                                    "query": clean_query,
                                    "title": result.get("title", ""),
                                    "snippet": result.get("snippet", "")
                                }],
                                ids=[str(uuid.uuid4())]
                            )
                            
                            # Save raw content
                            self.search_results.append({
                                "query": query,
                                "url": url,
                                "title": result.get("title", ""),
                                "snippet": result.get("snippet", ""),
                                "content": text,
                                "length": len(text)
                            })
                            processed_urls.add(url)  # Add URL to processed set
                            print_success(f"Successfully processed URL: {url}")
                            processed_count += 1
                            
                    except requests.exceptions.RequestException as e:
                        print_error(f"Failed to fetch URL {url}: {e}")
                        continue
                    except Exception as e:
                        print_error(f"Failed to process URL {url}: {e}")
                        continue
                        
            except Exception as e:
                print_error(f"Search failed for query '{query}': {e}")
                continue
        
        # Save search results
        if self.output_folder:
            results_file = os.path.join(self.output_folder, "search_results.json")
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(self.search_results, f, indent=2)
            print_step(f"Saved {len(self.search_results)} search results to {results_file}")
        
        print_success("Content gathering completed")

    def forward(self, query: str) -> str:
        """Retrieve relevant content based on the query."""
        try:
            assert isinstance(query, str), "Your search query must be a string"
            
            # Generate query embedding
            query_embedding = self.encoder.encode(query)
            
            # Query the vector store
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=20  # Get enough context
            )
            
            # Format results as text
            formatted_results = "\nRetrieved documents:\n" + "".join(
                [
                    f"\n\n===== Document {str(i)} (Source: {results['metadatas'][0][i]['source']}) =====\n" + doc
                    for i, doc in enumerate(results['documents'][0])
                ]
            )
            
            # Save query results if output folder exists
            if self.output_folder:
                query_results = {
                    "query": query,
                    "results": [
                        {
                            "content": doc,
                            "metadata": meta,
                            "distance": dist  # Add distance score
                        }
                        for doc, meta, dist in zip(
                            results['documents'][0], 
                            results['metadatas'][0],
                            results['distances'][0] if 'distances' in results else [0] * len(results['documents'][0])
                        )
                    ]
                }
                
                # Test JSON serialization
                json.dumps(query_results)
                
                query_file = os.path.join(self.output_folder, "query_results.json")
                with open(query_file, "w", encoding="utf-8") as f:
                    json.dump(query_results, f, indent=2)
            
            return formatted_results
            
        except json.JSONDecodeError as e:
            print_error(f"Failed to create query results JSON: {e}")
            return "Error: Failed to process search results"
        except Exception as e:
            print_error(f"Search failed: {e}")
            return f"Error during search: {str(e)}"

class BaseAgent:
    """Base class for all agents with common functionality."""
    def __init__(self, output_folder: str):
        try:
            if not DEEPSEEK_API_KEY:
                raise ValueError("DEEPSEEK_API_KEY not found in .env file")
            
            self.client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL
            )
            self.output_folder = output_folder
            
        except Exception as e:
            print_error(f"Failed to initialize {self.__class__.__name__}", e)
            raise

    def save_output(self, data: Any, filename: str):
        """Save output data to a file."""
        if self.output_folder:
            try:
                # Determine appropriate subdirectory based on filename or class type
                if isinstance(self, ResearchAgent) or "research" in filename.lower():
                    subdir = "research"
                elif isinstance(self, ScriptWriterAgent) or "script" in filename.lower():
                    subdir = "script"
                elif isinstance(self, EvaluatorAgent) or "eval" in filename.lower():
                    subdir = "evaluation"
                else:
                    subdir = "debug"
                
                file_path = os.path.join(self.output_folder, subdir, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    if isinstance(data, (dict, list)):
                        json.dump(data, f, indent=2)
                    else:
                        f.write(str(data))
            except Exception as e:
                print_error(f"Failed to save output file {filename}: {e}")

    def get_response(self, messages: List[Dict[str, str]], save_as: str = None) -> str:
        """Get response from Deepseek API with debugging."""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages
            )
            
            content = response.choices[0].message.content
            print_step(f"Raw API Response:\n{content}")
            
            if save_as and self.output_folder:
                save_debug_file(self.output_folder, content, save_as)
            
            return content
            
        except Exception as e:
            print_error(f"API call failed: {e}")
            return ""

    def clean_json_response(self, response: str) -> str:
        """Clean JSON response by removing markdown code blocks and other non-JSON content."""
        try:
            # Remove markdown code block markers
            response = re.sub(r'```json\s*', '', response)
            response = re.sub(r'```\s*', '', response)
            response = response.strip()
            
            # Find the first { and last }
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError(f"No valid JSON object found in response: {response}")
                
            # Extract just the JSON part
            json_str = response[start_idx:end_idx + 1]
            
            # Test if it's valid JSON
            json.loads(json_str)  # This will raise JSONDecodeError if invalid
            
            return json_str
            
        except Exception as e:
            print_error(f"Failed to clean JSON response: {e}")
            print_error("Raw response:", response)
            raise

class ResearchAgent(BaseAgent):
    """Agent responsible for research planning and execution."""
    def __init__(self, output_folder: str, urls_per_query: int = 3):
        super().__init__(output_folder)
        self.urls_per_query = urls_per_query
        self.retriever_tool = ContentRetrieverTool(output_folder=output_folder, urls_per_query=urls_per_query)

    def plan_research(self, topic: str, max_queries: int) -> List[str]:
        """Plan research queries based on topic and video requirements."""
        prompt = f"""
        As a research expert, create EXACTLY {max_queries} focused search queries to gather comprehensive information about {topic}.
        
        Requirements:
        - Generate EXACTLY {max_queries} queries, no more, no less
        - Each query should target a different aspect of the topic
        - Keep queries short (4-6 words) and specific
        - Include a mix of factual, historical, and engaging content
        - Focus on information that would be interesting in a video
        - Avoid redundant or overlapping queries
        
        Format:
        - Return EXACTLY {max_queries} queries, one per line
        - Do not include numbering or bullet points
        - Do not include quotes or special characters
        - Do not include any other text or explanations
        
        Example output format (if {max_queries} were 3):
        topic history origins background
        topic major achievements milestones
        topic interesting unknown facts
        """
        
        response = self.get_response(
            messages=[
                {
                    "role": "system", 
                    "content": f"You are a research planning expert. Generate EXACTLY {max_queries} focused search queries that will yield comprehensive and engaging video content. No more, no less. Return ONLY the queries, one per line, with no additional text."
                },
                {"role": "user", "content": prompt}
            ],
            save_as="research_queries.txt"
        )
        
        # Clean up queries
        queries = [
            q.strip().strip('"').strip("'")  # Remove quotes and whitespace
            for q in response.strip().split("\n")
            if q.strip() and not q.startswith(('-', '*', '•', '1.', '2.'))  # Remove any list markers
        ]
        
        # Replace generic "topic" with actual topic in queries
        queries = [q.replace("topic", topic) for q in queries]
        
        # Verify we have exactly the requested number of queries
        if len(queries) < max_queries:
            print_error(f"LLM returned fewer queries ({len(queries)}) than requested ({max_queries})")
            # Generate additional queries by appending numbered variations
            base_queries = [
                f"{topic} history background formation",
                f"{topic} major achievements milestones",
                f"{topic} interesting facts trivia",
                f"{topic} cultural impact influence",
                f"{topic} recent developments news",
                f"{topic} unique characteristics features",
                f"{topic} notable events moments",
                f"{topic} public reception reviews",
                f"{topic} behind the scenes stories",
                f"{topic} legacy lasting impact"
            ]
            while len(queries) < max_queries and len(queries) < len(base_queries):
                queries.append(base_queries[len(queries)])
            
            # If we still need more queries, add numbered variations
            while len(queries) < max_queries:
                base_query = f"{topic} facts details part {len(queries) + 1}"
                queries.append(base_query)
                
        elif len(queries) > max_queries:
            print_error(f"LLM returned more queries ({len(queries)}) than requested ({max_queries})")
            queries = queries[:max_queries]
        
        # Save for review
        self.save_output({
            "topic": topic,
            "requested_queries": max_queries,
            "actual_queries": len(queries),
            "generated_queries": queries,
            "raw_response": response
        }, "research_queries.json")
        
        return queries

    def execute_research(self, topic: str, params: Dict) -> Dict:
        """Execute research plan and gather information."""
        try:
            print_step("Planning research queries...")
            search_queries = self.plan_research(topic, params['search_terms'])
            
            print_step("Executing research plan...")
            self.retriever_tool.gather_content_with_queries(search_queries)
            research_data = self.retriever_tool.forward(topic)
            
            research_output = {
                "raw_data": research_data,
                "queries_used": search_queries,
                "urls_per_query": self.urls_per_query,
                "total_queries": len(search_queries)
            }
            
            # Ensure the output is valid JSON
            json.dumps(research_output)  # Test serialization
            
            self.save_output(research_output, "research_output.json")
            return research_output
        except json.JSONDecodeError as e:
            print_error(f"Failed to create valid research output JSON: {e}")
            # Return a basic valid structure
            return {
                "raw_data": "Error: Failed to gather research data",
                "queries_used": search_queries if 'search_queries' in locals() else [],
                "urls_per_query": self.urls_per_query,
                "total_queries": 0
            }
        except Exception as e:
            print_error(f"Research execution failed: {e}")
            raise

class ScriptWriterAgent(BaseAgent):
    """Agent responsible for initial script creation."""
    def create_script(self, research_data: Dict, params: Dict) -> Dict:
        """Create initial video script based on research."""
        try:
            json_example = {
                "intro_script": "Opening hook and introduction text",
                "questions": [
                    {
                        "question": "The question text",
                        "answer": "The answer text",
                        "fact": "An interesting related fact",
                        "timestamp": "MM:SS format"
                    }
                ],
                "outro_script": "Closing remarks and call to action",
                "visual_notes": "Visual suggestions and transitions",
                "timestamps": {
                    "intro": "MM:SS format",
                    "questions": ["MM:SS format"],
                    "outro": "MM:SS format"
                }
            }
            
            prompt = f"""
            Create an engaging {params['format']} video script using the provided research data.
            Video Length: {params['length']} minutes
            Questions: {params['questions']}
            Topic: {params['topic']}

            Research Data:
            {research_data['raw_data']}

            Requirements:
            1. Create a structured script with clear sections
            2. Include specific timestamps
            3. Write engaging questions and explanations
            4. Add voiceover text
            5. Suggest visual elements
            
            Return a valid JSON object matching this exact structure:
            {json.dumps(json_example, indent=2)}

            Important:
            - Return ONLY the JSON object, no other text
            - Do not include markdown code block markers
            - Ensure all fields match the example structure exactly
            """

            response = self.get_response(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional video script writer. Return ONLY a valid JSON object matching the specified structure exactly. No markdown, no explanations."
                    },
                    {"role": "user", "content": prompt}
                ],
                save_as="script_response.txt"
            )

            # Clean and parse JSON
            json_str = self.clean_json_response(response)
            script = json.loads(json_str)
            
            # Validate script structure
            required_fields = ["intro_script", "questions", "outro_script", "visual_notes", "timestamps"]
            if not all(field in script for field in required_fields):
                raise ValueError(f"Script missing required fields: {[f for f in required_fields if f not in script]}")
            
            self.save_output(script, "initial_script.json")
            return script
            
        except json.JSONDecodeError as e:
            print_error(f"Failed to parse script JSON: {e}")
            print_error("Raw response:", response)  # Log the raw response for debugging
            # Return a basic valid structure
            return {
                "intro_script": "Error: Failed to generate script",
                "questions": [],
                "outro_script": "",
                "visual_notes": "",
                "timestamps": {"intro": "00:00", "questions": [], "outro": "00:00"}
            }
        except Exception as e:
            print_error(f"Script creation failed: {e}")
            raise

class PolishingAgent(BaseAgent):
    """Agent responsible for enhancing and polishing the script."""
    def polish_script(self, script: Dict, params: Dict) -> Dict:
        """Polish and enhance the script for maximum engagement."""
        try:
            json_example = {
                "intro_script": "Enhanced opening hook and introduction",
                "questions": [
                    {
                        "question": "Enhanced question text",
                        "answer": "Enhanced answer text",
                        "fact": "Enhanced interesting fact",
                        "timestamp": "MM:SS format",
                        "transition": "Transition text to next question"
                    }
                ],
                "outro_script": "Enhanced closing remarks and call to action",
                "visual_notes": "Enhanced visual suggestions and transitions",
                "timestamps": {
                    "intro": "MM:SS format",
                    "questions": ["MM:SS format"],
                    "outro": "MM:SS format"
                },
                "hashtags": ["list", "of", "trending", "hashtags"],
                "engagement_notes": "Platform-specific engagement tips"
            }
            
            prompt = f"""
            Enhance this {params['format']} video script for maximum engagement.
            
            Original Script:
            {json.dumps(script, indent=2)}

            Requirements:
            1. Improve hook and intro
            2. Enhance transitions between questions
            3. Add engaging facts/context
            4. Optimize pacing
            5. Add platform-specific elements
            6. Include trending hashtags
            7. Enhance visual suggestions
            
            Return a valid JSON object matching this exact structure:
            {json.dumps(json_example, indent=2)}
            """

            response = self.get_response(
                messages=[
                    {"role": "system", "content": "You are an expert in social media engagement and video optimization. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                save_as="polish_response.txt"
            )

            # Clean and parse JSON
            json_str = self.clean_json_response(response)
            polished_script = json.loads(json_str)
            
            self.save_output(polished_script, "polished_script.json")
            return polished_script
            
        except json.JSONDecodeError as e:
            print_error(f"Failed to parse polished script JSON: {e}")
            # Return enhanced version of input script
            return {
                **script,  # Keep original content
                "hashtags": ["#error", "#retry"],
                "engagement_notes": "Error: Failed to enhance script"
            }
        except Exception as e:
            print_error(f"Script polishing failed: {e}")
            raise

class EvaluatorAgent(BaseAgent):
    """Agent responsible for evaluating other agents' work."""
    def evaluate_research(self, research_output: Dict, params: Dict) -> Tuple[float, str]:
        """Evaluate research quality and coverage."""
        try:
            json_example = {
                "scores": {
                    "comprehensiveness": 0,
                    "relevance": 0,
                    "credibility": 0,
                    "engagement": 0,
                    "coverage": 0
                },
                "total_score": 0,
                "feedback": "Detailed feedback text",
                "improvement_suggestions": ["list", "of", "suggestions"]
            }
            
            prompt = f"""
            You are evaluating research output for a {params['format']} video about {params['topic']}.
            Your task is to score the research and provide feedback.
            
            Research Output:
            {json.dumps(research_output, indent=2)}

            Score each criterion from 0-10:
            1. Comprehensiveness: How well does it cover all aspects?
            2. Relevance: How relevant is the content to the topic?
            3. Credibility: How reliable are the sources?
            4. Engagement: How engaging is the content?
            5. Topic coverage: How well does it cover the specific topic?

            Respond with a JSON object exactly matching this structure:
            {json.dumps(json_example, indent=2)}

            Important:
            - Ensure all scores are numbers between 0 and 10
            - Calculate total_score as the average of all scores
            - Provide specific, actionable feedback
            - List 3-5 concrete improvement suggestions
            - Return ONLY the JSON object, no other text
            """

            response = self.get_response(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert content research evaluator. You must return a valid JSON object exactly matching the specified structure. No other text or explanations."
                    },
                    {"role": "user", "content": prompt}
                ],
                save_as="research_eval_response.txt"
            )

            # Clean and parse JSON
            json_str = self.clean_json_response(response)
            evaluation = json.loads(json_str)
            
            # Validate the evaluation structure
            if not all(key in evaluation for key in ["scores", "total_score", "feedback", "improvement_suggestions"]):
                raise ValueError("Evaluation missing required fields")
            
            self.save_output(evaluation, "research_evaluation.json")
            return evaluation["total_score"], evaluation["feedback"]
            
        except json.JSONDecodeError as e:
            print_error(f"Failed to parse evaluation JSON: {e}")
            return 5.0, "Error: Failed to evaluate research"
        except Exception as e:
            print_error(f"Research evaluation failed: {e}")
            return 5.0, str(e)

    def evaluate_script(self, script: Dict, params: Dict) -> Tuple[float, str]:
        """Evaluate script quality and engagement potential."""
        try:
            json_example = {
                "scores": {
                    "hook_strength": 0,
                    "engagement_flow": 0,
                    "platform_optimization": 0,
                    "content_quality": 0,
                    "production_value": 0
                },
                "total_score": 0,
                "feedback": "Detailed feedback text",
                "improvement_suggestions": ["list", "of", "suggestions"]
            }
            
            prompt = f"""
            You are evaluating a {params['format']} video script about {params['topic']}.
            Your task is to score the script and provide feedback.
            
            Script:
            {json.dumps(script, indent=2)}

            Score each criterion from 0-10:
            1. Hook strength: How compelling is the opening?
            2. Engagement flow: How well does it maintain interest?
            3. Platform optimization: How well is it optimized for {params['format']}?
            4. Content quality: How good is the content?
            5. Production value: How well are visuals and timing handled?

            Respond with a JSON object exactly matching this structure:
            {json.dumps(json_example, indent=2)}

            Important:
            - Ensure all scores are numbers between 0 and 10
            - Calculate total_score as the average of all scores
            - Provide specific, actionable feedback
            - List 3-5 concrete improvement suggestions
            - Return ONLY the JSON object, no other text
            """

            response = self.get_response(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert video content evaluator. You must return a valid JSON object exactly matching the specified structure. No other text or explanations."
                    },
                    {"role": "user", "content": prompt}
                ],
                save_as="script_eval_response.txt"
            )

            # Clean and parse JSON
            json_str = self.clean_json_response(response)
            evaluation = json.loads(json_str)
            
            # Validate the evaluation structure
            if not all(key in evaluation for key in ["scores", "total_score", "feedback", "improvement_suggestions"]):
                raise ValueError("Evaluation missing required fields")
            
            self.save_output(evaluation, "script_evaluation.json")
            return evaluation["total_score"], evaluation["feedback"]
            
        except json.JSONDecodeError as e:
            print_error(f"Failed to parse evaluation JSON: {e}")
            return 5.0, "Error: Failed to evaluate script"
        except Exception as e:
            print_error(f"Script evaluation failed: {e}")
            return 5.0, str(e)

def get_video_parameters(use_hardcoded: bool = False):
    """Get video parameters from user input or use hardcoded values for testing."""
    if use_hardcoded:
        print_step("Using hardcoded parameters for testing")
        return {
            "format": "TikTok",
            "length": 1.0,
            "questions": 5,
            "topic": "Nirvana",
            "urls_per_query": 1,
            "search_terms": 1  # Number of search queries to generate
        }
    
    print_step("Getting video parameters from user")
    
    try:
        # Get video format
        while True:
            format_input = input(colored("Enter video format (e.g., TikTok, YouTube Short, Instagram Reel): ", "green")).strip()
            if format_input:
                break
            print_error("Video format cannot be empty")

        # Get video length
        while True:
            try:
                length_input = float(input(colored("Enter video length in minutes (e.g., 1.5): ", "green")))
                if 0 < length_input <= 10:  # Reasonable limit for short-form content
                    break
                print_error("Video length must be between 0 and 10 minutes")
            except ValueError:
                print_error("Please enter a valid number")

        # Get number of questions/items
        while True:
            try:
                questions_input = int(input(colored("Enter number of questions/items (1-20): ", "green")))
                if 1 <= questions_input <= 20:
                    break
                print_error("Number of questions must be between 1 and 20")
            except ValueError:
                print_error("Please enter a valid number")

        # Get topic
        while True:
            topic_input = input(colored("Enter the topic for the video: ", "green")).strip()
            if topic_input:
                break
            print_error("Topic cannot be empty")

        # Get number of URLs per search query
        while True:
            try:
                urls_per_query = int(input(colored("Enter number of URLs to process per search query (1-5): ", "green")))
                if 1 <= urls_per_query <= 5:
                    break
                print_error("Number of URLs must be between 1 and 5")
            except ValueError:
                print_error("Please enter a valid number")

        # Get number of search terms
        while True:
            try:
                search_terms = int(input(colored("Enter number of search terms to generate (1-20): ", "green")))
                if 1 <= search_terms <= 20:
                    break
                print_error("Number of search terms must be between 1 and 20")
            except ValueError:
                print_error("Please enter a valid number")

        return {
            "format": format_input,
            "length": length_input,
            "questions": questions_input,
            "topic": topic_input,
            "urls_per_query": urls_per_query,
            "search_terms": search_terms
        }

    except KeyboardInterrupt:
        print_error("\nInput interrupted by user")
        raise
    except Exception as e:
        print_error("Error getting video parameters", e)
        raise

def format_script_as_text(script: Dict) -> str:
    """Convert script JSON to human-readable text format."""
    text = []
    
    # Add intro
    text.append("=== INTRODUCTION ===")
    text.append(script["intro_script"])
    text.append("")
    
    # Add questions
    text.append("=== MAIN CONTENT ===")
    for i, q in enumerate(script["questions"], 1):
        text.append(f"[{q['timestamp']}] Question {i}:")
        text.append(f"Q: {q['question']}")
        text.append(f"A: {q['answer']}")
        text.append(f"Fact: {q['fact']}")
        if "transition" in q:
            text.append(f"Transition: {q['transition']}")
        text.append("")
    
    # Add outro
    text.append("=== OUTRO ===")
    text.append(script["outro_script"])
    text.append("")
    
    # Add visual notes
    text.append("=== VISUAL NOTES ===")
    text.append(script["visual_notes"])
    text.append("")
    
    # Add hashtags if present
    if "hashtags" in script:
        text.append("=== HASHTAGS ===")
        text.append(" ".join(script["hashtags"]))
        text.append("")
    
    # Add engagement notes if present
    if "engagement_notes" in script:
        text.append("=== ENGAGEMENT NOTES ===")
        text.append(script["engagement_notes"])
    
    return "\n".join(text)

def main():
    try:
        print_step("Starting Multi-Agent Video Content Planner")
        
        # Get parameters from user (default to user input)
        params = get_video_parameters(use_hardcoded=False)
        
        # Create output folder
        output_folder = create_output_folder(params['topic'])
        
        # Initialize agents
        research_agent = ResearchAgent(output_folder, params['urls_per_query'])
        script_writer = ScriptWriterAgent(output_folder)
        polishing_agent = PolishingAgent(output_folder)
        evaluator = EvaluatorAgent(output_folder)
        
        # Research Phase
        print_step("Starting Research Phase...")
        research_output = research_agent.execute_research(params['topic'], params)
        research_score, research_feedback = evaluator.evaluate_research(research_output, params)
        
        if research_score < 7.0:
            print_step(f"Research score ({research_score}) below threshold. Feedback: {research_feedback}")
            print_step("Re-executing research with improvements...")
            # Clear previous search results before retrying
            research_agent.retriever_tool.search_results = []
            research_output = research_agent.execute_research(params['topic'], params)
            # Re-evaluate after retry
            research_score, research_feedback = evaluator.evaluate_research(research_output, params)
        
        # Script Writing Phase
        print_step("Creating Initial Script...")
        initial_script = script_writer.create_script(research_output, params)
        script_score, script_feedback = evaluator.evaluate_script(initial_script, params)
        
        if script_score < 7.0:
            print_step(f"Script score ({script_score}) below threshold. Feedback: {script_feedback}")
            print_step("Recreating script with improvements...")
            initial_script = script_writer.create_script(research_output, params)
            # Re-evaluate after retry
            script_score, script_feedback = evaluator.evaluate_script(initial_script, params)
        
        # Polishing Phase
        print_step("Polishing Script...")
        final_script = polishing_agent.polish_script(initial_script, params)
        final_score, final_feedback = evaluator.evaluate_script(final_script, params)
        
        # Save final outputs
        print_step("Saving Final Output...")
        
        # Save JSON version
        with open(os.path.join(output_folder, "final_script.json"), "w", encoding="utf-8") as f:
            json.dump({
                "script": final_script,
                "metadata": {
                    "research_score": research_score,
                    "research_feedback": research_feedback,
                    "initial_script_score": script_score,
                    "script_feedback": script_feedback,
                    "final_script_score": final_score,
                    "final_feedback": final_feedback,
                    "parameters": params
                }
            }, f, indent=2)
        
        # Save human-readable text version
        text_script = format_script_as_text(final_script)
        with open(os.path.join(output_folder, "final_script.txt"), "w", encoding="utf-8") as f:
            f.write(text_script)
        
        print_success("Video content plan generated successfully")
        print_success(f"All data saved to: {output_folder}")
        print_step(f"Final Scores:")
        print_step(f"- Research: {research_score}/10")
        print_step(f"- Initial Script: {script_score}/10")
        print_step(f"- Final Script: {final_score}/10")
        print_step(f"\nFinal Feedback: {final_feedback}")
        
    except Exception as e:
        print_error("Main execution failed", e)
        return 1

if __name__ == "__main__":
    main() 