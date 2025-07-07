# Activate virtual environment
.\venv\Scripts\activate

# Create output file and write header
"Sample Bedtime Stories Generated" | Out-File -FilePath "sample_stories.txt"
"============================" | Out-File -FilePath "sample_stories.txt" -Append
"" | Out-File -FilePath "sample_stories.txt" -Append

# Story 1: Friendly Cloud
"Story 1: A Friendly Cloud" | Out-File -FilePath "sample_stories.txt" -Append
"Command: python -m bedtime_stories.cli tell 'a friendly cloud that brings rainbow rain'" | Out-File -FilePath "sample_stories.txt" -Append
"Output:" | Out-File -FilePath "sample_stories.txt" -Append
python -m bedtime_stories.cli tell "a friendly cloud that brings rainbow rain" | Out-File -FilePath "sample_stories.txt" -Append
"" | Out-File -FilePath "sample_stories.txt" -Append

# Story 2: Garden Friends
"Story 2: Garden Friends" | Out-File -FilePath "sample_stories.txt" -Append
"Command: python -m bedtime_stories.cli tell 'a tiny garden fairy who helps flowers grow at night'" | Out-File -FilePath "sample_stories.txt" -Append
"Output:" | Out-File -FilePath "sample_stories.txt" -Append
python -m bedtime_stories.cli tell "a tiny garden fairy who helps flowers grow at night" | Out-File -FilePath "sample_stories.txt" -Append
"" | Out-File -FilePath "sample_stories.txt" -Append

# Story 3: Sleepy Animals
"Story 3: Sleepy Animals" | Out-File -FilePath "sample_stories.txt" -Append
"Command: python -m bedtime_stories.cli tell 'woodland animals getting ready for bedtime'" | Out-File -FilePath "sample_stories.txt" -Append
"Output:" | Out-File -FilePath "sample_stories.txt" -Append
python -m bedtime_stories.cli tell "woodland animals getting ready for bedtime" | Out-File -FilePath "sample_stories.txt" -Append
"" | Out-File -FilePath "sample_stories.txt" -Append

# Story 4: Kind Helper
"Story 4: Kind Helper" | Out-File -FilePath "sample_stories.txt" -Append
"Command: python -m bedtime_stories.cli tell 'a gentle lighthouse that helps lost boats find their way home'" | Out-File -FilePath "sample_stories.txt" -Append
"Output:" | Out-File -FilePath "sample_stories.txt" -Append
python -m bedtime_stories.cli tell "a gentle lighthouse that helps lost boats find their way home" | Out-File -FilePath "sample_stories.txt" -Append
"" | Out-File -FilePath "sample_stories.txt" -Append

# Story 5: Magic Dreams
"Story 5: Magic Dreams" | Out-File -FilePath "sample_stories.txt" -Append
"Command: python -m bedtime_stories.cli tell 'a magical pillow that gives sweet dreams'" | Out-File -FilePath "sample_stories.txt" -Append
"Output:" | Out-File -FilePath "sample_stories.txt" -Append
python -m bedtime_stories.cli tell "a magical pillow that gives sweet dreams" | Out-File -FilePath "sample_stories.txt" -Append

# Deactivate virtual environment
deactivate 