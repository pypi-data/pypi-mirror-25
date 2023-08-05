"""
End-to-end test with fake remote and microserver APIs
"""
from __future__ import absolute_import, print_function, unicode_literals

import responses


@responses.activate
def test_readme_example(monkeypatch):
    from zenaton.testing.examples.readme import main

    monkeypatch.setenv('ZENATON_APP_ID', 'APP_ID')
    monkeypatch.setenv('ZENATON_APP_ENV', 'APP_ENV')
    monkeypatch.setenv('ZENATON_API_TOKEN', 'API_TOKEN')
    monkeypatch.delenv('ZENATON_BASE_URL', raising=False)

    responses.add(
        responses.POST,
        'https://zenaton.com/api/instances',
        status=200,
        json={
            'msg': 'workflow zenaton.testing.examples.readme:MyWorkflow launched',
            'custom_id':'4zwjxjp0axwk4os0',
            'instance_id':'4zwjxjp0axwk4os0-pc132y8aflcs88g',
        },
    )

    main()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'https://zenaton.com/api/instances?api_token=API_TOKEN&app_env=APP_ENV&app_id=APP_ID'
