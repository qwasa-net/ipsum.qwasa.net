import ipsum


def application(env, start_response):

    output = ipsum.make_all_texts(n=13, m=8)

    if '.json' in env.get('REQUEST_URI', ''):
        ct = "application/json; charset=utf-8"
        data = ipsum.output_json(output)
    else:
        ct = "text/html; charset=utf-8"
        data = ipsum.output_html(output)

    start_response('200 OK', [('Content-Type', ct), ('Cache-Control', 'no-cache')])
    return [bytes(data, encoding="utf-8", errors="ignore")]
