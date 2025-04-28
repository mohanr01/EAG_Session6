# Ticket Booking Agent

This is a ticket booking agent that can book tickets for trains and buses. 

The agent is built with a functional programming architecture consisting of four main modules: **Perception**, **Memory**, **Decision-Making**, and **Action**.

## Features

- **Functional programming architecture** with immutable state
- **Contextual understanding of user queries** using Google's Gemini AI
- **Persistent memory** with immutable state management
- **Structured decision-making process**

## Architecture

The agent consists of four main modules, all implemented using functional programming principles:

1. **Perception (LLM)**:  
   - Pure functions for user input processing and natural language understanding using Google's Gemini Pro model.

2. **Memory**:  
   - Immutable state management for conversation history, user preferences, and recommendations.

3. **Decision-Making**:  
   - Pure functions for analyzing input and determining appropriate actions.

4. **Action**:  
   - Pure functions for executing decisions and generating formatted responses.

## Setup

1. **Clone the repository**

2. **Install `uv` (if not already installed):**
   ```bash
   pip install uv
   ```

3. **Create and activate a virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   .venv\Scripts\activate     # On Windows
   ```

4. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Set up your Google API key:**

   **Option 1**: Set as an environment variable:  
   - For Unix/macOS:  
     ```bash
     export GOOGLE_API_KEY='your-api-key'
     ```
   - For Windows:  
     ```bash
     set GOOGLE_API_KEY='your-api-key'
     ```

   **Option 2**: Pass directly when initializing the agent.

## Usage

1. **Run the agent:**
   ```bash
   uv run main.py
   ```

2. **How it works:**
   - The agent will ask for user preferences to book a ticket and provide suggestions.
   - If the user preferences are not satisfied, the agent will prompt the user to give expected values to book a ticket.

### Example Interactions

Provide a query to book tickets (train, bus, cinema).  
Some sample queries:
1. "Can you book a train ticket from Tambaram to Tenkasi tomorrow for 2 people?"  
2. "Can you book a bus ticket from Tambaram to Tenkasi tomorrow for 2 people?"

**Example Input:**  
```plaintext
Can you book a train ticket from Tambaram to Tenkasi tomorrow for 2 people?
```

## Requirements

- **Python 3.7+**
- **Google API key** for Gemini Pro
- **`uv` package manager**
- Dependencies listed in `pyproject.toml`

## Development

The codebase follows functional programming principles:
- Pure functions
- Immutable state
- Type hints
- No side effects (except for I/O operations)
- Composition over inheritance
