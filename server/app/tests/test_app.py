from .. import app
from .. import tasks

class TestApp(object):

    def test_client_config(self, test_app):
        assert len(test_app.clients()) == 2
        
    
    def test_aes(self, test_aes_cipher):
        value = '{"disk":7.3,"cpu":100.0,"memory":56.2}'
        encrypted_value = test_aes_cipher.encrypt(value)
        decrypted_value = test_aes_cipher.decrypt(encrypted_value)

        assert decrypted_value == value


    def test_statistics_collector_get(self, test_stats_collector):
        stats = test_stats_collector.get()
        assert type(stats) is dict
        assert 'cpu' in stats


    def test_collect_statistics_task(self, test_app):
        client = test_app.clients()[0]
        assert tasks.collect_statistics(client) is not None


    def test_dir_exists(self):
        dirs = ['tmp', 'home', 'var']
        assert tasks.dir_exists(dirs, 'tmp') == True
        assert tasks.dir_exists(dirs, 'root') == False

    