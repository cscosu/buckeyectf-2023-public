use std::io::Read;

use pnet::packet::icmp::echo_request::EchoRequestPacket;
use pnet::packet::icmp::{IcmpPacket, IcmpTypes};
use pnet::packet::icmp::echo_reply::MutableEchoReplyPacket;
use pnet::packet::ip::IpNextHeaderProtocols;
use pnet::packet::ipv4::{MutableIpv4Packet, Ipv4Packet};
use pnet::packet::{MutablePacket, Packet, FromPacket};
use pnet::transport::TransportChannelType::Layer3;
use pnet::transport::{transport_channel, ipv4_packet_iter};
use pnet::util;

const FILE: &str = "flag.png";
// Number of bytes of flag data to send in each reply
const SEGMENT_SIZE: usize = 64;

pub struct FlagData {
    flag_data: Vec<u8>,
    segment_size: usize
}

impl FlagData {
    pub fn new(fname: &str, segment_size: usize) -> Result<FlagData, std::io::Error> {
        let mut file = std::fs::File::open(fname)?;

        let mut bytes = Vec::new();

        file.read_to_end(&mut bytes)?;

        Ok(FlagData {
            flag_data: bytes,
            segment_size
        })
    }

    pub fn data_segment_from_index(&self, index: usize) -> Vec<u8> {
        let start = self.segment_size * index;
        if start > self.flag_data.len() {
            return Vec::new();
        }
        let mut end = self.segment_size * (index + 1);
        if end > self.flag_data.len() {
            end = self.flag_data.len()
        }

        let data = &(self.flag_data)[start..end];
        data.to_vec()
    }
}

// Checks if is a IPv4, ICMP Echo request packet.
fn check_coolness(packet: &Ipv4Packet) -> bool {
    if packet.get_next_level_protocol() != IpNextHeaderProtocols::Icmp {
        // Not ICMP, I don't care!
        return false;
    }
    match IcmpPacket::new(packet.payload()) {
        Some(icmp_packet) => {
            if icmp_packet.get_icmp_type() != IcmpTypes::EchoRequest {
                // Not a request? I don't care!!
                return false;
            }
        },
        None => return false // Too short? Join the club!
    }

    return true;
}

fn main() {
    println!("Starting");
    let flag_data = FlagData::new(FILE, SEGMENT_SIZE).expect("Could not open flag file!");

    let protocol = Layer3(IpNextHeaderProtocols::Icmp);

    let (mut tx, mut rx) = match transport_channel(4096, protocol) {
        Ok((tx, rx)) => (tx, rx),
        Err(e) => panic!(
            "An error occurred when creating the transport channel: {}",
            e
        ),
    };

    let mut iter = ipv4_packet_iter(&mut rx);
    loop {
        match iter.next() {
            Ok((packet, addr)) => {
                if !check_coolness(&packet) {
                    // Not interested if not cool.
                    continue;
                }

                let ipv4 = packet.from_packet();
                let src = ipv4.source;
                let dest = ipv4.destination;


                let Some(echo_request_packet) = EchoRequestPacket::new(&ipv4.payload) else {
                    eprintln!("Could not parse EchoRequestPacket... weird.");
                    continue;
                };

                // Bytes in ICMP paylods (= request payload + flag data chunk)
                let mut payload_bytes = Vec::new();
                payload_bytes.extend(echo_request_packet.payload());
                let seq = echo_request_packet.get_sequence_number();


                let flag_data = flag_data.data_segment_from_index(seq.into());
                let segment_size = flag_data.len();
                payload_bytes.extend(flag_data);
                
                let mut vec2: Vec<u8> = vec![0; echo_request_packet.packet().len() + segment_size];
                let Some(mut echo_reply) = MutableEchoReplyPacket::new(&mut vec2[..]) else {
                    eprintln!("Could not parse MutableEchoReplyPacket... weird.");
                    continue;
                };

                // Start with old echo request
                echo_reply.clone_from(&echo_request_packet);
                // Should be echo reply
                echo_reply.set_icmp_type(IcmpTypes::EchoReply);
                echo_reply.set_payload(&payload_bytes);
                
                
                // Recalculate reply checksum
                let new_checksum = util::checksum(echo_reply.packet(), 1);
                echo_reply.set_checksum(new_checksum);

                // now, ipv4 packet
                let mut vec: Vec<u8> = vec![0; packet.packet().len() + segment_size];
                let mut new_ipv4_packet = MutableIpv4Packet::new(&mut vec[..]).unwrap();
                new_ipv4_packet.clone_from(&packet);

                // Switch the source and destination ports
                new_ipv4_packet.set_source(dest);
                new_ipv4_packet.set_destination(src);
                let new_len = echo_reply.packet().len() as u16;
                new_ipv4_packet.set_total_length(new_len + 20);
                new_ipv4_packet.set_payload(echo_reply.packet());

                println!("Sending response to {src}");

                match tx.send_to(new_ipv4_packet, addr) {
                    Ok(_) => (),
                    Err(e) => eprintln!("failed to send packet: {}", e),
                }
            }
            Err(e) => {
                panic!("An error occurred while reading: {}", e);
            }
        }
    }
}