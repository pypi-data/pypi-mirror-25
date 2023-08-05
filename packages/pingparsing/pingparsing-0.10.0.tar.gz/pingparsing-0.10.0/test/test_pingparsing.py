# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import itertools

from pingparsing import EmptyPingStatisticsError
import pytest
import six

from .common import (
    PING_DEBIAN_SUCCESS,
    ping_parser,
)


@pytest.fixture
def ping_text():
    return six.b("""
PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
""")


PING_DEBIAN_UNREACHABLE_0 = """
PING 192.168.207.100 (192.168.207.100) 56(84) bytes of data.

--- 192.168.207.100 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4009ms
"""
PING_DEBIAN_UNREACHABLE_1 = PING_DEBIAN_UNREACHABLE_0 + "\n"
PING_DEBIAN_UNREACHABLE_2 = PING_DEBIAN_UNREACHABLE_1 + "\n"
PING_DEBIAN_UNREACHABLE_3 = PING_DEBIAN_UNREACHABLE_0 + "\npipe 4\n"

PING_FEDORA_LOSS = six.b("""
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.

--- 192.168.0.1 ping statistics ---
1688 packets transmitted, 1553 received, +1 duplicates, 7% packet loss, time 2987ms
rtt min/avg/max/mdev = 0.282/0.642/11.699/0.699 ms, pipe 2, ipg/ewma 1.770/0.782 ms
""")
PING_FEDORA_UNREACHABLE = """
PING 192.168.207.100 (192.168.207.100) 56(84) bytes of data.
From 192.168.207.128 icmp_seq=1 Destination Host Unreachable
From 192.168.207.128 icmp_seq=2 Destination Host Unreachable
From 192.168.207.128 icmp_seq=3 Destination Host Unreachable
From 192.168.207.128 icmp_seq=4 Destination Host Unreachable
From 192.168.207.128 icmp_seq=5 Destination Host Unreachable

--- 192.168.207.100 ping statistics ---
5 packets transmitted, 0 received, +5 errors, 100% packet loss, time 4003ms
"""
PING_FEDORA_EMPTY_BODY = six.b("""
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.

--- 192.168.0.1 ping statistics ---
""")

# ping google.com -n 10:
#   Windows 7 SP1
PING_WINDOWS_SUCCESS = six.b("""
Pinging google.com [216.58.196.238] with 32 bytes of data:
Reply from 216.58.196.238: bytes=32 time=87ms TTL=51
Reply from 216.58.196.238: bytes=32 time=97ms TTL=51
Reply from 216.58.196.238: bytes=32 time=56ms TTL=51
Reply from 216.58.196.238: bytes=32 time=95ms TTL=51
Reply from 216.58.196.238: bytes=32 time=194ms TTL=51
Reply from 216.58.196.238: bytes=32 time=98ms TTL=51
Reply from 216.58.196.238: bytes=32 time=93ms TTL=51
Reply from 216.58.196.238: bytes=32 time=96ms TTL=51
Reply from 216.58.196.238: bytes=32 time=96ms TTL=51
Reply from 216.58.196.238: bytes=32 time=165ms TTL=51

Ping statistics for 216.58.196.238:
    Packets: Sent = 10, Received = 10, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 56ms, Maximum = 194ms, Average = 107ms
""")
PING_WINDOWS_UNREACHABLE_0 = """
Pinging 192.168.207.100 with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 192.168.207.100:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
"""
PING_WINDOWS_UNREACHABLE_1 = PING_WINDOWS_UNREACHABLE_0 + "\n"
PING_WINDOWS_UNREACHABLE_2 = PING_WINDOWS_UNREACHABLE_1 + "\n"
PING_WINDOWS_INVALID = """
Pinging 192.168.207.100 with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 192.168.207.100:
"""

PING_OSX_SUCCESS = """
PING google.com (172.217.6.238): 56 data bytes
64 bytes from 172.217.6.238: icmp_seq=0 ttl=53 time=20.482 ms
64 bytes from 172.217.6.238: icmp_seq=1 ttl=53 time=32.550 ms
64 bytes from 172.217.6.238: icmp_seq=2 ttl=53 time=32.013 ms
64 bytes from 172.217.6.238: icmp_seq=3 ttl=53 time=28.498 ms
64 bytes from 172.217.6.238: icmp_seq=4 ttl=53 time=46.093 ms

--- google.com ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 20.482/31.927/46.093/8.292 ms
"""

PING_ALPINE_LINUX_SUCCESS = """
PING heise.de (193.99.144.80): 56 data bytes

--- heise.de ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 0.638/0.683/0.746 ms
"""


class Test_PingParsing_parse(object):

    @pytest.mark.parametrize(["ping_text", "expected"], [
        [
            PING_DEBIAN_SUCCESS,
            {
                "packet_transmit": 60,
                "packet_receive": 60,
                "packet_loss_rate": 0.0,
                "packet_loss_count": 0,
                "rtt_min": 61.425,
                "rtt_avg": 99.731,
                "rtt_max": 212.597,
                "rtt_mdev": 27.566,
                "packet_duplicate_rate": 0,
                "packet_duplicate_count": 0,
            }
        ], [
            PING_FEDORA_LOSS,
            {
                "packet_receive": 1553,
                "packet_transmit": 1688,
                "packet_loss_rate": 7.997630331753558,
                "packet_loss_count": 135,
                "rtt_min": 0.282,
                "rtt_max": 11.699,
                "rtt_mdev": 0.699,
                "rtt_avg": 0.642,
                "packet_duplicate_rate": 0.0643915003219575,
                "packet_duplicate_count": 1,
            }
        ], [
            PING_FEDORA_UNREACHABLE,
            {
                "packet_transmit": 5,
                "packet_receive": 0,
                "packet_loss_rate": 100.0,
                "packet_loss_count": 5,
                "rtt_min": None,
                "rtt_avg": None,
                "rtt_max": None,
                "rtt_mdev": None,
                "packet_duplicate_rate": None,
                "packet_duplicate_count": 0,
            }
        ], [
            PING_WINDOWS_SUCCESS,
            {
                "packet_transmit": 10,
                "packet_receive": 10,
                "packet_loss_rate": 0.0,
                "packet_loss_count": 0,
                "rtt_min": 56,
                "rtt_avg": 107,
                "rtt_max": 194,
                "rtt_mdev": None,
                "packet_duplicate_rate": None,
                "packet_duplicate_count": None,
            }
        ], [
            PING_OSX_SUCCESS,
            {
                "packet_duplicate_count": None,
                "packet_duplicate_rate": None,
                "packet_loss_count": 0,
                "packet_loss_rate": 0.0,
                "packet_receive": 5,
                "packet_transmit": 5,
                "rtt_avg": 31.927,
                "rtt_max": 46.093,
                "rtt_mdev": 8.292,
                "rtt_min": 20.482,
            }
        ], [
            PING_ALPINE_LINUX_SUCCESS,
            {
                "packet_duplicate_count": None,
                "packet_duplicate_rate": None,
                "packet_loss_count": 0,
                "packet_loss_rate": 0.0,
                "packet_receive": 5,
                "packet_transmit": 5,
                "rtt_avg": 0.683,
                "rtt_max": 0.746,
                "rtt_mdev": None,
                "rtt_min": 0.638,
            }
        ],
    ] + list(itertools.product(
        [
            PING_DEBIAN_UNREACHABLE_0,
            PING_DEBIAN_UNREACHABLE_1,
            PING_DEBIAN_UNREACHABLE_2,
        ],
        [{
            "packet_transmit": 5,
            "packet_receive": 0,
            "packet_loss_rate": 100.0,
            "packet_loss_count": 5,
            "rtt_min": None,
            "rtt_avg": None,
            "rtt_max": None,
            "rtt_mdev": None,
            "packet_duplicate_rate": None,
            "packet_duplicate_count": 0,
        }]
    )) + list(itertools.product(
        [
            PING_WINDOWS_UNREACHABLE_0,
            PING_WINDOWS_UNREACHABLE_1,
            PING_WINDOWS_UNREACHABLE_2,
        ],
        [{
            "packet_transmit": 4,
            "packet_receive": 0,
            "packet_loss_rate": 100.0,
            "packet_loss_count": 4,
            "rtt_min": None,
            "rtt_avg": None,
            "rtt_max": None,
            "rtt_mdev": None,
            "packet_duplicate_rate": None,
            "packet_duplicate_count": None,
        }]
    )))
    def test_normal_text(self, ping_parser, ping_text, expected):
        ping_parser.parse(ping_text)

        assert ping_parser.as_dict() == expected

    def test_empty(self, ping_parser, ping_text):
        ping_parser.parse(ping_text)
        ping_parser.parse("")

        assert ping_parser.packet_transmit is None
        assert ping_parser.packet_receive is None
        assert ping_parser.packet_loss_rate is None
        assert ping_parser.rtt_min is None
        assert ping_parser.rtt_avg is None
        assert ping_parser.rtt_max is None
        assert ping_parser.rtt_mdev is None
        assert ping_parser.packet_duplicate_count is None

    @pytest.mark.parametrize(["ping_text", "expected"], [
        [PING_FEDORA_EMPTY_BODY, EmptyPingStatisticsError],
        [PING_WINDOWS_INVALID, EmptyPingStatisticsError],
    ])
    def test_exception(self, ping_parser, ping_text, expected):
        with pytest.raises(expected):
            ping_parser.parse(ping_text)
