import json
import re


class ExManager:
    # todo: fix ugly hack
    try:
        with open('../regexes/expressions.json') as fh:
            expressions = json.load(fh)
    except:
        import ekphrasis.regexes.generate_expressions
        with open('../regexes/expressions.json') as fh:
            expressions = json.load(fh)

    def get_compiled(self):
        regexes = {k.lower(): re.compile(self.expressions[k]) for k, v in
                   self.expressions.items()}
        return regexes

    def print_expressions(self):
        {print(k.lower(), ":", self.expressions[k]) for k, v in
         sorted(self.expressions.items())}
