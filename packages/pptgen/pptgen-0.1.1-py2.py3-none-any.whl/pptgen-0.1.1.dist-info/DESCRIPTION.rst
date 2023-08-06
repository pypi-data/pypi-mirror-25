PPTGen
======

PPTGen is a library and tool to make PowerPoint presentations from data.

Installation
------------

    pip install pptgen

Usage
-----

PPTGen lets you modify the contents of a PowerPoint presentation based on data.
For example, you can:

- Update charts, images and text from data
- Create a series of slides using a template from spreadsheets or database

**Examples are in `tests/`.** You can run the commands below in the `tests/` directory.

PPTGen takes a YAML configuration file as input.

    pptgen config.yaml

The YAML configuration defines the `source`, `target`, `data` and any number of
rules. Here is a simple configuration that just copies a source PPTX to a
target PPTX without any changes.

```yaml
source: input.pptx           # Default input
target: out-unchanged.pptx   # Default output
```

You can override these parameters using `--source <path>` and `--target <path>`.

    pptgen config.yaml --source input.pptx --target out-cmdline.pptx

### Shapes

In PowerPoint, all shapes have names. To see shape names, select Home tab >
Drawing group > Arrange drop-down > Selection pane. Or press ALT + F10.

![Selection pane](help/selection-pane.png)

To change the shape names, double-click on the name in the selection pane.

### Text

To change the title on the input slide to "New title", use this configuration `config-text.yaml`:

```yaml
source: input.pptx
target: out-text.pptx
change-title:             # This section defines the first change.
                          # (You can replace "change-title" with anything.)
  Title 1:                # Take the shape named "Title 1"
    text: New Title       # Replace its text with "New Title"
```

To *substitute* text instead of replacing the full title -- for example, to just
replace "title" with "heading", and "Old" with "New" use `config-replace.yaml`:

```yaml
source: input.pptx
target: out-replace.pptx
replace-title:                    # The change section can be called anything
  Title 1:                        # Take the shape named "Title 1"
    replace:                      # Replace these keywords
      "Old": "New"                #   Old -> New
      "Title": "Heading"          #   Title -> Heading
```

Replacement only works for words that have the same formatting. For example, in
some_where_, "where" is underlined. You cannot replace "somewhere". But you can
replace "some" and "where" independently.

### Images

To change the picture on an image, use `config-image.yaml`:

```yaml
source: input.pptx
target: out-image.pptx
change-image:
  Picture 1:                      # Take the shape named "Picture 1"
    image: sample.png             # Replace the image with sample.png
```

The image can be a URL or a file path.

### Groups

To change groups' contents, use a nested configuration. For example, if the group
named "Group 1" has text named "Caption" and an image named "Picture", this
`config-group.yaml` replaces those:

```yaml
source: input.pptx
target: out-group.pptx
change-image:
  Group 1:                        # Take the shape named "Group 1"
    Caption:                      # Find the shape named "Caption" inside it
      text: New caption           #   Change its text to "New caption"
    Picture:                      # Find the shape named "Picture" inside it
      image: sample.png           #   Replace the image with sample.png
```

### Data

PPTGen can change presentations with data from various sources. This example
shows all ways of loading data:

```yaml
source: input.pptx
target: out-unchanged.pptx
data:                               # The data section
  cities: {csv: cities.csv}         # Load CSV data into "cities" key
  sales: {xlsx: sales.xlsx, sheet: Sheet1}   # Load Excel sheet into "sales" key
  tweets: {json: tweets.json}       # Load JSON data into "tweets" key
  sample: {yaml: sample.yaml}       # Load YAML data into "config"
  direct: {values: {x: 1, y: 2}}    # The "direct" key takes values directly
```

### Templates

You can use values from the data anywhere, as a template. See
`config-template.yaml`:

```yaml
source: input.pptx
target: out-template.pptx
data:
  tweets: {json: tweets.json}
text-template:
  Title 1:
    text: "Tweet from @{{ tweets[0]['user']['screen_name'] }}"
  Picture 1:
    image: "{{ tweets[0]['user']['profile_image_url'] }}"
```

The values inside `{{ ... }}` are evaluated as Python expressions in the context
of `data`.

### Charts

TBD

### Tables

TBD

### Slides

By default, changes are applied to all slides. To restrict changes to a specific
slide, use one of these:

1. `slide-number` indicates the slide number starting with slide 1.
2. `slide-title` is a regular expression that matches the slide title.

For example, this applies the `change-title` rule only on slide 1.

```yaml
source: input.pptx
target: out-text.pptx
change-title:
  slide-number: 1         # Apply this change only on slide 1
  Title 1:
    text: New title
```

To create multiple slides from data, add `data:` to the change. For example:

```yaml
source: input.pptx
target: out-slides.pptx
data:
  sales: {xlsx: sales.xlsx}
change-title:
  slide-number: 1         # Apply this change only on slide 1
  data: sales             # For each row in sales.xlsx, create a new slide
  Title 1:
    text: "Region {{ region }} has sales of ${{ sales }}"
```

### Layouts

To create multiple shapes using data, use `layout:` and `data:`. For example:

```yaml
source: input.pptx
target: out-layout.pptx
data:
  sales: {xlsx: sales.xlsx}
multiple-objects:
  Picture 1:                          # Take the Picture 1 shape
    data: sales                       # Duplicate it for each row in sales
    layout: horizontal                # Lay the images out horizontally
    image: "{{ region }}.png"         # Change the picture using this template
```

Currently, `layout:` supports `horizontal` and `vertical`. We may extend this to
`grid: [<columns>, <rows>]` and `wrap: <items>`.


Development
-----------

To set up the development environment, clone this repo. Then run:

    pip uninstall pptgen
    pip install -e .

Create a branch for local development using `git checkout -b <branch>`.
Test your changes by running `nosetests`.
Commit your branch and send a merge request.

Release
-------

When releasing a new version of pptgen:

1. Check [build errors](http://code.gramener.com/sanjay.yadav/pptgen/pipelines).
2. Run `make tests` on Python 2.7 and on 3.x
3. Update version number in `pptgen/release.json`
4. Push `dev` branch to the server. Ensure that there are no build errors.
5. Merge with master, create an annotated tag and push the code:

    git checkout master
    git merge dev
    git tag -a v1.x.x           # Annotate with a one-line summary of features
    git push --follow-tags
    git checkout dev            # Switch back to dev

6. Release to PyPi

    python setup.py sdist bdist_wheel --universal
    twine upload dist/*


