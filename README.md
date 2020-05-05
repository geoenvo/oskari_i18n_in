# English - Bahasa Indonesia Translation (Oskari v1.55.2)


## How to run
The translate.py script will map the translation from the input file to the desired output file.

Example below: translate from `en` language `oskari_lang_en.js` input file to `in` language `oskari_lang_in.js` using the `en_in.txt` translation string mapping file
````
python translate.py -m en_in.txt -idi en -ido in -i oskari_lang_en.js -o output/oskari_lang_in.js
````
