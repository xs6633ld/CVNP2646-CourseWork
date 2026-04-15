import pytest
from network_monitor import *


@pytest.fixture
def sample_config():
    return NetworkConfig(port_scan_threshold=25, syn_flood_threshold=100)


@pytest.fixture
def valid_packet_line():
    return "192.168.1.5,10.0.0.1,54321,443,TCP,SYN"


@pytest.fixture
def sample_packets():
    return [
        {
            'src_ip': '192.168.1.5',
            'dst_ip': '10.0.0.1',
            'src_port': 54321,
            'dst_port': 443,
            'protocol': 'TCP',
            'flags': 'SYN'
        },
        {
            'src_ip': '192.168.1.5',
            'dst_ip': '10.0.0.1',
            'src_port': 54322,
            'dst_port': 80,
            'protocol': 'TCP',
            'flags': 'SYN'
        }
    ]


# -----------------------------
# Parser Tests
# -----------------------------
def test_parse_valid_packet(valid_packet_line):
    packet = parse_packet_line(valid_packet_line)

    assert packet["src_ip"] == "192.168.1.5"
    assert packet["dst_port"] == 443


def test_parse_invalid_too_few_fields():
    with pytest.raises(ValueError):
        parse_packet_line("1,2,3")


def test_parse_invalid_ports():
    with pytest.raises(ValueError):
        parse_packet_line("1,2,abc,80,TCP,SYN")


def test_parse_empty():
    with pytest.raises(ValueError):
        parse_packet_line("")


def test_parse_whitespace():
    line = " 192.168.1.5 , 10.0.0.1 , 1234 , 80 , TCP , SYN "
    packet = parse_packet_line(line)
    assert packet["src_port"] == 1234


# -----------------------------
# Detection Tests
# -----------------------------
def test_port_scan_below_threshold(sample_packets, sample_config):
    assert detect_port_scan(sample_packets, "192.168.1.5",
                            sample_config.port_scan_threshold) is False


def test_port_scan_above_threshold(sample_config):
    packets = [
        {"src_ip": "192.168.1.5", "dst_port": p, "protocol": "TCP", "flags": ""}
        for p in range(1, 31)
    ]

    assert detect_port_scan(packets, "192.168.1.5",
                            sample_config.port_scan_threshold) is True


def test_syn_flood_detection(sample_config):
    packets = [
        {"src_ip": "192.168.1.5", "protocol": "TCP", "flags": "SYN"}
        for _ in range(150)
    ]

    assert detect_syn_flood(packets, "192.168.1.5",
                            sample_config.syn_flood_threshold) is True


def test_syn_flood_mixed_protocol(sample_config):
    packets = [
        {"src_ip": "192.168.1.5", "protocol": "UDP", "flags": ""}
        for _ in range(200)
    ]

    assert detect_syn_flood(packets, "192.168.1.5",
                            sample_config.syn_flood_threshold) is False


# -----------------------------
# Integration Tests
# -----------------------------
def test_analyze_traffic_full_pipeline(sample_packets, sample_config):
    results = analyze_traffic(sample_packets, sample_config)

    assert "total_packets" in results
    assert results["total_packets"] == len(sample_packets)


def test_analyze_empty(sample_config):
    results = analyze_traffic([], sample_config)

    assert results["total_packets"] == 0
    assert len(results["port_scans"]) == 0