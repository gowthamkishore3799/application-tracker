# Job Application Tracker Automation

This project automates the process of tracking job applications. It allows you to save time by automating the entry of job applications into Notion, as well as providing an organized record of all your applications.

### Features
- **Track job applications**: Automatically creates an entry in Notion with the details of the job application such as company name, job position, job description, qualifications, etc.
- **Automatic resume linking**: Allows you to pass in the job application URL and the resume URL to create a new entry for tracking.
- **Customizable**: Easily extendable for future features like automatic status updates based on input email.
- **CLI Integration**: Link the script to a ZSH shell with an alias for easy execution.
- **Time-saving**: Saves significant time by automating the tedious process of manually adding job applications to a tracker.

### Technologies Used
- **OpenAI**: For integrating AI capabilities.
- **BeautifulSoup**: To scrape job application details from job URLs.
- **Notion API**: For automating the creation of entries in Notion.

### Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Install required packages**:
   You will need to install the following Python packages:
   ```bash
   pip install openai beautifulsoup4 notion
   ```

3. **Configure the Notion API**:
   - Follow the Notion API setup guide to create an integration and obtain an API key.
   - Set up your Notion database where the job application entries will be stored.

4. **Running the Script**:
   - Link the Python script to your ZSH shell and create an alias to execute the function. 
     For example, you can add this to your `.zshrc` file:
     ```bash
     alias jobtrack="python /path/to/job_tracker.py"
     ```

5. **Using the Script**:
   - Execute the script by passing the job URL and resume URL:
     ```bash
     jobtrack <job_url> <resume_url>
     ```

### Future Features
- **Automatic status updates**: The application will be able to automatically update the status of each job application by parsing the input email.
- **CLI Enhancements**: Further exploration of the Command Line Interface (CLI) for better user experience.

### Example Usage
```bash
jobtrack "https://company.com/job/123" "https://yourresume.com/resume.pdf"
```

This command will create a new entry in your Notion database with the job and resume details.
