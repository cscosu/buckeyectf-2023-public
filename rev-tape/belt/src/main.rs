use std::{env, io::{Read, self}, fs::File, collections::VecDeque};

use hex::decode;


#[derive(Debug)]
struct BeltStack {
    stack: VecDeque<u8>
}

impl BeltStack {
    fn new(len: usize) -> Self {
        BeltStack { 
            stack: VecDeque::from(vec![0xBB; len])
        }
    }

    pub fn push(&mut self, value: u8) {
        self.stack.rotate_right(1);

        self.stack.pop_front().unwrap();
        self.stack.push_front(value)
    }

    pub fn pop(&mut self) -> u8 {
        self.stack.rotate_left(1);

        self.stack.back().unwrap().clone()
    }

    pub fn cpush(&mut self) {
        let front = self.stack.front().unwrap().clone();
        self.stack.rotate_right(1);

        self.stack.pop_front().unwrap();
        self.stack.push_front(front)
    }

    pub fn pivot(&mut self) {
        self.stack
            .make_contiguous()
            .reverse();
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let input_filename = &args[1];
    let mut program_bytes = Vec::new();

    let stdin = io::stdin();

    File::open(input_filename)
        .expect("Could not open program file")
        .read_to_end(&mut program_bytes).expect("Could not read program file");


    let mut stack = BeltStack::new(64);

    let mut program_counter: usize = 0;
    loop {
        let current_byte = program_bytes.get(program_counter)
            .expect("Program counter invalid");

        program_counter += 1;

        // Debuging prints helpful
        //println!("Program counter = {program_counter}");
        //dbg!(&stack);
        match current_byte {
            // Push
            0x00 => {
                let value_to_push = program_bytes.get(program_counter).expect("Push with no value to push...");
                program_counter += 1;

                stack.push(value_to_push.clone());
            }
            // Pop
            0x01 => {
                stack.pop();
            }
            // CPush
            0x02 => {
                stack.cpush();
            }
            // BZ
            0x10 => {
                let offset = stack.pop();
                let condition = stack.pop();
                if condition == 0 {
                    program_counter += usize::from(offset);
                }
            }
            // BNZ
            0x12 => {
                let offset = stack.pop();
                let condition = stack.pop();
                if condition != 0 {
                    program_counter += usize::from(offset);
                }
            }
            // ADD
            0x20 => {
                let src1 = stack.pop();
                let src2 = stack.pop();
                let result = src1.saturating_add(src2);
                stack.push(result);
            }
            // Sub
            0x21 => {
                let src1 = stack.pop();
                let src2 = stack.pop();
                let result = src1.saturating_sub(src2);
                stack.push(result);
            }
            // Mult
            0x22 => {
                let src1 = stack.pop();
                let src2 = stack.pop();
                let result = src1.saturating_mul(src2);
                stack.push(result);
            }
            // Div
            0x23 => {
                let src1 = stack.pop();
                let src2 = stack.pop();
                let result = src1.saturating_div(src2);
                stack.push(result);
            }
            // Nand
            0x24 => {
                let src1 = stack.pop();
                let src2 = stack.pop();
                let result = !(src1 & src2);
                stack.push(result);
            }
            // Print
            0x40 => {
                let value_to_print = stack.pop();
                print!("{}", value_to_print as char);
            }
            // Printh
            0x41 => {
                let value_to_print = stack.pop();
                println!("{:#02x}", value_to_print);
            }
            // Get
            0x42 => {
                let mut buf = String::new();
                stdin.read_line(&mut buf).unwrap();
                let byte = buf.as_bytes()[0];
                stack.push(byte);
            }
            // Geth
            0x43 => {
                let mut buf = String::new();
                stdin.read_line(&mut buf).unwrap();
                let buf = buf.trim();
                let byte = decode(buf)
                    .expect("Back hex input");
                stack.push(byte[0]);
            }
            // EXIT
            0x50 => {
                println!("[+] Exiting...");
                break;
            }
            _ => {
                panic!("Invalid byte {:#02x} at index {}", current_byte, program_counter)
            }
        }

        if program_counter == program_bytes.len() {
            break;
        }
    }

    println!("[+] Done!")

}


