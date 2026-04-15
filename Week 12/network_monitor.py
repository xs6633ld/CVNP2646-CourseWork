import argparse
import logging
import sys
import json
from pathlib import Path


class NetworkConfig:
    """Configuration for network traffic analysis."""

    # Threshold for detecting port scanning (unique destination ports)
    DEFAULT_PORT_SCAN_THRESHOLD = 25

    # Threshold for detecting SYN flood attacks (number of SYN packets)
    DEFAULT_SYN_FLOOD_THRESHOLD = 100

    # Packet rate threshold (reserved for future use)
    DEFAULT_PACKET_RATE_THRESHOLD = 1000

    def __init__(self, port_scan_threshold=None, syn_flood_threshold=None):
        """Initialize config with optional overrides."""
        self.port_scan_threshold = port_scan_threshold or self.DEFAULT_PORT_SCAN_THRESHOLD
        self.syn_flood_threshold = syn_flood_threshold or self.DEFAULT_SYN_FLOOD_THRESHOLD


# -----------------------------
# Logging
# -----------------------------
def setup_logging(log_file="network_monitor.log", log_level="INFO") -> logging.Logger:
    """Configure logging with file and console handlers."""
    logger = logging.getLogger("network_monitor")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# -----------------------------
# Pure Functions
# -----------------------------
def parse_packet_line(line: str) -> dict:
    """Parse CSV packet line into dictionary."""
    if not line or not line.strip():
        raise ValueError("Empty line")

    parts = [p.strip() for p in line.split(",")]

    if len(parts) != 6:
        raise ValueError("Invalid field count")

    src_ip, dst_ip, src_port, dst_port, protocol, flags = parts

    try:
        src_port = int(src_port)
        dst_port = int(dst_port)
    except ValueError:
        raise ValueError("Ports must be numeric")

    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol.upper(),
        "flags": flags.upper()
    }


def is_syn_packet(packet: dict) -> bool:
    """Check if packet is TCP SYN."""
    return packet.get("protocol") == "TCP" and "SYN" in packet.get("flags", "")


def detect_port_scan(packets: list, src_ip: str, threshold: int) -> bool:
    """Detect port scanning activity."""
    ports = {
        pkt["dst_port"]
        for pkt in packets
        if pkt.get("src_ip") == src_ip
    }
    return len(ports) > threshold


def detect_syn_flood(packets: list, src_ip: str, threshold: int) -> bool:
    """Detect SYN flood attack."""
    syn_count = sum(
        1 for pkt in packets
        if pkt.get("src_ip") == src_ip and is_syn_packet(pkt)
    )
    return syn_count > threshold


# -----------------------------
# I/O Functions
# -----------------------------
def load_traffic_log(filepath: str) -> list:
    """Load and parse traffic log file."""
    logger = logging.getLogger("network_monitor")
    packets = []

    try:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    packet = parse_packet_line(line.strip())
                    packets.append(packet)
                    logger.debug("Parsed packet: %s", packet)
                except ValueError:
                    logger.error("Parse error at line %d", line_num)
    except FileNotFoundError:
        logger.error("File not found: %s", filepath)
        raise
    except PermissionError:
        logger.error("Permission denied: %s", filepath)
        raise

    logger.info("Loaded %d packets", len(packets))
    return packets


def analyze_traffic(packets: list, config: NetworkConfig) -> dict:
    """Analyze packets for suspicious activity."""
    logger = logging.getLogger("network_monitor")

    results = {
        "total_packets": len(packets),
        "port_scans": [],
        "syn_floods": []
    }

    src_ips = {pkt["src_ip"] for pkt in packets}

    for ip in src_ips:
        if detect_port_scan(packets, ip, config.port_scan_threshold):
            logger.warning("Port scan detected from %s", ip)
            results["port_scans"].append(ip)

        if detect_syn_flood(packets, ip, config.syn_flood_threshold):
            logger.warning("SYN flood detected from %s", ip)
            results["syn_floods"].append(ip)

    logger.info("Analysis complete")
    return results


# -----------------------------
# CLI
# -----------------------------
def create_parser() -> argparse.ArgumentParser:
    """Create CLI parser."""
    parser = argparse.ArgumentParser(
        description="Network Traffic Monitor",
        epilog="Example: %(prog)s traffic.log -o results.json -v"
    )

    parser.add_argument("input_file", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("results.json"))
    parser.add_argument("-p", "--port-scan-threshold", type=int, default=25)
    parser.add_argument("-s", "--syn-flood-threshold", type=int, default=100)
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
    parser.add_argument("-v", "--verbose", action="store_true")

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate CLI arguments."""
    if not args.input_file.exists():
        raise FileNotFoundError(f"Input file not found: {args.input_file}")

    if not args.input_file.is_file():
        raise ValueError("Input path must be a file")

    if args.port_scan_threshold < 1 or args.syn_flood_threshold < 1:
        raise ValueError("Thresholds must be positive")

    if args.verbose:
        args.log_level = "DEBUG"


# -----------------------------
# MAIN
# -----------------------------
def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        validate_args(args)

        logger = setup_logging(log_level=args.log_level)
        logger.info("Network Monitor starting")

        config = NetworkConfig(
            port_scan_threshold=args.port_scan_threshold,
            syn_flood_threshold=args.syn_flood_threshold
        )

        packets = load_traffic_log(str(args.input_file))
        results = analyze_traffic(packets, config)

        # Write JSON output
        with open(args.output, "w") as f:
            json.dump(results, f, indent=4)

        logger.info("Results written to %s", args.output)

        print("\n✓ Analysis complete")
        print(f"  Total packets: {results['total_packets']}")
        print(f"  Port scans: {len(results['port_scans'])}")
        print(f"  SYN floods: {len(results['syn_floods'])}")

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())