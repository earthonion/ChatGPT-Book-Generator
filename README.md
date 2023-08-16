# ChatGPT-Book-Generator

Generate complete books in PDF format from any given title with the ChatGPT-Book-Generator. The generator uses a `chapters.json` file to outline the book, creating one if it doesn't exist or using an existing one if provided.

## Features

- **Automatic Book Generation:** Input any title, and a complete book will be generated.
- **Customizable Chapters:** Use or create a `chapters.json` file to outline the structure of the book.

## Example of `chapters.json` Structure

```json
{
  "Chapter 1: Lorem": {
    "Subchapter 1: What is it?": [
      "Its medieval origins to the digital era",
      "Dummy text used in laying out print and its variants"
    ],
    "Subchapter 2: ...": [
      // Add content here
    ]
  },
  "Chapter 2: ...": {
    // Add content here
  }
}
```

## Setup

### Prerequisites

- **Python Packages:** The necessary Python packages can be installed by using the requirements file included in the project. In your terminal, run:

  ```bash
  pip install -r requirements.txt
  ```

- **DejaVu Font:** This project uses the DejaVu font. Ensure it's installed on your system. You can download it from [here](https://dejavu-fonts.github.io/Download.html) and follow the instructions for your operating system to install it.

- **OpenAI API Key:** You'll need to obtain an OpenAI API key from [your user settings](https://platform.openai.com/account/api-keys).

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/earthonion/ChatGPT-Book-Generator/
   cd ChatGPT-Book-Generator/
   ```

2. **Install Dependencies:** Use the requirements file to install all necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Edit Configuration:** Open the `config.py` file and include your OpenAI API key.

4. **Run the Script:** Once you've set up everything, simply run:

   ```bash
   python book_gen.py
   ```
