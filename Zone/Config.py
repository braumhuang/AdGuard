# coding=utf-8
from pathlib import Path
import os

ip_port = '127.0.0.1:7890'

proxy_server = '--proxy-server={}'.format(ip_port)

header_accept = 'text/html,application/xhtml+xml,application/xml;' \
                'q=0.9,image/avif,image/apng,*/*;' \
                'q=0.8,application/signed-exchange;v=b3;q=0.9'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/109.0.0.0 Safari/537.36'

cookie = 'notified_popup_id=%2C76; ixd_lastclick=6828,1713104716; uid=nsRrmsoDQZlsQMBzqScZ; suid=nsRrmsoDQZlsQMBzqScZ; ' \
         'i3_ab=212c5726-f722-43a0-801f-44b65c950ad3; rieSh3Ee_ga=GA1.1.2136454605.1713104716; ' \
         '_gcl_au=1.1.2051942765.1713104716; _yjsu_yjad=1713104716.9a8f1b25-c7c1-4056-96e5-9020cb90cecc; ' \
         '_dga=GA1.3.2136454605.1713104716; age_check_done=1; _ga=GA1.3.1615602644.1713104740; ' \
         'adpf_uid=JUKcNpeZKfFCLLhA; _tt_enable_cookie=1; _ttp=ec95OYx8GzkBVJg1HNi4dIdbbwM; ' \
         'digital[play_bitrate]=FullHD%20(1080p); guest_id=BApcVA9MVV9BUFwL; digital[play_muted]=1; ' \
         'digital[play_volume]=0.5; ckcy=1; cto_bundle=yPopAV9xdXpuJTJCMk9XcCUyQjNzejVrTnBlTUVNV0JUZ3psNU1FT0VnMzdIeVFtS' \
         'TFrN3ZQRnFhbm9tWFhiSjVEU1ZlOGM4Z3lSdzVVcTllQml2dGdwNVlKeGhicEtxRDlmQUVlTEFTVjhkcUtoYjEyZkV6VCUyRll5aWtxZlRrTU' \
         'JraHhWSEpSWUtZJTJCYkJaVTZOTkxCR0syZWVVbzdPdyUzRCUzRA; rieSh3Ee_ga_KQYE0DE5JW=GS1.1.1714109222.5.0.1714109222.0.0.2078636295'

header = {
    'accept': header_accept,
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh,en;q=0.9,zh-CN;q=0.8',
    'user-agent': user_agent,
    'cookie': cookie
}

proxies = {
    'http': 'http://{}'.format(ip_port),
    'https': 'http://{}'.format(ip_port),
}

root_path = Path(__file__).parent.parent

qxc_path = os.path.join(root_path, 'QuantumultX\Winston.qxc')

if __name__ == '__main__':
    print(qxc_path)