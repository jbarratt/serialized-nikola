# Copyright (c) 2012 Roberto Alsina y otros.
# Tweaked by Joshua Barratt

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

from nikola.plugin_categories import Task
from nikola.utils import config_changed


class Archive(Task):
    """Render the post archives."""

    name = "render_archive"

    def gen_tasks(self):
        kw = {
            "messages": self.site.MESSAGES,
            "translations": self.site.config['TRANSLATIONS'],
            "output_folder": self.site.config['OUTPUT_FOLDER'],
            "filters": self.site.config['FILTERS'],
        }
        self.site.scan_posts()

        # TODO add next/prev links for years
        template_name = "archive.tmpl"

        # TODO: posts_per_year is global, kill it
        for lang in kw["translations"]:
            output_name = os.path.join(
                kw['output_folder'], self.site.path("archive", None, lang))

            context = {"years": []}
            all_posts = []

            for year, posts in list(self.site.posts_per_year.items()):

                post_list = [self.site.global_data[post] for post in posts]
                post_list.sort(key=lambda a: a.date)
                post_list.reverse()
                # file this by year for display
                context["years"].append({"year": year, "posts": post_list})
                # generic_post_list_renderer also wants a list of all of them
                all_posts += post_list

            context["years"].sort(key=lambda a: a['year'], reverse=True)
            context["lang"] = lang
            context["title"] = kw["messages"][lang]["Archive"]
            context["permalink"] = self.site.link("archive", None, lang)

            task = self.site.generic_post_list_renderer(
                lang,
                all_posts,
                output_name,
                template_name,
                kw['filters'],
                context,
            )

            task_cfg = {1: task['uptodate'][0].config, 2: kw}
            task['uptodate'] = [config_changed(task_cfg)]
            task['basename'] = self.name
            yield task
