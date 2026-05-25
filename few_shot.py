import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            
            # collect unique tags - flatten the list of lists properly
            all_tags = []
            for tags in self.df['tags']:
                if isinstance(tags, list):
                    all_tags.extend(tags)
            self.unique_tags = list(set(all_tags))
            
            # DEBUG: Print what we have
            print("=== DEBUG INFO ===")
            print(f"Total posts: {len(self.df)}")
            print(f"\nUnique tags: {self.unique_tags}")
            print(f"\nFirst 3 rows:")
            print(self.df[['tags', 'language', 'length', 'line_count']].head(3))
            print(f"\nLanguages available: {self.df['language'].unique()}")
            print(f"\nLengths available: {self.df['length'].unique()}")
            print(f"\nSample tags in first row: {self.df['tags'].iloc[0]}")

    def get_filtered_posts(self, length, language, tag):
        print(f"\n=== FILTERING ===")
        print(f"Looking for: length={length}, language={language}, tag={tag}")
        
        # Check each filter separately
        tag_filter = self.df['tags'].apply(lambda tags: tag in tags if isinstance(tags, list) else False)
        lang_filter = self.df['language'] == language
        length_filter = self.df['length'] == length
        
        print(f"Posts with tag '{tag}': {tag_filter.sum()}")
        print(f"Posts with language '{language}': {lang_filter.sum()}")
        print(f"Posts with length '{length}': {length_filter.sum()}")
        
        df_filtered = self.df[tag_filter & lang_filter & length_filter]
        
        print(f"Posts matching ALL filters: {len(df_filtered)}")
        
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    print(f"\nAll available tags: {fs.get_tags()}")
    posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(f"\nResult: {posts}")