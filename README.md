# Strategic Game Simulator

A Python implementation of game theory concepts simulating strategic interactions between players with various decision-making strategies.


##  Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Game Types](#-game-types)
- [Player Strategies](#-player-strategies)
- [Simulation Workflow](#-simulation-workflow)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

##  Features

-  Multiple classic game theory scenarios
-  Pre-built AI player strategies
-  Custom game configuration
-  Advanced analytics and visualization
-  Iterative simulation capabilities
-  Evolutionary strategy support

##Workflow

graph TD
    A[Initialize Game] --> B[Configure Players]
    B --> C[Set Payoff Matrix]
    C --> D[Run Iterations]
    D --> E[Record Moves]
    E --> F[Calculate Payoffs]
    F --> G{More iterations?}
    G -->|Yes| D
    G -->|No| H[Analyze Results]
    H --> I[Generate Visualizations]

    
##  Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Steps
```bash
# Clone the repository
git clone https://github.com/sujalk777/Strategic_game.git
cd Strategic_game

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
