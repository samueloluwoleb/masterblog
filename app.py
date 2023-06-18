from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    blog_posts = load_data('blogposts_database.json')
    print(blog_posts)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        blog_posts = load_data('blogposts_database.json')
        new_id = (blog_posts[-1]["id"]) + 1
        new_post = {"id": new_id, "author": author, "title": title, "content": content}
        blog_posts.append(new_post)
        json_data = json.dumps(blog_posts)

        with open("blogposts_database.json", "w") as fileobj:
            fileobj.write(json_data)
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_data('blogposts_database.json')
    for count, post in enumerate(blog_posts):
        if post['id'] == post_id:
            del blog_posts[count]

    json_data = json.dumps(blog_posts)

    with open("blogposts_database.json", "w") as fileobj:
        fileobj.write(json_data)
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = load_data('blogposts_database.json')
    for post_data in blog_posts:
        if post_data['id'] == post_id:
            post = post_data

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        blog_posts = load_data('blogposts_database.json')
        for post_data in blog_posts:
            if post_data['id'] == post_id:
                post_data['title'] = title
                post_data['author'] = author
                post_data['content'] = content

        json_data = json.dumps(blog_posts)

        with open("blogposts_database.json", "w") as fileobj:
            fileobj.write(json_data)
        return redirect('/')

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()

