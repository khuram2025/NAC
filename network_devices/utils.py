from netmiko import ConnectHandler

def change_port_vlan(switch, port, vlan):
    device = {
        'device_type': 'cisco_ios',  # Adjust based on your switch type
        'ip': switch.ip_address,
        'username': switch.username,
        'password': switch.password,
    }

    try:
        with ConnectHandler(**device) as conn:
            commands = [
                f'interface {port}',
                f'switchport access vlan {vlan}',
                'exit'
            ]
            output = conn.send_config_set(commands)
        return True, output
    except Exception as e:
        return False, str(e)