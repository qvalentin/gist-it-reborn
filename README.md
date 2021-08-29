# Gist-it Reborn

Embed any code from GitHub in your website just like a gist.

Based on this original [Repo](https://github.com/robertkrimen/gist-it), but quickly and dirtily rewritten in Python 3 using [Pygments](https://pygments.org/).

# Usage

Add the following snippet to your html or markdown to have the code be placed at that position.

```html

<script src="https://example.com/https://github.com/qvalentin/gist-it-reborn/blob/main/server.py"></script>

```

### Config

#### style

With the style query parameter you can select a highlighting style. A preview of possible values can be found [here](https://help.farbox.com/pygments.html).

Just append the query parameter `style` to the url.

```html
https://example.com/https://github.com/qvalentin/gist-it-reborn/blob/main/server.py?style=monokai

```

#### Selecting lines

You can choose to only show certain lines of the code. The parameter `slice` can be given in the format `from:to`.

```html
https://example.com/https://github.com/qvalentin/gist-it-reborn/blob/main/server.py?slice=5:20

```





