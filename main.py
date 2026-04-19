from html.parser import HTMLParser

class InstagramParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_a = False
        self.href = ""
        self.capture_name = False
        self.current_username = None
        self.users = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href.startswith("/") and href.count("/") == 2:
                self.in_a = True
                self.href = href.strip("/")
                self.current_username = self.href
        if tag == "span":
            if any(k == "dir" and v == "auto" for k, v in attrs):
                self.capture_name = True

    def handle_data(self, data):
        if self.capture_name and self.current_username:
            text = data.strip()
            if text and text != self.current_username:
                if self.current_username not in self.users:
                    self.users[self.current_username] = text

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_a = False
        if tag == "span":
            self.capture_name = False

def extract_users(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        parser = InstagramParser()
        parser.feed(f.read())
    return parser.users

def main():
    followers_old = extract_users("followers_old.html")
    followers_new = extract_users("followers_new.html")
    following = extract_users("following.html")
    old = set(followers_old.keys())
    new = set(followers_new.keys())
    foll = set(following.keys())
    unfollowed = old - new
    not_following_back = foll - new
    print("\n--- Dejaron de seguirme ---")
    for u in sorted(unfollowed):
        print(f"{followers_old.get(u, u)} ({u})")
    print("\n--- Los sigo pero no me siguen ---")
    for u in sorted(not_following_back):
        print(f"{following.get(u, u)} ({u})")

if __name__ == "__main__":
    main()
