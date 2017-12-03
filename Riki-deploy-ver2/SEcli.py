import argparse
import pypandoc
import os
import webbrowser
import config

def convert(file):
    output = file[:-3]
    file = os.path.join(config.CONTENT_DIR, file)
    if os.path.isfile(file):
        pypandoc.convert_file(file, 'pdf', outputfile="content/pdf/" + output + ".pdf")
        abspath = os.path.abspath(config.CONTENT_DIR + "/pdf/"  + output + ".pdf")
        webbrowser.get(config.BROWSER_PATH).open_new_tab(abspath)
        return "PDF conversion was successful."
    else:
        return "The given file does not exist."

def smartDelete(file):
    fileSplit = file.split('.')
    if (fileSplit[1] == "pdf"):
        file = os.path.join(config.CONTENT_DIR + "/pdf/", file)
        if os.path.isfile(file):
            os.remove(file)
            return "The PDF file was successfully deleted."
        else:
            return "The given PDF file does not exist."
    elif (fileSplit[1] == "md"):
        file = os.path.join(config.CONTENT_DIR, file)
        if os.path.isfile(file):
            pdfFile = os.path.join(config.CONTENT_DIR + "/pdf/", fileSplit[0] + ".pdf")
            if (os.path.isfile(pdfFile)):
                os.remove(pdfFile)
                os.remove(file)
                return "Both the markdown and its corresponding PDF file were deleted."
            else:
                os.remove(file)
                return "The markdown file was successfully deleted."
        else:
            return "The given markdown file does not exist."
    else:
        return "Please enter an existing PDF or markdown file name."

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pdf', help='PDF Conversion')
parser.add_argument('-d', '--delete', help='File deletion')
args = parser.parse_args()
if args.pdf is not None:
    print(convert(args.pdf))

if args.delete is not None:
    print(smartDelete(args.delete))

