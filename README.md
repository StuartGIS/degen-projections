Before every tournament:
1. Create a "draft_results" csv file after the draft
2. Upload that csv to the repository
3. Use that filename as the filename for the draft_results variable in the code. Should be two replacements.
4. Update the text tournament description for the course, location, and dates.

After every tournament:
1. Download a csv of the Drafted Players Detailed Live-Tournament Scoring table, and add a tourney_num column and values
2. Upload that table to the repo
3. Download a csv of the Full Field Detailed Live-Tournament Scoring table.
4. Add a tourney_num column to that table and give it its correct number.
5. Upload those csv's to the repo.
6. Update the season standings descriptions x3
7. Update season earnings
8. Update season geography picks


### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
