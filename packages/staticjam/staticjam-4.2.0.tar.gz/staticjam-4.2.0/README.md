# StaticJaM: Static, Markdown, and Jinja

Automagically creates HTML files/directories (for your website) from
markdown files you've writen.

Demo/example: [SlimeMaid's website](https://slimemaid.zone)!
[SlimeMaid's website is on
GitHub](https://github.com/slimemaid/slimemaid.github.io/), so you can poke
around to get acclimated, but be warned: sometimes it was built with `nextrelease`.

StaticJaM is a static site generator with these features:

  * Perfect for [GitHub Pages](https://pages.github.com/)
  * Uses [Jinja2 templating](http://jinja.pocoo.org/)
  * Doesn't get in the way of your HTML, CSS, etc
  * All website pages, blog posts are markdown files
  * Automatically creates category indexes, blog indexes, blog layout
  * You can use it *just* for building a blog `staticjam make blog`,
    or for just building web pages (`staticjam make pages`),
    and even both (`staticjam make both`)

## Using

Get started quick:

  1. `pip install staticjam` or `pip install .`
  2. `staticjam --help`
  3. `staticjam init`
  4. Go to `_staticjam_source/blog` and make a directory called `foo`
  5. Create `2017-04-30_example.md` in `foo`, something like:
       ```
       # Some Title
       Hiya folks!
       ```
  6. Make a file called `index.md` in `_staticjam_source/pages/` with
     similar contents
  7. `staticjam make both` 
  8. `staticjam test`

## Important notes

**Most important note:** Run `staticjam` only when your terminal's current
working directory is your project directory (directory containing
`_staticjam_source`).

  * Make sure you run `staticjam` from your project directory (the one
    that has `_staticjam_source` inside), as `staticjam` will output files
    to current directory (the directory you're in when you run the script),
    and search for files in the current directory.
  * Only works in Python3, so make note!
  * Keep all your images, media, etc., in a `static/` folder,
    it helps keeps things oranized!
  * Once your site is generated, test with `python3 -m http.server`!
  * Currently you *have* to create all the templates staticjam needs
    to create the website. On the upside, you can copy [SlimeMaid's
    templates](https://github.com/SlimeMaid/slimemaid.github.io).

## Project layout

`staticjam init` will create everything you need for your `_staticjam_source`
directory. Here's an example layout of a StaticJaM website/project.

    __init__.py

    static/
        background-stripes.png
        background-flowers.png

    _staticjam_source/
        __init__.py

        templates/
            base.html
            page.html
            blog-post.html
            blog-index.html
            blog-category-index.html

        pages/
            index.md
            about.md

        blog/
            2017-05-01_dear-diary.md

            photo-shoots/
                2017-04-15_pretty-pictures.md
                2017-05-11_more-pretty-pictures.md

Some notes about the above:

    * `static/`: where you keep all your media, images, etc.
    * `_staticjam_source/templates`: all of the Jinja2 templates, used
      in generating your website!
    * `pages/`: put markdown files here and they'll be turned into pages
      for your website.
    * `blog/`: where you put blog posts! Blog posts are markdown files with
      the file name format `YYYY-MM-DD_url-slug-here.md`. You can put a post
      in a directory like `blog/photo-shoots` and then that post belongs to
      the category `photo-shoots` and a category index will be created for
      `photo-shoots`

### Example: Custom background for specific page

So you have `templates`, `pages`, and a `blog` directory. Imagine
`_staticjam_source/index.md` looks like this:

    Background: /static/background-flowers.png        

    # Beautiful Home Page!
    This is the home page! It's special and has flowers for a background!

Let's say `_staticjam_source/templates/page.html` looks like this:

    <!DOCTYPE html>
    <html>
    <head>
        <title>whatever...</title>
    </head>
    <body style="background-image: url('{{ page.meta.background[0]}}')">
        <h1>{{ page.title }}</h1>
        {{ page.content }}
    </body>
    </html>

It'd output an HTML file that looks like this (with the background set to
flowers!):

    <!DOCTYPE html>
    <html>
    <head>
        <title>whatever...</title>
    </head>
    <body style="background-image: url('{{ page.meta.background[0]}}')">
        <h1>Beautiful Home Page</h1>
        <p>This is the home page! It's special and has flowers for a
        background!</p>
    </body>
    </html>

## Having a hard time installing?

Generally, `python3 -m pip install staticjam` will work automagically.

### Windows

  1. Install the latest stable Python (Python 3.x).
  2. `py -m pip install staticjam`

Use `py -m staticjam make both` instead of just `staticjam make both` (for example).
