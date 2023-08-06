
import uuid

from IPython.display import HTML

from .css_flexbox import CSS


class Flexbox:
    """
    Manages CSS construction, validation, help
    """

    def __init__(self, dic_input):
        """
        Create css from user dic input
        Check against css_standard and fill default values
        """
        dic_css = {}

        for level in ['container', 'item']:

            dic_css[level] = {}
            for e in CSS.dic_struct[level]:
                if e.get('default', None) is not None:
                    dic_css[level][e['name']] = e['default']

            if level in dic_input:
                for k, v in dic_input[level].items():
                    if self.is_valid(k, v, level=level):
                        dic_css[level][k] = v

        # specific flex-flow
        level = 'container'
        dic_css[level]['flex-flow'] = '{} {}'.format(
            dic_css[level]['flex-direction'], dic_css[level]['flex-wrap'])
        dic_css[level].pop('flex-direction')
        dic_css[level].pop('flex-wrap')

        # specific flex
        level = 'item'
        dic_css[level]['flex'] = '{:.2f} {:.2f} {}'.format(
            dic_css[level]['flex-grow'], dic_css[level]['flex-shrink'], dic_css[level]['flex-basis'])
        dic_css[level].pop('flex-grow')
        dic_css[level].pop('flex-shrink')
        dic_css[level].pop('flex-basis')

        self.dic_css = dic_css
        self.build_css()

    def is_valid(self, k, v, level):
        """
        Checks if value v is valid for field k at level leve
        """
        if level in CSS.dic_field:
            dic = CSS.dic_field[level]
        else:
            return False

        if k not in dic:
            # gives transparent access to other CSS fields
            return True

        if 'override' in dic[k]:
            return False

        if 'li_possible' in dic[k]:
            if v in dic[k]['li_possible']:
                return True

        elif dic[k]['type'] in ['int', 'float']:
            val_min = dic[k]['min']
            if v > val_min:
                return True

        elif dic[k]['type'] == 'length':
            if self.is_length_size(v):
                return True

        else:
            return False

    def is_length_size(self, val):
        """
        Checks if string is a css length/size
        ie eg 100px 50% 1.6rem or auto
        """
        val = val.strip()
        for suffix in ['px', '%', 'rem']:
            if val.endswith(suffix):
                val = val.split(suffix)[0]
                if val.isdigit():
                    return True

        if val == 'auto':
            return True

        return False

    def build_css(self):
        """
        Creates css string from css dic
        """
        dic_css = self.dic_css

        uid = uuid.uuid1()
        div_container_start = '.flex-parent-%s {\n' % (uid)
        div_item_start = '.flex-child-%s {\n' % (uid)
        div_end = '}\n'

        level = 'container'
        li_css_container = ['%s: %s;\n' %
                            (k, v) for k, v in dic_css[level].items()]
        css_container = ''.join(li_css_container)
        css_container = div_container_start + css_container + div_end

        level = 'item'
        li_css_item = ['%s: %s;\n' % (k, v) for k, v in dic_css[level].items()]
        css_item = ''.join(li_css_item)
        css_item = div_item_start + css_item + div_end

        css = '<style>\n' + css_container + css_item + '</style>'

        self.uid = uid
        self.css = css



def display_flex(li_content, flexbox=None):
    """
    main function
    similar to IPython.display in use
    but adds flex CSS layout capability

    Default to standard IPython display
    if li_content not a list
    """
    if flexbox is None:
        # default config
        flexbox = Flexbox({})

    if isinstance(li_content, str):
        # fallback to standard display
        return HTML(li_content)

    is_list = isinstance(li_content, list)
    is_all_element_str = all([isinstance(e, str) for e in li_content])
    assert is_list and is_all_element_str, 'First arg must be a list of str (HTML)'

    is_flexbox = isinstance(flexbox, Flexbox)
    assert is_flexbox, 'Second arg must be a Flexbox instance'

    uid = flexbox.uid
    css = flexbox.css

    li_div = ['<div class=flex-child-%s>%s</div>' %
              (uid, content) for content in li_content]
    content = ''.join(li_div)
    html = '<div><div class=flex-parent-%s>%s</div></div>' % (uid, content)
    content = css + html
    return HTML(content)
