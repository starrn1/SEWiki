import argparse
import pypandoc
import os
import webbrowser
import config

def convert(file):
    output = file[:-3]
    file = os.path.join(config.CONTENT_DIR, file)
    pypandoc.convert_file(file, 'pdf', outputfile="content/pdf/" + output + ".pdf")
    abspath = os.path.abspath(config.CONTENT_DIR + "/pdf/"  + output + ".pdf")
    webbrowser.get(config.BROWSER_PATH).open_new_tab(abspath)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pdf', help='PDF Conversion')
args = parser.parse_args()
if args.pdf is not None:
    convert(args.pdf)

