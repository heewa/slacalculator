#!/usr/bin/env python
import json
import logging

from flask import Flask, request

from calc import find_and_calc


app = Flask(__name__)


# To make debugging easier, accept both GET & POST.
@app.route('/slack_message', methods=['GET', 'POST'])
def slack_message():
    results = find_and_calc(request.args.get('text', request.form.get('text', '')))
    if results:
        response = {
            'text': '\n'.join(
                '`%s = %s`' % (formula, result)
                for formula, result in results
            )
        }
    else:
        response = {'msg': 'No formulas found.'}

    return json.dumps(response)


if __name__ == '__main__':
    app.run(debug=False)
