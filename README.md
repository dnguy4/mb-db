# Millenium Blades DB

## [Website Link](https://dnguy4.github.io/mb-db/)

A wiki for the cards of the board game [Millennium Blades](https://www.level99games.com/products/millennium-blades) by [Level 99 Games](http://www.level99games.com/). This is an unofficial fan-work and is not affliated or endorsed by Level 99 Games. The BGG link of the game is found [here](https://boardgamegeek.com/boardgame/151347/millennium-blades). The site is hosted on Github pages and it was generated using the Pelican static site generator.

# How It Was Made

## Extracting the Images

Using `scripts/xlsx_to_df.py`, I generated an sqlite database from the [card list spreadsheet](https://docs.google.com/spreadsheets/d/15proioQiSmX-JKtzbaeAObBk34xrkMoD83SSPrxRhR0/edit?gid=518044373#gid=518044373) by MyKarato. I then extracted card images from the Tabletop Simulator [mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2646310815).

This was done by first checking my `Tabletop Simulator/Mods/Images` folder. This will contain images from other mods too, so I'd suggest renaming the folder before downloading the mod and opening it in-game. Most the assets will follow a similar resolution and tiling pattern, which is detailed by the `dims` variable within `scripts/extractor.py`.

After extracting the image assets, I used `scripts/batch_test.py` to match the card images to a relevant card from the sqlite database. I tried a couple of libraries to identify the cards, and [keras_ocr](https://keras-ocr.readthedocs.io/en/latest/) worked best for me. This script takes a while to run. I parallelized it a bit; if you have a CUDA GPU, you can run it faster for sure. This `scripts/batch_test.py` mostly classifies the card images if the card name is written at the top of the card. You can run `scripts/find_missing.py` to further identify missing images.

## Making the Website

I was originally planning on making this an actual wiki, but that would cost money and require moderation. I decided to host a static website on Github Pages instead, since that would be free.

Jekyll was considered for generating this website. due to my greater expertise with Python, I settled on using [Pelican](https://getpelican.com/) + [Jinja](https://jinja.palletsprojects.com/en/stable/). Pelaican was a bit tricky to wrap my head around at first, especially with how I wasn't making a blog. I abused the definition of static pages and ended up writing custom HTML instead of markdown. `scripts/generate_pages` was used to generate most of the site pages. These pages were kept outside the content/pages directory in order to not display them on the sidebar of the website along with the about page. THanks to pelicanconf.py letting me define variables for Jinja to use, generating the pages was simple enough.

For my theme, I used the [pelican-fh5co-marble](https://github.com/claudio-walser/pelican-fh5co-marble) theme by [claudio-walser](https://github.com/claudio-walser) as the starting point. I updated the theme to use bootstrap 5 and less custom javascript/css. I'm quite happy with how it responsive it is for the amount of effort I put in.

Lastly, I implemented search via [pelican-search](https://github.com/pelican-plugins/search), which uses [Stork](https://stork-search.net/) internally. I knew I needed search functionality within website. The existance of pelican-search was the deciding point for me to use a static website + pelican. Stork is no longer being actively [developed](https://github.com/jameslittle230/stork/discussions/360). It works great for now, but in the future I might have to swap it. The stork js file is being served by a CDN which may not exist after 2027, according to the Stork developer. I'll have to check in a few years.


# How to Build the Site

1. Clone the repo and the submodule repo, my fork of the pelican-fh5co-marble at the mb-theme [branch](https://github.com/dnguy4/pelican-fh5co-marble/tree/mb-theme).

2. Download the [uv package manager](https://github.com/astral-sh/uv). This will let you install Python if you haven't already.

3. Install the  dependencies. You can do this via uv sync.

4. Create the content/images folder, either by running the extraction + OCR scripts detailed in [the prior section](#Extracting-the-Images) or by downloading the images folder [here](https://github.com/dnguy4/mb-db/tree/gh-pages/images) from my gh-pages branch.

5. Install the stork [plugin](https://stork-search.net/docs/install) for your OS. This will generate the search index so the site can be searched. Once stork is installed, make sure it's added to your path. If `stork --help` works, it is installed and pelican-search should work.

6. If building locally, set the SITEURL to "". Otherwise, set it to the URL where you're going to host the site. In either case, run `scripts/generate_pages`. This will generate the card and set pages within the content folder.

7. Run the website locally using the command `pelican -r -l -t ./pelican-fh5co-marble`. This will generate a `output` folder and host a server hosting that website. With the -l flag, it'll listen to changes and reload live.


## Publishing the Site

This should be done after step 7. You should have your own fork of the repo at this point.

1. When you're ready to publish the site, run `pelican -d -t ./pelican-fh5co-marble/ -s publishconf.py`. This will delete the old content within `output` and build the site using the publishconf settings. Make sure that the siteurl within publishconf matches your hosting site url.

2. Use `ghp-import output -b gh-pages` to generate a new gh-pages branch, using the `output` folder.

3. Run `git push origin gh-pages` to push your gh-pages branch. Make sure your fork has enabled Github pages with the gh-pages as the source. Now it should be live!