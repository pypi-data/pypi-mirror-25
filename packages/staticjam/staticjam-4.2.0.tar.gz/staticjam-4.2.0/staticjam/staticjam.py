"""The main logic for StaticJaM

"""

import sys
import os
sys.path.append(os.getcwd())
import datetime
import glob
import inspect
import webbrowser
from collections import namedtuple
from http.server import HTTPServer, SimpleHTTPRequestHandler

import jinja2
from bs4 import BeautifulSoup, Tag
from markdown import Markdown


class MissingImmediateParagraphError(Exception):
    """Missing immediate paragraph!

    StaticJaM tried to process a Markdown blog post
    you wrote which lacks a paragraph of text which
    comes right after the document title. It should
    look something like this:

      # Example Document Title

      Here is an example of an "immediate paragraph,"
      which is used for article summaries.

    You must have an immediate paragraph. Here's what the
    first 140 characters of your Markdown look like:

      %s

    Note that if the above space is blank it is because your
    file is empty (the file contains %d characters).

    """

    def __init__(self, soup):
        markdown_text = soup.get_text()
        markdown_length = len(markdown_text)
        super().__init__(self.__doc__ % (markdown_text[:140], markdown_length))


class WebPage:
    """A webpage on the static site.

    HTML content (converted from markdown) and associated
    information. Includes tools to render into a webpage.

    It is encouraged to inherit this class, possibly overriding the
    class constants EXTENSIONS, TEMPLATE, and TEMPLATE_NOUN. These
    constants allow you to control how markdown is converted to HTML
    and how webpages are templated/rendered.

    Constants:
        EXTENSIONS (list): The Python `markdown` package extensions
            to use when converting markdown to HTML.
        TEMPLATE (str): Jinja template to use when rendering.
        TEMPLATE_NOUN (str): The keyword which will be used to supply
            this WebPage to the Jinja template.

    Attributes:
        meta (dict): WebPage's metadata, specifically written
            by the user in their markdown meta! Markdown meta
            looks like this:

                Title: hah
                Author: kitty
                                  
                First paragraph here.

            Specifically, markdown.extensions.meta implements this
            feature, so it's worth giving that a looksee.
        content (BeautifulSoup): A BeautifulSoup of the HTML
            created from a source markdown file. Does not
            having first <h1>/opening heading in it. This is
            not a full HTML document (templates are applied
            when rendering).
        title (str): First heading of the post, the
            name. The title is the first h1/heading of the
            soup/contents.

    """

    EXTENSIONS = [
        'markdown.extensions.footnotes',
        'markdown.extensions.meta',
    ]
    TEMPLATE = 'page.html'
    TEMPLATE_NOUN = 'page'

    def __init__(self, path_to_source_markdown):
        markdown = Markdown(extensions=self.EXTENSIONS)
        with open(path_to_source_markdown) as f:
            markdown_as_html = markdown.convert(f.read())
        self.meta = markdown.Meta
        self.content = BeautifulSoup(markdown_as_html, 'html.parser')

        # NOTE: matches, removes first <h1>...</h1> from self.content!
        self.title = self.content.h1.extract().get_text()

    def __repr__(self):
        class_name = self.__class__.__name__
        replacements = (class_name, title[:6], content[:6])
        return '<%s title="%s" content="%s">' % replacements

    def render(self):
        """Magically returns a "ready for production" HTML document.

        Uses self's HTML content as the meat, but also gives Jinja
        templates other info like title and the metadata.

        See Also:
            The class constants TEMPLATE, TEMPLATE_NOUN.

        Returns:
            str: Full HTML document/web page for your static site,
                ready for writing out to a web page or whatever!

        """

        jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader(
                '_staticjam_source',
                'templates',
            )
        )
        page_template = jinja_env.get_template(self.TEMPLATE)
        page_html = page_template.render(**{self.TEMPLATE_NOUN: self})
        return generated_by_staticjam(page_html)


class Post(WebPage):
    """Blog post; article; a WebPage that belongs to the blog.

    A blog post, created from markdown source (given a file path).

    See Also:
        WebPage

    Constants:
        SUMMARY_CHARACTER_LIMIT (int): --
        TEMPLATE (str): jinja2 template to pull from the jinja2
            environment. This temple is used to render the post.
        MARKDOWN_SOURCE (str): --
        DATE_FORMAT (str): for strftime

    Attributes:
        href (str): Relative path to this article (html). Usable for
            both writing to local directory and as the href attribute
            of a link, in order to link to this post.
        category (str): Derived from the name of the directory
            containing this post. This is the string name of the
            category and not the actual Category class, for more
            info just checkout Category class.
        summary (str): A string summary (truncated) of the first
            paragraph of the content.
        content (BeautifulSoup): --
        timestamp (str): ---
        timestamp_as_int (int): --

    """

    SUMMARY_CHARACTER_LIMIT = 100
    TEMPLATE = 'blog-post.html'
    TEMPLATE_NOUN = 'post'
    MARKDOWN_SOURCE = os.path.join(
        '_staticjam_source',
        'blog'
    )
    DATE_FORMAT = "%a, %d %b %Y"

    def __init__(self, file_path):
        """

        Arguments:
            file_path (str): Path to the markdown source file, which
                is a blog post.

        """

        super().__init__(file_path)
        self.category = self.get_category(file_path)
        self.summary = self.summarize(self.content)
        self.href = self.get_href(self.category, file_path)
        self.timestamp, self.timestamp_as_int = self.get_both_timestamps(file_path)

        if self.category and not os.path.exists('blog/' + self.category):
            os.makedirs('blog/' + self.category)

    @classmethod
    def get_category(cls, path_to_file):
        """Return the directory which contains path_to_file.

        Returns:
            str|None: if this post is in the blog root, like,
                `_staticjam_source/blog/whatever.md` it'll return
                `None` because it doesn't have a category!

        """

        grandparent_parent_directories = path_to_file.split(os.path.sep)[-3:-1]
        if grandparent_parent_directories == ['_staticjam_source', 'blog']:
            return None
        else:
            category = os.path.basename(os.path.dirname(path_to_file))
            return category

    @classmethod
    def summarize(cls, soup):
        """Take BeautifulSoup and summarize the first paragraph.

        Returns:
            str:

        """

        try:
            first_paragraph = soup.find('p').get_text()
        except AttributeError as e:
            raise MissingImmediateParagraphError(soup)

        if len(first_paragraph) > cls.SUMMARY_CHARACTER_LIMIT:
            return first_paragraph[:cls.SUMMARY_CHARACTER_LIMIT] + '&hellip;'
        else:
            return first_paragraph

    @staticmethod
    def get_href(category, file_path):
        """Path usable on both web server and for writing
        HTML locally.

        Arguments:
            category (str):
            file_path (str):

        """

        file_name_md = os.path.basename(file_path)
        return os.path.join(
            'blog',
            category if category else '',
            os.path.splitext(file_name_md)[0],
            'index.html',
        )

    @classmethod
    def get_both_timestamps(cls, file_path):
        """Returns both the nice string/human-legible timestamp, as
        well as the int version for sorting.

        """

        blog_post_file_name = os.path.basename(file_path)
        timestamp = blog_post_file_name.split('_', 1)[0]
        nice_timestamp = datetime.datetime.strptime(
            timestamp,
            '%Y-%m-%d'
        ).strftime(cls.DATE_FORMAT)
        return nice_timestamp, int(timestamp.replace('-', ''))


class Category:
    """Almost a webpage but more of a tool/meta

    Useful for buildling out blog! Not used in post.category cuz
    """

    def __init__(self, name, posts=None):
        self.name = name
        self.posts = posts if posts else []
        self.index_href = os.path.join(
            'blog',
            self.name,
            'index.html',
        )


    def render_index(self):
        jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader(
                '_staticjam_source',
                'templates',
            )
        )
        category_template = jinja_env.get_template('blog-category-index.html')
        category_index_html = category_template.render(
            category=self.name,
            posts=self.posts,
        )
        return generated_by_staticjam(category_index_html)
        

class Blog:
    """

    An abstraction for handling the actual content of pages
    and posts.

    Attributes:
        posts (list[Post]): Posts sorted by creation time!

    """

    def __init__(self):
        self.posts = sorted(
            [post for post in self.yield_posts()],
            key=lambda x: x.timestamp_as_int,
            reverse=True,
        )
        self.categories = self.get_categories(self.posts)

    @staticmethod
    def get_categories(posts):
        categories = {}
        for post in posts:
            if post.category is None:
                continue

            if post.category not in categories:
                categories[post.category] = Category(
                    post.category,
                    posts=[post,],
                )
            else:
                categories[post.category].posts.append(post)

        return categories

    @staticmethod
    def yield_posts():
        all_the_posts = []
        search_path = os.path.join(Post.MARKDOWN_SOURCE, '**/*.md')
        for file_path in glob.iglob(search_path, recursive=True):
            yield Post(file_path)

    @staticmethod
    def make_necessary_directories(posts):
        for post in posts:
            directory = os.path.split(os.path.splitext(post.href)[0])[0]
            if not os.path.exists(directory):
                os.makedirs(directory)

    def write_out_all(self):
        # whoah...
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method.startswith('write_out_'):
                method()

    def write_out_posts(self):
        for post in self.posts:
            with open(post.href, 'w', encoding='utf-8') as f:
                f.write(post.render())

    def write_out_category_indexes(self):
        # create the category indexes
        for category_name, category in self.categories.items():
            with open(category.index_href, 'w', encoding='utf-8') as f:
                f.write(category.render_index())

    def write_out_blog_index(self):
        # .. finally render the blog index
        jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader(
                '_staticjam_source',
                'templates',
            )
        )
        template = jinja_env.get_template('blog-index.html')
        blog_index_path = os.path.join('blog', 'index.html')
        categories_alphabetized = sorted(self.categories.keys())
        with open(blog_index_path, 'w', encoding='utf-8') as f:
            html_string = template.render(
                posts=self.posts,
                categories=categories_alphabetized,
            )
            f.write(generated_by_staticjam(html_string))


# NOTE: rename to html finish up? since it also prettifies
# FIXME: this naming is confusing
def generated_by_staticjam(html_string):
    """Adds <meta name="generator" content="StaticJaM"> to the
    <head> of an HTML string.

    Arguments:
        html_string (str):

    Returns:
        str: ...

    """

    # I use lxml because of a bug I encountered in a template
    # with <dd>asdf</dt> really breaking things...
    soup = BeautifulSoup(html_string, 'lxml')
    # Weird beautifulsoup workaround (name is a positional argument
    # already, and while it allows any attributes, name is already used)
    meta_tag = Tag(
        builder=soup.builder,
        name='meta',
        attrs={'name': 'generator', 'content': 'StaticJaM'},
    )
    soup.head.insert(1, meta_tag)
    return str(soup.prettify())


def was_generated_by_staticjam(html_file_path):
    """Does file at html_file_path have <meta content='StaticJaM'>?

    This is used to determine which HTML files are generated by
    StaticJaM and which are not.

    """

    with open(html_file_path) as f:
        html_string = f.read()
    soup = BeautifulSoup(html_string, 'html.parser')
    staticjam_meta = soup.find('meta', content='StaticJaM')
    return True if staticjam_meta else False


def http_server_test():
    print("TIP: You can 'make' while server is running and just refresh!")
    print("Opening ur web browser...")
    webbrowser.open('http://localhost:8000/')
    print("CTRL+C to exit...")
    httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


# NOTE: don't forget prune, meta generated, also advice in docs about /static
def prune_generated_content(skip_asking_for_permission, ask_verbosely):
    """Prune content generated by StaticJaM, namely HTML files and
    directories.

    """

    # Pages
    pages_to_be_deleted = []
    for file_path in glob.iglob('*.html', recursive=False):
        if was_generated_by_staticjam(file_path):
            pages_to_be_deleted.append(file_path)

    # Blog
    blog_items_to_be_deleted = []
    for file_path in glob.iglob('blog/**/*.html', recursive=True):
        if was_generated_by_staticjam(file_path):
            blog_items_to_be_deleted.append(file_path)

    # Summary/ask permission before going ahead and deleting!
    if not skip_asking_for_permission:
        summary_question = (
            "OK to delete %d pages, %d blog items (y/n)? "
            % (len(pages_to_be_deleted), len(blog_items_to_be_deleted))
        )
        if ask_verbosely:
            for item in pages_to_be_deleted + blog_items_to_be_deleted:
                print(item)

        yes_or_no = None
        while yes_or_no not in ('y', 'n'):
            yes_or_no = input(summary_question).lower()

        if yes_or_no == 'n':
            sys.exit()
            return None  # FIXME: wait, what?

    # Do all the deleting!

    # Delete all the HTML files generated by
    # StaticJaM (blog posts, pages, category indexes, etc.)
    for file_path in pages_to_be_deleted + blog_items_to_be_deleted:
        os.remove(file_path)

    # delete the directories left in blog only if theyre empty
    for directory_contents in os.walk('blog', topdown=False):
        directory_path, directory_names, file_names = directory_contents
        # ... try to delete all of the subdirectories of this current
        # directory
        for subdirectory_name in directory_names:
            subdirectory_path = os.path.join(directory_path, subdirectory_name)
            try:
                os.rmdir(subdirectory_path)
            except OSError:
                print("you have files left in %s" % subdirectory_path)
                continue


def init():
    """Setup a _staticjam_source directory with the
    minimum required to get started.

    """

    # FIXME: !!!! if staticjam source already exists exit
    # create _staticjam_source
    os.mkdir('_staticjam_source')

    # create _staticjam_source/blog
    os.mkdir(os.path.join('_staticjam_source', 'blog'))

    # create _staticjam_source/pages
    os.mkdir(os.path.join('_staticjam_source', 'pages'))

    # create _staticjam_source/templates
    templates_directory = os.path.join('_staticjam_source', 'templates')
    os.mkdir(templates_directory)

    # create all the template files
    # FIXME: pkgdata lol
    base_html = '''
        {% macro blog_post_header(post, only_dl=False) -%}
          {% if not only_dl %}
          <header>
            <h1><a href="/{{ post.href }}">{{ post.title }}</a></h1>
          {% endif %}
            <dl>
              {% if post.category %}
              <dt>Theme</dt>
              <dd><a href="/blog/{{ post.category }}">{{ post.category }}</a></dd>
              {% endif %}

              <dt>Timestamp</dt>
              <dd>{{ post.timestamp }}</dd>
            </dl>
          {% if not only_dl %}
          </header>
          {% endif %}
        {%- endmacro %}
        <!DOCTYPE html>
        <html>
        <head>
            <title>{% block title %}{% endblock %} @ demo</title>
        </head>
        <body>
            <article>
                <header>
                    <h1>{% block article_title %}{% endblock %}</h1>
                    {% block article_header_extra %}{% endblock %}
                </header>
                {% block body %}{% endblock %}
            </article>
        </body>
        </html>
    '''
    with open(os.path.join(templates_directory, 'base.html'), 'w') as f:
        f.write(base_html)

    blog_category_index = '''
        {% extends "base.html" %}
        {% block title %}{{ category }} blog posts{% endblock %}
        {% block article_title %}Posts in {{ category }}{% endblock %}

        {% block body %}
          {% for post in posts %}
            <section>
              {{ blog_post_header(post) }}
              <p>{{ post.summary }}</p>
            </section>
          {% endfor %}
        {% endblock %}
    '''
    with open(os.path.join(templates_directory, 'blog-category-index.html'), 'w') as f:
        f.write(blog_category_index)

    blog_index = '''
        {% extends "base.html" %}
        {% block title %}Blog{% endblock %}
        {% block article_title %}Demo Blog{% endblock %}
        {% block article_header_extra %}
          <p>
            Categories:
            {% for category in categories %}
            <a href="/blog/{{ category }}">{{ category }}</a>&nbsp;
            {% endfor %}
          </p>
        {% endblock %}
        {% block body %}
          {% for post in posts %}
            <article>
              {{ blog_post_header(post) }}
              <p>{{ post.summary }}</p>
            </article>
          {% endfor %}
        {% endblock %}
    '''
    with open(os.path.join(templates_directory, 'blog-index.html'), 'w') as f:
        f.write(blog_index)

    blog_post = '''
        {% extends "base.html" %}
        {% block title %}{{ post.title }}{% endblock %}
        {% block article_title %}{{ post.title }}{% endblock %}

        {% block article_header_extra %}
            {{ blog_post_header(post, only_dl=True) }}
        {% endblock %}

        {% block body %}
          {{ post.content }}
        {% endblock %}
    '''
    with open(os.path.join(templates_directory, 'blog-post.html'), 'w') as f:
        f.write(blog_index)

    page_html = '''
        {% extends "base.html" %}
        {% block title %}{{ page.meta.title[0] }}{% endblock %}
        {% block article_title %}{{ page.title }}{% endblock %}
        {% block body %}
            {{ page.content }}
        {% endblock %}
    '''
    with open(os.path.join(templates_directory, 'blog-post.html'), 'w') as f:
        f.write(page_html)

    # touch all the __inits__.py lol
    open(os.path.join('_staticjam_source', '__init__.py'), 'a').close()
    open('__init__.py', 'a').close()


def create_blog():
    blog = Blog()
    blog.make_necessary_directories(blog.posts)
    blog.write_out_posts()
    blog.write_out_category_indexes()
    blog.write_out_blog_index()


def create_pages():
    search_path = '_staticjam_source/pages/*.md'
    for file_path in glob.iglob(search_path, recursive=False):
        page_html = WebPage(file_path).render()

        # get HTML output name...
        file_name_md = os.path.basename(file_path)
        output_file_path = os.path.splitext(file_name_md)[0] + '.html'

        # output page content...
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
