import sys

code = open("sanskrit-hyphenation.tex").read()
tpl = open("package.tpl").read()

print("% This file was mechanically generated, don't edit it!")
sys.stdout.write(tpl.replace("$CODE", code))
