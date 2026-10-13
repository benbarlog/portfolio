"""Render every page to plain HTML in docs/ so the site can be hosted on GitHub Pages.

Usage: python manage.py build_static_site
"""
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import Client, override_settings
from django.urls import reverse, set_script_prefix

PAGES = ['home', 'about', 'experience', 'projects', 'resume', 'contact']

# GitHub Pages serves a project site at https://<user>.github.io/<repo-name>/
SITE_PREFIX = '/portfolio-website/'


class Command(BaseCommand):
    help = 'Export the site as static HTML into docs/ for GitHub Pages.'

    def handle(self, *args, **options):
        out_dir = Path(settings.BASE_DIR) / 'docs'
        if out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir()

        with override_settings(STATIC_URL=SITE_PREFIX + 'static/', ALLOWED_HOSTS=['testserver']):
            client = Client()
            for name in PAGES:
                # Reverse without the prefix to get the path the client should request,
                # then render with the prefix so links in the page point under /<repo-name>/.
                set_script_prefix('/')
                path = reverse(name)
                set_script_prefix(SITE_PREFIX)
                response = client.get(path)
                page_dir = out_dir / path.lstrip('/')
                page_dir.mkdir(parents=True, exist_ok=True)
                (page_dir / 'index.html').write_bytes(response.content)
                self.stdout.write(f'Wrote {page_dir / "index.html"}')

        shutil.copytree(Path(__file__).resolve().parents[2] / 'static', out_dir / 'static')
        # Tell GitHub Pages not to run the files through Jekyll.
        (out_dir / '.nojekyll').touch()
        self.stdout.write(self.style.SUCCESS(f'Static site built in {out_dir}'))
