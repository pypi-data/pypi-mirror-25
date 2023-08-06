# djangocms-fullslider

Full page slider plugin for Django CMS

djangocms-fullslider uses [Vegas Background Slider](https://vegas.jaysalvat.com/)([MIT License](https://github.com/jaysalvat/vegas/blob/master/LICENSE.md)) inside.

## How to use pugin

1. Install through pip:

```bash
pip install djangocms-fullslider
```

2. Add `djangocms_fullslider` to your `INSTALLED_APPS` setting

3. Enjoy Fullpage Slider in placeholder

Plugin settings description could be found at [Vegas settings documentation](http://vegas.jaysalvat.com/documentation/settings/)


## Customize css and js locations

You can declare `FULLSLIDER` variable in your django settings with following optional fields:

* `JS_URL` - specify URL to custom Vegas JS file. By default value is `STATIC_URL + 'djangocms_fullslider/js/vegas.min.js'`

* `CSS_URL` - specify URL to custom Vegas CSS file. By default value is `STATIC_URL + 'djangocms_fullslider/css/vegas.min.css'`

So, your final config could looks like:

```python
FULLSLIDER = {
    "JS_URL": "<URL TO YOUR CUSTOM VEGAS JS>",
    "CSS_URL": "<URL TO YOUR CUSTOM VEGAS CSS>"
}
```

## Development procedures

Ensure that all python sources contain license notice:

```bash
./development/copyright-update
```

Building distribution package:

```bash
./build.sh clean build
```

Uploading package to PyPi:

```bash
./build.sh publish
```
