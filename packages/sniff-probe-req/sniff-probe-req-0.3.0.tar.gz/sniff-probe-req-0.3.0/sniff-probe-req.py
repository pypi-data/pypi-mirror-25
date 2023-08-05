#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import *
from csv import writer
from re import compile, match
from os import geteuid
from sys import argv, exit
from argparse import ArgumentParser, FileType

def parseProbeReq(packet):
    timestamp = packet.getlayer(RadioTap).time
    s_mac = packet.getlayer(RadioTap).addr2
    essid = packet.getlayer(Dot11ProbeReq).info.decode("utf-8")

    # If the probe request contains an ESSID.
    if essid:
        if "essid_filter" in globals() and not essid in essid_filter:
            return

        if "essid_regex" in globals() and not match(essid_regex, essid):
            return

        print("{timestamp} - {s_mac} -> {essid}".format(timestamp=timestamp, s_mac=s_mac, essid=essid))

        if "outfile" in globals():
            outfile.writerow([timestamp, s_mac, essid])

if __name__ == "__main__":
    ap = ArgumentParser(description="Wi-Fi Probe Requests Sniffer")
    essid_arguments = ap.add_mutually_exclusive_group()

    essid_arguments.add_argument("-e", "--essid", nargs="+", help="ESSID of the APs to filter (space-separated list)")
    ap.add_argument("--exclude", nargs="+", help="MAC addresses of the stations to exclude (space-separated list)")
    ap.add_argument("-i", "--interface", required=True, help="wireless interface to use (must be in monitor mode)")
    ap.add_argument("-o", "--output", type=FileType("a"), help="output file to save the captured data (CSV format)")
    essid_arguments.add_argument("-r", "--regex", help="regex to filter the ESSIDs")
    ap.add_argument("-s", "--station", nargs="+", help="MAC addresses of the stations to filter (space-separated list)")

    args = vars(ap.parse_args())

    if not geteuid() == 0:
        exit("[!] You must be root")

    if args["output"]:
        outfile = writer(args["output"], delimiter=";")

    if args["essid"]:
        essid_filter = args["essid"]

    if args["regex"]:
        essid_regex = compile(args["regex"])

    filter = "type mgt subtype probe-req"

    if args["exclude"]:
        filter += " and not ("

        for i, station in enumerate(args["exclude"]):
            if i == 0:
                filter += "ether src host {s_mac}".format(s_mac=station)
            else:
                filter += " || ether src host {s_mac}".format(s_mac=station)

        filter += ")"

    if args["station"]:
        filter += " and ("

        for i, station in enumerate(args["station"]):
            if i == 0:
                filter += "ether src host {s_mac}".format(s_mac=station)
            else:
                filter += " || ether src host {s_mac}".format(s_mac=station)

        filter += ")"

    print("[*] Start sniffing probe requests...")

    try:
        sniff(iface=args["interface"], filter=filter, prn=parseProbeReq)
    except IOError:
        exit("[!] Interface doesn't exist")
