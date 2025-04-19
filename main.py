import instaloader, random, os, time
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
ACCOUNT = os.getenv("ACCOUNT")
PASSWORD = os.getenv("PASSWORD")

#parsing environment variable and removing whitespaces
POSTS = os.environ.get('POSTS').split(',')
POSTS = [item.strip() for item in POSTS]

print(f"Downloading comments from {POSTS}")

L = instaloader.Instaloader(
    request_timeout=60,
    user_agent="Mozilla/5.0 (Linux; Android 11; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/89.0.4389.105 Mobile Safari/537.36",
    max_connection_attempts=3
)

def get_comments(post):
    attempts = 0
    comments_retrieved = 0
    while attempts < 3:
        try:
            comments = []
            for comment in post.get_comments():
                #get main comments
                comments.append({
                    "post_shortcode": post.shortcode,
                    "comment_id": comment.id,
                    "comment_date": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    "username": comment.owner.username,
                    "text": comment.text,
                    "likes": comment.likes_count,
                    "is_reply": False
                })
                comments_retrieved+=1
                print(f"Comments retrieved: {comments_retrieved}")

                #get replies (if any)
                if hasattr(comment, 'answers') or 'edge_threaded_comments' in comment._node:
                    replies_retrieved = 0
                    for reply in comment.answers:
                        comments.append({
                            "post_shortcode": post.shortcode,
                            "parent_id": comment.id,
                            "comment_id": reply.id,
                            "comment_date": reply.created_at_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            "username": reply.owner.username,
                            "text": reply.text,
                            "likes": reply.likes_count,
                            "is_reply": True
                        })
                        replies_retrieved+=1
                        print(f"-- Replies retrieved: {replies_retrieved}\n")
                        time.sleep(random.uniform(1.5, 3))  #delay to avoid instagram block
                time.sleep(random.uniform(1.5, 4))  #delay to avoid instagram block
            return comments
        
        except Exception as e:
            print(f"Error (attempt {attempts + 1}/3): {str(e)}")
            attempts += 1
            time.sleep(random.uniform(15, 30))  #wait if error
    return []

try:
    #try to login from session file
    L.load_session_from_file(ACCOUNT) if os.path.exists(f"{ACCOUNT}.json") else L.login(ACCOUNT, PASSWORD)
    
    all_data = []
    
    for shortcode in POSTS:
        try:
            print(f"\nProcessing post: {shortcode}")
            
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            print(f"Caption: {post.caption[:100]}... | Likes: {post.likes}")
            
            comments = get_comments(post)
            print(f"Saving {len(comments)} comments...")

            #Exporting data to csv
            df = pd.DataFrame(comments)
            filename = f"{shortcode}_comments_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"\nData saved in {filename} | Total for {shortcode}: {len(df)} comments.")

            print("Getting next post data...")
            #delay between posts
            time.sleep(random.uniform(12, 25))
            
        except Exception as e:
            print(f"Exception in post {shortcode}: {str(e)}")
            time.sleep(60)  #continue after one minute

    print("No more posts detected.")

except Exception as e:
    print(f"Fatal error: {str(e)}")
finally:
    L.close()