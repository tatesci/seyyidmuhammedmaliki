# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(open(1,'wb'), encoding='utf-8', errors='replace')
tpl = io.open('lib_template.html', encoding='utf-8').read()
data = io.open('library.json', encoding='utf-8').read()
assert '__DATA__' in tpl
out = tpl.replace('__DATA__', data)
io.open('lib.html', 'w', encoding='utf-8').write(out)
print('lib.html  %.2f MB' % (os.path.getsize('lib.html')/1048576))
