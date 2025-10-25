# Assignment 6: Design Patterns in Financial Software Architecture 📈

This project is a sophisticated algorithmic trading engine designed to simulate and execute trading strategies based on real-time market data. It leverages various design patterns to ensure modularity, flexibility, and maintainability. The engine supports multiple trading strategies, data sources, and analytics metrics, making it a versatile tool for quantitative analysis and automated trading.

**Authors:** Yuting Li, Xiangchen Liu, Simon Guo, Rajdeep Choudhury

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
---

## 🚀 Key Features

- **Modular Design:** Utilizes design patterns like Singleton, Factory, Builder, Strategy, Observer, and Command for a highly modular and extensible architecture.
- **Multiple Trading Strategies:** Supports Mean Reversion and Breakout strategies out-of-the-box, with easy integration of new strategies.
- **Real-time Data Processing:** Processes market data in real-time, generating trading signals and executing trades based on the configured strategy.
- **Portfolio Management:** Manages a portfolio of financial instruments, allowing for complex portfolio structures and trade execution.
- **Analytics Integration:** Integrates with analytics decorators to add metrics like volatility, beta, and drawdown to instruments.
- **Logging and Alerting:** Provides comprehensive logging and alerting capabilities to monitor trading activity and potential issues.
- **Data Source Flexibility:** Supports multiple data sources, including JSON, XML, and CSV files, through a data adapter pattern.
- **Command Pattern:** Implements the command pattern for trade execution, enabling undo functionality.

## 🛠️ Tech Stack

- **Programming Language:** Python 🐍
- **Design Patterns:**
    - Singleton
    - Factory
    - Builder
    - Strategy
    - Observer
    - Command
    - Decorator
    - Composite
    - Adapter
- **Data Handling:**
    - `json`: For reading JSON configuration and data files.
    - `csv`: For reading instrument and market data from CSV files.
    - `xml.etree.ElementTree`: For parsing XML data files.
- **Data Structures:**
    - `typing`: For type hinting.
    - `collections.deque`: For storing price history in strategies.
- **Abstract Base Classes:** `abc` module for defining abstract classes.
- **Operating System:** `os` module for file path manipulation.
- **Modules:**
    - `patterns.singleton`
    - `patterns.factory`
    - `patterns.builder`
    - `patterns.strategy`
    - `patterns.observer`
    - `patterns.command`
    - `analytics`
    - `data_loader`
    - `reporting`
    - `engine`
    - `models`

## 📦 Getting Started

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt # if you have a requirements.txt file
    # or install manually if you don't have requirements.txt
    # pip install any specific dependencies mentioned in the file summaries
    ```

### Running Locally

1.  Configure the application:

    *   Modify `data/config.json` to set the desired logging level, data paths, and default trading strategy.
    *   Ensure that the paths to the data files in `data/config.json` are correct.
    *   Update `instruments.csv` and `portfolio_structure.json` with your desired instrument and portfolio configurations.

2.  Run the main script:

    ```bash
    python main.py
    ```

## 📂 Project Structure

```
├── data/
│   ├── config.json           # Application configuration
│   ├── instruments.csv       # Instrument data
│   └── portfolio_structure.json # Portfolio structure definition
├── patterns/
│   ├── builder.py          # Builder pattern implementation
│   ├── command.py          # Command pattern implementation
│   ├── factory.py          # Factory pattern implementation
│   ├── observer.py         # Observer pattern implementation
│   ├── singleton.py        # Singleton pattern implementation
│   └── strategy.py         # Strategy pattern implementation
├── analytics.py            # Analytics decorators
├── data_loader.py          # Data loading adapters
├── engine.py               # Trading engine implementation
├── main.py                 # Main application entry point
├── models.py               # Data models
├── reporting.py            # Logging and alerting observers
├── README.md               # This file
└── requirements.txt        # Project dependencies (if available)
```

## 🤝 Contribution Guidelines

We welcome contributions to the `FINM32500-HW6` project! Please follow these guidelines to ensure a smooth collaboration process.

### Code Style

*   Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
*   Use a linter (e.g., `flake8` or `ruff`) to check your code before submitting.

### Branch Naming Conventions

Please use descriptive branch names for new features and bug fixes:

*   **Features:** `feature/your-feature-name` (e.g., `feature/add-mean-reversion-strategy`)
*   **Bug Fixes:** `bugfix/issue-description` (e.g., `bugfix/fix-data-loading-error`)
*   **Documentation:** `docs/update-readme`

### Pull Request Process

1.  **Fork** the repository.
2.  **Create** a new branch from `main` (or the appropriate base branch).
3.  **Implement** your changes, ensuring they align with the project's goals.
4.  **Write Tests:** For new features or bug fixes, please add or update relevant tests in the `tests/` directory.
5.  **Run Tests:** Ensure all existing tests pass and your new tests cover your changes adequately.
6.  **Commit** your changes with clear, concise commit messages.
7.  **Push** your branch to your forked repository.
8.  **Open a Pull Request** against the `main` branch of the original repository.
9.  **Provide a clear description** of your changes, why they are needed, and any relevant context.

### Testing Requirements

All contributions must include appropriate tests. New features require new tests, and bug fixes should include a test that demonstrates the bug and its fix. Ensure your changes do not break existing functionality by running the full test suite.

### License

This project is protected under the MIT LICENSE. For more details, refer to the LICENSE file.

##  Acknowledgments

This project was created as part of the FINM 32500 course at **The University of Chicago Physical Sciences Division**. Inspiration from various open-source backtesting frameworks.

**Copyright © 2025 Lauristt**
