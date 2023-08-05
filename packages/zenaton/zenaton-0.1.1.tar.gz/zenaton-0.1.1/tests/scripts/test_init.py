from __future__ import absolute_import, print_function, unicode_literals

from zenaton.testing.compat import MagicMock, patch


@patch('sys.exit')
@patch('zenaton.scripts.init.init_microserver')
@patch('zenaton.scripts.init.setup_logging')
def test_main(mock_setup_logging, mock_init, mock_exit):
    from zenaton.scripts.init import main

    main([])

    mock_setup_logging.assert_called_once_with(debug=False, verbose=False)
    mock_init.assert_called_once_with(base_url=None)
    mock_exit.assert_called_once_with(0)


@patch('sys.exit')
@patch('zenaton.scripts.init.init_microserver')
@patch('zenaton.scripts.init.setup_logging')
def test_main_override_url(mock_setup_logging, mock_init, mock_exit):
    from zenaton.scripts.init import main

    main(['--microserver-url=http://localhost:4002/'])

    mock_setup_logging.assert_called_once_with(debug=False, verbose=False)
    mock_init.assert_called_once_with(base_url='http://localhost:4002/')
    mock_exit.assert_called_once_with(0)


@patch('sys.exit')
@patch('zenaton.scripts.init.init_microserver')
@patch('zenaton.scripts.init.setup_logging')
def test_main(mock_setup_logging, mock_init, mock_exit):
    from zenaton.scripts.init import main

    mock_init.side_effect = RuntimeError

    main([])

    mock_exit.assert_called_once_with(1)


@patch('zenaton.scripts.init.MicroserverAPI')
@patch('zenaton.scripts.init.Config')
def test_init_microserver(mock_config_class, mock_microserver_class):
    from zenaton.scripts.init import init_microserver

    mock_config_class.return_value.to_dict.return_value = {'foo': 'bar'}

    mock_microserver_instance = MagicMock()
    mock_microserver_class.return_value = mock_microserver_instance

    init_microserver(base_url='http://localhost:4002/')

    mock_microserver_class.assert_called_once_with(
        base_url='http://localhost:4002/',
    )
    mock_microserver_instance.send_config.assert_called_once_with(
        config={'foo': 'bar'}
    )
