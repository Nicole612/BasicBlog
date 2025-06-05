from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


@app.route('/')
def index():
    """Render the home page with a list of all blog posts."""
    with open("blog_posts.json") as f:
        blog_posts = json.load(f)
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the form to add a new blog post and handle form submission."""
    if request.method == 'POST':
        new_post = {
            "title": request.form["title"],
            "author": request.form["author"],
            "content": request.form["content"]
        }

        with open('blog_posts.json', 'r+') as f:
            posts = json.load(f)
            new_post["id"] = max([p['id'] for p in posts], default=0) + 1
            posts.append(new_post)
            f.seek(0)
            json.dump(posts, f, indent=2)
        return redirect(url_for("index"))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete the blog post with the given ID and redirect to the home page."""
    with open('blog_posts.json', 'r') as f:
        posts = json.load(f)

    updated_posts = [p for p in posts if p['id'] != post_id]

    with open('blog_posts.json', 'w') as f:
        json.dump(updated_posts, f, indent=2)

    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    """Return the blog post with the given ID from the JSON file """
    with open('blog_posts.json', 'r+') as f:
        posts = json.load(f)
        return next((p for p in posts if p['id'] == post_id), None)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Display a form to update a blog post and handle the update submission."""

    if request.method == 'POST':
        with open('blog_posts.json', 'r+') as f:
            posts = json.load(f)
            for p in posts:
                if p["id"] == post_id:
                    p['title'] = request.form['title']
                    p['author'] = request.form['author']
                    p['content'] = request.form['content']
                    break
            f.seek(0)
            f.truncate()
            json.dump(posts, f, indent=2)
        return redirect(url_for('index'))

    post = fetch_post_by_id(post_id)

    if post is None:
        return f"Post not found", 404

    return render_template('update.html', post=post)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)