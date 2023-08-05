# -*- coding: utf-8 -*-

def archy( obj, prefix='', unicode=True):
    def chr(s):
        chars = {'\u000d' : '\n',
                 '\u2502' : '|',
                 '\u2514' : '`',
                 '\u251c' : '+',
                 '\u2500' : '-',
                 '\u252c' : '-'}
        if not unicode:
            return chars[s]
        return s

    if type(obj) == str:
        obj = { 'label': obj}

    nodes = []
    if 'nodes' in obj:
        nodes = obj['nodes']

    lines = ''
    if 'label' in obj:
        lines = obj['label']
    lines = lines.split('\n')

    splitter = '\n' + prefix + '  '
    if len(nodes) > 0:
        splitter = '\n' + prefix + chr('\u2502') + ' '

    def mapNodes(nodes):
        out = []
        for i, node in enumerate(nodes):
            last = i == len(nodes) -1
            more = ('nodes' in node) and len(node['nodes']) 
            prefix_ = prefix + chr('\u2502') + ' '
            if last:
                prefix_ = prefix + '  '

            outs = (prefix +
                    (chr('\u2514') if last else chr('\u251c')) + chr('\u2500') +
                    (chr('\u252c') if more else chr('\u2500')) + ' ' +
                    archy(node, prefix=prefix_, unicode=unicode)[len(prefix) + 2:])
            out.append(outs)
            
        return ''.join(out)
        
    out = prefix + splitter.join(lines) + '\n' + mapNodes(nodes)

    return out
