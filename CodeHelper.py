import sublime, sublime_plugin
import os
import json

class CodeHelperCommand(sublime_plugin.WindowCommand):
    def init(self):
        settings = sublime.load_settings('CodeHelper.sublime-settings')
        current = settings.get('current')
        projects = settings.get('projects')
        self.prefix = settings.get('prefix')
        self.code_json = getJsonFile(projects[current]['code'])
        self.str_json = getJsonFile(projects[current]['str'])

    def run(self, **args):
        self.init();

        if args['from'] == 'code_string' and \
           args['to'] == 'code_num':
            self.data = getWholeJson(self.code_json, False)
        elif args['from'] == 'code_num' and \
             args['to'] == 'code_string':
            self.data = getWholeJson(self.code_json, True)
        elif args['from'] == 'code_string' and \
             args['to'] == 'code_msg':
            self.data = getWholeJson(self.str_json, False)
        elif args['from'] == 'code_msg' and \
             args['to'] == 'code_string':
            self.data = getWholeJson(self.str_json, True)
        
        self.key_list = getKeyList(self.data)
        if not self.key_list:
            return
        self.window.show_quick_panel(self.key_list, self.on_done)

    def getKey(self, index):
        return str(self.key_list[index])

    def getValue(self, index):
        return str(self.data[self.getKey(index)])

    def on_done(self, index):
        if (index == -1):
            return
        output(self.window, '' + self.getKey(index) + ' --> ' + self.getValue(index))
        

def output(window, text):
    output_view = window.get_output_panel('test')
    output_view.run_command('sublime_code_helper_output_text', {'text': text + '\n' })
    window.run_command("show_panel", {"panel": "output.test"})

class SublimeCodeHelperOutputText(sublime_plugin.TextCommand):
    def run(self, edit, text = None):
        if not text:
            return
        print(self.view.size())
        print(text)
        self.view.insert(edit, self.view.size(), text)

def echo(s):
    sublime.message_dialog(str(s))

def getJsonFile(path) :
    # todo file not exist
    f = open(path)
    content = f.read();
    json_obj = ''
    try:
        json_obj = json.loads(content);
    except Exception:
        echo("Your have syntax error, in file: " + path)
    f.close()
    return json_obj

def getWholeJson(obj, order = True):
    result = {}
    ergodicJson(result, obj, '', order)
    return result

def ergodicJson(result, obj, before, order):
    for key in obj:
        pre_str = ''
        if before:
            pre_str = before + '.'
        whole_key = str.upper(pre_str + key);
        value = obj[key]
        if type(value) == dict:
            ergodicJson(result, value, whole_key, order)
        elif order:
            value = str.capitalize(str(value))
            result[value] = whole_key
        else:
            result[whole_key] = value
   
def getKeyList(dict):
    return list(dict.keys());