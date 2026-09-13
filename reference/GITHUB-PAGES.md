# GitHub Pages setup

The site is configured for **https://luigipacheco.github.io/arc3133/**. The repository is `luigipacheco/arc3133`; its publishing branch is `main`.

## One-time setup

1. Commit and push the prepared site files, including `.github/workflows/pages.yml`, `_data/blender_images.json`, the generated course pages, and `images/blender`.
2. In the repository, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**.
3. In **Actions**, open **Check and deploy course site** and run it on `main` if the push ran before Pages was enabled.
4. Wait for both **build** and **deploy** to pass, then open the URL shown by the deployment.

The workflow builds with GitHub's official Jekyll Pages action. It checks that generated pages match the curriculum, checks local links and image downloads, then uploads only `_site`. A pull request runs the build and checks without deploying. A push to `main` deploys only after the checks pass. No personal access token is required.

GitHub's [publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) describe the repository setting and deployment permissions.

## Before each update

Edit `syllabus/course.yml`, including its release lists, then run:

```text
bundle install
python -m pip install -r scripts/requirements.txt
python scripts/sync_course.py
bundle exec jekyll build
python scripts/verify_course.py
```

Commit the source edits and regenerated pages together. Commit newly created images and Blender downloads as well. The workflow deliberately fails when a source change has not been regenerated.

For a local preview, run `bundle exec jekyll serve` and open `http://127.0.0.1:4000/arc3133/`. Keep `url` and `baseurl` in `_config.yml` unchanged for this project site.

The gallery follows the tutorial release list. Release controls determine which lesson pages and navigation entries appear; they are not access controls for the repository or downloadable assets. All 24 screenshot PNGs are available in `images/blender`, including the ZIP for preparing slides.

Resources offers individual Blender downloads and the supporting point-cloud data. Do not restore the old all-session ZIP; it is retained under `reference/archive` and excluded from the site. Arrays has one session page and one planned tutorial video, with two separate reference files.

The build excludes syllabus sources, instructor references, scripts, earlier code exercises, `slides/src` and dependency folders. Earlier slide decks remain available where linked from the course.
