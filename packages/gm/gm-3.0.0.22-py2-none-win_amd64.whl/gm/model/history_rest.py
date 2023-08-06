import datetime
import requests

from gm.constant import HISTORY_REST_ADDR
from gm.csdk.c_sdk import py_gmi_get_serv_addr


class HistoryRestApi(object):
    HISTORY_TICKS_URL = '/v3/data-history/ticks'
    HISTORY_BARS_URL = '/v3/data-history/bars'
    HISTORY_N_TICKS_URL = '/v3/data-history/ticks-n'
    HISTORY_N_BARS_URL = '/v3/data-history/bars-n'

    def __init__(self):
        addr = (py_gmi_get_serv_addr(HISTORY_REST_ADDR))
        if isinstance(addr, bytes):
            addr = bytes.decode(addr)
        self.base_url = 'http://{}'.format(addr)

    def get_history_bars(self, symbols, frequency, start_time, end_time, fields=None,
                         skip_suspended=True, fill_missing=None, adjust='pre', df=False):

        data = {'symbols': symbols,
                'frequency': frequency,
                'start_time': start_time,
                'end_time': end_time,
                'fields': fields,
                'skip_suspended': skip_suspended,
                'fill_missing': fill_missing,
                'adjust': adjust
                }

        try:
            url = self.base_url + HistoryRestApi.HISTORY_BARS_URL
            data = requests.get(url, params=data)
            data = data.json()
            data = data['data']
            for info in data:
                if info.get('eob'):
                    info['eob'] = datetime.datetime.strptime(info['eob'], '%Y-%m-%dT%H:%M:%S.000Z')
                if info.get('bob'):
                    info['bob'] = datetime.datetime.strptime(info['bob'], '%Y-%m-%dT%H:%M:%S.000Z')
            return data
        except Exception:
            raise ValueError


if __name__ == '__main__':
    a = HistoryRestApi()
    print (a.get_history_bars(symbols='SHSE.000300', frequency='1d', start_time='2017-04-11', end_time='2017-05-21', fields='close,eob,bob'))