# Hours Wasted

A simple desktop app to track how many hours you've spent on different projects.  
Built with Python and Tkinter.

## Features

- Create and select projects
- Start/stop a timer to track hours spent
- See total hours for each project
- Compact mode: shrink the window to just show hours and an expand button
- Data saved automatically to `projects.json`

## Usage

1. **Install Python**  
   Make sure you have Python 3 installed.

2. **Run the app**  
   Open a terminal in the project folder and run:
   ```
   python main.py
   ```

3. **Track your time**
   - Create a new project or select an existing one.
   - Click **Start** to begin tracking.
   - Click **Stop** to save your hours.
   - Use **Compact Mode** to shrink the window; click **X** to expand again.

## Data

All project hour data is saved in `projects.json` in the same folder.

## Screenshots

![Full UI](screenshot_full.png)
![Compact Mode](screenshot_compact.png)

## License

MIT