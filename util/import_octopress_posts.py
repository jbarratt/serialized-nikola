#!/usr/bin/env python

import sys
import os
import glob
import re


def octo_parse(octo_post):
    """
        Input: an octopress post
        Output: a tuple of (dict of metadata, string of body)
    """
    fm_count = 0
    meta = {}
    body = []

    with open(octo_post, 'r') as f:
        for l in f.readlines():
            if fm_count >= 2:
                # everything after frontmatter is body
                body.append(l)
            elif re.match('^\s*-+\s*$', l):
                # YAML frontmatter marker
                fm_count = fm_count + 1
            else:
                # I'm only interested in date and title from
                # Octopress frontmatter. Others may want more.
                m = re.match('^\s*(date|title): (.*?)$', l)
                if m:
                    (key, value) = m.groups()
                    meta[key] = value.strip('" ')

        # Pull the date out of the filename
        m = re.search('(\d{4})-(\d{2})-(\d{2})-(.*?).markdown', octo_post)
        if m:
            (year, month, day, slug) = m.groups()
            if "date" not in meta:
                # if it has a date, it's better, because it has time
                # if not make something up
                meta['date'] = "%s/%s/%s 13:37" % (year, month, day)
            else:
                meta['date'] = meta['date'].replace('-', '/')
            meta['slug'] = slug
            meta['year'] = year
            meta['month'] = month
        else:
            print "warning, can't get slug from %s" % octo_post
        return (meta, ''.join(body))


def nikola_save(np_dir, meta, body):
    """
        Input: directory for posts
               metadata hash
               body text

        .. title: How to make money
        .. slug: how-to-make-money
        .. date: 2012/09/15 19:52:05
        .. tags:
        .. link:
        .. description:
    """

    newdir = "%s/%s/%s/%s" % (np_dir, meta['year'], meta['month'], meta['slug'])
    # make this an index so we end up with YYYY/MM/<slug>/index.html
    meta['slug'] = 'index'
    try:
        os.makedirs(newdir)
    except OSError:
        pass

    newfile = "%s/index.md" % (newdir)
    with open(newfile, 'w') as f:
        f.write('<!--\n')
        for key in ['title', 'date', 'slug']:
            f.write('.. %s: %s\n' % (key, meta[key]))
        for key in ['tags', 'link', 'description']:
            f.write('.. %s:\n' % key)
        f.write('-->\n')
        f.write('\n%s' % body)


def main():
    """
        Input: octopress posts directory
        Output: nikola posts directory

        For each file
            * strip the yaml front matter
            * parse the file name to fill in missing bits of the front matter
            * fill in nikola front matter
            * rename from YYYY-MM-DD-<slug>.markdown to YYYY/MM/<slug>.md
    """
    op_dir = sys.argv[1]
    np_dir = sys.argv[2]

    for op_file in glob.glob('%s/*.markdown' % op_dir):
        (meta, body) = octo_parse(op_file)
        nikola_save(np_dir, meta, body)


if __name__ == '__main__':
    main()
