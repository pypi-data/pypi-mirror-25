#!python
# coding=utf-8
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Transform a unified diff from stdin to a colored
# side-by-side HTML page on stdout.
#
# Authors: Olivier Matz <zer0@droids-corp.org>
#          Alan De Smet <adesmet@cs.wisc.edu>
#          Sergey Satskiy <sergey.satskiy@gmail.com>
#          scito <info at scito.ch>
#
# Inspired by diff2html.rb from Dave Burt <dave (at) burt.id.au>
# (mainly for html theme)
#
# TODO:
# - The sane function currently mashes non-ASCII characters to "."
#   Instead be clever and convert to something like "xF0"
#   (the hex value), and mark with a <span>.  Even more clever:
#   Detect if the character is "printable" for whatever definition,
#   and display those directly.

import sys, re, htmlentitydefs, getopt, StringIO, codecs, datetime
try:
    from simplediff import diff, string_diff
except ImportError:
    sys.stderr.write("info: simplediff module not found, only linediff is available\n")
    sys.stderr.write("info: it can be downloaded at https://github.com/paulgb/simplediff\n")

# minimum line size, we add a zero-sized breakable space every
# LINESIZE characters
linesize = 20
tabsize = 8
show_CR = False
encoding = "utf-8"
lang = "fr"
algorithm = 0
desc = "File comparison"
dtnow = datetime.datetime.now()
modified_date = "%s+01:00"%dtnow.isoformat()

html_hdr = """<!DOCTYPE html>
<html lang="{5}" dir="ltr"
    xmlns:dc="http://purl.org/dc/terms/">
<head>
    <meta charset="{1}" />
    <meta name="generator" content="diff2html.py (http://git.droids-corp.org/gitweb/?p=diff2html)" />
    <!--meta name="author" content="Fill in" /-->
    <title>HTML Diff{0}</title>
    <link rel="shortcut icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEXAAAAAgAD///+K/HwIAAAAJUlEQVQI12NYBQQM2IgGBQ4mCIEQW7oyK4phampkGIQAc1G1AQCRxCNbyW92oQAAAABJRU5ErkJggg==" type="image/png" />
    <meta property="dc:language" content="{5}" />
    <!--meta property="dc:date" content="{3}" /-->
    <meta property="dc:modified" content="{4}" />
    <meta name="description" content="{2}" />
    <meta property="dc:abstract" content="{2}" />
    <img style="width:180px;height:60px;" class="logo_askida" align="right" src="data:image/png;base64,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">
    <br>
    <br>
    <h1 style="color:black" align="center">R&eacutesultats de la comparaison de fichiers</h1>
    <hr>
    <style>
        a{{ color:#9eb6d4}}
        table{{ align="center"; border:2px #c6bcb3; width: 95%; font-family: Abel, monospace }}
        td.line {{ color:#8080a0 border-bottom: 1px solid #ddd }}
        th {{ padding-left: 20px; border: 1px #c6bcb3; text-align: left; background: #9eb6d4; color: black font-size:3em; font-family: Abel, monospace}}
        tr.diffunmodified td {{ font-size:0.75em; background: #e8e8e8 }}
        tr.diffhunk td {{ font-size:0.75em; background: #c9c2bb }}
        tr.diffadded td {{ font-size:0.75em; background: #e3fce3 }}
        tr.diffdeleted td {{ font-size:0.75em; background: #ffe2e2 }}
        tr.diffchanged td {{ font-size:0.75em; background: #f7f7d7 }}
        span.diffchanged2 {{ background: #e2c483 }}
        span.diffponct {{ color: #B08080 }}
        tr.diffmisc td {{}}
        tr.diffseparator td {{}}
    </style>
</head>
<body>
"""

html_footer = """
<footer>
    <p>Modified at {1}. HTML formatting created by diff2html in collaboration with <a href="https://askida.com/"; a=summary">Askida</a>.    </p>
</footer>
</body></html>
"""

table_hdr = """
		<table class="diff,table">
"""

table_footer = """
</table>
"""

DIFFON = "\x01"
DIFFOFF = "\x02"

buf = []
add_cpt, del_cpt = 0, 0
line1, line2 = 0, 0
hunk_off1, hunk_size1, hunk_off2, hunk_size2 = 0, 0, 0, 0


# Characters we're willing to word wrap on
WORDBREAK = " \t;.,/):-"

def sane(x):
    r = ""
    for i in x:
        j = ord(i)
        if i not in ['\t', '\n'] and (j < 32):
            r = r + "."
        else:
            r = r + i
    return r

def linediff(s, t):
    '''
    Original line diff algorithm of diff2html. It's character based.
    '''
    if len(s):
        s = unicode(reduce(lambda x, y:x+y, [ sane(c) for c in s ]))
    if len(t):
        t = unicode(reduce(lambda x, y:x+y, [ sane(c) for c in t ]))

    m, n = len(s), len(t)
    d = [[(0, 0) for i in range(n+1)] for i in range(m+1)]


    d[0][0] = (0, (0, 0))
    for i in range(m+1)[1:]:
        d[i][0] = (i,(i-1, 0))
    for j in range(n+1)[1:]:
        d[0][j] = (j,(0, j-1))

    for i in range(m+1)[1:]:
        for j in range(n+1)[1:]:
            if s[i-1] == t[j-1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min((d[i-1][j][0] + 1, (i-1, j)),
                          (d[i][j-1][0] + 1, (i, j-1)),
                          (d[i-1][j-1][0] + cost, (i-1, j-1)))

    l = []
    coord = (m, n)
    while coord != (0, 0):
        l.insert(0, coord)
        x, y = coord
        coord = d[x][y][1]

    l1 = []
    l2 = []

    for coord in l:
        cx, cy = coord
        child_val = d[cx][cy][0]

        father_coord = d[cx][cy][1]
        fx, fy = father_coord
        father_val = d[fx][fy][0]

        diff = (cx-fx, cy-fy)

        if diff == (0, 1):
            l1.append("")
            l2.append(DIFFON + t[fy] + DIFFOFF)
        elif diff == (1, 0):
            l1.append(DIFFON + s[fx] + DIFFOFF)
            l2.append("")
        elif child_val-father_val == 1:
            l1.append(DIFFON + s[fx] + DIFFOFF)
            l2.append(DIFFON + t[fy] + DIFFOFF)
        else:
            l1.append(s[fx])
            l2.append(t[fy])

    r1, r2 = (reduce(lambda x, y:x+y, l1), reduce(lambda x, y:x+y, l2))
    return r1, r2


def diff_changed(old, new):
    '''
    Returns the differences basend on characters between two strings
    wrapped with DIFFON and DIFFOFF using `diff`.
    '''
    con = {'=': (lambda x: x),
           '+': (lambda x: DIFFON + x + DIFFOFF),
           '-': (lambda x: '')}
    return "".join([(con[a])("".join(b)) for a, b in diff(old, new)])


def diff_changed_ts(old, new):
    '''
    Returns a tuple for a two sided comparison based on characters, see `diff_changed`.
    '''
    return (diff_changed(new, old), diff_changed(old, new))


def word_diff(old, new):
    '''
    Returns the difference between the old and new strings based on words. Punctuation is not part of the word.

    Params:
        old the old string
        new the new string

    Returns:
        the output of `diff` on the two strings after splitting them
        on whitespace (a list of change instructions; see the docstring
        of `diff`)
    '''
    separator_pattern = '(\W+)';
    return diff(re.split(separator_pattern, old, flags=re.UNICODE), re.split(separator_pattern, new, flags=re.UNICODE))


def diff_changed_words(old, new):
    '''
    Returns the difference between two strings based on words (see `word_diff`)
    wrapped with DIFFON and DIFFOFF.

    Returns:
        the output of the diff expressed delimited with DIFFON and DIFFOFF.
    '''
    con = {'=': (lambda x: x),
           '+': (lambda x: DIFFON + x + DIFFOFF),
           '-': (lambda x: '')}
    return "".join([(con[a])("".join(b)) for a, b in word_diff(old, new)])


def diff_changed_words_ts(old, new):
    '''
    Returns a tuple for a two sided comparison based on words, see `diff_changed_words`.
    '''
    return (diff_changed_words(new, old), diff_changed_words(old, new))


def convert(s, linesize=0, ponct=0):
    i = 0
    t = u""
    for c in s:
        # used by diffs
        if c == DIFFON:
            t += u'<span class="diffchanged2">'
        elif c == DIFFOFF:
            t += u"</span>"

        # special html chars
        elif htmlentitydefs.codepoint2name.has_key(ord(c)):
            t += u"&%s;" % (htmlentitydefs.codepoint2name[ord(c)])
            i += 1

        # special highlighted chars
        elif c == "\t" and ponct == 1:
            n = tabsize-(i%tabsize)
            if n == 0:
                n = tabsize
            t += (u'<span class="diffponct">&raquo;</span>'+'&nbsp;'*(n-1))
        elif c == " " and ponct == 1:
            t += u'<span class="diffponct">&middot;</span>'
        elif c == "\n" and ponct == 1:
            if show_CR:
                t += u'<span class="diffponct">\</span>'
        else:
            t += c
            i += 1

        if linesize and (WORDBREAK.count(c) == 1):
            t += u'&#8203;'
            i = 0
        if linesize and i > linesize:
            i = 0
            t += u"&#8203;"

    return t


def add_comment(s, output_file):
    output_file.write(('<tr class="diffmisc"><td colspan="4">%s</td></tr>\n'%convert(s)).encode(encoding))


def add_filename(f1, f2, output_file):
    output_file.write(("<tr><th colspan='2'>%s</th>"%convert(f1, linesize=linesize)).encode(encoding))
    output_file.write(("<th colspan='2'>%s</th></tr>\n"%convert(f2, linesize=linesize)).encode(encoding))


def add_hunk(output_file, show_hunk_infos):
    if show_hunk_infos:
        output_file.write('<tr class="diffhunk"><td colspan="2">Offset %d, %d lines modified</td>'%(hunk_off1, hunk_size1))
        output_file.write('<td colspan="2">Offset %d, %d lines modified</td></tr>\n'%(hunk_off2, hunk_size2))
    else:
        # &#8942; - vertical ellipsis
        output_file.write('<tr class="diffhunk"><td colspan="2">&#8942;</td><td colspan="2">&#8942;</td></tr>')


def add_line(s1, s2, output_file):
    global line1
    global line2

    orig1 = s1
    orig2 = s2

    if s1 == None and s2 == None:
        type_name = "unmodified"
    elif s1 == None or s1 == "":
        type_name = "added"
    elif s2 == None or s1 == "":
        type_name = "deleted"
    elif s1 == s2:
        type_name = "unmodified"
    else:
        type_name = "changed"
        if algorithm == 1:
            s1, s2 = diff_changed_words_ts(orig1, orig2)
        elif algorithm == 2:
            s1, s2 = diff_changed_ts(orig1, orig2)
        else: # default
            s1, s2 = linediff(orig1, orig2)

    output_file.write(('<tr class="diff%s">' % type_name).encode(encoding))
    if s1 != None and s1 != "":
        output_file.write(('<td class="diffline">%d </td>' % line1).encode(encoding))
        output_file.write('<td class="diffpresent">'.encode(encoding))
        output_file.write(convert(s1, linesize=linesize, ponct=1).encode(encoding))
        output_file.write('</td>')
    else:
        s1 = ""
        output_file.write('<td colspan="2"> </td>')

    if s2 != None and s2 != "":
        output_file.write(('<td class="diffline">%d </td>'%line2).encode(encoding))
        output_file.write('<td class="diffpresent">')
        output_file.write(convert(s2, linesize=linesize, ponct=1).encode(encoding))
        output_file.write('</td>')
    else:
        s2 = ""
        output_file.write('<td colspan="2"></td>')

    output_file.write('</tr>\n')

    if s1 != "":
        line1 += 1
    if s2 != "":
        line2 += 1


def empty_buffer(output_file):
    global buf
    global add_cpt
    global del_cpt

    if del_cpt == 0 or add_cpt == 0:
        for l in buf:
            add_line(l[0], l[1], output_file)

    elif del_cpt != 0 and add_cpt != 0:
        l0, l1 = [], []
        for l in buf:
            if l[0] != None:
                l0.append(l[0])
            if l[1] != None:
                l1.append(l[1])
        max_len = (len(l0) > len(l1)) and len(l0) or len(l1)
        for i in range(max_len):
            s0, s1 = "", ""
            if i < len(l0):
                s0 = l0[i]
            if i < len(l1):
                s1 = l1[i]
            add_line(s0, s1, output_file)

    add_cpt, del_cpt = 0, 0
    buf = []


def parse_input(input_file, output_file, input_file_name, output_file_name,
                exclude_headers, show_hunk_infos):
    global add_cpt, del_cpt
    global line1, line2
    global hunk_off1, hunk_size1, hunk_off2, hunk_size2

    if not exclude_headers:
        title_suffix = ' ' + input_file_name
        output_file.write(html_hdr.format(title_suffix, encoding, desc, "", modified_date, lang).encode(encoding))
    output_file.write(table_hdr.encode(encoding))

    while True:
        l = input_file.readline()
        if l == "":
            break

        m = re.match('^--- ([^\s]*)', l)
        if m:
            empty_buffer(output_file)
            file1 = m.groups()[0]
            while True:
                l = input_file.readline()
                m = re.match('^\+\+\+ ([^\s]*)', l)
                if m:
                    file2 = m.groups()[0]
                    break
            add_filename(file1, file2, output_file)
            hunk_off1, hunk_size1, hunk_off2, hunk_size2 = 0, 0, 0, 0
            continue

        m = re.match("@@ -(\d+),?(\d*) \+(\d+),?(\d*)", l)
        if m:
            empty_buffer(output_file)
            hunk_data = map(lambda x:x=="" and 1 or int(x), m.groups())
            hunk_off1, hunk_size1, hunk_off2, hunk_size2 = hunk_data
            line1, line2 = hunk_off1, hunk_off2
            #add_hunk(output_file, show_hunk_infos) # Val: What is the use of that line? If usefull, please reactivate.
            continue

        if hunk_size1 == 0 and hunk_size2 == 0:
            empty_buffer(output_file)
            #add_comment(l, output_file)#The comments should not be seen by user of Askida. Might be usefull for debugging
            continue

        if re.match("^\+", l):
            add_cpt += 1
            hunk_size2 -= 1
            buf.append((None, l[1:]))
            continue

        if re.match("^\-", l):
            del_cpt += 1
            hunk_size1 -= 1
            buf.append((l[1:], None))
            continue

        if re.match("^\ ", l) and hunk_size1 and hunk_size2:
            empty_buffer(output_file)
            hunk_size1 -= 1
            hunk_size2 -= 1
            buf.append((l[1:], l[1:]))
            continue

        empty_buffer(output_file)
        #add_comment(l, output_file) #The comments should not be seen by user of Askida. Might be usefull for debugging

    empty_buffer(output_file)
    output_file.write(table_footer.encode(encoding))
    if not exclude_headers:
        output_file.write(html_footer.format("", dtnow.strftime("%d.%m.%Y")).encode(encoding))


def usage():
    print '''
diff2html.py [-e encoding] [-i file] [-o file] [-x]
diff2html.py -h

Transform a unified diff from stdin to a colored side-by-side HTML
page on stdout.
stdout may not work with UTF-8, instead use -o option.

   -i file     set input file, else use stdin
   -e encoding set file encoding (default utf-8)
   -o file     set output file, else use stdout
   -x          exclude html header and footer
   -t tabsize  set tab size (default 8)
   -l linesize set maximum line size is there is no word break (default 20)
   -r          show \\r characters
   -k          show hunk infos
   -a algo     line diff algorithm (0: linediff characters, 1: word, 2: simplediff characters) (default 0)
   -h          show help and exit
'''

def main():
    global linesize, tabsize
    global show_CR
    global encoding
    global algorithm

    input_file_name = ''
    output_file_name = ''

    exclude_headers = False
    show_hunk_infos = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:i:o:xt:l:rka:",
                                   ["help", "encoding=", "input=", "output=",
                                    "exclude-html-headers", "tabsize=",
                                    "linesize=", "show-cr", "show-hunk-infos", "algorithm="])
    except getopt.GetoptError, err:
        print unicode(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--encoding"):
            encoding = a
        elif o in ("-i", "--input"):
            input_file = codecs.open(a, "r", encoding)
            input_file_name = a
        elif o in ("-o", "--output"):
            output_file = codecs.open(a, "w")
            output_file_name = a
        elif o in ("-x", "--exclude-html-headers"):
            exclude_headers = True
        elif o in ("-t", "--tabsize"):
            tabsize = int(a)
        elif o in ("-l", "--linesize"):
            linesize = int(a)
        elif o in ("-r", "--show-cr"):
            show_CR = True
        elif o in ("-k", "--show-hunk-infos"):
            show_hunk_infos = True
        elif o in ("-a", "--algorithm"):
            algorithm = int(a)
        else:
            assert False, "unhandled option"

    # Use stdin if not input file is set
    if not ('input_file' in locals()):
        input_file = codecs.getreader(encoding)(sys.stdin)

    # Use stdout if not output file is set
    if not ('output_file' in locals()):
        output_file = codecs.getwriter(encoding)(sys.stdout)

    parse_input(input_file, output_file, input_file_name, output_file_name,
                exclude_headers, show_hunk_infos)

def parse_from_memory(txt, exclude_headers, show_hunk_infos):
    " Parses diff from memory and returns a string with html "
    input_stream = StringIO.StringIO(txt)
    output_stream = StringIO.StringIO()
    parse_input(input_stream, output_stream, '', '', exclude_headers, show_hunk_infos)
    return output_stream.getvalue()


if __name__ == "__main__":
    main()
