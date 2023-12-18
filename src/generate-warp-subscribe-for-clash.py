import copy

import confutilPPP
import pandas as pd
import yaml


def get_ip_port_s(_csv_file):
    try:
        ip_port_s_: (str, str) = []
        df = pd.read_csv(csv)
        # 遍历DataFrame
        for index in range(len(df)):
            # 获取每一行的数据
            row = df.iloc[index]
            ip_port = row['IP:PORT']
            # 提取ip和port
            ip = ip_port.split(':')[0]
            port = ip_port.split(':')[1]
            ip_port_s_.append((ip, port))
        return ip_port_s_
    except Exception as e:
        print(e)
        return None


def get_template_config(_template_config_file='./template/config.yml'):
    try:
        with open(_template_config_file, 'r', encoding='utf-8') as f:
            config_ = yaml.load(f.read(), Loader=yaml.FullLoader)
            return config_
    except Exception as e:
        print(e)
        return None


def build_configuration(_template_config: dict, _ip_port_s: (), _private_key: str, _public_key: str,
                        _config_name: str,
                        _ipv6: str, _ip: str = '172.16.0.100', _nodes_count: int = 16):
    try:
        # name
        name = 'WARP-{}'
        nodes = []
        for i, j in enumerate(_ip_port_s):
            node = {
                'name': name.format(i),
                'type': 'wireguard',
                'server': j[0],
                'port': int(j[1]),
                'ip': _ip,
                'ipv6': _ipv6,
                'public-key': _public_key,
                'private-key': _private_key,
                'mtu': 1280,
                'udp': True,
                'dns': ['1.1.1.1', '223.5.5.5']
            }
            tmp_node = copy.deepcopy(node)
            nodes.append(tmp_node)
            if i >= _nodes_count - 1:
                break

        config = copy.deepcopy(_template_config)
        config['proxies'] = copy.deepcopy(nodes)

        proxy_groups = config['proxy-groups']
        for i, j in enumerate(proxy_groups):
            if '节点选择' in j['name'] or '自动选择' in j['name']:
                for k in range(_nodes_count):
                    proxy_groups[i]['proxies'].append(name.format(k))

        # 保存配置文件
        with open(f'../config/{_config_name}.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        exit(0)


if __name__ == '__main__':
    template_node = {
        'private-key': '',
        'public-key': '',
        'config-name': '',
        'ipv6': '',
        'ip': '172.16.0.100',
        'nodes_count': 16
    }
    conf = [template_node]
    # 读取模板配置文件
    template_config_file = './template/config.yml'
    template_config = get_template_config(template_config_file)

    # 读取CSV文件
    csv = 'C:\\Users\\Administrator\\Desktop\\联网\\WARP\\Warp工具箱-优选端点\\result.csv'
    ip_port_s = get_ip_port_s(csv)

    node_s = confutilPPP.check_config(conf)

    for i in node_s:
        config_name = i['config-name']
        print(f'生成 {config_name} 配置文件中...')
        build_configuration(template_config, ip_port_s, i['private-key'], i['public-key'], i['config-name'], i['ipv6'],
                            i['ip'], i['nodes_count'])
        print(f'生成 {config_name} 配置文件成功！')
        print(
            f'{config_name} 配置文件链接: https://mirror.ghproxy.com/https://raw.githubusercontent.com/aurorax-neo/vpn-subscribe/vpn-subscribe/config/{i["config-name"]}.yml')
